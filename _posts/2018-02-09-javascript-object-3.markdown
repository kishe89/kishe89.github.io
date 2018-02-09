---
layout: post
title:  "Javascript Object-3"
date:   2018-02-09 17:42:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Javascript
---

```
자바스크립트 패턴과 테스트
길벗출판사,(지은이) 래리 스펜서, 세스 리처즈 ,(옮긴이) 이일웅
```
참고

### new 를 이용한 객체의 생성
---
```javascript
function human(name, sex) {
    this.name = name;
    this.sex = sex;
};

let jiwoon = new human('김지운', true);
let taehwan = new human('김태환',false);

function student(name, sex) {

    if(!(this instanceof student)){
        throw new Error('이 객체는 new를 사용하여 생성해야 합니다.');
    }
    this.name = name;
    this.sex = sex;
};

human.prototype.isMale = function () {
    return true === this.sex;
};

console.log(jiwoon.name);
console.log('human is male? : '+jiwoon.isMale());

console.log(taehwan.name);
console.log('human is male? : '+taehwan.isMale());

```
앞에서도 이야기 했듯이 new 는 내부적으로 빈객체를 생성하고 생성된 객체에 bind 된 this 를 만들기에
new 로 호출한 this 는 객체의 컨텍스트가 된다.


##### new 생성객체의 SOLID/DRY 요약표

|원칙|결과|
|---|---|
|단일 책임|생성한 객체가 한 가지 일에만 전념토록 해야 한다. 생성자 함수에 의존성을 주입할 수 있다는 점에서 도움이 될 것이다.|
|개방/폐쇄|다음 절에서 상속을 다룰 때 new 로 생성한 객체를 어떻게 확장할 수 있는지 알게 될 것이다.|
|리스코프 치환|상속을 잘 이용하면 가능하다.|
|인터페이스 분리|상속과 다른 코드 공유 패턴을 이용하면 가능하다.|
|의존성 역전|의존성은 어렵지 않게 생성자 함수에 주입할 수 있다.|
|DRY((반복하지 마라)|new 객체 생성 패턴을 쓰면 아주 DRY한 코드가 된다.|

javascript 의 scope 는 선언할 때 생성이된다(lexical scope).
리터럴로 선언하던 뭐로 선언을 하던 선언을 해야 자기자신의 스코프가 생성된다.

지금 human 의 경우 선언이 되었기에 자신의 내부에서 선언되는것은 human 의 스코프내에서 동작하게된다.
그에 반해 this 는 우리가 선언하지 않았다. global 객체에 바인드된 this 인것이다.

아래에 예를 들어본다.

##### scope example
```javascript
function animal(name, sex) {
    let object = {
        name: name,
        sex: sex,
        isMale:function () {
            return this.sex === true;
        }
    }
    return object;
}
let ani = animal('고양이',true);
console.log('animal is a male? :'+ani.isMale());
```
animal function 안에서 선언한 object 는
```javascript
{
   name: name,
   sex: sex,
   isMale:function () {
      return this.sex === true;
   }
}
```
위 객체 영역내에서 scope 를 가지게 된다. 선언이 되었기 때문이다.

new 는 {} 를 생성해준다는 이야기다.

객체를 생성하게되면 prototype 을 받게되는데 human 과 animal 의 차이를 생각해본다.

두개의 차이를 보면 human 은 필요한 메서드를 prototype 에 구현하고 있고 animal 은 객체내의 속성으로 구현하고있다.

prototype 에 정의된 내용은 객체 전체를 통틀어 하나만이 존재하게 된다. 이를 해당 prototype 을 상속받는 모든 객체가 공유하는 형태이다.

animal 은 객체를 생성시마다 함수또한 생성하고 있다.

##### 객체마다 함수 사본 존재
```javascript
function animal(name, sex) {
    let object = {
        name: name,
        sex: sex,
        isMale:function () {
            return this.sex === true;
        }
    }
    return object;
}
let ani = animal('고양이',true);
let cow = animal('소',false);
console.log(ani.name+' is a male? :'+ani.isMale());
console.log(cow.name+' is a male? :'+cow.isMale());
cow.isMale = function () {
    return this.sex === false;
};
console.log(ani.name+' is a male? :'+ani.isMale());
console.log(cow.name+' is a male? :'+cow.isMale());
```
각자의 함수를 가지고 있는지 확인하기 위해 위 코드를 보도록 한다.

cow 의 isMale 에 이전의 male 확인 조건의 반대 조건에 대해 비교후 리턴하도록 수정한 함수를 전달했다.

변경 이전에는 ani.isMale() 은 true, cow.isMale() 은 false 를 반환하였다.

변경 후는 ani.isMale() 은 이전과 같이 true 를, cow.isMale() 또한 true 를 반환할 것이다.

물론 각자에 대해 변경이 가능하다는 점에서 유용하게 보일 수 있지만 만약 각자에 대해 변경이 가능해야한다면 의존성 주입을 통해 해결하는 것이 좋을것이다.

prototype 을 이용하면 이런 문제들이 해결 된다.

prototype 을 이용한 상속을 위해서는 어떻게 해야하는지 보겠다.

##### prototype 이용한 상속흉내
```javascript
function human(name, sex) {
    this.name = name;
    this.sex = sex;
};
human.prototype.isMale = function () {
    return true === this.sex;
};
function student(name, sex) {

    if(!(this instanceof student)){
        throw new Error('이 객체는 new를 사용하여 생성해야 합니다.');
    }
    this.name = name;
    this.sex = sex;
};
student.prototype = new human();
student.prototype.hop = function () {
    return this.name + " 가 껑충 뛰었어요 !";
};

let jinyoung = new student('이진영',true);

console.log(jinyoung.hop());
```
보면 선언한 human 을 생성하는 new human 을 student 의 prototype 으로 삼았다.
동작은 정상적으로 된다.

prototype 지정시에 어떤 인자가 전달될지 모르므로 human 각 속성에 할당하는 코드가 존재하고 student 에서도 동일한 코드가 반복된다.

또한 human 은 인자를 전달하지 않았으므로 undefind 인 name, sex 를 가지고 다닌 꼴이 된다.

이 문제를 해결하기 위한 방법으로는 생성로직을 바로 사용하는 방법이 있다.

### 함수형 상속
```javascript
function Police(name,sex){
    if(!(this instanceof Police)){
        throw new Error('이 객체는 new를 사용하여 생성해야 합니다.');
    }
    let object = new human(name,sex);
    object.hop = function () {
        return this.name + " 가 껑충 뛰었어요 !";
    }
    return object;
};

let policeJiwoon = new Police('김지운',true);
let policelee = new Police('이창현',true);
console.log(policeJiwoon.hop());
console.log(policelee.hop());
policelee.hop = function () {
    return this.name + " 가 껑충 날랐어요 !";
};
console.log(policeJiwoon.hop());
console.log(policelee.hop());
```
위 처럼 생성자를 바로 이용하고 이로 생성된 객체를 확장하는 형태로 생성을 하게되면 생성자 값세팅을 반복하는 코드는 필요 없고 불필요한 속성도 가지지 않는다.

하지만 객체별 함수 사본을 가지는 문제가 생긴는데 이러한 부분을 최소한으로 줄일 수 있도록 설계를 잘 해야한다.

##### 함수형 상속 패턴의 SOLID/DRY 요약표

|원칙|결과|
|---|---|
|단일 책임 원칙|함수형 상속은 모듈 패턴을 사용하므로 의존성 주입과 애스팩트 장식에 친화적이다. 상속한 모듈에는 반드시 한가지 책임만 부여해야한다.|
|개방/폐쇄|함수형 상속은 모듈 확장에 관한 한 완벽한 메커니즘이다. 모듈을 수정하지 않고 확장이 가능하다.|
|리스코프 치환|함수형 상속은 수정 없이 모듈을 확장할 수 있게 해주므로 상속받은 모듈은 자신이 상속한 모듈로 대체될 수 있다. 하지만 계약 위반(상속이야 다되지만 실 사용하지 않는 부분이 많이 상속된다면 설계 변경 필요)이 일어나는지 확인해야한다.|
|인터페이스 분리|응집된 모듈 API 자체가 분리된 인터페이스이다.|
|의존성 역전|임의 모듈 생성 방식으로 만든 모듈을 상속에 사용했다면 의존성은 쉽게 주입할 수 있다.|
|DRY|설계만 잘한다면 모듈을 이용한 함수형 상속은 DRY 한 코드로 향하는 이상적인 지름길이다.|

### 멍키 패칭(Monkey-pathcing)
---
```javascript
'use strict';

let MyApp = {};
MyApp.Hand = function () {
    this.dataAboutHand = {};
};
MyApp.Hand.prototype.arrangeAndMove =  function(sign) {
    this.dataAboutHand = sign;
};

MyApp.Human = function (handFactory) {
    this.hands = [handFactory(), handFactory()];
};
MyApp.Human.prototype.useSignLanguage = function(message){
    let sign = {};
    this.hands.forEach((hand)=>{
        hand.arrangeAndMove(sign)
    });
    return '손을 움직여 수화하고 있어. 무슨 말인지 알겠니?';
};

MyApp.Gorilla = function (handFactory) {
    this.hands = [handFactory(), handFactory()];
};
MyApp.TechSignLanguageToKoKoko = function () {
    let handFactory = ()=>{
        return new MyApp.Hand();
    };

    let trainer = new MyApp.Human(handFactory);
    let koko = new MyApp.Gorilla(handFactory);

    koko.useSignLanguage = trainer.useSignLanguage;

    console.log(koko.useSignLanguage('안녕하세요!'));
}();

MyApp.TechSignLanguageToKoKoko;
```

MyApp.Gorilla 는 useSignLanguage 를 가지고 있지 않다.
```javascript
koko.useSignLanguage = trainer.useSignLanguage;
```
위에서 멍키 패칭이 일어나서 고릴라에게 휴먼의 useSignLanguage 를 전달한다.

위 코드에서 위험성이 존재하는 곳이 있는데 고릴라가 hands 를 가지고 있기 때문에 이는 사용가능하다.
해당 속성을 가지고 있는지 체크하는 코드가 필요하다.

이러한 멍키패칭을 통해서 다른 객체에 정의된 기능들을 빌려 사용할 수 있다.

다음 포스팅에서는 Javascript 의 콜백 패턴에 대해 알아본다.
