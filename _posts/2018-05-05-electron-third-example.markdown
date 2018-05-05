---
layout: post
title:  "Electron & Socket.io 를 이용한 챗봇 개발기3"
date:   2018-05-05 17:14:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Electron
---


이전 [포스팅]에서는 [Electron] 의 [BrowserWindow] 에 대해서 주로 봤다.

이번 포스팅에서는 아직 작업중인 채팅 서버에 대해서 포스팅을 적는다.

앞에서 이야기 했듯이 서버쪽 DB는 MongoDB 를 이용하고 있다.

MongoDB의 native API 를 wrapping 해놓은 ODM 인 [mongoose]란 것이 있다.

이를 이용하면 RDB 를 이용할때와 같이 스키마 형태로 Document 를 설계하는데 도움을 준다.

일단 이를 이용한 모델들을 하나씩 보도록 한다.


### Model
---


##### User Model

```javascript

'use strict';

let mongoose = require('mongoose');
let Schema = mongoose.Schema;

let UserSchema = new Schema({
  id:String,
  nickName:String,
  authOrg:String,
  token:String,
  socketId:String,
  PUBG_ID:String,
  PUBG_NICK:String,
  Matches:[{type:String}],
  waitingJoinRoomList:[{ type: Schema.Types.ObjectId, ref: 'Room'}],
  JoinRoomList:[{ type: Schema.Types.ObjectId, ref: 'Room'}],
  CreatedAt: { type:Date, default: Date.now },
  UpdatedAt: { type:Date, default: Date.now }
});

module.exports = mongoose.model('User',UserSchema);

```

첫번째로 User 모델이다. mongoose 의 Schema 객체를 기반으로 model을 만들고 만들어진 모델을 export 할것이다.

일단 PUBG 의 API 를 봐가며 작업중이므로 변경될 수 있는 여지가 많다.

각각의 프로퍼티는 아래와 같다.

|키|내용|
|---|---|
|id|Oauth를 통해서 발급된 AppID|
|nickName|채팅에 사용할 닉네임|
|authOrg|Oauth 를 해준 앱 ex) facebook,kakao,...|
|toekn|모든 API를 콜할 때 필요한 jwt 기반 토큰. sha256 암호화|
|PUBG_ID|유저가 등록할 본인의 PUBG_ID|
|PUBG_NICK|유저가 등록할 본인의 PUBG 닉네임|
|Matches|게임 매칭 리스트 (캐시용)|
|waitingJoinRoomList|방에 초대받은 리스트. 아직 참여는 안한상태의 방리스트|
|JoinRoomList|참가하고있는 방의 리스트|
|CreatedAt|가입 시간 UTC 0 기준|
|UpdatedAt|User 의 모든 상태 변경된 시간 UTC 0 기준|

위와 같이 일단 User는 설계하였다. Matches의 경우는 PUBG API 에서 Populated 데이터를 보내주질 않아서 일단 이쪽도
해당 Match의 id 들을 저장하도록 하였다.

지금 Populated 데이터와 mapping 하는 함수를 작성하고 있는데 이게 작업되면 변경될 것이다.

##### Room Model

```javascript
'use strict';

let mongoose = require('mongoose');
let Schema = mongoose.Schema;

let RoomSchema = new Schema({
  roomName:String,
  status:{type: Number, required : true},
  InvitedUser:[{ type: Schema.Types.ObjectId, ref: 'User'}],
  Participant:[{ type: Schema.Types.ObjectId, ref: 'User'}],
  messages:[{type: Schema.Types.ObjectId, ref: 'Message'}],
  CreatedAt: { type:Date, default: Date.now }
});

module.exports = mongoose.model('Room',RoomSchema);
```

Room 모델이다.

Room 모델의 각 프로퍼티는 아래와 같다.

|키|내용|
|---|---|
|roomName|유저가 입력한 방이름|
|status|방의 타입(매칭방,기본채팅방,봇방)|
|InvitedUser|방에 초대된 유저의 리스트|
|Participant|방에 참가한 유저의 리스트|
|messages|방에서 오고가는 메시지들의 reference id|
|CreatedAt|방의 생성시간 UTC 0기준|

document 내에서 추가적이 조작이 필요치 않다면 사실 embeded 시키는 것이 더 좋다고 생각하는데

추가적으로 해당 내용들의 update 등이 필요할듯 한 내용들이라 참조의 형태로 만들었다.

embeded 시켜도 물론 조작은 가능하지만 코드로 짜야할 부분이 내 경우는 경험상 늘어났다.

##### Message Model

```javascript

'use strict';

let mongoose = require('mongoose');
let Schema = mongoose.Schema;

let MessageSchema = new Schema({
  author:{ type: Schema.Types.ObjectId, ref: 'User'},
  textMessage:String,
  url:String,
  viewer:[{type: Schema.Types.ObjectId, ref: 'User'}],
  CreatedAt: { type:Date, default: Date.now }
});

module.exports = mongoose.model('Message',MessageSchema);

```

메시지 모델이다.

각 속성은 아래와 같다.

|키|내용|
|---|---|
|author|메시지를 보낸 유저의 ObjectId|
|textMessage|메시지 내의 텍스트|
|url|메시지 내의 url|
|viewer|message가 보내질 당시의 방안 유저 리스트. 읽을시 pull될거임|
|CreatedAt|메시지 전송된 시간|

일단은 기본적인 채팅의 메시지를 만들었는데 나중에 음성채팅등이 들어가게 되면 변경될 수 있다.


### 프로젝트 기본적인 구조
---

프로젝트는 현재 express 프레임워크 4.16.0 버전을 기반으로 작성중이며 사용한 node 버전은 8.9.4 버전을 쓰고 있다.

```
/
-/bin
--/www
-/chatapp
--/bot_function
---봇코드
--/model
---User.js
---Room.Js
---Message.js
--/user_function
---createRoom.js
---inviteRoom.js
---onMessage.js
---onMessage_Action.js
---onMessage_PUBG.js
---onMessage_Privacy.js
---onNotification.js
---validateHandshake.js
--bot.js
--userspace.js
-/credentials
-/init
-/node_modules
-/public
-/routes
-/test
-/view
-app.js
-package.json
-.gitignore
-README.md
```

프로젝트의 디렉토리 구조는 위와 같이 구성하였는데 credentials는 실제 배포시에는 배포하지 않는다.
해당 내용은 환경변수로 세팅할 것이기 때문이다. 개발당시에는 편리를 위해 파일로 관리할것이다.


```
주의 - credential 들은 실수로라도 github public repository 와 같은
공개 저장소에는 올라가지 않도록 주의해야한다.
깃기반 저장소는 .gitignore 파일로 배포환경에는 배포환경에 맞는 .xxignore 파일로 잘 관리해준다.

```


### app.js
---

```javascript
let createError = require('http-errors');
let express = require('express');
let path = require('path');
let cookieParser = require('cookie-parser');
let logger = require('morgan');
let io = require('socket.io')();
let indexRouter = require('./routes/index');
let usersRouter = require('./routes/users');
let mongoose = require('mongoose');
let Initializer = require('./init/Initializer');
let app = express();

Initializer.InitMongoDB(process.env,mongoose);

app.io = io;
// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/users', usersRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});
// error handler
app.use(function(err, req, res) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

let botNsp= io.of('/bot');
require('./chatapp/bot')(botNsp);
require('./chatapp/userspace')(io);

module.exports = app;

```

이 부분은 거의 대부분 초기 프로젝트를 생성하면 작업 되어있는 부분이다.

```javascript
let io = require('socket.io')();
```
[socket.io] 모듈을 로드하고

```javascript
let mongoose = require('mongoose');
let Initializer = require('./init/Initializer');

Initializer.InitMongoDB(process.env,mongoose);
let app = express();
app.io = io;
```

[mongoose] 및 초기 mongodb 커넥션을 맺어줄 초기화 작업 함수를 로드한다.
그리고 `app.io = io` 를 해준다.

이유는 express 버전이 3.~ 에서 4.~로 업그레이드 되면서 http 서버의 생성을 www 에 맡기도록 구조가 변경되었기 때문이다.


```javascript
let server = http.createServer(app);
let io = app.io;


io.attach( server );
io.set('transports', ['websocket']);
```

`/bin/www` 에 위와 같이 코드를 추가 및 변경한다.

io의 set 함수를 이용하여 여러가지 속성을 정의 및 추가할 수 있는데 일단 나는 [socket.io]의 모든 기능을 이용하지 않을것이다.

[socket.io]를 이용하는 가장 큰이유는 하위 호환을 위해서 사용하긴 한다.

WebSocket 이 생긴지 좀 되긴 했지만 Android 기준으로 4.4 아래 버전에서는 WebSocket 을 브라우저에서 지원 못하는 경우가 있다.

물론 지금 개발하는게 데탑용이긴 하지만 추후 모바일로 갈 때를 생각안할 수 없다.

[socket.io]는 지원되는 통신 방법중 transports 의 내용들중 가능한 방법으로 업그레이드하는 로직이 들어있다.

하지만 `transports` 속성을 셋하게 되면 해당 어레이의 속성들안에서 업그레이드를 하게 된다.

내가 올릴 환경이 앞단의 proxy를 내가 세팅할 수 있고 한 환경이면 sticky session 을 세팅하는 방법을 이용할 수 있으나

그렇지 못한 경우가 있다.

그럴 경우 handshake 를 하는도중 업그레이드 로직을 타게되면 origin 을 못찾아 소켓의 연결이 끊겼다 재접속(재접속 옵션을 켜놓으면)되었다하는 광경을 볼 수 있다.

그래서 업그레이드가 되지 않도록 애시당초 하나의 통신방법만을 허용해놓은것이다.

다시 app.js 의 내용을 보면 하단에 아래와 같은 코드를 볼 수 있다.

```javascript
let botNsp= io.of('/bot');
require('./chatapp/bot')(botNsp);
require('./chatapp/userspace')(io);

```

유저들간의 채팅구역과 bot 과 유저간의 채팅구역을 네임스페이스로 나누었다.

네임스페이스를 나누는것은 io.of(path) 함수가 제공한다.

해서 소켓의 handshake 도중 검증과 연결후의 이벤트 처리콜백들은 각각
-./chatapp/bot.js
-./chatapp/userspace.js

에서 등록되고 처리된다.

### userspace.js

```javascript

'use strict';

function UserSpace(io) {
  const jwt = require('jsonwebtoken');
  const pubg_token = require('../credentials/pubg_token');
  const axios = require('axios');
  const instance = axios.create({
    baseURL: 'https://api.playbattlegrounds.com/',
    timeout: 1000,
    headers: {
      'Authorization': pubg_token,
      'Accept': 'application/vnd.api+json'
    }
  });

  const secretKey = 'kimjiwoon';
  const sendToken = require('./user_function/sendToken');
  const onMessage = require('./user_function/onMessage');
  const onNotification = require('./user_function/onNotification');
  const createRoom = require('./user_function/createRoom');
  const validateHandShake = require('./user_function/validateHandShake');
  const leaveRoom = require('./user_function/leaveRoom');
  const onMessage_Privacy = require('./user_function/onMessage_Privacy');
  const onViewerUpdate = require('./user_function/onViewerUpdate');
  const inviteRoom = require('./user_function/inviteRoom');
  const onMessage_Action = require('./user_function/onMessage_Action');
  const onMessage_PUBG = require('./user_function/onMessage_PUBG');
  io.use(validateHandShake);
  io.on('connection',(socket)=> {
    sendToken(socket);
    onNotification(socket);
    onMessage(socket,jwt);
    createRoom(socket,jwt);
    leaveRoom(socket,jwt);
    onMessage_Privacy(socket,jwt);
    onViewerUpdate(socket,jwt);
    inviteRoom(socket,jwt);
    onMessage_Action(socket,jwt,instance);
    onMessage_PUBG.findPUBG_User(socket,jwt,instance,secretKey);
    onMessage_PUBG.findPopulatedMatchList(socket,jwt,instance,secretKey);
  });
};

module.exports=UserSpace;

```

개발중이기에 `const secretKey = 'kimjiwoon';`와 같은 코드가 있는 것이다.

위에서도 이야기 했듯이 이러한 값들은 환경변수를 이용하는것이 좀 더 안전하다.

app.js 에서 전달받은 io 객체에서 처리할 이벤트의 콜백들을 등록하는 곳이다.
그리고 콜백에서 사용할 PUBG API 호출용 http 클라이언트를 하나 만든다.

이용한 라이브러리는 [axios]이다. 이전까진 노드 네이티브 http 혹은 requestify 를 이용했는데

[axios]의 promise 기본 지원이 좋아서 사용해봤다.

함수 하나당 하나의 로드로 구성하려했는데 파일도 너무 많아지고 로드 구문이 너무 많아지는 감이 있어서 이부분은

onMessage_PUBG의 형태로 리팩토링을 할 것이다.

전체를 다 보긴 힘들고 onMessage_PUBG형태로 바꿀것이기 때문에 이것만 한번 본다.

```javascript
'use strict';

function findPUBG_User(socket, jwt, instance, secretKey) {
  socket.on('find-pubg-user',(message)=>{
    const path = '/players';
    const region = message.region;
    const targetNick = message.targetNick;
    const tokenValidate = (secretKey)=>{
      return new Promise((resolve,reject)=>{
        jwt.verify(message.token,secretKey,(err,user)=>{
          if(err){
            reject(err);
            return;
          }
          console.log(socket.id+":"+JSON.stringify(message));
          console.log(user);
          resolve(user);
        });
      });
    };
    const makeRequest = (user)=>{
      return new Promise((resolve,reject)=>{
        if(region){
          if(targetNick){
            const url = '/shards/'+region+path+'?filter[playerNames]='+targetNick;
            const request = {
              user:user,
              url:url
            };
            return resolve(request);
          }
          return reject(new Error('Invalid targetNick Parameter'));
        }
        return reject(new Error('Invalid Region Parameter'));
      });
    };
    const requestProfileToPUBG = (request)=>{
      return instance.get(request.url);
    };
    const filterProfile = (response)=>{
      return new Promise((resolve, reject)=>{
        const data = response.data;
        if(data.data[0]){
          const user = data.data[0];
          return resolve(user);
        }
        return reject(new Error('Not Exist User Information'));
      });
    };
    const updateUserInformation = (pubgUser)=>{
      const User = require('../model/User');
      const user = socket.user;
      const query = {
        _id:user._id
      };
      const options = {
        new:true
      };
      user.PUBG_ID = pubgUser.id;
      user.PUBG_NICK = pubgUser.attributes.name;
      pubgUser.attributes.matches.data.forEach((match)=>{
        user.Matches.push(match);
      });
      return User.findOneAndUpdate(query,user,options).exec();
    };
    const responseSuccessToUser = (user)=>{
      socket.user = user;
      socket.emit('find-pubg-user-success',user);
    };
    const responseFailToUser = (e)=>{
      socket.emit('find-pubg-user-fail',e);
    };
    tokenValidate(secretKey)
      .then(makeRequest)
      .then(requestProfileToPUBG)
      .then(filterProfile)
      .then(updateUserInformation)
      .then(responseSuccessToUser)
      .catch(responseFailToUser);
  });
};


function findPopulatedMatchList(socket, jwt, instance, secretKey) {
  socket.on('find-pubg-matches-populated',(message)=>{
    const path = '/matches';
    const region = message.region;
    const tokenValidate = (secretKey)=>{
      return new Promise((resolve,reject)=>{
        jwt.verify(message.token,secretKey,(err,user)=>{
          if(err){
            reject(err);
            return;
          }
          console.log(socket.id+":"+JSON.stringify(message));
          console.log(user);
          resolve(user);
        });
      });
    };
    const makeRequest = (user)=>{
      return new Promise((resolve,reject)=>{
        if(path){
          if(region){
            const requestList = [];
            socket.user.Matches.forEach((match)=>{
              const url = '/shards/'+region+path+'/'+match;
              requestList.push(instance.get(url));
            });
            return resolve(requestList);
          }
          return reject(new Error('Invalid Region Parameter'));
        }
        return reject(new Error('Invalid Path Parameter'));
      });
    };
    const requestMatchInfoToPUBG = (requestList)=>{
      return Promise.all(requestList)
    };
    const replaceListTorosterList = (rosterDataList)=>{
      const result = [];
      rosterDataList.forEach((rosterData)=>{
        const rosterList = [];
        const copyrosterData = Array.from(rosterData,x=>x);
        let removedCount = 0;
        rosterData.forEach((roster,index)=>{
          if(roster.type === 'roster'){
            rosterList.push(roster);
            copyrosterData.splice(index-removedCount,1);
            removedCount++;
          }
        });
        result.push({
          rosterData:copyrosterData,
          rosterList:rosterList
        });
      });

      return Promise.resolve(result);
    };
    const replaceListToparticipant = (Object)=>{
      Object.forEach((element)=>{
        element.rosterData.forEach((participant)=>{
          if(participant.type === 'participant'){
            element.rosterList.forEach((roster)=>{
              roster.relationships.participants.data.forEach((participantReference,index)=>{
                if(participantReference.id === participant.id){
                  roster.relationships.participants.data[index] = participant;
                }
              });
            });
          }
        });
      });
      return Promise.resolve(Object);
    };
    const filterMatches = (responseList)=>{
      return new Promise((resolve,reject)=>{
        const rosterDataList = [];
        if(responseList.length === 0){
          reject(new Error('Not Found Match Information'));
        }
        responseList.forEach((response)=>{
          rosterDataList.push(response.data.included);
        });
        return resolve(rosterDataList);

      });
    };
    const responseSuccessToUser = (matches)=>{
      socket.emit('find-pubg-matches-populated-success',matches);
    };
    const responseFailToUser = (e)=>{
      socket.emit('find-pubg-matches-populated-fail',e);
    };
    tokenValidate(secretKey)
      .then(makeRequest)
      .then(requestMatchInfoToPUBG)
      .then(filterMatches)
      .then(replaceListTorosterList)
      .then(replaceListToparticipant)
      .then(responseSuccessToUser)
      .catch(responseFailToUser);
  });

};



exports.findPUBG_User = findPUBG_User;
exports.findPopulatedMatchList = findPopulatedMatchList;
```

내부 비동기처리는 일단 최대한 피했다.

플랫한것이 가독성은 좋긴하지만 사실 내부적으로 비동기 처리를 할 수 있는것은 비동기처리 하는것이 좋다.
하지만 그에 따라 코드의 가독성이 급속도로 떨어지는 문제가 있는데 협업을 하게 되면 그에 맞게 짜야할 것이다.

나만 알아볼 수 있는 코드는 성능이 좋더라도 피해야한다고 생각한다.
내가 천년만년 작업할 것이 아니기 때문이다.

makeRequest 의 url만드는 부분은 수정되어야할 부분이다.

현재 PUBG API URL 구조가 머리에 전부 박히질 않아서 하드코딩 해놓았다.

코드 내용을 보면 `socket.on('event',callback)` 과 `socket.emit('event',callback)`이 반복되는 모습을 볼 수 있다.

[socket.io]에서는 socket의 이벤트 리스너는 `socket.on`에 이벤트 발생은 `socket.emit`을 이용하도록 API를 제공한다.

이벤트의 발생은 받을 타겟의 범위에 따라 다른 함수들을 제공한다.

해당 내용은 [emit-cheatsheet]를 참고하도록 한다.

이전에는 지원안하던 ack도 지원을 한다.

해당 코드의 자세한 내용은 다음 포스팅으로 넘긴다. 맥북이 글이 너무 길다고 성내듯이 느려진다.

[emit-cheatsheet]:https://socket.io/docs/emit-cheatsheet/
[axios]:https://github.com/axios/axios
[포스팅]:https://kishe89.github.io/electron/2018/04/04/electron-second-example.html
[socekt.io]:https://socket.io/
[mongoose]:http://mongoosejs.com/
[Electron]:https://electronjs.org/
[BrowserWindow]:https://electronjs.org/docs/api/browser-window

