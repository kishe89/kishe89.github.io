---
layout: post
title:  "Javascript test framework usage"
date:   2018-01-30 18:58:00
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

Dependency Injection 은 의존성을 가지는 코드를 분리해낼때 좋은 기법이다.
이를 가능하게 하기 위해서는 SOLID 를 최대한 만족시켜야한다.

지금 만드는 의존성 주입 컨테이너에서 바로 주입된 의존성들을 이용하지 않아서 느껴지지 않을 수 있지만
리스코프 치환원칙을 지키지 않는 의존성 코드를 주입받았다고 생각해보자.

그 코드는 사용하기 어려울 것이다. 사용하더라도 특정 상황에서 에러를 발생시킬 가능성이 생긴다.
계약을 지키지 못하고 상속거부가 일어난 코드들은 사용시 필요한 기능에 따라 파편화 되는데 이를 전부 처리해주지 못하면 코드단계에서 오류가 발생하게 된다.

단일책임원칙을 지키지 못한 코드는 불필요한 코드조각들을 들고 다니면서 코드의 복잡도를 올릴것이다.

계방폐쇠원칙을 지키지 못한 코드는 기능의 확장 및 추가를 위해서 이전 코드를 수정하여 의존성을 가지는 다른 코드들에게 안좋은 영향을 미칠 수 있고
의존관계 역전 원칙을 지키지 못하는 코드는 코드상에 모든 기능에대한 구현이 들어가서 위 개방폐쇠원칙을 지키기 힘들 것이다.

[SOLID]가 모든걸 해결해주지 못하고 또한 상황에 따라 저 원칙들및 법칙을 모두 지키는 코드가 오히려 불필요한 작업을 발생시킬 수 있다.
TDD 는 개발자에게 기계적으로 [SOLID]를 지키기 쉽게 코드를 작성할 수 있게 해준다. 시작을 하게되면 일단 반은 성공이므로 처음부터 너무 추상화에 열심히일 필요는 없다.

위의 코드의 실행을하게 되면 아래와 같은 화면을 볼 수 있다.

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


[Jasmine-travis]:https://github.com/jasmine/jasmine/blob/master/.travis.yml
[SOLID]:https://ko.wikipedia.org/wiki/SOLID
[Jasmine]:https://jasmine.github.io/index.html
[Jasmine-Matchers]:https://jasmine.github.io/api/2.6/matchers.html
