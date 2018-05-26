---
layout: post
title:  "Electron & Socket.io 를 이용한 챗봇 개발기4"
date:   2018-05-26 16:14:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Electron
---


이전 [포스팅]에서는 [socket.io]와 [mongoose]를 활용헌 웹소켓 API를 작성하는 방법을 간단히 봤다.

이번 글에서는 이전에 설명하지 않은 코드 부분을 마저 본다.

클라이언트측 코드는 다음 포스팅부터 보도록 하겠다.

일단 이전 코드를 전부 설명하기보단 2개의 api중 한가지만 보도록한다.

### findPUBG_User API

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
exports.findPUBG_User = findPUBG_User;
```

`findPUBG_User` function은 `socket.on('find-pubg-user',callback)` 을 호출한다.

socket 의 이벤트 리스너에게 'find-pubg-user' 이벤트가 발생시 호출할 콜백을 등록해주는데 이 콜백은
다음과 같은 처리를 해야한다.

1. 이벤트를 발생시킨 클라이언트의 유효성을 검사
2. 배틀그라운드 유저정보를 검색
3. 검색된 배틀그라운드 유저정보를 우리측 User 정보에 Update
4. 클라이언트에게 응답.

위 작업중 3번의 경우는 클라이언트게 응답을 좀 더 빠르게 주기 위해 2번에서 가져온 데이터를 클라이언트에 응답하고 우리측 User 정보에  Update하도록 할 수도 있을것이다.
하지만 일단은 데이터를 일관성있게 유지하기 쉽게 모든 처리가 된 후 응답하도록한다.

##### 1. 이벤트를 발생시킨 클라이언트의 유효성을 검사

1번작업을 하는 함수는 `tokenValidate` 함수이다.

```javascript
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
```

결과로는 Promise 를 리턴하는데 리턴되는 Promise는 jwt 토큰을 검증하고 복호화에 성공혹은 실패하면
작업을 종결하는 Promise이다.

정상적으로 복호화되면 resolve로 결정하고 복호화된 객체를 파라미터로 전달한다.

실패시에는 reject로 결정하고 에러 객체를 파라미터로 전달한다.

이 부분은 전체 API에서 동일하게 작동하기때문에 따로 뺐지만 코드내용은 동일하니 그대로 본다.

##### 2. 배틀그라운드 유저정보를 검색

이 부분은 세부적으로 3단계로 나뉜다.
처음은 PUBG서버의 API 요청을 생성하는 작업
두번째는 요청을 날리는 작업
세번째는 응답을 적절히 필터하는 작업 이다.

1. 요청생성
    ```javascript
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
      ```

    첫번째로 요청을 생성하는 작업인데 물론 위에서 이야기한 작업을 한번에 다 해도 괜찮지만 파라미터 유효성검증 함수등 부가적인 로직이 들어가면 점점 더 거대해질 수 있기때문에
    분리하였다.

    일단은 파라미터가 있는지 없는지만 확인 후 넘어가도록 하였다.
    모든 파라미터가 있는경우 만든 request 객체를 resolve로 전달한다.
    그 이외에는 전부 reject 시킨다.

2. 만들어진 request 객체로 요청
    ```javascript
    const requestProfileToPUBG = (request)=>{
          return instance.get(request.url);
        };
    ```

    1번에서 생성한 request 객체를 인자로 받고 앞에서 이야기 했던 axios instance 를 이용하여 get method 로 요청을 보낸다.
    참고로 다시 이야기 하지만 axios 를 사용한것은 promise 를 기반으로 작동하기 때문에 사용하였다. 즉 instance.get 의 결과로는
    promise 를 반환한다.

3. 응답을 적절히 필터
    ```javascript
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
    ```

    `instance.get(request.url);` 의 결과로 반환될 응답을 적절히 필터한다.
    해당 요청의 응답으로는 user 의 정보조회를 위한 링크등 여러가지 정보들이 포함되서 오는데 지금은 그 정보들이 필요치않다.
    해서 제외하고 저장하기 위해 나머지 정보는 거른다.


##### 3 검색된 배틀그라운드 유저정보를 우리측 User 정보에 Update
```javascript
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
```

mongoose 의 model의 내장함수를 사용하기 위해 정의해놓은 User 모델을 로드한다.

그리고 query는 document의 ObjectID 를 이용하기 위해서
```javascript
const query = {
        _id:user._id
      };
```
와 같이 작성하고 options 도 올바르게 작성한다.

그 후 Update할 object를 만들어주는데 match 정보들을 user에게 저장해놓기 위해서
```javascript
pubgUser.attributes.matches.data.forEach((match)=>{
        user.Matches.push(match);
      });
```
로 저장하도록 한다.

최종적으로 user 에는 match에 대한 정보들과 id, name이 셋된다.

이를 DB에 반영하기 위해서는 `User.findOneAndUpdate(query,user,options).exec();` 를 호출해준다.
굳이 exec 를 호출한건 promise를 반환받기 위해서이다.

[mongoose]의 document 를 잘 보아야한다. 몇몇 함수들은 promise 를 반환하지 않거나 반환받기위해 해줘야하는 작업이 있을 수 있다.

`User.findOneAndUpdate(query,user,options).exec();` 를 호출하게 되면 query에 따른 document를 검색하고 찾으면 두번째 파라미터로 전달된 object로 업데이트 하게된다.
없다면 options 의 option에 따라 다르게 처리된다.

여기까지면 우리측 DB 의 작업이 끝난다.

##### 4 클라이언트에게 응답

```javascript
const responseSuccessToUser = (user)=>{
  socket.user = user;
  socket.emit('find-pubg-user-success',user);
};
const responseFailToUser = (e)=>{
  socket.emit('find-pubg-user-fail',e);
};
```
응답의 경우 두가지가 필요한데 성공과 실패에 대한 응답이다.
성공시에는 성공 이벤트를 실패시에는 실패이벤트를 클라이언트에게 응답한다.

이제 이를 최종적으로 호출해보면 아래와 같이 호출할 수 있을 것이다.
```javascript
tokenValidate(secretKey)
      .then(makeRequest)
      .then(requestProfileToPUBG)
      .then(filterProfile)
      .then(updateUserInformation)
      .then(responseSuccessToUser)
      .catch(responseFailToUser);
```
Promise를 이용하는 이유중 또 한가지가 중간에 로직을 추가하기 쉬워진다는 장점이 있다.

위에서 물론 각각의 응답 결과에 대한 것을 알고 있어야하지만 그와 상관없는 처리나 순서가 보장될 필요 없는 작업등을

추가 삭제하기 쉬워진다.

앞에서 이야기했듯이 우리측 DB에 저장하는 작업은 후에 PUBG서버에 동일한 요청을 보내는 횟수를 줄일 목적인거지

무조건 저장되어야만 어플리케이션이 동작하는 것은 아니다.

그럴 경우 위에서 responseSuccessToUser 와 updateUserInformation 의 처리순서는 바뀌어도 상관없다.

물론 파라미터를 동일하게 해주기 위해 약간의 작업은 해야하지만 무지막지한 콜백체인에서 하는 것보다는 훨씬 가벼운
작업일 것이다.



[emit-cheatsheet]:https://socket.io/docs/emit-cheatsheet/
[axios]:https://github.com/axios/axios
[포스팅]:https://kishe89.github.io/electron/2018/05/05/electron-third-example.html
[socket.io]:https://socket.io/
[mongoose]:http://mongoosejs.com/
[Electron]:https://electronjs.org/
[BrowserWindow]:https://electronjs.org/docs/api/browser-window

