---
layout: post
title:  "JavaScript callback-1"
date:   2018-02-11 04:07:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Javascript
---

```
자바스크립트 패턴과 테스트
길벗출판사,(지은이) 래리 스펜서, 세스 리처즈 ,(옮긴이) 이일웅
```
참고

**JavaScript 에서 함수들은 파라미터로 함수를 받을 수 있고 응답으로 함수 또는 결과를 응답할 수 있다.**

```javascript
function add(value1,value2,saveFunc){
  let result = value1 + value2;
  return saveFunc(result);
}
```

위 코드에서 value1, value2 는 더할 값이고 saveFunc 는 결과 값을 저장할 함수가 된다.

여기서 saveFunc 은 value1 + value2 가 result 에 담긴 후에 동기적으로 실행되는 함수이다.

이런 함수를 콜백(동기식) 이라고 한다.

이외에 io 처리 혹은 연산량이 많은 데이터처리 함수등은 실행 흐름에서 점유를 줄이기위해서 일단 다른 로직으로 이동한 후
이벤트등에 의해 호출 될 수 있는데 이런 함수를 콜백(비동기식) 이라고 한다.

동기식은 위 예제로도 이해가 될거다.

비동기식이 문제인데 가장 유명한 예는 Timer 를 이용한 예제일 것이다.

```javascript
setTimeout(function(){
  console.log('Hello');
}, 3000);
console.log('Hi');
```

setTimeout 함수의 콜백으로 console.log('Hello')를 호출하는 함수를 등록해주었다.
이 함수는 3초 지연후에 실행되는 콜백이다.

즉 위와 같이 코드를 작성하였다면 동기식으로 동작한다면 순서대로 console 창에는

1. Hello

2. Hi

가 찍힐 것이다. 결과를 보도록 한다.

![Alt text](/assets/javascript_tdd_image/ex5/index1.png)

결과는 Hi 가 찍히고 Hello 가 찍힐 것이다.

**setTimeout 은 전달받은 callback 을 함께 전달받은 delay 값 이후 호출한다.**

#### 주의사항
```
setTimeout 은 제공된 delay 보다 빨리 실행되지 않는다는 것만 보장한다.
```


이러한 동작은 EventEmitter, EventListener 를 정의하여 우리가 작성할 수도 있고 Node Js 와 Javascript 에서 제공한다.

또한 비동기 콜백 처리를 쉽고 읽기 쉽게 하기위한 여러가지 방안들이 제안되고 생겨났다.

초반에는 비동기 콜백을 waterfall 형태로 표현하는 것부터 **Promise 패턴, async await** 까지 많은 패턴들이 생겨났다.

일단 간단한 계산기 어플리케이션을 만드는것을 예로 들겠다.

모든 기능은 먼저 테스트를 작성하고 테스트를 성공시켜나가는 과정으로 작성된다.

### Calculator_tests01
---

```javascript
describe('Calculator',()=>{
    let myApp;
    const dummyArray = [
        1,2,3,4,5,6,7,8,9,10
    ];
    beforeEach(()=>{
        myApp = new MyApp();
        myApp.setCalculator(new Calculator());
    });

    describe('Calculator.add()',()=>{

        it('integer parameters add',()=>{
            const result= myApp.calculator.add(1,2,3);
            expect(result).toBe(6);
        });
        it('integer parameters & ArrayParameter add',()=>{
            const result= myApp.calculator.add(1,2,dummyArray);
            expect(result).toBe(58);
        });

    });
});
```
일단은 계산기의 덧셈 테스트를 작성하도록 한다.

필요한 기능은 인자로 여러개의 숫자를 받을 수 있고 혹은 array 로 전달된 데이터도 더해주는 덧셈기능이다.

일단 테스트의 시작을 위해 MyApp 과 Calculator 를 작성한다.

### MyApp01
---

```javascript
'use strict';
let MyApp = function () {
    if(!(this instanceof MyApp)){
        throw new Error('this instance created by new');
    }
};

MyApp.prototype.setCalculator = function (calculator) {
    this.calculator = calculator;
};
```

### Calculator01
---

```javascript
'use strict';
let Calculator = function () {
    if(!(this instanceof Calculator)) {
        return new Error('Call by new');
    }
};

Calculator.prototype.add = (...args)=>{
};
```

### Calculator.html
```html
<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <link data-require="jasmine@2.0.0" data-semver="2.0.0" rel="stylesheet" href="http://cdn.jsdelivr.net/jasmine/2.0.0/jasmine.css" />
    <script data-require="jasmine@2.0.0" data-semver="2.0.0" src="http://cdn.jsdelivr.net/jasmine/2.0.0/jasmine.js"></script>
    <script data-require="jasmine@2.0.0" data-semver="2.0.0" src="http://cdn.jsdelivr.net/jasmine/2.0.0/jasmine-html.js"></script>
    <script data-require="jasmine@2.0.0" data-semver="2.0.0" src="http://cdn.jsdelivr.net/jasmine/2.0.0/boot.js"></script>

    <script src="Calculator.js"></script>
    <script src="MyApp.js"></script>
    <script src="Calculator_tests.js"></script>
</head>

<body>
<h1>Calculator Test.(Callback Example)</h1>
</body>

</html>
```

여기까지 작성하고 Calculator.html 을 실행하여 테스트를 돌려본다.

![Alt text](/assets/javascript_tdd_image/ex5/index2.png)

위와 같이 테스트는 실패할 것이다.

add 에는 아무런 작업도 하지 않았기에 당연한 일이다.

그럼 첫번째 테스트를 성공시키기 위해 최소한의 작업을 해본다.

Calculator 의 add 를 아래와 같이 수정한다.

### Calculator02
---

```javascript
Calculator.prototype.add = (...args)=>{
    let result = 0;
    args.forEach((value)=>{
        result+=value;
    });
    return result;
};
```

그리고 Calculator.html 을 실행하여 테스트를 돌려본다.

![Alt text](/assets/javascript_tdd_image/ex5/index3.png)

첫번째 테스트가 성공했다. add 를 잘보면 Arrow Function 으로 선언을 해주었다.

주로 표현식을 나타내고 익명함수를 작성하는데 사용할 수 있는데 Arrow Function 은 자기자신의 this, arguments, super 또는 new.target 을 바인딩하지 않는다.

대신 Function 표현에 비해 짧게 표현할 수 있다. 일반적으로 메소드(객체의 행동)을 제외한 곳에 사용하는 게 적당하다.

하지만 지금 우리의 add 는 this 가 필요가 없고 파라미터를 받기때문에 간결하게 표현하기 위해 사용하였다.

arguments 를 바인딩하지 않기때문에 사용할 수 없는데 이를 대체하는 방법으로는 나머지 매게변수(... 으로 표현)이 있다.

위 add function 의 선언부를 보면 ...args 가 보일 것이다.

...args 로 표현된 부분 부터 그 뒤까지 전달된 모든 변수를 args array 로 가지게 된다.

모든 매게변수를 args array 로 받으면 전달되는 매게변수의 갯수는 신경쓸 필요가 없다.

args 를 forEach 문을 이용하여 순회하며 result 에 더해 나간 후 result 를 반환하도록 하였다.

그럼 이제 두번째 테스트를 성공할 수 있게 생각해본다.

### Calculator03
---

```javascript
Calculator.prototype.add = (...args)=>{
    let result = 0;
    args.forEach((value)=>{
        if(Array.isArray(value)){
            value.forEach((value)=>{
                result += value;
            });
            return result;
        }
        result+=value;
    });
    return result;
};
```
위와 같은 코드를 생각할 수 있을 것이다. 위 코드는 돌려보면 테스트를 통과한다.

Array 가 섞여서 들어오더라도 처리할 수 있는 덧셈 기능이 완성되었다.

헌데 위 코드에서 보면 DRY 하지 않은 부분이 보인다.
```javascript
if(Array.isArray(value)){
   value.forEach((value)=>{
      result += value;
   });
return result;
}
```
이 부분은 원래 add 가 하는일과 다른게 없다. args Array 를 받아서 순회하며 result 에 더하는 것이다.

자기자신을 호출해주면 될것같다.(재귀적)

### Calculator04
---

```javascript
Calculator.prototype.add = (...args)=>{
    let result = 0;
    args.forEach((value)=>{
        if(Array.isArray(value)){
            value.forEach((value)=>{
                result += Calculator.prototype.add(value);
            });
            return result;
        }
        result+=value;
    });
    return result;
};
```
코드가 오히려 길어졌다. 허나 행위자체의 의미가 동일하니 알아보기는 더 쉬울 것이다.

그리고 의외의 효과를 같이 얻었다. 아래의 테스트를 작성해서 돌려보자.

### Calculator_tests02
---

```javascript
describe('Calculator',()=>{
    let myApp;
    const dummyArray = [
        1,2,3,4,5,6,7,8,9,10
    ];
    const dummyNdepthArray = [
        1,2,3,4,5,6,7,8,9,10,
        [
            1,2,3,4,5,6,7,8,9,10,
            [
                1,2,3,4,5,6,7,8,9,10
            ]
        ]
    ]
    beforeEach(()=>{
        myApp = new MyApp();
        myApp.setCalculator(new Calculator());
    });

    describe('Calculator.add()',()=>{

        it('integer parameters add',()=>{
            const result= myApp.calculator.add(1,2,3);
            expect(result).toBe(6);
        });
        it('integer parameters | ArrayParameter add',()=>{
            const result= myApp.calculator.add(1,2,dummyArray);
            expect(result).toBe(58);
        });
        it('N depth ArrayParameter add',()=>{
            const result= myApp.calculator.add(1,2,dummyNdepthArray);
            expect(result).toBe(168);
        });
    });
});
```

dummyNdepthArray 는 array 안에 array 가 들어있는 3차 배열이다.

동일 행위에 대해서 우리가 처음에 작성한 코드라면 위 테스트는 실패할 것이다.

왜냐하면 차원에 대해서 일반화를 시키지 않았기 때문이다.

일단 테스트를 돌려본다.

![Alt text](/assets/javascript_tdd_image/ex5/index4.png)

테스트는 성공한다.

같은 행위에 대해 차원이 다를경우는 재귀를 이용하면 반복 코드를 제거하고 좀더 명확히 작성할 수 있다.

DRY 하게 짜기위한 노력의 보상이라고 생각하자.

### Calculator05
---

```javascript
Calculator.prototype.add = (...args)=>{
    let result = 0;
    args.forEach((value)=>{
        if(Array.isArray(value)){
            result += Calculator.prototype.add(...value);
            return;
        }
        result+=value;
    });
    return result;
};
```

```장준영 님 피드백.```

나머지 매개변수는 파라미터 전달식으로도 사용가능하다.

이때는 나머지 매개변수가 아닌 전개 연산자라고 한다.

나머지 매개변수나 전개 연산자나 문법은 비슷하다.

하지만 동작의 차이가 있는데 전개 연산자를 나머지 매개변수로 사용시 여러개의 길이 미정인 파라미터들을
하나의 파라미터로 묶는 동작을 하고

전개 연산자로서 사용하면 iterable 한 데이터에 대해서 각각의 element 로 분리할 수있다.

즉 ```[1,2,3,4,5]``` 의 array 가 있다고 했을 때 위의 코드상에서 보자면

```
(...args)=>{ // 1,2,3,4,5 => [1,2,3,4,5] 로 변환
};
```


```
Calculator.prototype.add(...value); // [1,2,3,4,5] => 1,2,3,4,5 로 전개
```
가 된다.

위와 같이 작성하면 Array 에 대해서 다시 순회할 필요가 없어진다.

---

여태 이번 포스팅의 주제인 **Callback** 에 대해 이야기 하지 않았다.

왜냐하면 우리는 이미 **Callback**을 사용하고있다.

일반적으로 우리가 많이 사용하는 for 문을 생각해본다.

```javascript
for(let index = 0 ; index < args.length ; index++){
  //TODO
  done(args[index]);
}
```
forEach 를 for 문으로 바꾸게 되면 위와 같이 변경될것이다.

Array 를 순회하며 각 element 들을 제공된 함수에 파라미터로 던져주는 역할을 한다.

불필요한 index 의 선언등이 필요없으므로 코드가 많이 짧아지고 실수할 포인트가 줄어든다.
물론 필요하다면 Callback 으로 index, 순회될 배열도 받을 수 있다.

또한 이런 Callback 또한 일반 함수처럼 체인을 할 수 있다.

```javascript
Calculator.prototype.add = (...args)=>{
    let result = 0;
    args.forEach((value)=>{
        if(Array.isArray(value)){
            value.forEach((value)=>{
                result += value;
            });
            return result;
        }
        result+=value;
    });
    return result;
};
```
앞에서 1차원 Array 를 처리하기 위해 짰던 코드가 콜백체인을 나타내준다.

forEach 의 콜백안에 또 forEach 함수를 체인하고 그 forEach 의 콜백이 체인되는 형태이다.

이러한 형태로 10차원까지 간 코드를 생각해보면 끔찍할 것이다.

동기식으로 동작하는 함수들은 그나마 괜찮지만 함수 내부에 비동기 함수들이 몇 depth 씩 연결되있고 그러한 함수가 여러개라면 실행순서를 읽기도 힘들고
코드또한 오류를 발생시킬 가능성이 높아진다.

CallBack 에서 주의 할 것이 이것만 있는게 아니다.

this 또한 현제 실행중인 CallBack 을 가리킬 거라고 예상할 수 있지만 그렇지 않다.

Arrow function 을 이용해 콜백을 작성시 this 는 특히 조심 해야한다.

이제 비동기 함수 호출시 좀 더 안전하게 사용하기 위해 제안된 **Promise 패턴, async await**를 본다.

일단 **Promise** 에대해 알아본다.

Promise 는 ES5 에서 추가되었는데 이전에는 모듈로 제공되었다.
```javascript
new Promise( /* executor */ function(resolve, reject) { ... } );
```
기본 구문은 위와 같은데 실행자(function) 은 resolve, reject 이라는 Promise 의 상태를 결정하는 메서드를 가지고 있다.

이 두 메서드는 각자 fulfill(이행됨), reject(거절됨)을 결정하게 된다.

이행 혹은 거절이 아닌 상태는 pending(대기됨) 상태인데 프로세스가 실행중인 상태로 이해하면 된다.

이행 이나 거절로 결정된 상태 즉 resolve, reject 가 호출된 상태는 settled(처리됨)이라고 한다.

resolve 나 reject 는 thenable 즉 then 을 지닌 Promise 를 반환한다.

이를 통해 연속적으로 체인이 가능하다.

이외에도 Promise 는 all, race 메서드를 제공한다.

```javascript
Promise.all(iterable)
```
Promise.All 메서드는 모든 Promise 가 결정된 상태를 기다렸다 결정되며 하나라도 거절되면 거절 즉시 reject 한다.

```javascript
Promise.race(iterable)
```
Promise.race 메서드는 iterable 객체가 전달시 상태가 결정되면 바로 그 상태로 결정한다.

Promise 는 비동기 콜백 체인 및 동기 콜백 체인 코드를 좀 더 Flat(평평) 하게 해준다.

콜백체인은 indent depth 의 증가를 불러오는데 단순한 함수들만이 존재하면 그나마 다행일 것이다.

하지만 그안에 여러 분기 조건문, 반복문, 비동기처리 함수 등이 존재하면 Callback Hell 을 볼 수 있다.

##### Callback Hell
```javascript
app.post('/stamp/check',function(req,res){
        req.body.req_status = State_enum.get("/stamp/check");
        var stamp_validator = require('../validator/Stamp_validator.js')(req.body,State_enum);
        var access_token = new UserAccesstoken();
        if(stamp_validator === "SUCCESS"){
            access_token.findOneNick(req.body.nick,function(err,data){
                if(err){
                    generator.normal(res,res_code.notenough_data,res_code.msg_empty,res_code.msg_invalidaccesstoken);
                    return;
                }else{
                    if(!data){
                        //valid accesstoken not exist
                        generator.normal(res, res_code.notenough_data, res_code.msg_empty, res_code.msg_invalidaccesstoken);
                    }else{
                        //valid accesstoken exist
                        if(data.otp === req.body.accesstoken){
                            //valid
                            var town_code = req.body.town_code;
                            var nick = req.body.nick;

                            Clearpool.of('master').getConnection(function(err,connection){
                                if(err){
                                    generator.cleardb(connection,err,res,res_code.dberr, res_code.emptydata,res_code.msg_fail);
                                    return;
                                }
                                connection.query(Town.findTownCode(town_code),function (err, town) {
                                    if(err){
                                        generator.cleardb(connection,err,res,res_code.dberr, res_code.emptydata,res_code.msg_fail);
                                        return;
                                    }else{
                                        if(!town[0]){
                                            //invalid town_code

                                            var unexpected_result = {TOWN_CODE : "-1"};
                                            generator.cleardb(connection,err,res,res_code.success,unexpected_result,res_code.msg_success);
                                        }else{
                                            //valid town_code

                                            connection.query(Stamp.findAbleCheck(),[nick,town[0].TOWN_CODE,town[0].REGION_CODE],function (err, sccount) {
                                                if(err){
                                                    generator.cleardb(connection,err,res,res_code.dberr, res_code.emptydata,res_code.msg_fail);
                                                    return;
                                                }else{
                                                    if(sccount[0]){
                                                        var count = sccount[0].SC_COUNT+1;
                                                        connection.beginTransaction(function (err) {
                                                            if(err){
                                                                generator.cleardb(connection,err,res,res_code.dberr, res_code.emptydata,res_code.msg_fail);
                                                                return;
                                                            }
                                                            connection.query(Stamp.stampCheck(),[town[0].TOWN_CODE,town[0].REGION_CODE,nick,count],function (err, result) {
                                                                if(err){
                                                                    if(err.message.indexOf("ER_DUP_ENTRY") != -1) {
                                                                        unexpected_result = {TOWN_CODE : -1};
                                                                        generator.cleardb(connection,err,res,res_code.success, unexpected_result,res_code.msg_success);
                                                                    }
                                                                    else generator.cleardb(connection,err,res,res_code.dberr, res_code.emptydata,res_code.msg_fail);
                                                                    return;
                                                                }
                                                                Clearpool.of('slave1').getConnection(function (err, slave_connection) {
                                                                    if (err) {
                                                                        res.status(500).send({code: "03", resultData: res_code.msg_fail_update_pw, message: "slaveDBFAIL"});
                                                                        connection.rollback(function (err) {
                                                                            connection.release();
                                                                        });
                                                                        slave_connection.release();
                                                                        return;
                                                                    }
                                                                    slave_connection.beginTransaction(function (err) {
                                                                        if(err){
                                                                            res.status(500).send({code: "03", resultData: res_code.msg_fail_update_pw, message: "slaveDBFAIL"});
                                                                            connection.rollback(function (err) {
                                                                                connection.release();
                                                                            });
                                                                            slave_connection.release();
                                                                            return;
                                                                        }
                                                                        slave_connection.query(Stamp.stampCheck(),[town[0].TOWN_CODE,town[0].REGION_CODE,nick,count],function(err,rows){
                                                                            if(err){
                                                                                if(err.message.indexOf("ER_DUP_ENTRY") != -1) {
                                                                                    unexpected_result = {TOWN_CODE : -1};
                                                                                    slave_connection.release();
                                                                                    connection.rollback(function (err) {
                                                                                        generator.cleardb(connection,err,res,res_code.success, unexpected_result,res_code.msg_success);
                                                                                    });
                                                                                }
                                                                                else {
                                                                                    slave_connection.release();
                                                                                    connection.rollback(function (err) {
                                                                                        generator.cleardb(connection,err,res,res_code.dberr, res_code.emptydata,res_code.msg_fail);
                                                                                    });
                                                                                }
                                                                                return;
                                                                            }
                                                                            connection.commit(function (err) {
                                                                                if(err){
                                                                                    slave_connection.rollback(function (err) {
                                                                                        slave_connection.release();
                                                                                    });
                                                                                    connection.rollback(function (err) {
                                                                                        generator.cleardb(connection,err,res,res_code.dberr, res_code.emptydata,res_code.msg_fail);
                                                                                    });
                                                                                    return;
                                                                                }
                                                                                slave_connection.commit(function (err) {
                                                                                    if(err){
                                                                                        slave_connection.rollback(function (err) {
                                                                                            slave_connection.release();
                                                                                        });
                                                                                        connection.rollback(function (err) {
                                                                                            generator.cleardb(connection,err,res,res_code.dberr, res_code.emptydata,res_code.msg_fail);
                                                                                        });
                                                                                        return;
                                                                                    }
                                                                                    connection.query(Stamp.stampfind(),[nick,town[0].TOWN_CODE,count],function(err,stamp){
                                                                                        if(err){
                                                                                            slave_connection.release();
                                                                                            generator.cleardb(connection,err,res,res_code.dberr, res_code.emptydata,res_code.msg_fail);
                                                                                            return;
                                                                                        }
                                                                                        slave_connection.release();
                                                                                        generator.cleardb(connection,err,res,res_code.success,stamp[0],res_code.msg_success);

                                                                                    });
                                                                                });
                                                                            });
                                                                        });
                                                                    });
                                                                });

                                                            });
                                                        });
                                                    }else{
                                                        unexpected_result = {TOWN_CODE : -2};
                                                        generator.cleardb(connection,err,res,res_code.success, unexpected_result,res_code.msg_success);
                                                    }
                                                }
                                            });
                                        }
                                    }
                                });
                            });
                        }else{
                            //valid accesstoken
                            generator.normal(res, res_code.notenough_data, res_code.msg_empty, res_code.msg_invalidaccesstoken);
                        }

                    }
                }
            })
        }else{
            generator.normal(res,res_code.notenough_data,stamp_validator)
        }
    });
```
위와 같은 코드를 실제로 작성했었다.

저정도까지 가려면 사실 설계 & 리팩토링을 안해야한다.(본인이 짰었음-_-)

혹시라도 수정하라고 하는 일이 없길 빌어야한다.

하늘에게 기도하며 돌아가길 바라거나 수많은 로그를 확인해야할 것이다.

어쨋든 저러한 코드를 아래와 같이 변경할 수 있다.(같은 코드는 아니다.)

##### Promise 이용
```javascript
module.exports = (req,res,next)=>{
    const User = require('../../../../model/User');
    const bcrypt = require('bcrypt-nodejs');
    const Article = require('../../../../model/Article');
    const AsyncArticleItemSavePromise = require('../util/ArticleItemSavePromise');
    const photos = req.files['photos'];
    const kml = req.files['kml'];
    const AccessToken = req.headers['x-access-token'];
    const {articleItems,Nick,App,AppId,Contents,Publish_range} = req.body;

    const tokenValidate = (user)=>{
        return new Promise((resolve,reject)=>{
            if(user){
                bcrypt.compare(user.DecryptValue,AccessToken,function (err) {
                    if(err){
                        const error = new Error('AccessToken Invalid');
                        error.status = 401;
                        reject(error);
                    }else{
                        resolve(user);
                    }
                });
            }else{
                const error = new Error('User Not Found');
                error.status = 404;
                reject(error);
            }

        });
    };
    const createArticleSaveTask = (user)=>{
        let Task =[];
        articleItems.forEach((item)=>{
            Task.push(new AsyncArticleItemSavePromise(item,user));
        });
        let object = {
            Task:Task,
            user:user
        }
        return object;
    };
    const articleSaveTaskExcute = (object)=>{
        Promise.all(object.Task).then((article_items)=>{
            object.article_items = article_items;

            return new Promise((resolve,reject)=>{
                let pathArray =[];
                let kmlpath = '';
                if(photos){
                    for(let index = 0; index<photos.length; index++){
                        pathArray.push(photos[index].path);
                    }
                }
                if(kml){
                    kmlpath = kml.path;
                }
                const article = new Article({
                    Kml_Uri:kmlpath,
                    Contents:Contents,
                    Images:pathArray,
                    Publish_range:Publish_range,
                    Article_List:object.article_items,
                    PostedBy:object.user._id
                });
                article.save().then((savedArticle)=>{
                    res.json(savedArticle);
                    resolve();
                }).catch(()=>{
                    const error = new Error('Article Save Fail');
                    error.status = 500;
                    reject(error);
                })
            });
        }).catch((errors)=>{
            return new Promise((resolve,reject)=>{
                const error = new Error(errors);
                error.status = 500;
                reject(error);
            });
        })
    }
    const onError = (error)=>{
        next(error,req,res,next);
    };

    User.findOne({Nick:Nick,App:App,AppId:AppId})
        .populate({path:'Friends',select:'_id Nick App'})
        .exec()
        .then(tokenValidate)
        .then(createArticleSaveTask)
        .then(articleSaveTaskExcute)
        .catch(onError);
};
```
위의 코드에서 몇 부분만 보면된다.

```javascript
User.findOne({Nick:Nick,App:App,AppId:AppId})
        .populate({path:'Friends',select:'_id Nick App'})
        .exec()
        .then(tokenValidate)
        .then(createArticleSaveTask)
        .then(articleSaveTaskExcute)
        .catch(onError);
```
이게 실행의 순서이다. 물론 각 콜백안에 Promise 가 들어가있는 것들이 있지만 큰 흐름은 저렇다.

유저를 찾고, 토큰을 검증하고 ,아티클 저장 작업을 생성하고, 아티클 저장 작업을 실행한다.

코드의 indent 가 정말 앞의 콜백헬 코드에 비해 많이 줄었다.

3~4 depth 정도는 애교로 봐줄 수 있다.


