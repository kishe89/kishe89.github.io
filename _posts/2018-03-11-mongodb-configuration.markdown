---
layout: post
title:  "mongodb-configuration"
date:   2018-03-11 16:14:00
author: 김지운
cover:  "/assets/instacode.png"
categories: DB
---

이전에 작성한 [mongodb install]에서는 mongodb 의 설치를 진행하였다.

이번엔 기본적인 세팅들에 대해서 알아본다.

##### mongod.conf
```
systemLog:
  destination: file
  path: "/data/log/mongodb"
  logAppend: true
storage:
  journal:
    enabled: true
    commitIntervalMs: 200
  dbPath:
    "/data/db"
  wiredTiger:
    engineConfig:
      cacheSizeGB: 2
      journalCompressor: snappy
      directoryForIndexes: false
    collectionConfig:
      blockCompressor: snappy
    indexConfig:
      prefixCompression: true
processManagement:
  fork: false
net:
  bindIp: 127.0.0.1
  port: 27017
setParameter:
  enableLocalhostAuthBypass: false
```

mongodb configuration file 의 포맷은 원래 key=value 형식의 텍스트에서 2.6 부터 YAML 포맷으로 변경되었다.

인덴트에 따라 구분되므로 인덴트에 주의하여 작성한다.

그렇다고 겁먹을 필요는 없다.

실행시 configuration file 의 잘못된 부분에 대해서 에러를 띄워주므로 잘못되면 해당 부분을 수정하면서 차근차근 하면된다.

일단 처음 보이는 부분은 `systemLog`를 세팅하는 부분이다.
```
systemLog:
  destination: file
  path: "/data/log/mongodb"
  logAppend: true
```
`destination` 은 무엇으로 저장할지에 대한 옵션으로 `string` 으로 지정한다.

이때 들어갈 수 있는 값은 `file`, `syslog` 로 위처럼 `file` 로 지정한 경우는

해당 `file` 을 쓸 `path` 를 같이 지정해주어야 한다.

위의 경우는 log 를 `/data/log/mongodb` 에 저장하라는 의미이다.

`destination`을 `syslog` 로 지정하거나 미지정시

해당 런타임의 standard output 으로 출력한다.

이외에도 quiet, verbosity, traceAllExceptions, ... 의 다양한 옵션이 존재한다.

이중 몇개만 일단 보면 verbosity 는 로그의 레벨을 지정하는 부분으로 0 to 5 의 값을 지정할 수 있다.

당연히 올라갈 수록 자세한 로그를 보여주지만 로그가 자세히 많이 출력될 수록 성능에 영향을 끼치니 개발시나 디버깅시에만 높여서 키는게 좋을듯 하다.

verbosity 는 component 마다 따로 세팅할 수 있다.

위에서 `logAppend` 의 경우는 Default 는 false 이다.

true 일 경우에는 존재하는 파일의 end 부터 다시 작성해나간다.

false 일 경우에는 존재하는 것들을 백업하고 새로운 로그파일을 작성한다.

나머지 시스템 로그에 대한 자세한 옵션은 필요에 따라 [MongoDB configuration Documents]를 참고하도록한다.

이제 그 다음 설정값인 `storage`를 보도록한다.

가장 만만해 보이는 `dbPath` 부터 보면 실제 data 를 저장할 경로를 지정할 부분이다.

`journal` 은 저널링을 할 때 사용할 journal 의 허용여부 및 journal 의 commitInterval 등을 지정할 수 있다.

[mongodb install] 에서 이야기 했듯이 성능에 영향을 미치는 옵션이니 적절히 세팅해줘야 한다.

`storage` 의 옵션들은 storageEngine 에 따라서 달라지는 부분이 많다.

storageEngine 의 종류는 아래표와 같다.

|이름|내용|
|---|---|
|mmapv1|Original Engine 으로 빅엔디안 미지원|
|wiredTiger|3.2 부터 default 로 사용|
|inMemory|Enterprise 3.2 이상에서만 사용 가능하다.|

달라지는 부분은 문서들을 보는것이 빠르므로 [MongoDB configuration Documents] 를 참조한다.

일단 사용하는 `wiredTiger` 로 세팅을 계속해본다.

엔진 밑으로 세부 세팅들이 쭈우우욱 이어지는데 `engineConfig`부터 본다.
```
cacheSizeGB: 2
journalCompressor: snappy
directoryForIndexes: false
```
이 3가지 옵션을 세팅하였는데 각각 본다.
`cacheSizeGB` 는 GB 단위로 세팅하며 범위는 256MB 에서 10TB 까지 이다.

mongodb 가 내부적으로 캐시에 사용할 수 있는 메모리 세팅부분으로 default 는 두가지중 하나를 사용한다.
1. 50% of RAM minus 1 GB
2. 256 MB.

환경에서의 RAM 에서 1GB를 뺀것의 50% 혹은 256MB 를 사용하게 된다.

`journalCompressor` 는 journal 을 압축할건지 압축한다면 어떻게 압축할지를 세팅하는 부분이다.

none, snappy, zlib 를 지원한다.

`directoryForIndexes` 는 default 는 false 이다.

true 로 세팅시에는 mongod 는 `dbPath` 로 지정한 경로 아래로 index 들과 collection 들을 분리하여 subdirectory 를 생성하고

각각의 subdirectory 에 저장된다.

참고로 [MongoDB configuration Documents]에 storage.Engine(mmapv1,wiredTiger,inMemory).xxx 의 세팅들은 각각의

엔진들에서만 사용되는 세팅이다.

```
collectionConfig:
      blockCompressor: snappy
```

collectionsConfig 의 blockCompressor 는 이름과 같이 collection 의 데이터의 압축에대해서 위의 journalCompressor 와 마찬가지로 세팅한다.

이 압축은 컬렉션의 생성시 오버라이드 될 수 있다.

만약 이전에 snappy 로 지정하고 생성된 컬렉션이 있는 DB 에 대해서 zlib 로 변경하는 경우가 생긴다면

이전에 생성된 컬렉션들은 snappy 로 압축하고 새로 생성되는 컬렉션들에 대해서 zlib 로 압축한다.

```
indexConfig:
      prefixCompression: true
```

위 옵션또한 배포 시점의 설정을 따르게 된다.

false 인 상태로 배포했을때 생성된 index 들은 설정을 바꾸고 배포하더라도 영향을 받지 않는다.

```
processManagement:
  fork: false
```
`processManagement` 가 나타내는 것처럼 proces 를 어떻게 할지에 대한 옵션이다.

`fork` 의 default 는 false 이다.

mongod, mongos 는 기본적으로 daemon 형태로 뜨지 않는다.

리눅스에서는 초기화 스크립트를 작성하여 서비스로 띄우던가 하고 나머지에선 fork true 해주면

백그라운드에 daemon 형태로 뜨게된다.

이외에 pidFilePath, timeZoneInfo 옵션이 있다.

pid 를 지정하고 파일로 저장한다. 타임존인포는 타임존 데이터를 지정하는것으로

`/usr/share/zoneinfo` 의 값을 default 로 사용하며 MongoDb 배포 일정마다 최신 데이터로 업데이트 된다.

하지만 타임존 데이터베이스의 업데이트 주기와 MongoDB 업데이트 주기가 다르니 필요하면 다운받아서 옵션에 경로를 지정해주면된다.

`net` 설정은 상당히 많은데 대부분 인증관련한 내용이다.

ssl 관련 내용은 설정하면서 작성한다.

그리고 이후 작성할 샤딩을 진행하는 과정중에 다시 설정하게 될 것이다.

```
setParameter:
  enableLocalhostAuthBypass: false
```
`setParameter`는 MongoDB Server 매개변수들을 세팅하는것이다.

`enableLocalhostAuthBypass` 는 로컬호스트에서 인증을 할지에 대한것이다.

default 는 true 이다.

대략적인 환경에 대해서 보았다.

다음글은 라즈베리 파이에서 64 bit 운영체제 설치 후 3.x 버전대의 mongodb 설치를 하고난뒤

샤딩하는 과정부터 정리해보도록 하겠다.

[MongoDB configuration Documents]:https://docs.mongodb.com/manual/reference/configuration-options/
[mongodb install]:https://kishe89.github.io/db/2018/03/09/mongodb-install.html
