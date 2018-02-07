---
layout: post
title:  "Java Refactoring Intro"
date:   2018-01-04 18:13:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Java
---

1일 1포스팅의 처음이다.

일단 시작은 길벗에서 출판된 자바로 배우는 리팩토링 입문이란 책을 기본으로 내가 읽으며 느낀 점을
기본으로 시작한다(책 리뷰어 신청했는데 되버려서ㅎㅎ).

일단 리팩토링(Refactoring)은 기본적으로 코드의 좀 더 나은 확장성, 재사용성, 가독성을 가지기 위한 작업이며 노력이다.

최근의 소프트웨어는 멈춰있지 않고 발전속도 또한 점점 가속화 되어가며 트렌드는 따로따로 따라가려면 어지간한 노력가지고는
불가능에 가까워지고 있으며 오픈소스 문화, agile방법론, DevOps문화의 정착에 따라 점점 더 생산성에 포커스가 맞춰지는
상황에서 기존 코드가 완벽히 커플링 되어있으면 모든 소프트웨어는 매번 재개발을 할 수 밖에없는데 이는 오히려 생산성을 저해하고
개발 비용의 증가를 가지고 올 것이다.

리팩토링을 통한 꾸준한 코드 구조에대한 개선 노력을 들이면 좀 더 유연한 대처가 가능해진다.
거기에 요즘 언어들은 멀티패러다임 형태로 서로의 장점들을 흡수하며 버전업 되어가기 때문에 더욱이 리팩토링, 패턴, 알고리즘등에 대한
공부가 필요하다고 개인적으로 느끼고 있다.

서론은 이정도로 하고 그럼 어떤 작업이 리팩토링일까에 대해 생각해보자

예를 들어서 아래 코드 처럼 파라미터로 받은 두 정수를 덧셈 뺄셈하는 Calculator 객체 코드가 있다고 하자.

이 객체는 단지 입력받는 두개의 정수 파라미터에 대해 덧셈과 뺄셈만을 위한 객체이다.
###### Calculator.java
```java
package example_1_intro;

public class Calculator {
	public int addition(int value1, int value2) {
		return value1+value2;
	}
	public int subtraction(int value1, int value2) {
		return value1-value2;
	}
}

```

이 코드에 나눗셈, 곱셈하는 기능을 추가하는 행위는 리팩토링일까?

아래의 Calculator.java 처럼 나눗셈, 곱셉을 추가함으로써 위에서 말했듯이 좀 더 나은 확장성, 재사용성, 가독성을 가지게 되었나에 대해 생각해보자.

물론 기능이 추가됨에 따라 이 4가지 기능을 사용해야하는 소프트웨어에대한 재사용성이 늘었다고 주장할 수 있을것이다.
하지만 확장성과 가독성이 증대 되었냐에 대한 질문에는 답할 수 없을 것이다.

또한 재사용성에 대해서도 덧셈과 뺄셈만 필요한 코드(우리의 Calculator객체)에 대해서는 불필요한 코드가 들어감에 따라 재사용성이 늘었다고 주장하는 것도
무조건적으로 타당하지는 않을것이다.

이러한 작업은 그저 기능의 추가로 볼 수 있지 리팩토링이라고는 할 수 없을것이다.
정수를 이용한 곱셈 및 나눗셈으로 인한 올림 버림으로 발생하는 문제를 수정하는 것(좀 더 정확한 수치가 필요할 때)에 대해서도 생각해보자.

즉 올림 버림으로 인해 실수부가 잘리는 문제가 버그인 경우 이를 수정하는 행위 또한 리팩토링이 아닌 그저 버그 수정이라고 볼 수 있다.
###### Calculator.java
```java
package example_1_intro;

public class Calculator {
	public int addition(int value1, int value2) {
		return value1+value2;
	}
	public int subtraction(int value1, int value2) {
		return value1-value2;
	}
	public int division(int value1, int value2) {
		return value1/value2;
	}
	public int multiplication(int value1, int value2) {
		return value1*value2;
	}
}

```

우리가 리팩토링할 코드는 동작(처음 우리가 필요했던 Calculator는 그저 덧셈과 뺄셈기능만을 필요로 하는 계산기였다.)에 변경이 있어서는 안된다.

그렇다면 위 2가지 코드를 보고 어떤 행위를 통해서 Calculator를 좀 더 확장성 재사용성, 가독성을 가지게 할 수 있을까?

일단 Java에서 제공하는 interface를 이용해서 행위를 분리해보겠다.
###### Addition.java
```java
package example_1_intro;
public interface Addition {
	public int addition(int value1, int value2);
}
```
###### Subtraction.java
```java
package example_1_intro;
public interface Subtraction {
	public int subtraction(int value1, int value2);
}
```
###### Multiplication.java
```java
package example_1_intro;
public interface Multiplication {
	public int multiplication(int value1, int value2);
}
```
###### Division.java
```java
package example_1_intro;
public interface Division {
	public int division(int value1, int value2);
}
```

위 처럼 4개의 인터페이스를 만들었다. 그리고 아래 Calculator.java소스를 보면 만든 인터페이스들을 implements해줬다.
###### Calculator.java
```java
package example_1_intro;

public class Calculator implements Addition,Subtraction{
	@Override
	public int addition(int value1, int value2) {
		// TODO Auto-generated method stub
		return value1+value2;
	}

	@Override
	public int subtraction(int value1, int value2) {
		// TODO Auto-generated method stub
		return value1-value2;
	}
}

```
이 행위는 리팩토링일까?

기존의 동작의 변경이 없으면서 좀 더 나을 재사용성, 확장성, 가독성을 얻었을까?
우리가 처음 필요했던 Calculator는 입력받은 두 정수의 덧셈과 뺄셈을 하는 기능을 가진 객체였다.

위 코드는 일단 기존에 했던 기능을 하는데 무리는 없어보인다. 즉 기존의 동작은 가능하다.

그리고 우린 어떠한 기능도 추가하지 않았다. 또한 Calculator의 필요 행위는 Calculator에 정의되지 않고
interface에 정의 되었기에 해당 기능중 불필요한게 있다면 그저 implements를 안하면 되며 특정 기능이 필요하다면
interface를 하나 더 만들어 implements하면 될 것이다.
##### Calculator.java
```java
package example_1_intro;

public class Calculator implements Addition,Subtraction,Division,Multiplication{

	@Override
	public int addition(int value1, int value2) {
		// TODO Auto-generated method stub
		return value1+value2;
	}

	@Override
	public int subtraction(int value1, int value2) {
		// TODO Auto-generated method stub
		return value1-value2;
	}

	@Override
	public int multiplication(int value1, int value2) {
		// TODO Auto-generated method stub
		return value1*value2;
	}

	@Override
	public int division(int value1, int value2) {
		// TODO Auto-generated method stub
		return value1/value2;
	}
}
```
Calculator에 전부 implements한 경우는 만약 Calculator를 상속하여 사용하려고 할 경우 기능이 전부 필요치 않다면
이 또한 불필요한 기능의 추가가 될 수 있을것이다.

하지만 Calculator의 기능들이 앞으로 사용될 객체의 Base가 될 수 있는 모든 객체의 공통된 행동이라면
이 방법이 더 좋을 순 있다.

하지만 코드가 점점 비대해짐에 따라 테스트를(4가지 함수 다 테스트 해야함) 하기 힘들어질 수 있다.

우리의 Calculator가 처음에 이야기 했듯이 2가지 기능만을 가지길 원했지만 추가되는데 있어서 좀 더 나은 확장성, 재사용성, 가독성을 가지기
위해 어떤 방법이 있을까?

아래의 ExtendedCalculator.java를 보자
##### ExtendedCalculator.java
```java
package example_1_intro;

public class ExtendedCalculator extends Calculator implements Multiplication,Division{

	@Override
	public int addition(int value1, int value2) {
		// TODO Auto-generated method stub
		return super.addition(value1, value2);
	}

	@Override
	public int subtraction(int value1, int value2) {
		// TODO Auto-generated method stub
		return super.subtraction(value1, value2);
	}

	@Override
	public int division(int value1, int value2) {
		// TODO Auto-generated method stub
		return value1/value2;
	}

	@Override
	public int multiplication(int value1, int value2) {
		// TODO Auto-generated method stub
		return value1*value2;
	}

}

```
Calculator의 두가지 기능인 덧셈, 뺄셈에 대해서 테스트가 통과했다는 가정을 하자.

그럴 경우 ExtendedCalculator는 division과 multiplication 두가지 기능에 대한 테스트케이스만을
통과하면 될 것이다.

우리는 ExtendedCalculator에서 addition과 subtraction에 대해 따로 작업을 하지 않고 앞에서 성공한
Calculator의 addition과 subtraction을 사용하고 있기 때문이다.

우리는 단순히 기능을 추가하지 않았다.
기능을 추가하기 위해 구조를 변경하고 개선하려고 노력한 것이다.
물론 지금 변경한 구조가 최선은 아닐 수 있다.

하지만 추가하기 위한 행위 자체에 대해서는 유연해 졌으며 기존 코드에대해 기능을 추가하는 행위에 대해서는 이전 보다
적은 노력이 들 것이다.

이러한 행위 자체를 리팩토링이라고 한다.
우리가 리팩토링 해야할 부분들은 코드에서 악취가 나는 부분 혹은 기술적 부채가 쌓여있는 부분이다.

책에서 나타내는 22가지 악취표를 보면 우리가 어떤 부분에 대해서 리팩토링해야 할지에 대한 가이드가 될 수 있을거같다.
앞으로 해나갈 내용이며 이에대해 아래 표에 앞으로 포스트 링크를 하나씩 걸어 나갈 것이다.

|악취|내용|
|---|---|
|중복 코드|같은 코드가 곳곳에 중복되어 있다.|
|너무 긴 메서드|메서드가 너무 길다.|
|방대한 클래스|클래스의 필드나 메서드가 너무 많다.|
|과다한 매개변수|메서드가 받는 매개변수 개수가 너무 많다.|
|변경 발산|사양 변경이 있을 때 수정 내용이 곳곳에 흩어져 있다.|
|변경 분산|어떤 클래스를 수정하면 다른 클래스도 수정해야 한다.|
|속성 조작 끼어들기|언제나 다른 클래스 내용을 수정하는 클래스가 있다.|
|데이터 뭉치|합쳐서 다뤄야 할 데이터가 한 클래스에 모여 있지 않다.|
|기본 타입 집착|클래스를 만들지 않고 int 같은 기본 타입만 사용한다.|
|스위치 문|switch문이나 if문으로 동작을 나눈다.|
|평행 상속|하위 클래스를 만들면 클래스 계층의 다른 곳에도 하위 클래스를 만들어야 한다.|
|게으른 클래스|클래스가 별로 하는 게 없다.|
|의심스러운 일반화|'언젠간 이런 확장을 하겠지'라고 너무 일반화한다.|
|임시 속성|임시로만 쓰는 필드가 있다.|
|메시지 연쇄|메서드 호출 연쇄가 너무 많다.|
|중개자|맡기기만 하고 자신은 일하지 않는 클래스가 있다.|
|부적절한 관계|그럴 필요가 없는데도 양방향 링크를 걸거나 IS-A 관계가 없는데 상속을 사용한다.|
|클래스 인터페이스 불일치|클래스 인터페이스(API)가 적절하지 않다.|
|불완전한 라이브러리 클래스|기존 라이브러리 클래스를 사용하기 어렵다.|
|데이터 클래스|필드와 getter, setter 메서드뿐인 클래스가 있다.|
|상속 거부|상속한 메서드인데 호출하면 문제가 발생한다.|
|주석|코드의 모자란 점을 설명하기 위해 자세한 주석이 붙어 있다.|

리팩토링을 하여 얻는 이점은 분명히 있다. 하지만 과도한 리팩토링(데드라인을 못 지킴, 테스트 및 실행도 안해보고 리팩토링)등은 오히려
문제를 야기할 수 있으니 주의 해야한다.

내일은 코드상에 하드코딩된 상수값들에 대한 리팩토링 방법들에 대해서 포스팅 해야겠다.
