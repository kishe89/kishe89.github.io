---
layout: post
title:  "Javascript callback-2"
date:   2018-02-11 16:48:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Javascript
---

```
자바스크립트 패턴과 테스트
길벗출판사,(지은이) 래리 스펜서, 세스 리처즈 ,(옮긴이) 이일웅
```
참고

[Javascript callback-1] 에서는 Javascript 에서의 기본적인 **Callback** 의 작성 방법과 **Promise** 패턴에 대해 알아봤다.

**async await** 에 대해서 알아본다.

### async await 설정
---

##### .babelrc
```
{
"presets": ["es2017"]
}
```
##### package.json 에서 dependency injection
```
"babel-preset-es2017": "latest"
```

**async await**은 ES7 에서 추가되었다. 또한 Node js 에서는 7.6 version 아래로는 지원하지 않는다.

지금 글을 작성하는 이 시점에서 최신 버전은 9.5.0 이며 LTS 버전은 8.9.4 이다.

Babel 설정파일에 presets 은 es2017 을 추가 or 수정해준다.

### async await usage
---

```javascript
async function name([param[, param[, ... param]]]) {
   statements
}
```
[async function] 참조

async function 을 선언하는 기본 구문 형태이다.

async function 은 **Promise**를 리턴한다.

이 **Promise**는 resolve(이행됨), reject(거절됨) 상태로 리턴이 된다.

resolve 가 되는 조건은 정상적인 return 에 의하고 reject 는 exception 이 발생하거나 새로운 Error 를 throw 하면 발생한다.

statements 에는 실질적인 함수의 구현부를 작성하게된다.

**async await**의 목적은 사용하는 Promise 의 동작을 동기스럽게 사용할 수 있게 도와준다.(Promise.All 과 비슷하다.)

하지만 좀 더 비동기 흐름에대해 직접적인 제어를 할 수 있도록 도와준다.

Promise 만을 이용시에 All 과 race 는 각자 iterable 을 받아서 전체가 실행되길 기다리거나 먼저 처리 되는것에 따라 결정되었다.

이 부분에 대해서 좀 더 유연하게 처리가 가능하다.

async await 을 이용하여 각각의 비동기 함수들의 Promise 를 동기처럼 구성하거나 혹은 ```Promise.All(iterable)``` 과 같이 처리가 가능하다.

아래 예제는 [MDN web docs]에서 가지고 온 예제이다.

##### MDN web example
```javascript
function resolveAfter2Seconds(x) {
    return new Promise(resolve => {
        setTimeout(() => {
            resolve(x);
        }, 2000);
    });
};

async function add1(x) {
    var a = resolveAfter2Seconds(20);
    var b = resolveAfter2Seconds(30);
    return x + await a + await b;
};

add1(10).then(v => {
    console.log(v);  // prints 60 after 2 seconds.
});

async function add2(x) {
    var a = await resolveAfter2Seconds(20);
    var b = await resolveAfter2Seconds(30);
    return x + a + b;
};

add2(10).then(v => {
    console.log(v);  // prints 60 after 4 seconds.
});
```
resolveAfter25seconds(x) 함수는 새로운 Promise 를 반환한다.

응답되는 Promise 는 2초뒤에 전달받은 x 를 이행함으로 Promise 를 결정하는 함수이다.

add1(x) 함수의 앞을 잘 본다. async function 이라고 선언 되어있다.

async function 은 앞에서 이야기 했듯이 정상 return 에 대해서 Promise.resolve(value)를 하게 된다.

위 예제를 아래처럼 수정해본다.

##### MDN web example modify
```javascript
function resolveAfter2Seconds(x) {
    return new Promise(resolve => {
        setTimeout(() => {
            resolve(x);
        }, 2000);
    });
};

async function add1(x) {
    var a = resolveAfter2Seconds(20);
    var b = resolveAfter2Seconds(30);
    return x + await a + await b;
};

add1(10).then(v => {
    console.log(v);  // prints 60 after 2 seconds.
});

async function add2(x) {
    var a = await resolveAfter2Seconds(20);
    var b = await resolveAfter2Seconds(30);
    return x + a + b;
};

add2(10).then(v => {
    console.log(v);  // prints 60 after 4 seconds.
});

async function add3(x) {
    var a = resolveAfter2Seconds(20);
    var b = resolveAfter2Seconds(30);
    return x + a + b;
};

add3(10).then(v => {
    console.log(v);  //immediately prints  10[object Promise][object Promise]
});
```
add3 함수를 추가하였다.

일단 add1 부터 차근차근 보도록 한다.

resolveAfter25seconds(20),(30) 을 가지는 a,b 변수를 선언하고 return 에서 전달받은 x+ await a+ await b 를 호출하였다.

await 는 해당 Promise 가 settled 될때까지 기다리게 되는데 위와 같이 Promise 를 반환받아서 await 를 하게되면 처리시간이 다른경우는 오래 걸리는쪽에 맞춰서(병렬) 반환하게 된다.

위에서는 2000 밀리초로 모두 같아서 못느끼지만 하나의 함수의 delay 를 따로 줘서 구현해보면 알 수 있다.

add3 함수는 안에서 Promise 들이 settled 될때까지 기다리지 않았다.

출력은 바로 일어나게되며 전달한 값인 10에 Promise 객체를 나타내는 로그가 붙어서 나올 것이다.

아래의 예를 본다.
```javascript
function resolveAfter2Seconds(x) {
    return new Promise(resolve => {
        setTimeout(() => {
            resolve(x);
        }, 2000);
    });
};
function resolveAfter4Seconds(x) {
    return new Promise(resolve => {
        setTimeout(() => {
            resolve(x);
        }, 4000);
    });
};

async function add1(x) {
    var a = resolveAfter2Seconds(20);
    var b = resolveAfter2Seconds(30);
    return x + await a + await b;
};

add1(10).then(v => {
    console.log(v);  // prints 60 after 2 seconds.
});

async function add2(x) {
    var a = await resolveAfter2Seconds(20);
    var b = await resolveAfter2Seconds(30);
    return x + a + b;
};

add2(10).then(v => {
    console.log('add2 : '+v);  // prints 60 after 4 seconds.
});

async function add3(x) {
    var a = await resolveAfter2Seconds(20);
    var b = await resolveAfter4Seconds(30);
    return x + a + b;
};

add3(10).then(v => {
    console.log('add3 : '+v);  // prints  60 after 6 seconds
});

async function add4(x) {
    var a =  resolveAfter2Seconds(20);
    var b =  resolveAfter4Seconds(30);
    return x + await a + await b;
};

add4(10).then(v => {
    console.log('add4 : '+v);  // prints  60 after 4 seconds
});
```
실행 순서가 어떻게 될 지 생각해본다.

일단 add1 의 then 에 등록된 Callback 이 가장먼저 실행 될것이다.

그 후 'add2 의 then 에 등록된 Callback 이 호출될 것이다.' 라고 생각할 수 있다.

하지만 로그를 보면 놀라운 결과가 나온다.

![Alt text](/assets/javascript_tdd_image/ex5/index5.png)

로그에는 **add1 -> add4 -> add2 -> add3** 의 순서로 찍힌다.

add2 와 add4 는 4초의 delay 를 동일하게 가지는데 함수의 호출 순서대로가 아닌 로그의 출력이 일어났다.

add2 는 순차 처리를 하고 add4 는 병렬로 처리하고 있기 때문이다.

꼭 add2 와 같은 방식으로 처리해야 할 것이 아니라면 add1, add4 와 같이 작성하는게 속도에서 이점이 있다.

어쨋든 위 예를 보면 대부분의 내용은 이해할 수 있을것으로 생각한다.

**async 는 return 하게되면 Promise.resolve 로 thenable Promise 를 리턴한다.**

**async 는 exception, Error 를 throw 하면 Promise.reject 로 Promise 를 리턴한다.**

**await 를 통해서 Promise 가 settled 까지 기다릴 수 있다.**


앞에서 작성하던 계산기는 다음 포스팅에서 지금까지 본 내용을 포함하여 작성한다.


[Javascript callback-1]:https://kishe89.github.io/javascript/2018/02/11/javascript-callback-1.html
[async function]:https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Statements/async_function
[MDN web docs]:https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Statements/async_function
