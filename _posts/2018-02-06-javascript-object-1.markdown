---
layout: post
title:  "Javascript Object-1"
date:   2018-02-05 19:24:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Javascript
---

```
자바스크립트 패턴과 테스트
길벗출판사,(지은이) 래리 스펜서, 세스 리처즈 ,(옮긴이) 이일웅
```
참고

##### Javascript 에서 원시형과 객체
---

Javascript 에서 원시형은 문자열, 숫자, 불, null, undefined, Symbol(ES 6) 만 존재한다.

문자열, 숫자, 불은 각각 Wrapper 를 가지고 있다.
원시형의 상수값을 사용할 때는 어지간하면 변수에 값을 넣어서 참조형식으로 사용하는 것이 좋다.
그리고 그냥 변수로 사용하는것보다는 필요한 변수들을 묶어서 객체로 만들고 prototype 재정의를 통해서 묶어서 사용하는 것이 좋다.
일단 prototype 은 객체 생성시마다 새로 생성되지 않는다.

객체는 객체 리터럴(Object literal)로 선언, new, 생성자 가 있다.
##### 객체 생성
```javascript
let animal = {type:'dog',age:3,sex:'male',name:'puppy'};
let Animal = function (name) {
    return {type:'dog',age:3,sex:'male',name:name};
};
let AnimalObject = function (name) {
    this.type = 'dog';
    this.age = 3;
    this.sex = 'male';
    this.name = name;
};
let add = function (a,b) {
    this.result = a+b;
}
let myDog = Animal('puppy');
let myDogBaby = new AnimalObject('puppy_junior');
let returned = add(1,2);
console.log(myDog);
console.log(myDogBaby);
console.log(global.result);
console.log(returned.result);
```
javascript 에서 function 의 this 는 global 객체를 가르킨다.
new 키워드를 사용하거나 리터럴로 반환하거나 혹은 함수내에서 새로운 객체를 생성하여 반환을 해야 정상적으로 우리가바라는 생성자의 역할을 할 수 있다.
Arrow Function 을 생성자로 사용할 수 없는 이유가 바로 여기에 있다. Arrow Function 은 자기자신의 this 를 바인드 하지 않는다.
어쨋든 위 animal,Animal,AnimalObject 는 생성자로서 역할을 한다.

그런데 밑에 add 라는 것은 어떻게 될것인가 add 를 호출할 때 new 로 호출하지 않았다.
그렇기에 this 는 global 객체이고 global 객체에 result 프로퍼티를 생성하고 3이 할당될것이다.
returned 는 undefined 로 나오고 returned.result 는 당연히 에러를 뱉을것이다.

이 이야기는 AnimalObject 또한 new 를 빼먹고 호출시 동일한 문제를 발생시킬 수 있다는 것이다.
그리고 로그를 보면 알겠지만 오브젝트 리터럴을 선언하거나 반환한 것과 new 를 이용한 나머지 객체에는 차이가 있다.
![Alt text](/assets/javascript_tdd_image/javascript-object-1/index1.png)

위 로그를 보면 알겠지만 new AnimalObject 를 통해 생성한것은 객체의 내용앞에 AnimalObject 라고 이름이 나온다.
그에 비해 객체 리터럴을 이용한 곳에는 이름이 없다.

간단한 자료와 많은 기능이 필요치 않다면 원시형을 사용해도 괜찮다. 하지만 값의 유효성 체크등 생성시 어떠한 처리를 해야할 경우 단순 객체리터럴 생성(animal)은
불가능 하지만 Animal 과같이 함수에서 리턴하는 형태로 처리하면 생성시의 처리가 가능해진다.

new 는 내부적으로 생성자.prototype 을 상속하는 객체를 생성하고 생성된 객체는 자기자신에게 bind 된 this 를 지닌다. 그리고 new 로 호출한 함수는 기본적으로 return 을 명시하지 않을시 앞에서 만든 this 를 반환한다.
add 함수가 우리가 원하는대로 new 를 붙이지 않더라도 정상적으로 본인의 result 를 가지려면 크게 두가지 방법이 있다.
##### new 를 호출안하고 생성방법
```javascript
let add = function (a,b) {
    let that = {};
    that.result = a+b;
    return that;
}

let add = function (a,b) {
    if(!(this instanceof add)){
        return new add(a,b);
    }
    this.result = a+b;
}
```
첫번째 방법은 함수내에서 객체 리터럴로 새로운 객체를 생성해 리턴하는 방법과 instanceof 를 이용해 객체인지 분별해서
객체가 아닐시 new 로 자기자신을 생성하도록 하는 방법이 있다.
두번째 방법은 앞에서도 사용했었던 방법이고 첫번째 방법은 어찌보면 꼼수에 가까운 방법이다. new 가 없을때 이용하던 방법이다.(ES1 에서 추가)

어쨋든 우리는 TDD 를 위해서 모든 함수, 객체는 테스트 가능해야한다.
그렇기에 단순 객체 리터럴 생성보다는 제어가능한 객체로 생성하는 방법들을 자주 사용할 것이다.

**원시형의 SOLID/DRY 요약표**

|원칙|결과|
|---|---|
|단일 책임|원시형은 단일책임의 원칙을 가장 잘 지킨다.|
|개방/폐쇠|확장에 개방적이지 못하는 점에서 위배하지만 변경에 폐쇄적인것으론 최고다. 원시형은 불변값(Immutable)이다.|
|리스코프 치환|해당 없다.|
|인터페이스 분리|인터페이스 구현이 불가능하다.|
|의존성 역전|의존성은 없다.|
|DRY(Don't Repeat Yourself)|WET(Write Everything Twice) 하다.|

**객체 리터럴의 SOLID/DRY 요약표**

|원칙|결과|
|---|---|
|단일 책임|단순 객체 리터럴은 아주 작은 편이라 이 항목을 위배하는 일은 없다. 모듈 API 를 구성하는 덩치가 큰 객체 리터럴은 자신의 모듈이 담당한 모든 책임을 진다.|
|개방/폐쇠|객체 리터럴 특성상 제멋대로 확장 될 수 있다.|
|리스코프 치환|상속을 구현하지 않는 이상 해당 없다.|
|인터페이스 분리|모듈 패턴 및 멍키 패칭을 참고|
|의존성 역전|단순 객체 리터럴은 내부에 의존성을 주입할 생성자가 없으니 의존성 역전은 불가능하다.|
|DRY(Don't Repeat Yourself)|싱글톤이 아닌 객체 리터럴은 WET(Write Everything Twice) 한 코드가 되기 일쑤다.|

