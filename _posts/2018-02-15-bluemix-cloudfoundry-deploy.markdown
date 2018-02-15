---
layout: post
title:  "Bluemix(IBM Paas) CloudFoundry Deploy"
date:   2018-02-15 14:50:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Bluemix(IBM)
---

클라우드 서비스중 IBM 의 Bluemix 에서의 CloudFoundry Application 배포에 대해서 알아본다.

일단 CloudFoundry 는 오픈 소스이다.

CloudFoundry 에서 배포는 클라우드 파운드리 BOSH 배치(deployment) 스크립트 언어를 이용한다.

CloudFoundry 는 초기 개발에서부터 모든 테스트 단계, 그리고 배치(deployment)에 이르는 완전한 애플리케이션 수명 주기를 지원하기 때문에 지속적 배포에 적합하다.

CloudFoundry 에서 데이터베이스, 스토리지, 메시지 시스템등의 외부 의존 모듈들은 모두 서비스로 간주된다.

```
cf push appname -i 2 -m 256M
```

위와 같은 스크립트를 이용하여 배포하게 되는데 i 는 인스턴스의 갯수이고 m 은 인스턴스별 메모리 할당량이다.

이때 Docker 이미지가 각각의 컨테이너에 배포되게 된다.

CloudFoundry cli 를 이용해 로그등을 확인할 수 있고 어플리케이션의 시작 종료등을 할 수 있다.

일단 Bluemix 에서 CloudFoudry(Node js runtime) Application 을 배포하는 방법을 설명한다.

처음 할일은 IBM Cloud 계정을 생성한다.

그러고 나서는 CF CLI 혹은 IBM Cloud CLI를 설치한다.

CF CLI 는 CloudFoundry 에 대해서 관리할 수 있는 API 를 제공하고 IBM Cloud CLI 는 kubernetes 등에 대한 관리 API 까지 제공한다.

이 설명은 IBM Cloud CLI 를 설치하고 진행하도록한다.

설치하게 되면 터미널을 한번 껏다 켜준다.

설치전 열려있던 세션에대해서 적용이 안될 경우가 있다.

그리고 express(nodejs) 프로젝트를 하나 생성하고 생성한 프로젝트 의 루트로 이동한다.

위에서 내가 생성한 프로젝트의 경로는
```
/Users/kjw/MyProject/BlogExample/CFDeployExample
```
이다.
##### Path example
![Alt text](/assets/Bluemix/cf_deploy_ex/index1.png)

해당 프로젝트의 루트로 cd 를 이용해서 이동한다.

express 로 생성하게 되면 기본적으로 에러페이지와 인덱스페이지가 작성되어있다.

이 Application 을 배포해보겠다.

처음은 본인 계정으로 로그인이 필요하다.


이때 처음 실행이라면 혹시 API endpoint 를 물어볼 수 있다.

각 Region 별 API endpoint 는 아래 표와 같다.

|Region|API endpoint|
|---|---|
|US South and US East|api.ng.bluemix.net|
|Sydney and AP North|api.au-syd.bluemix.net|
|Germany|api.eu-de.bluemix.net|
|United Kingdom|api.eu-gb.bluemix.net|

위 표를 보고 사용할 Region 의 API endpoint 를 넣어준다.

그리고 아래 명령어를 쳐서 로그인을 시작한다.

##### bluemix login example

조직 과 영역에 대해서 지정해줘야하는데 잘 모를경우에는

##### 조직 보는 명령어
```
bx cf o
```
##### 영역 보는 명령어
```
bx cf spaces
```

를 콘솔에서 실행해보고 확인하여 입력하거나
```
bx target --cf
```
를 실행하면 default 로 잡힐 것이다.

이제 배포할 region, organization, space 모두 세팅 되었다.

콘솔에서
```
bx cf push AppName -i 1 -m 64M
```
을 실행해보자. 주의할 것은 AppName 부분은 본인들 어플리케이션 이름으로 적어줘야한다.

뒤에 URL 바인딩 될 URL 을 적을 수도 있으나 안적고 AppName 만 적을경우 해당 앱이름으로 URL 이 바인딩된다.

해서 이 예에서는 아래와 같이 실행할 것이다.

```
bx cf push CFDeployExample -i 1 -m 64M
```

명령을 실행하게 되면 배포가 시작된다.

모두 다운 받고 이미지 생성하고 배포하고 나면 인스턴스가 실행되며 인스턴스에 대한 간략한 정보와 함께 URL 이 표시되어있다.

해당 URL 로 접속해보면 정상접속이 된다.

![Alt text](/assets/Bluemix/cf_deploy_ex/index6.png)

이외에 서비스(DB,MQ,Storage,...) 바인딩은 홈페이지의 Documents 를 참조하면 된다.

기본적으로 서비스의 Credential 들은 이미지의 환경변수에 세팅된다.

Documents 를 참조하여 해당 부분을 세팅해주면 된다.

자세한 설명은 [Bluemix Getting started tutorial] 에도 나와있다.

[Bluemix Getting started tutorial]:https://console.bluemix.net/docs/runtimes/nodejs/getting-started.html#getting-started-tutorial
