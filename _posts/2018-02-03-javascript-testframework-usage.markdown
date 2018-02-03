---
layout: post
title:  "Javascript test framework usage"
date:   2018-02-03 14:28:00
author: 김지운
cover:  "/assets/instacode.png"
---

node 에서 기본적으로 모듈은 보통 require 를 통해서 load 하게되는데
이 모듈은 module.exports 혹은 export 한 모듈들이다.
node 에서의 기본적인 모듈 로드 스타일은 CommonJs 를 따르는데 이외에도 ES 의 import, RequiresJS 의 require 를 이용하던가
하는데 이는 또한 혼용이 가능하다. 거기에 ES 와 기존 javascript API 들의 혼용에도 코드는 동작한다. 또한 서버사이드에서의 스코프와 브라우저에서의 스코프는 차이를 가진다.물론 호환성을 생각하면 좋은 이야기지만
너무 다양한 스타일이 혼재하여 머리아픈 상황이 발생할 수 있다.

자바스크립트는 정말 적은 코드로 많은 일을 할 수 있는 멋진 언어이다.
하지만 아직 표준화에 대한 부분은 멀고도 험한것같다. IE의 퇴출에 얼마나 걸릴지 모르는것처럼...

일단 사설이 길었는데 이런 이야기를 한 것은 공부를 위해서는 한가지 스타일로 통일해서 하는 것이 좋기 때문이다.
앞으로의 내용은
```
자바스크립트 패턴과 테스트
길벗출판사,(지은이) 래리 스펜서, 세스 리처즈 ,(옮긴이) 이일웅
```

책을 본인도 공부하면서 적어 나갈 것이다.
물론 책내용에도 나와있지만 **[SOLID]에 대한 내용은 로버트 마틴의 클린 코드(아마 절판이었던듯)와 마틴파울러의 클린 소프트웨어등의 서적등을
통해 읽어보면 좋을 것이다. Object Oriented Design 의 교과서적인 키워드이다.**

### Jasmine 사용법
---
앞에서 Jasmine 에서 웹페이지를 통해 test 결과등에 대해 보고 실행할 수 있다고 했다.
이를 위해서는 html 에서 필요한 script 와 css 파일을 로드해야한다. 로드하는 내용은 아래와 같다.
그리고 Jasmine 을 실행할 수 있는 브라우저 환경은 Safari, Chrome, Firefox, PhantomJS, and new Internet Explorer 등이며
자세한 버전은 [Jasmine-travis]에 나와있다.
```html
<link rel="shortcut icon" type="image/png" href="jasmine/lib/jasmine-{#.#.#}/jasmine_favicon.png">
<link rel="stylesheet" type="text/css" href="jasmine/lib/jasmine-{#.#.#}/jasmine.css">

<script type="text/javascript" src="jasmine/lib/jasmine-{#.#.#}/jasmine.js"></script>
<script type="text/javascript" src="jasmine/lib/jasmine-{#.#.#}/jasmine-html.js"></script>
<script type="text/javascript" src="jasmine/lib/jasmine-{#.#.#}/boot.js"></script>
```
스크립트들을 로드하고 아래처럼 내가 테스트할 스크립트 코드들 또한 로드해준다.

```html
<!DOCTYPE html>
<html>

  <head>
    <meta charset="UTF-8">
    <link data-require="jasmine@2.0.0" data-semver="2.0.0" rel="stylesheet" href="http://cdn.jsdelivr.net/jasmine/2.0.0/jasmine.css" />
    <script data-require="jasmine@2.0.0" data-semver="2.0.0" src="http://cdn.jsdelivr.net/jasmine/2.0.0/jasmine.js"></script>
    <script data-require="jasmine@2.0.0" data-semver="2.0.0" src="http://cdn.jsdelivr.net/jasmine/2.0.0/jasmine-html.js"></script>
    <script data-require="jasmine@2.0.0" data-semver="2.0.0" src="http://cdn.jsdelivr.net/jasmine/2.0.0/boot.js"></script>

    <script src="DiContainer_00.js"></script>
    <script src="DiContainer_01_tests.js"></script>
  </head>

  <body>
    <h1>즐거운 TDD Dependency Injection Test</h1>
  </body>

</html>
```
이번에 테스트할 코드는 DiContainer로 수정해나가는 코드에 대해서는 DiContainerXX로 변경해나간다.

그리고 각각의 테스트 페이지는 index_xx.html 로 작성해나간다.

처음으로 작업할 코드는 Dependency Injection 을 수행하는 DiContainer 이다.
javascript 에서 함수는 일급시민, 일급객체등으로 불리는 최상위 Object 이다. 객체의 모델링은 prototype 을 재정의하여 작성한다.

##### DiContainer00
```javscript
DiContainer = function () {

};

DiContainer.prototype.register = function (name, dependencies, func) {

};
```
DiContainer 라는 객체를 정의하고 DiContainer 의 원형에 register 라는 name, dependencies, func 를
파라미터로 받는 함수를 정의해줬다. 일단 생성이 정상적으로 되는지 테스트를 위해서 상세구현은 하지 않고 테스트해본다.

##### DiContainer_01_tests
```javascript
describe("DiContainer",() => {

    let container;
    beforeEach(()=>{
        container =new DiContainer();
    });
    describe('register(name, dependencies, func)',()=>{
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
앞에서 describe 는 테스트 꾸러미라고 이야기 했다. DiContainer 테스트 꾸러미이기에
describe("DiContainer",func) 로 func 에 DiContainer 테스트 꾸러미의 테스트 케이스를 작성하였다.
헌데 우리가 테스트 해야할 테스트는 DiContainer 의 모든걸 테스트 해야하는데 객체의 함수는 여러가지가 있을 수 있다.
해서 테스트 꾸러미 안에는 다시 테스트 꾸러미를 작성할 수 있다.
TDD 의 원칙을 생각하면 모든 테스트를 작은 조각으로 작성한후 통합하는 과정이 있어야하는데
이 과정을 아주 세부적인 부분까지 하면 처음부터 테스트가 하기 싫어질 수 있다.
그럴땐 어느정도 묶어서 작성하는 것도 좋은 방법이다.(시작을 안할정도로 힘들다면 그래도 시작할 수 있게 적절히 타협도 필요하다)

해서 DiContainer 테스트 꾸러미 안에서는 DiContainer 에서 재정의할 함수들을 테스트 해나갈것이다.
각각의 함수들은 다시 테스트꾸러미를 가지는 구조이다.

##### index_01.html 실행화면
![Alt text](/assets/javascript_tdd_image/ex1/index1.png)

register 에서 아무런 동작도 하지 않기에 toThrow 에서 기대하는 익셉션 발생은 없을 것이다.

이제 register 에서 Error 를 throw 하게 변경해본다.
##### DiContainer_01
```javascript
DiContainer = function () {
    if(!(this instanceof DiContainer)){
        return new DiContainer();
    }
};

DiContainer.prototype.register = function (name, dependencies, func) {
    let ix;

    if(typeof name !== 'string'
    || !Array.isArray(dependencies)
    || typeof func !== 'function'){
        throw new Error(this.messages.registerRequiresArgs);
    }
    for(ix = 0 ; ix<dependencies.length; ix++){
        if(typeof dependencies[ix] !== 'string'){
            throw new Error(this.messages.registerRequiresArgs);
        }
    }
};
DiContainer.prototype.messages = {
    registerRequiresArgs: '이 생성자 함수는 인자가 3개 있어야 합니다 : '+'문자열, 문자열 배열, 함수'
};
```

DiContainer 의 생성을 생성자를 통해서 하도록 강제하고
register 에서는 전달받은 name 의 타입이 string 이 아닌지 확인하고
dependencies 는 Array 인지 그리고 func 는 function 인지 확인하여 아닐경우 에러를 발생시킨다.
에러의 메시지는 DiContainer.prototype.messages 에 정의한다.

이렇게 변경한 후 실행하게 되면 앞에 테스트케이스의 badArgs 의 잘못된 파라미터들의 전달마다 Error 를 thorw 하여 테스트는 성공하게 된다.
##### index_02.html 실행화면
![Alt text](/assets/javascript_tdd_image/ex1/index2.png)

그리고 좀 더 견고한 테스트를 작성하려면 메시지를 외부로 드러내는 것이 좋다.
그래서 DiContainer_01_tests.js 를 작성해본다.
##### DiContainer_01_tests.js
```javascript
describe("DiContainer",() => {

    let container;

    beforeEach(()=>{
        container =new DiContainer();
    });
    describe('register(name, dependencies, func)',()=>{
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
                }).toThrowError(container.messages.registerRequiresArgs);
            })
        });
    });
});
```
toThrowError 는 Error 가 throw 되면 호출 될 콜백이며 이에 인자로 메시지를 전달해준다.
테스트 외부에서도 메시지를 확인할 수 있으므로 보기 좀 더 명확한 테스트가 된다.
등록 부분의 negative test 는 어느정도 된것 같으니 이제 컨테이너에 의존성이 잘 들어갔는지 확인할 get 함수의 테스트를 작성해본다.
get 함수는 등록된 성명이 아닐경우 undefined 를 반환한다.
##### DiContainer_02.tests
```javascript
describe("DiContainer",() => {

    let container;

    beforeEach(()=>{
        container =new DiContainer();
    });
    describe('register(name, dependencies, func)',()=>{
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
                }).toThrowError(container.messages.registerRequiresArgs);
            })
        });
    });
    describe('get(name)',()=>{
        it('성명이 등록되어 있지 않으면 undefined 를 반환한다.',()=>{
            expect(container.get('noDefined')).toBeUndefined();
        });
    });
});
```
그리고 테스트를 돌려보자. 테스트는 실패할 것이다.
![Alt text](/assets/javascript_tdd_image/ex1/index3.png)
테스트가 정상적으로 실행은 될 수 있게 함수만 만들도록한다.
```javascript
DiContainer.prototype.get = function (name){
};
```
undefined 를 반환히지 않았는데 성공한다. 함수의 실행후 리턴이 없을시 리턴이 undefined 이기 때문이다.
일단 운좋게 성공한 테스트는 놔두고 get 함수의 목적에 맞는 코드를 작성해본다.

```javascript
DiContainer = function () {
    if(!(this instanceof DiContainer)){
        return new DiContainer();
    }
    this.registeredList = [];
};
DiContainer.prototype.messages = {
    registerRequiresArgs: '이 생성자 함수는 인자가 3개 있어야 합니다 : '+'문자열, 문자열 배열, 함수'
};

DiContainer.prototype.register = function (name, dependencies, func) {
    let ix;

    if(typeof name !== 'string'
    || !Array.isArray(dependencies)
    || typeof func !== 'function'){
        throw new Error(this.messages.registerRequiresArgs);
    }
    for(ix = 0 ; ix<dependencies.length; ++ix){
        if(typeof dependencies[ix] !== 'string'){
            throw new Error(this.messages.registerRequiresArgs);
        }
    }
    this.registeredList[name] = {func:func};
};
DiContainer.prototype.get = function (name){
    return this.registeredList[name].func();
};
```

DiContainer 에 registeredList 라는 array 필드를 작성하고 register 에서는 전달된 정상적인 파라미터를 해당 array 에 넣어준다.
그리고 get 함수에서는 전달받은 이름에 맞는 함수를 실행한 결과를 반환하도록 작성한다.
그리고 다시 테스트를 실행해보면 이전에 성공하던 undefined 를 기대하던 테스트는 실패하고 새로 작성한 테스트는 성공할 것이다.

![Alt text](/assets/javascript_tdd_image/ex1/index4.png)
return 되는 것은 함수의 실행결과인데 name 으로 검색한 결과가 undefined 일것인데 func 를 호출하니 없는 함수를 호출하는 결과가 된다.
이제 get 에서 처음 작성한 '성명이 등록되어 있지 않으면 undefined 를 반환한다.' 를 만족하도록 등록되지 않은경우에 대한 처리를한다.

```javascript
DiContainer.prototype.get = function (name){
    let registration = this.registeredList[name];

    if(registration === undefined){
        return undefined;
    }
    return registration.func();
};
```

이제 테스트를 다시 실행해보면 전부 성공하게 된다.
![Alt text](/assets/javascript_tdd_image/ex1/index5.png)

get 은 자신이 반환하는 객체에 의존성을 제공할 수 있다.
의존성을 등록하는 테스트를 작성해본다.

##### 의존성 등록 테스트
```javascript
describe("DiContainer",() => {

    let container;

    beforeEach(()=>{
        container =new DiContainer();
    });
    describe('register(name, dependencies, func)',()=>{
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
                }).toThrowError(container.messages.registerRequiresArgs);
            })
        });
    });
    describe('get(name)',()=>{
        it('성명이 등록되어 있지 않으면 undefined 를 반환한다.',()=>{
            expect(container.get('noDefined')).toBeUndefined();
        });
        it('등록된 함수를 실행한 결과를 반환한다.',()=>{
            const name = 'MyName';
            const returnFromRegisteredFunction = 'something';
            container.register(name,[],function(){
                return returnFromRegisteredFunction;
            });
            expect(container.get(name)).toBe(returnFromRegisteredFunction);
        });
        it('등록된 함수에 의존성을 제공한다.',()=>{
            const main = 'main';
            let mainFunc;
            const dep1 = 'dep1';
            const dep2 = 'dep2';

            container.register(main, [dep1, dep2], (dep1Func, dep2Func)=>{
                return ()=>{
                    return dep1Func()+dep2Func();
                }
            });
            container.register(dep1,[],()=>{
                return ()=>{
                    return 1;
                }
            });
            container.register(dep2,[],()=>{
                return ()=>{
                    return 2;
                }
            });
            mainFunc = container.get(main);
            expect(mainFunc()).toBe(3);
        })
    });
});
```
##### DiContainer
```javascript
DiContainer = function () {
    if(!(this instanceof DiContainer)){
        return new DiContainer();
    }
    this.registeredList = [];
};
DiContainer.prototype.messages = {
    registerRequiresArgs: '이 생성자 함수는 인자가 3개 있어야 합니다 : '+'문자열, 문자열 배열, 함수'
};

DiContainer.prototype.register = function (name, dependencies, func) {
    let ix;

    if(typeof name !== 'string'
    || !Array.isArray(dependencies)
    || typeof func !== 'function'){
        throw new Error(this.messages.registerRequiresArgs);
    }
    for(ix = 0 ; ix<dependencies.length; ++ix){
        if(typeof dependencies[ix] !== 'string'){
            throw new Error(this.messages.registerRequiresArgs);
        }
    }
    this.registeredList[name] = {dependencies:dependencies ,func:func};
};
DiContainer.prototype.get = function (name){
    let registration = this.registeredList[name];
    const self = this;
    let dependencies = [];

    if(registration === undefined){
        return undefined;
    }

    registration.dependencies.forEach((dependencyName)=>{
        const dependency = self.get(dependencyName);
        dependencies.push(dependency === undefined ? undefined : dependency);
    });
    return registration.func.apply(undefined,dependencies);
};
```

DiContainer 의 get 함수를 약간 수정하여서 등록된 dependencies 에 대해서 재귀적으로 추가하도록 변경한다.
context 를 전달하기위해 self 를 만들어줬다.
그리고 self.get(xx)를 통해 dependency 를 dependencies(실행할 arguments)로 만들어주고 apply 를 통해서 함수호출을 하였다.
apply(context, arguments)로 context 위치에는 실행할 객체가 들어가게 된다.
apply 는 함수를 다른객체에서 사용할 때 사용하는데 undefined 를 주게되면 global 객체가 주체가된다.

테스트를 실행해보면 정상적으로 동작되는 것을 볼 수 있다.
![Alt text](/assets/javascript_tdd_image/ex1/index6.png)

이제 의존성 주입 컨테이너가 완성되었으니 실제 활용 테스트를 해본다.

##### Attendee
```javascript
/**
 * poor man's dependency injection 을 이용한 constructor
 * @param service
 * @param messenger
 * @param attendeeId
 * @return {Attendee}
 * @constructor
 */

Attendee = function (service, messenger, attendeeId) {
    if(!(this instanceof Attendee)){
        return new Attendee(attendeeId);
    }
    this.attendeeId = attendeeId;
    this.service = service;
    this.messenger = messenger;
};

Attendee.prototype.reserve = function (sessionId) {
    if(this.service.reserve(this.attendeeId, sessionId)){
        this.messenger.success('좌석 예약이 완료되었습니다!'+
            ' 고객님은 ' + this.service.getRemainingReservations()+
            ' 좌석을 추가 예약하실 수 있습니다.');
    }else{
        this.messenger.failure('죄송합니다. 해당 좌석은 예약하실 수 없습니다.');
    }
};
```
##### Messenger
```javascript
Messenger = function () {
    if(!(this instanceof Messenger)){
        return new Messenger();
    }
};
Messenger.prototype.success = function (message) {
    alert(message);
};
Messenger.prototype.failure = function (message) {
    alert(message);
}
```
##### ConferenceWebSvc
```javascript
ConferenceWebSvc = function () {
    if(!(this instanceof ConferenceWebSvc)){
        return new ConferenceWebSvc();
    }
    this.limit = 10;
    this.reservationList = [];
};
ConferenceWebSvc.prototype.reserve = function (attendeeId, sessionId) {
    if(this.reservationList.length === 10){
        return false;
    }
    this.reservationList.push({attendeeId:attendeeId,sessionId:sessionId});
    return true;
}
ConferenceWebSvc.prototype.getRemainingReservations = function () {
    return this.limit - this.reservationList.length;
}
```
##### DiContainer_tests
```javascript
describe("MyApp",()=>{
    let MyApp;
    beforeEach(()=>{
        MyApp = {};
        MyApp.diContainer = new DiContainer();
    });
    describe("MyApp-DiContainer",()=>{
        it('Attendee 생성 주입',()=>{
            const attendeeId = 123;
            const sessionId = 1;

            MyApp.diContainer.register('Service',[],()=>{
                return new ConferenceWebSvc();
            })
            MyApp.diContainer.register('Messenger',[],()=>{
                return new Messenger();
            });
            MyApp.diContainer.register('AttendeeFactory',['Service','Messenger'],(service, messenger)=>{
                return (attendeeId)=>{
                    return new Attendee(service, messenger, attendeeId);
                };
            });
            const attendee = MyApp.diContainer.get('AttendeeFactory')(attendeeId);
            attendee.reserve(sessionId);
        });
    });
    describe("DiContainer",() => {

        let container;
        beforeEach(()=>{
            container =new DiContainer();
        });
        describe('register(name, dependencies, func)',()=>{
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
                    }).toThrowError(container.messages.registerRequiresArgs);
                })
            });
        });
        describe('get(name)',()=>{
            it('성명이 등록되어 있지 않으면 undefined 를 반환한다.',()=>{
                expect(container.get('noDefined')).toBeUndefined();
            });
            it('등록된 함수를 실행한 결과를 반환한다.',()=>{
                const name = 'MyName';
                const returnFromRegisteredFunction = 'something';
                container.register(name,[],function(){
                    return returnFromRegisteredFunction;
                });
                expect(container.get(name)).toBe(returnFromRegisteredFunction);
            });
            it('등록된 함수에 의존성을 제공한다.',()=>{
                const main = 'main';
                let mainFunc;
                const dep1 = 'dep1';
                const dep2 = 'dep2';

                container.register(main, [dep1, dep2], (dep1Func, dep2Func)=>{
                    return ()=>{
                        return dep1Func()+dep2Func();
                    }
                });
                container.register(dep1,[],()=>{
                    return ()=>{
                        return 1;
                    }
                });
                container.register(dep2,[],()=>{
                    return ()=>{
                        return 2;
                    }
                });
                mainFunc = container.get(main);
                expect(mainFunc()).toBe(3);
            })
        });
    });
});
```
Attendee 를 보면 이전 작성했던 코드이다. 이전에 Attendee 를 작성하고 테스트를 할 때 ConferenceWebSvc, Messenger 는 작성을 안했다.
사실 ConferenceWebSvc 와 Messenger 는 각각 통신 및 클라이언트에 의존적이다. Attendee 를 테스트 하기위해서 DB 를 붙이고 API 를 작성하는건
일을위한 일을 하는것이 될것이다.

여기서는 대략적으로 테스트가 가능할만한 ConferenceWebSvc, Messenger 만을 작성하여 테스트를 진행한다.
구체적인 구현은 없어도 상관없다. 단지 Attendee 에서 이용하는 Messenger 의 success, failure 함수와 ConferenceWebSvc 의 reserve, getRemainingReservations 함수만 작성을 해주면된다.
굳이 이름이 ConferenceWebSvc 와 Messenger 일 필요도 없다.

해서 DiContainer_tests 를 보면 좌석 예약에 필요한 객체의 생성자 들과 Attendee 의 Factory 함수를 앞에서 작성한 DiContainer 를 이용하여 의존성 주입을 테스트하는 것을 볼 수 있다.
각각 'Service' 는 ConferenceWebSvc 를 생성하는 생성자, 'Messenger' 는 Messenger 를 생성하는 생성자, 'AttendeeFactory' 는 Attendee 를 생성하는 생성자이다.
또한 'AttendeeFactory' 는 'Service', 'Messenger' 를 의존성으로 가지고 있다.
즉 AttendeeFactory 의 등록된 javascript object 의 형태를 보면
```javascript
{
    dependencies:['Service', 'Messenger'],
    func:(service, messenger)=>{
       return (attendeeId)=>{
          return new Attendee(service, messenger, attendeeId);
       };
    }
}
```
와 같은 형태가 되며
```javascript
MyApp.diContainer.get('AttendeeFactory')(attendeeId)
```
get 이 호출되면 dependencies 에 추가 되어있는 dependency 들을 조회하며 앞에서 등록했던 'Service', 'Messenger' 의 func 들을
get 의 로컬 변수인 dependencies array 에 재귀적으로 추가하게 되고 이렇게 추가된 dependency(각 dependency 의 func)들을 파라미터로 'AttendeeFactory'를 호출하게 되고
'AttendeeFactory'의 반환함수인
```javascript
return (attendeeId)=>{
    return new Attendee(service, messenger, attendeeId);
}
```
에 attendeeId를 전달하여 호출했다.

결과적으로 반환되는것은
```javascript
new Attendee(service, messenger, attendeeId);
```
생성된 Attendee 객체가 반환된다. 반환된 객체를 이용하여 예약을 호출하게되면
정상적으로 실행되는 모습을 볼 수 있다.
테스트 케이스를 보면 MyApp 으로 테스트 꾸러미를 다시 묶었으며 DiContainer 와 인접하게 MyApp-DiContainer 테스트 꾸러미를 만들었다.
물론 MyApp 테스트케이스를 따로 만드는게 좋겠지만 지키기 어려운 원칙을 지키려고 시작조차 안하는 것보다는 이렇게라도 하는게 좋다고 생각해서 위처럼 나눴다.
최종적으로 테스트 실행화면은 아래처럼 나올 것이다.
![Alt text](/assets/javascript_tdd_image/ex1/index7.png)




[Jasmine-travis]:https://github.com/jasmine/jasmine/blob/master/.travis.yml
[SOLID]:https://ko.wikipedia.org/wiki/SOLID
[Jasmine]:https://jasmine.github.io/index.html
[Jasmine-Matchers]:https://jasmine.github.io/api/2.6/matchers.html
