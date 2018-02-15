---
layout: post
title:  "mongodb-connect"
date:   2018-02-15 16:05:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Bluemix(IBM)
---

[Bluemix(IBM Paas) CloudFoundry Deploy] 에서 배포한 웹 어플리케이션에 DB 를 붙여보도록한다.

연동할 DB 는 MongoDB 로 DBaas 형태의 서비스를 이용할 것이다.

무료 호스팅 MongoDB 는 [mLab] 의 서비스를 이용할 것이다.

계정생성을 하는 부분은 건너뛴다. 차근차근 진행하면 될것이다.

계정을 생성하고 로그인을 한다.

![Alt text](/assets/Bluemix/mongodb_connect/index1.png)

로그인을 하고나면 위와 같은 화면을 볼 수 있다.(현재 하나 생성해놓은 DB 가 있어서 리스트에 뜬다)

위 화면에서 Create new 버튼을 클릭한다.

![Alt text](/assets/Bluemix/mongodb_connect/index2.png)

Create new 버튼을 클릭했다면 위와 같은 페이지가 보일 것이다.

DB 호스팅 서비스를 제공하는 제공사별로 선택할 수 있다.

각 제공사별 데이터센터가 어디있냐의 차이는 있지만 나머진 크게 차이가 없다.

aws 에서 제공하는 sandbox 형태의 서비스를 선택한다.

그리 페이지 오른쪽 하단의 Continue 버튼을 클릭한다.

![Alt text](/assets/Bluemix/mongodb_connect/index3.png)

Region 을 선택하는 페이지가 뜬다.

us east 를 선택하고 오른쪽 하단의 Continue 버튼을 클릭한다.

MongoDB 버전이 나오고 DB 이름을 입력하라고 나오는데 적당히 입력하고 Continue 를 클릭한다.

최종적으로 선택하고 입력한 내용이 보여지고 확인 되었으면 Submit Order 를 클릭한다.

![Alt text](/assets/Bluemix/mongodb_connect/index4.png)

그러면 위와 같이 생성된 디비를 볼 수 있다. 방금 생성한 디비를 클릭 해보자.

그러면

```
To connect using the mongo shell:
mongo ds235778.mlab.com:35778/cfexample -u <dbuser> -p <dbpassword>
To connect using a driver via the standard MongoDB URI (what's this?):

mongodb://<dbuser>:<dbpassword>@ds235778.mlab.com:35778/cfexample
```
위와 같은 내용이 보일것이다. 접속시 사용할 방법에 대해 나와 있다.

그 아래의 Users 탭을 클릭해서 user 를 생성해주고 생선한 user 의 정보를 위 양식에 맞게 입력하여 접속하면 된다.

예를 들어서 user 의 Name 을 admin, password 를 admin 으로 세팅했다면

```
To connect using the mongo shell:
mongo ds235778.mlab.com:35778/cfexample -u admin -p admin
To connect using a driver via the standard MongoDB URI (what's this?):

mongodb://admin:admin@ds235778.mlab.com:35778/cfexample
```
이 되는것이다.

이제 이 DB 를 붙여보도록한다.

mongodb native driver 도 있지만 mongoose 를 이용하도록한다.

일단 프로젝트의 package.json 에 mongoose dependency 를 주입한다.

##### package.json
```javascript
{
  "name": "cfdeployexample",
  "version": "0.0.0",
  "private": true,
  "scripts": {
    "start": "node ./bin/www"
  },
  "dependencies": {
    "body-parser": "~1.18.2",
    "cookie-parser": "~1.4.3",
    "debug": "~2.6.9",
    "ejs": "~2.5.7",
    "express": "~4.15.5",
    "morgan": "~1.9.0",
    "serve-favicon": "~2.4.5",
    "mongoose": "latest"
  }
}
```

그리고 npm update 를 해준다.

우리가 저장할 데이터는 사용자의 UserAgent 값이다.

해서 해당 데이터를 저장할 스키마를 작성하도록 한다.

##### User.js
```javascript
/**
 * http://usejsdoc.org/
 */
let mongoose = require('mongoose');
let Schema = mongoose.Schema;
let UserSchema = new Schema({
    UserAgent: String,
    CreatedAt: { type:Date, default: Date.now }
});
module.exports = mongoose.model('user', UserSchema);
```

그리고 접속정보를 가지고 connection 을 얻을 코드를 Initializer 라고 하나 작성한다.

##### Initializer.js
```javascript
/**
 * CreatedAt 2017-11-16 14:07:00 kst
 * by kim ji woon
 *
 */

exports.InitMongoDB = function (env,mongoose) {

    if(!env.VCAP_SERVICES){
        /**
         * @TODO Local Initialization
         * Please Input ./credentials/credential.js
         */
        let credentials = require('./credential');
        const options = {
            connectTimeoutMS: 4000,
            keepAlive:true,
            ha:true,
            autoReconnect:true,
            reconnectTries:30
        };
        let db = mongoose.connect(credentials.MongodbURI,options);

    }else{
        /**
         * @TODO Production Environment Initialization
         */
        let service = JSON.parse(env.mLabmongodb);
        let mongodb = service['mLab-mongodb'];
        let connection_string = mongodb[0].credentials.uri;

        //mLab mongodb option
        const options = {
            connectTimeoutMS: 4000,
            keepAlive:true,
            ha:true,
            autoReconnect:true,
            reconnectTries:30
        };
        let db = mongoose.connect(connection_string,options);
    }
};
```

mongoose 버전에 따라 useMongoClient 를 사용해야 할 수 있다.

일단 간단하게 설명하면 process 의 환경변수중 VCAP_SERVICES 라는 것을 확인하여 CF 환경인지 로컬 환경인지 확인후 접속정보를 따로 가지고 오는것이다.

물론 로컬에도 VCAP_SERVICES 라는 환경변수를 세팅해놓고 사용한다면 잘못된 조건이고 cfenv 모듈등을 이용하여 확인 할 수 있다.

어쨋든 본인은 세팅 안해놨기에 문제없이 동작한다.

크레덴셜은
##### credential.js
```javascript
module.exports = {
    MongodbURI:"mongodb://<dbuser>:<dbpassword>@host:port/dbname"
};

```

로 작성한다. 단 dbuser, dbpassword, host, port, dbname  부분은 본인의 DB 정보를 적어준다.

그리고 app.js 에 아래처럼 추가해준다.

##### app.js
```javascript
var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');

var index = require('./routes/index');
var users = require('./routes/users');

var app = express();
var User = require('./model/User');
var mongoose = require('mongoose');
var Initializer = require('./init/Initializer');
Initializer.InitMongoDB(process.env,mongoose);

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use(function (req,res,next) {
  var useragent = req.headers['user-agent'];
  var user = new User();
  user.UserAgent = useragent;
  user.save(function (err, result) {
      if(err){
        console.log(result);
      }
      next();
  });
});

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', index);
app.use('/users', users);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;

```

하나씩 본다.

```javascript
var User = require('./model/User');
var mongoose = require('mongoose');
var Initializer = require('./init/Initializer');
Initializer.InitMongoDB(process.env,mongoose);
```
는 사용할 모델과 mongoose 의 mongodb client 를 초기화(커넥션얻기)하는 부분이다.

그리고 나서 요청이 올때마다 저장하기 위해 미들웨어로

```javascript

app.use(function (req,res,next) {
  var useragent = req.headers['user-agent'];
  var user = new User();
  user.UserAgent = useragent;
  user.save(function (err, result) {
      if(err){
        console.log(result);
      }
      next();
  });
});
```
와 같이 작성해주었다.

요청의 헤더에서 user-agent 정보를 파싱하고 앞에서 작성한 User 모델을 기반으로 객체를 생성한다.

그리고 생성된 인스턴스인 user.UserAgent 에 파싱한 정보로 초기화해주고 user.save 함수를 호출하여 저장하였다.

mongoose 는 Promise 를 지원하며 콜백부분은 Promise 로 치환가능하다.

해당 프로젝트를 배포 해본다.

```
bx cf push CFDeployExample -i 1 -m 64M
```
에러가 발생한다.

왜냐하면 로컬에서의 크레덴셜은 파일에서 가져오니 상관없지만 CF 환경에선 크레덴셜을 안가지고 오고 환경변수에서 가지고 오기때문이다.

환경변수 세팅은 웹을 이용하도록 한다.
일단 bluemix.net 에 로그인을 하고 본인이 배포한 앱을 찾아서 선택한다.

그리고 runtime 을 선택하고 environment variables 를 선택하면 아래 이미지 처럼 뜬다.

![Alt text](/assets/Bluemix/mongodb_connect/index5.png)

오른쪽 하단의 Add 버튼을 클릭해주면 입력할 수 있는 창이 활성화 되는데 NAME 에는 서비스 이름, Value 에
```
{"서비스 이름":[{"credentials": {"uri":"mongodb://<dbuser>:<dbpassword>@host:port/dbname"}}]}
```
위와 같이 입력해준다.

그리고 Save 를 눌러 저장한다. 그러면 인스턴스는 재시작된다.

재시작 되고 나서 다시 배포해보도록 한다.

혹여 로컬에서 사용하던 크레덴셜 파일이 올라가는 걸 방지하려면 .cfignore 를 작성해서 프로젝트의 루트에 두면 cf push 시 무시된다.

![Alt text](/assets/Bluemix/mongodb_connect/index6.png)

최종적으로 배포되고 URL 로 접속해보고 mLab 에서 db 를 선택하고 collection 을 확인해본다.

![Alt text](/assets/Bluemix/mongodb_connect/index7.png)

collection 이 정상적으로 생성된것을 볼 수 있고 해당 컬렉션을 클릭해보면 생성된 document 들이 보인다.

![Alt text](/assets/Bluemix/mongodb_connect/index8.png)

[Bluemix(IBM Paas) CloudFoundry Deploy]:https://kishe89.github.io/bluemix(ibm)/2018/02/15/bluemix-cloudfoundry-deploy.html
[mLab]:https://mlab.com/
