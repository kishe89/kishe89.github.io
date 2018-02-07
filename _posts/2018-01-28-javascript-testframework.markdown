---
layout: post
title:  "Javascript test framework"
date:   2018-01-28 18:58:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Javascript
---

이전까지 node js 에서 테스트 프레임웤은 [Mocha] 를 이용해왔는데 지금 읽고 있는 책(Javascript design pattern)에서는 [Jasmine] 을 이용한 테스트 케이스 작성을 설명하고 있어서 이에 대한 공부를 진행하려 한다.
Mocha 는 TDD(Test Driven Development) 에 필요한 API 들을 제공하는데 assertion 등은 외부라이브러리를 사용해야한다(BDD 스타일의 인터페이스도 지원한다).
Jasmine 은 BDD(Behavior Driven Development) 를 위한 API 들을 제공한다.

둘을 비교한 내용은 아래 링크에 잘 정리 되어있는듯 하여 첨부한다.

https://thejsguy.com/2015/01/12/jasmine-vs-mocha-chai-and-sinon.html

**BDD 의 장점은 테스트로 확일할 기능 또는 작동 로직을 일상 언어로 서술함에 따라 작성중인 코드가 '어떻게'가 아니라 '무엇'을 해야하는지 테스트 코드에 표현할 수 있다.**

### Mocha & Jasmine install
---
##### Mocha
```
npm install --global mocha
npm install --save-dev mocha
```
##### Jasmine
```
npm install --global jasmine
npm install --save-dev jasmine
```
npm 을 이용하여 각각 global 로 설치와 development dependency 로 설치하는 명령어이다.

package.json 을 이용할 경우는
##### package.json
```
{
  "name": "javascript_design_pattern_example",
  "version": "0.0.1",
  "scripts": {
    "test": "mocha ./example2_dependency_injection/DiContainer_01_tests.js --compilers js:babel-register"
  },

  "dependencies": {
    "mocha": "latest",
    "jasmine":"latest",
    "babel": "latest",
    "babel-cli":"latest",
    "babel-core": "latest",
    "babel-preset-env": "latest",
    "babel-polyfill": "latest",
    "babel-preset-es2015": "latest"
  }
}
```
와 같이 설정할 수 있다. 위 package.json 은 mocha 와 es6를 사용하기 위해 babel 설정을 한 것이다.
babel 사용을 위해서는 프로젝트 root 에 사용할 preset 을 나타내는 .babelrc 파일을 생성해줘야하며 .babelrc 는 아래처럼 구성된다.

##### .babelrc
```
{
"presets": ["es2015"]
}
```
node 에서는 babel-node 를 이용하는데 현재 node js 공부가 아니라 javascript design pattern 공부중이기에 babel 을 이용했다.


### Test Case 작성법
---
mocha 의 테스트 꾸러미의 시작은 describe(string, function)로 시작한다.
```javascript
describe('TestExample', function() {

  before(function() {
    // runs before all tests in this block
  });

  after(function() {
    // runs after all tests in this block
  });

  beforeEach(function() {
    // runs before each test in this block
  });

  afterEach(function() {
    // runs after each test in this block
  });

  // test cases
});
```

테스트 케이스는 mocha 는 it(string, function(done)) 으로 시작한다.
Jasmine 은 it(string, function()) 으로 시작한다.
mocha 같은 경우는 작업이 끝날 경우 호출될 done 을 전달하도록 권장한다.

***assert 같은 경우는 mocha 는 제공하지 않기때문에 node 기본 모듈로 제공되는 [Assert] 를 이용하였다.
이외에도 다양한 Assertion library(chai, expect.js, ...) 를 이용 가능하게 제공한다.
Jasmine 은 expect(thing).toBe(expected) 와 같이 expect().xxx() 의 assert API 들이 제공된다.
해당 API 는 matcher 로 제공되며 이는 [Jasmine-Matchers] 에 자세히 설명 되어있다.***

##### Mocha example

```
const assert  = require('assert');
describe('filterTEst', function() {
    const array = [
        {
            "_id": "5a19482ce3267b291bed9d37",
            "Contents": "권한테스트 비공개데이터",
            "PostedBy": {
                "_id": "5a0da87739848b22317c918a",
                "Nick": "김지운",
                "App": "kakao",
                "AppId": "1234567",
                "Profile": "post_1510844531521스크린샷 2017-11-15 오후 7.32.42.png",
                "AccessToken": "$2a$08$o6D0GM1T3m6Ajb57eWK3D.p/T47Xygnoz.zvQ427zKFu5p2XFchgm",
                "DecryptValue": "g41aeqax",
                "__v": 0,
                "CreatedAt": "2017-11-25T15:50:59.125Z",
                "Upload_Article": [],
                "Agree_Wait_Friends": [
                    "5a0ea7e2d6aebb2a8ae0d9a6"
                ],
                "Friends": [
                    "5a0ea6038e0a2d2a080886f9"
                ]
            },
            "__v": 0,
            "UpdatedAt": "2017-11-25T10:38:36.294Z",
            "CreatedAt": "2017-11-25T10:38:36.294Z",
            "Comments": [],
            "Article_List": [
                {
                    "_id": "5a19482ce3267b291bed9d35",
                    "Title": "kim",
                    "Place": "용당 동아아파트104동",
                    "PlaceType": "요식업",
                    "Loc": [
                        127.1231312,
                        34.324224
                    ],
                    "PostedBy": "5a0da87739848b22317c918a",
                    "__v": 0,
                    "UpdatedAt": "2017-11-25T10:38:36.085Z",
                    "CreatedAt": "2017-11-25T10:38:36.085Z"
                },
                {
                    "_id": "5a19482ce3267b291bed9d36",
                    "Title": "lee",
                    "Place": "Naver",
                    "PlaceType": "집",
                    "PostedBy": "5a0da87739848b22317c918a",
                    "__v": 0,
                    "UpdatedAt": "2017-11-25T10:38:36.087Z",
                    "CreatedAt": "2017-11-25T10:38:36.087Z"
                }
            ],
            "Publish_range": 2,
            "Images": [
                "article_1511606312384_스크린샷 2017-10-27 오후 3.31.04.png"
            ],
            "Like": 0
        },
        {
            "_id": "5a17e89406afe3274335381a",
            "Kml_Uri": "",
            "Contents": "오늘도 친구들만 보자!!!!!!!!!",
            "PostedBy": {
                "_id": "5a0ea7e2d6aebb2a8ae0d9a6",
                "Nick": "최석찬",
                "App": "kakao",
                "AppId": "24323232",
                "Profile": "post_1510909918662스크린샷 2017-10-27 오후 3.25.19.png",
                "AccessToken": "$2a$08$56gl232AwLtcL2fDssKdxeZjDiM3SaKFv0/hHWP3XNBOQLml7Ke/u",
                "DecryptValue": "9us1crpz",
                "__v": 0,
                "CreatedAt": "2017-11-25T15:50:59.125Z",
                "Upload_Article": [],
                "Agree_Wait_Friends": [],
                "Friends": []
            },
            "__v": 0,
            "UpdatedAt": "2017-11-24T09:38:28.129Z",
            "CreatedAt": "2017-11-24T09:38:28.129Z",
            "Comments": [],
            "Article_List": [
                {
                    "_id": "5a17e89306afe32743353818",
                    "Title": "kim",
                    "Place": "용당 동아아파트104동",
                    "PlaceType": "요식업",
                    "Loc": [
                        127.1231312,
                        34.324224
                    ],
                    "PostedBy": "5a0ea7e2d6aebb2a8ae0d9a6",
                    "__v": 0,
                    "UpdatedAt": "2017-11-24T09:38:27.911Z",
                    "CreatedAt": "2017-11-24T09:38:27.911Z"
                },
                {
                    "_id": "5a17e89306afe32743353819",
                    "Title": "lee",
                    "Place": "Naver",
                    "PlaceType": "서비스업",
                    "Loc": [
                        126.1231312,
                        35.324224
                    ],
                    "PostedBy": "5a0ea7e2d6aebb2a8ae0d9a6",
                    "__v": 0,
                    "UpdatedAt": "2017-11-24T09:38:27.912Z",
                    "CreatedAt": "2017-11-24T09:38:27.912Z"
                }
            ],
            "Publish_range": 1,
            "Images": [],
            "Like": 0
        },
        {
            "_id": "5a17e86c06afe32743353816",
            "Kml_Uri": "",
            "Contents": "오늘도 친구들만 보자!",
            "PostedBy": {
                "_id": "5a0ea7e2d6aebb2a8ae0d9a6",
                "Nick": "최석찬",
                "App": "kakao",
                "AppId": "24323232",
                "Profile": "post_1510909918662스크린샷 2017-10-27 오후 3.25.19.png",
                "AccessToken": "$2a$08$56gl232AwLtcL2fDssKdxeZjDiM3SaKFv0/hHWP3XNBOQLml7Ke/u",
                "DecryptValue": "9us1crpz",
                "__v": 0,
                "CreatedAt": "2017-11-25T15:50:59.125Z",
                "Upload_Article": [],
                "Agree_Wait_Friends": [],
                "Friends": []
            },
            "__v": 0,
            "UpdatedAt": "2017-11-24T09:37:48.948Z",
            "CreatedAt": "2017-11-24T09:37:48.948Z",
            "Comments": [],
            "Article_List": [
                {
                    "_id": "5a17e86c06afe32743353814",
                    "Title": "kim",
                    "Place": "용당 동아아파트104동",
                    "PlaceType": "요식업",
                    "Loc": [
                        127.1231312,
                        34.324224
                    ],
                    "PostedBy": "5a0ea7e2d6aebb2a8ae0d9a6",
                    "__v": 0,
                    "UpdatedAt": "2017-11-24T09:37:48.222Z",
                    "CreatedAt": "2017-11-24T09:37:48.222Z"
                },
                {
                    "_id": "5a17e86c06afe32743353815",
                    "Title": "lee",
                    "Place": "Naver",
                    "PlaceType": "서비스업",
                    "PostedBy": "5a0ea7e2d6aebb2a8ae0d9a6",
                    "__v": 0,
                    "UpdatedAt": "2017-11-24T09:37:48.224Z",
                    "CreatedAt": "2017-11-24T09:37:48.224Z"
                }
            ],
            "Publish_range": 1,
            "Images": [],
            "Like": 0
        },
        {
            "_id": "5a17e73e287b52008d9f10b0",
            "Contents": "오늘도 즐거운 하루 잘해보자!",
            "PostedBy": {
                "_id": "5a0ea7e2d6aebb2a8ae0d9a6",
                "Nick": "최석찬",
                "App": "kakao",
                "AppId": "24323232",
                "Profile": "post_1510909918662스크린샷 2017-10-27 오후 3.25.19.png",
                "AccessToken": "$2a$08$56gl232AwLtcL2fDssKdxeZjDiM3SaKFv0/hHWP3XNBOQLml7Ke/u",
                "DecryptValue": "9us1crpz",
                "__v": 0,
                "CreatedAt": "2017-11-25T15:50:59.125Z",
                "Upload_Article": [],
                "Agree_Wait_Friends": [],
                "Friends": []
            },
            "__v": 0,
            "UpdatedAt": "2017-11-24T09:32:46.674Z",
            "CreatedAt": "2017-11-24T09:32:46.674Z",
            "Comments": [],
            "Article_List": [
                {
                    "_id": "5a17e73e287b52008d9f10ae",
                    "Title": "kim",
                    "Place": "용당 동아아파트104동",
                    "PlaceType": "요식업",
                    "Loc": [
                        127.1231312,
                        34.324224
                    ],
                    "PostedBy": "5a0ea7e2d6aebb2a8ae0d9a6",
                    "__v": 0,
                    "UpdatedAt": "2017-11-24T09:32:46.413Z",
                    "CreatedAt": "2017-11-24T09:32:46.412Z"
                },
                {
                    "_id": "5a17e73e287b52008d9f10af",
                    "Title": "lee",
                    "Place": "Naver",
                    "PlaceType": "서비스업",
                    "PostedBy": "5a0ea7e2d6aebb2a8ae0d9a6",
                    "__v": 0,
                    "UpdatedAt": "2017-11-24T09:32:46.416Z",
                    "CreatedAt": "2017-11-24T09:32:46.416Z"
                }
            ],
            "Publish_range": 0,
            "Images": [
                "article_1511515963923_스크린샷 2017-10-27 오후 3.25.19.png",
                "article_1511515963987_스크린샷 2017-11-03 오후 2.44.58.png"
            ],
            "Like": 0
        }
    ];

    describe('filterTest1', function() {
        it('this is a test.', function() {
            // write test logic
            const expected_result = [
                {
                    "_id": "5a17e73e287b52008d9f10b0",
                    "Contents": "오늘도 즐거운 하루 잘해보자!",
                    "PostedBy": {
                        "_id": "5a0ea7e2d6aebb2a8ae0d9a6",
                        "Nick": "최석찬",
                        "App": "kakao",
                        "AppId": "24323232",
                        "Profile": "post_1510909918662스크린샷 2017-10-27 오후 3.25.19.png",
                        "AccessToken": "$2a$08$56gl232AwLtcL2fDssKdxeZjDiM3SaKFv0/hHWP3XNBOQLml7Ke/u",
                        "DecryptValue": "9us1crpz",
                        "__v": 0,
                        "CreatedAt": "2017-11-25T16:40:14.161Z",
                        "Upload_Article": [],
                        "Agree_Wait_Friends": [],
                        "Friends": []
                    },
                    "__v": 0,
                    "UpdatedAt": "2017-11-24T09:32:46.674Z",
                    "CreatedAt": "2017-11-24T09:32:46.674Z",
                    "Comments": [],
                    "Article_List": [
                        {
                            "_id": "5a17e73e287b52008d9f10ae",
                            "Title": "kim",
                            "Place": "용당 동아아파트104동",
                            "PlaceType": "요식업",
                            "Loc": [
                                127.1231312,
                                34.324224
                            ],
                            "PostedBy": "5a0ea7e2d6aebb2a8ae0d9a6",
                            "__v": 0,
                            "UpdatedAt": "2017-11-24T09:32:46.413Z",
                            "CreatedAt": "2017-11-24T09:32:46.412Z"
                        },
                        {
                            "_id": "5a17e73e287b52008d9f10af",
                            "Title": "lee",
                            "Place": "Naver",
                            "PlaceType": "서비스업",
                            "PostedBy": "5a0ea7e2d6aebb2a8ae0d9a6",
                            "__v": 0,
                            "UpdatedAt": "2017-11-24T09:32:46.416Z",
                            "CreatedAt": "2017-11-24T09:32:46.416Z"
                        }
                    ],
                    "Publish_range": 0,
                    "Images": [
                        "article_1511515963923_스크린샷 2017-10-27 오후 3.25.19.png",
                        "article_1511515963987_스크린샷 2017-11-03 오후 2.44.58.png"
                    ],
                    "Like": 0
                }
            ];
            array.slice().reverse().forEach(function(article,index,currentArray){

                if(article.Publish_range === 1){
                    if(!(article.PostedBy.Friends.indexOf("5a19482ce3267b291bed9d35")>-1)){
                        console.log(array.splice(((currentArray.length-1)-index),1));
                    }
                }else if(article.Publish_range === 2){
                    if(article.PostedBy._id !== '5a19482ce3267b291bed9d35'){
                        console.log(article.PostedBy._id+':'+'5a19482ce3267b291bed9d35');
                        console.log(array.splice(((currentArray.length-1)-index),1));
                    }
                }

            });
            assert.equal(array,expected_result,'Filter is Invalid');
        });
    });
});
```

Mocha 는 위 ``` const assert = require('assert');``` 와 같이 따로 assertion library 를 이용해야한다.
```javascript
it('this is a test',function())
```
에서는 array 에서 필요한 데이터만을 걸러내기 위한 로직 테스트를 진행하였다.
Jasmine 에서는

##### Jasmine example(자바스크립트 패턴과 테스트 - 길벗 출판사 예제)
```java
describe("DiContainer",() => {
    let DiContainer = require('./DiContainer_00');

    let container;
    beforeEach(()=>{
        container = DiContainer;
    });
    describe('register(name, dependencies, func',()=>{
        it('인자가 하나라도 빠졌거나 타입이 잘못되면 예외를 던진다',()=>{
            let badArgs = [
                [],
                ['Name'],
                ['Name',['Dependency1','Dependency2']],
                ['Name',function () {}],
                [1,['a','b'],function () {}],
                ['Name',[1,2],function () {}],
                ['Name',['a','b'],'should be a function']
            ];
            badArgs.forEach((args)=>{
                expect(()=>{
                    container.register.apply(container,args);
                }).toThrow();
            })
        });
    });
});
```
와 같이 작성하게 된다.
둘이 비슷한데 mocha 는 UI 로 표현하는 기능을 제공하는지 모르겠으나 Jasmine 은 HTML 페이지에서 테스트 내용과 결과에 대해 표시해주는게 괜찮은 것 같다.
Jasmine 은 공부를 하면서 더 자세히 봐야겠다.

[Mocha]:https://mochajs.org/
[Jasmine]:https://jasmine.github.io/index.html
[Assert]:https://nodejs.org/api/assert.html
[Jasmine-Matchers]:https://jasmine.github.io/api/2.6/matchers.html
