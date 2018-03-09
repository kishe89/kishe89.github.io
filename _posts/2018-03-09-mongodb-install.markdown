---
layout: post
title:  "mongodb-install1"
date:   2018-03-09 16:05:00
author: 김지운
cover:  "/assets/instacode.png"
categories: DB
---

이 포스팅은 진행형으로 몇개의 포스팅으로 나뉘어질 수 있다.

1. 인스톨
2. 샤딩

크게는 위 2개로 생각중인데 실제 진행하면서 늘어날 듯 하다.

클라우드 환경에서 개발을 하면서 DB 인스톨 및 세팅등을 직접 한적이 거의 없었다.

하지만 그건 회사에서 인프라 사용료나 서비스 사용료들을 지불 할 때의 이야기다.

개인적으로 프로젝트를 만들고 하면 그 비용은 엄청난 부담이다.

Compose mongodb 서비스는 ㅜ.ㅜ 1GB마다 인스턴스가 하나씩 늘어나는데 인스턴스당 18$/month 란다.

지금 개인적으로 진행하는 프로젝트에는 유저의 데이터 이전에 사용할 오픈데이터들의 용량만도 csv 기준 10GB가 넘는다.

즉 기본적으로 $180/month 가 들어가는게 된다. 한화로 따지면 대략 월 19~20만원...

이건 고정적인 수입이 없는 상태에서 개인이 감당하기 어려운 돈이다.

그래서 생각한게 라즈베리 파이와 외장하드를 이용하여 DB 서버를 구성하는 것이다.

짠내나지만 현실의 벽은 어쩔 수 없다...

그래서 진행하는 과정을 포스팅으로 남긴다.

일단 사용할 장비는 라즈베리파이3, 호환되는 micro SD(일단은 여기에 설치진행)

OS 는 Ubuntu 16.04.2(32bit) 포스팅 기준 최신 버전을 설치 하였다.

```
주의 : Mongodb version >3.x 는 64 bit 호환
```

apt 를 이용하여 바로 받을 수 있는 mongodb 의 버전은 2.6 이다.

최신버전을 받기위해서는 GPG 키를 임포트하고 레파지토리를 등록해줘야하는데 이는 다음 포스팅에서 진행한다.

일단 2.x 를 가지고 샤딩등의 세팅까지 끝내고 테스트까지 진행후에 차근차근 올리도록한다.

라즈베리파이3는 ARM 아키텍처로 amd 는 미지원이다.

또한 64비트 동작은 가능은 하나 따로 커널들 빌드하고 하는 과정을 해줘야하는듯 하다.

해서 3.x 설치시에는 그 부분이 진행되어 있는 OS 를 이용할 것이다.

현재 검색해본결과로는 라즈비안도 부분적으로 되는듯하여 테스트해볼 예정이다.

일단은 Ubuntu 를 이용하여 진행한다.

해서 일단 아래 스크립트를 실행하여 ubuntu 의 패키지 매니저를 업데이트 한다.

```
apt-get update
```

그럼 업데이트 안되있는 패키지들을 전부 업데이트 해줄 것이다.

```
apt-get install mongodb
```

로 mongodb 를 설치하게 되면 2.6이 깔릴것이다.

mongodb 는 초기에 default config 파일을 이용한 환경으로 뜨게 된다.

데몬을 띄우는 스크립트의 작성은 아래처럼 할 수 있다.

```
cd /lib/systemd/system/
vim mongod.service
systemctl daemon-reload
systemctl start mongod
systemctl enable mongod
```
작성한 service 스크립트로 리로드하고 moongod 를 시스템이 부팅시 시작될 수 있도록 서비스로 등록하고 허용한다.

스크립트는 아래처럼 작성한다.
```
[Unit]
Description=High-performance, schema-free document-oriented database
After=network.target
Documentation=https://docs.mongodb.org/manual

[Service]
User=mongodb
Group=mongodb
ExecStart=/usr/bin/mongod --quiet --config /etc/mongod.conf

[Install]
WantedBy=multi-user.target
```

다른건 건들지 말고 ExecStart 부분만 변경하면 된다.

실제 실행 명령행인데 설치된 mongodb 의 mongod 의 경로와 mongod 를 실행할 때의 arguments 를 정의하는 부분이다.

보면 `--config /etc/mongod.conf` 가 보이는데 이게 기본으로 잡힌 mongod.conf 이다.

vim or vi or nano 로 열어보면

현재 2.6의 버전에서는 `key=value` 형태로 작성되어있다.

최신버전들은 yaml 로 작성되어 있는데 이는 라즈비안 과 3.x 로 업그레이드 할 때 보도록한다.

일단 conf 파일은 손대지 말고 DB 에 유저를 추가해보도록 한다.

mongo 쉘을 열고 아래 명령을 실행한다.

```
use admin
```

그러면 admin db를 사용하겠다는 것이다.

그리고 실제 유저의 생성은 db.createUser 함수를 이용한다.
```
db.createUser({user:"admin", pwd:"admin123", roles:[{role:"root", db:"admin"}]})
```
user 는 user 의 이름, pwd 는 비밀번호, roles 는 읽기,쓰기,루트 권한등의 역할을 지정하는 어레이이다.

역할은 여러개가 들어갈 수 있는데 사용자별로 따로 생성해주면 된다.

일단은 위처럼 루트계정을 만들도록 한다.

정상적으로 생성이 되었다면 앞에서 작성한 mongod.service 를 다시 열도록한다.

```
ExecStart=/usr/bin/mongod --quiet --auth --config /etc/mongod.conf
```
그리고 ExecStart 에 --auth 를 추가하고 저장하도록한다.

실행시 인증을 통해 연결시켜주기 위함이다.

이제 기본적인 실행에 대한 설정은 완료 되었다.

현재 내부에서의 접속만이 가능한데 이제 외부 접속을 가능하게 진행해본다.

이를 하기 위해서 필요한 것은 네트워크 세팅과 mongod.conf 의 수정이다.

일단 네트워크 세팅부터 진행해본다.

우리가 익히 알고 있는 iptables 에 포트들을 연결해주면된다.

헌데 라즈베리파이에서 문제가 생겼다. 보통 이더넷의 이름이 eth0 형태로 잡히는데

내가 사용한 라즈베리파이만 그런건지 모르겠지만 실제 이더넷의 이름은 엄청 긴 이름이 잡혔다.

그래서 실제로 iptables 와 mongod.conf 를 수정하기 전에 수정할 것이 있다.

```
/etc/network/interfaces
```
를 수정하도록 한다.

```
auto eth0
iface eth0 inet static
address [ip주소]
network [ip주소에 마지막을 0으로]
netmask [서브넷마스크]
gateway [기본 게이트웨이]
broadcast [기본DNS서버]
```
위 내용에서 eth0 로 잡혀있는 것을 실제 본인의 네트워크 이더넷 이름으로 변경하도록한다.

실제 이름도 eth0 라면 변경하지 않아도 된다.

수정하고 나서 네트워크를 재시작한다.

```
/etc/init.d/networking restart
```

그리고 나서 외부통신을 위해

```
/etc/resolv.conf
```
에 DNS 를 추가하도록한다.

이제 iptables 를 수정하도록 한다.

인바운드 아웃바운드 및 방화벽설정을 진행하면 된다.

iptables 설정은 아래 사이트를 참조한다. 정리가 잘 되어있다.
[https://www.mkyong.com/mongodb/mongodb-allow-remote-access/]

이더넷 이름만 주의하여 작성하면 된다.

mongod.conf 는 위 사이트 내용에서 추가로 해야할 일이 있다.

위에서 32bit ubuntu 에서 3.x 를 사용하면 안된다고 이야기 했다.

이유는 64bit 에서의 호환을 목표로한 기능 구현들이 있기 때문이다.

journal 같은 옵션들이 그에 해당한다.

장애발생시 저널링을 통해서 복구하게 되는데 안타깝게도 32bit 에서는 default로 false 를 설장하도록 되있다.

journal 은 mongodb 의 연산에 대한 일종의 로그로 보면 되는데 성능 때문에 그렇다.

journal 은 메모리 맵 파일인데 이를 저장할 메모리 주소가 부족하기 때문에 생기게 되는 문제가 있다.

물론 journal 의 commit 을 설정할 수 있긴 하지만 64비트 운영체제로 갈아타면 사용 가능하니 일단 해당 기능은 false 로 세팅해준다.

그리고 bind_ip 의 경우 127.0.0.1 로 초기 세팅 되어있을 것인데 특정 ip 의 접근을 허용할 때 사용한다.

예를 들어서 샤딩을 하여서 여러개의 mongos,mongod 가 떠있을 때 해당 db 서버의 연결을 위한 인터페이스 정의이다.

지금은 손댈 필요가 없다.

나머지 부분의 옵션들은 [mongodb 공식 문서]를 참조하도록 한다.

해서 세팅후 서비스를 재시작하게 되면 해당 config 로 재시작된다.

mongo 쉘로 접속해보던 [MongoDB Compass] 로 접속해보면 접속되는걸 볼 수 있다.

다음은 샤딩과 레플리카셋 구성에 대해 정리되는대로 작성하도록 하겠다.

[MongoDB Compass]:https://www.mongodb.com/products/compass
[mongodb 공식 문서]:https://docs.mongodb.com/
[https://www.mkyong.com/mongodb/mongodb-allow-remote-access/]:https://www.mkyong.com/mongodb/mongodb-allow-remote-access/
[Bluemix(IBM Paas) CloudFoundry Deploy]:https://kishe89.github.io/bluemix(ibm)/2018/02/15/bluemix-cloudfoundry-deploy.html
[mLab]:https://mlab.com/
