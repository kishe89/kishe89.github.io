---
layout: post
title:  "JavaScript Object-2"
date:   2018-02-08 17:01:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Javascript
---

```
자바스크립트 패턴과 테스트
길벗출판사,(지은이) 래리 스펜서, 세스 리처즈 ,(옮긴이) 이일웅
```
참고

### 모듈 패턴
---

모듈 패턴은 Javascript 에서 데이터를 감추고 이를 조작가능한 API 로 제공하는데 있어서 가장 많이 사용하는 패턴이다.

모듈 패턴은 두가지 유형으로 나뉜다.

- 즉시실행 함수를 이용한 모듈
- 임의로 함수를 호출하여 생성하는 모듈

##### 임의 모듈 생성 & 즉시 실행 모듈 생성
```javascript
'use strict';
let MyApp = {};

MyApp.wildlifePreserveSimulator = (animalMaker)=>{

    let animals = [];

    return {
        addAnimal:(speices, sex)=>{
            animals.push(animalMaker.make(speices, sex));
        },
        getAnimalCount:()=>{
            return animals.length;
        },
        getAnimal:(index)=>{
            return animals[index];
        }
    }
};

let realAnimalMaker = (function(){
    let that = {};
    that.make = (species, sex)=>{
        return {species, sex};
    };
    return that;
}());

let preserve = MyApp.wildlifePreserveSimulator(realAnimalMaker);

preserve.addAnimal('gorila','male');
preserve.addAnimal('human','female');
console.log(preserve.getAnimal(0));
console.log(preserve.getAnimalCount());
```

위에서 wildlifePreserveSimulator 는 임의 모듈 생성을 한것이고 realAnimalMaker 는 즉시 실행 모듈을 생성한 것이다.

임의 모듈 생성은 우리가 일반적으로 많이 봐온 패턴이다.

realAnimalMaker 를 보 함수의 선언 후 바로 ()로 함수를 호출하고 있다.

이렇게 함수를 생성할 때 바로 실행할 수 있는데 이는 함수의 선언이 표현식으로 변경했기 때문이다.

즉시 실행 함수로 선언된 이름공간을 가지는 전역 변수에 할당된 후 해당 모듈의 싱글톤 인스턴스가 된다.

모듈을 생성할 때는 다음 사항을 유념 해야한다.

1. 단일 책임 원칙을 잊지 말고 한 모듈에 한 가지 일만 시킨다. 그래야 결속력이 강하고 다루기 쉬운 아담한 API 를 작성하게 된다.
2. 모듈 자신이 쓸 객체가 필요하다면 의존성 주입 형태로 객체를 제공하는 방안을 고려하라.
3. 다른 객체 로직을 확장하는 모듈은 해당 로직의 의도가 바뀌지 않도록 분명히 밝힌다.(리스코프 치환 원칙)

##### 모듈의 SOLID/DRY

|원칙|책임|
|---|---|
|단일 책임 원칙|모듈은 태생 자체가 의존성 주입과 친화적이고 애스팩트 지향적이라 단일 책임 유지는 어렵지 않다.|
|개방/폐쇄|다른 모듈에 주입하는 형태로 얼마든지 확장할 수 있다. 통제해야 하는 모듈은 수정하지 못하게 차단할 수 있다.|
|리스코프 치환|의존성의 의미를 뒤바꾸는 일만 없으면 별문제 없다.|
|인터페이스 분리|결합된 API 모듈 자체가 자바스크립트에서 분리된 인터페이스나 다름없다.|
|의존성 역전|임의 모듈은 의존성으로 주입하기 쉽다. 모듈이 어떤 형태든 다른 모듈에 주입할 수 있다.|
|DRY|제대로만 쓴다면 DRY 한 코드를 유지하는 데 아주 좋은 방법이다.|

### 객체의 프로토타입과 프로토타입 상속
---

객체 리터럴은 Object.prototype 에 연결이 되게 된다.

앞에서 계속 선언했던 function 은 Function.prototype 에 연결이 되게 된다.

prototype 에는 유용한 함수들이 정의 되어있는데 아래 코드를 보도록 한다.

```javascript
'use strict';

let chimp = {
    hasThumbs:true,
    swing:()=>{
        return '나무 꼭대기에 대롱대롱 매달려 있네요';
    }
};
console.log(chimp.toString());
```
chimp 객체 리터럴은 hasThumbs 필드와 swing 이라는 메서드(객체내의 function)를 가지고 있다.

chimp 에는 toString 이라는 메서드를 정의한적이 없다. 그렇다면 로그에는 undefined 가 떠야할 것이다.
하지만 실행해보면 chimp 의 내부를 보여줄 것이다.

chimp 가 내부에 toString 메서드를 가지고 있다면 어떻게 될까?

Javascript 엔진은 chimp 의 메서드가 있는지 확인하고 있디면 chimp 의 toString 을 없다면 Object 의 원형에 있는 toString 을 호출하게 된다.

```javascript
'use strict';

let chimp = {
    hasThumbs:true,
    swing:()=>{
        return '나무 꼭대기에 대롱대롱 매달려 있네요';
    },
    toString:()=>{
        return '침팬치';
    }
};
console.log(chimp.toString());
```
로그에는 침팬치 가 출력될것이다.

지금 한 행위는 프로토타입을 재정의 한 것이다.

공유되는 이런 프로토타입을 상속받고 개별적인 속성을 확장하는 방법을 보도록한다.

```javascript
'use strict';
let ape = {
    hasThumbs: true,
    hasTail: false,
    swing: ()=>{
        return '메달리기';
    }
};

let chimp = Object.create(ape);
let bonobo = Object.create(ape);

bonobo.habitat = 'Centeral Africa';
console.log(bonobo.habitat); // Centeral Africa
console.log(chimp.habitat); // undefined
console.log(bonobo.hasTail); // false
console.log(bonobo.swing()); // 메달리기

console.log(chimp.hasThumbs); // true
console.log(bonobo.hasThumbs);// true

ape.hasThumbs = false;

console.log(chimp.hasThumbs); // false
console.log(bonobo.hasThumbs);// false

bonobo.hasThumbs = true;
console.log(chimp.hasThumbs); // false
console.log(bonobo.hasThumbs);// true
```
ape 라는 공유 프로토타입용 리터럴 객체를 만들었다.

ES5 에서 추가된 Object.create() 함수를 이용하면 프로토타입이 연결된 객체를 만들 수 있다.

앞에서 생성한 ape 를 이용하여 chimp 와 bonobo 객체를 생성하였고 bonobno 에는 habitat 을 추가 해주었다.
실행을 해보면 주석을 달아놓은것과 같이 나올 것이다.

bonobo 의 경우 ape 에 정의해놓은 모든 필드와 메서드를 가지고 있다.

거기에 habitat 이라는 속성을 추가했고 chimp 는 ape 프로토타입과 연결된 프로토타입만을 가지고 있다.
공유 프로토타입의 경우 해당 프로토타입을 수정하게되면 해당 프로토타입을 상속받은 모든 객체에 영향을 주게된다.

그래서 중간에 ape.hasThumbs 를 false 로 변경하게되면 chimp, bonobo 의 hasThumbs 는 모두 false 를 나타낸다.
그 밑에 bonobo.hasThumbs 를 수정한것은 공유 프로토타입을 수정한 것이아니라 bonobo.hasThumbs 를 정의한것과 같다.(위에서 toString 을 정의한것)

그렇기에 공유프로퍼티를 이용하고 자기자신의 hasThumbs 는 정의되지 않은 chimp 에는 영향을 주지않고 변경이 가능하다.
chimp 를 에게 색을 주고 싶다면 어떻게 해야할까?

```javascript
'use strict';
let ape = {
    hasThumbs: true,
    hasTail: false,
    swing: ()=>{
        return '메달리기';
    }
};

let chimp = Object.create(ape);
let bonobo = Object.create(ape);

bonobo.habitat = 'Centeral Africa';
console.log(bonobo.habitat); // Centeral Africa
console.log(chimp.habitat); // undefined
console.log(bonobo.hasTail); // false
console.log(bonobo.swing()); // 메달리기

console.log(chimp.hasThumbs); // true
console.log(bonobo.hasThumbs);// true

ape.hasThumbs = false;

console.log(chimp.hasThumbs); // false
console.log(bonobo.hasThumbs);// false

bonobo.hasThumbs = true;
console.log(chimp.hasThumbs); // false
console.log(bonobo.hasThumbs);// true

chimp.color = 'Gray';
let colorChimp = Object.create(chimp);
colorChimp.color = 'Gray';

console.log(colorChimp.color);
```

chimp 에 색을 나타내는 color 필드를 추가하고 chimp 를 공유 프로토타입으로 사용한다.

chimp 를 공유 프로토타입으로 사용하여 생성한 colorChimp 는 color 를 지니는 객체가 된다.
ape -> chimp -> colorChimp 까지 프로토타입이 체인 되었는데 이 depth 가 깊어지면 성능상의 문제가 생길수 있다.

너무 깊은 프로토타입 체인은 쓰지 않는 편이 좋다.

prototype 을 이용한 상속과 체인은 Javascript 스러운 코드를 작성하는데 많은 도움을 준다.

또한 prototype 은 위 코드에서도 나타나듯이 하나의 복제본을 레퍼런스하게 된다.

그러하여 각각의 객체가 따로 복제본을 가지지 않고 이는 메모리 절약을 도와준다.

객체를 생성하는 방법으로는 new 키워드를 이용한 방법도 존재한다.

다음 포스팅에서는 new 를 이용한 생성을 보겠다.

