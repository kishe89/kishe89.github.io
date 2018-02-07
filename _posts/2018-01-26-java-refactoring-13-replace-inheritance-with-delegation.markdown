---
layout: post
title:  "Java Refactoring Replace Inheritance with Delegation"
date:   2018-01-26 02:35:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Java
---

A 클래스와 B 클래스가 있고 B 는 A 를 상속받는다면 B 는 A 의 기능을 바로 이용할 수있다.
이것은 상속(Inheritance)이다. 위임(Delegation)은 B 클래스가 A 클래스의 인스턴스를 가지고(위임 필드)
B에서 A의 메서드를 호출하는 것이다. A 의 기능의 실행을 B 에게 위임하는 것이다.
상속은 상위클래스의 기능들중 불필요한 기능들까지 B 가 상속받을 수 있다. 예를 들어서
국무총리는 공직자(Prime minister is a Official)와 같이 클래스간 관계가 IS-A 관계일 때는 경찰은 공직자이기에 공직자로 가져야할
속성(field), 행동(method)를 모두 가지고 있어야 할것이다.

대통령 또한 공직자이다. 대통령과 국무총리를 생각해보자.
치안 유지를 위해 공직자로서 대통령이 해야할 일과 국무총리가 해야할 일은 다를 것이다.
예를 들어서 계엄령 선포를 할 때를 생각해보면 대통령이 계엄령을 내릴 수 없을 때 국무총리가 계엄령을 내려야 할 수 있을것이다.

이럴때 대통령의 행동(계엄령선포)를 국무총리가 행동(계엄령선포)를 해야하는데 이때 국무총리가 대통령을 상속받는다면
대통령의 권위에 도전하는 일(대통령의 모든 행동을 국무총리가 할 수 있음)이 발생할 수 있을 것이다.

오직 국무총리는 대통령의 부재시 대신해서 계엄령선포를 할 수 있으면 되며 평시에는 이런 일이 필요도 없을 것이다.
이렇게 일부의 기능만이 필요하여 상속거부가 일어나는 경우를 상속으로 처리한 것을 리팩토링 할 것이다.

국무총리가 대통령 인스턴스를 가지므로 HAS-A 관계가 성립한다.
즉 잘못된 IS-A -> HAS-A로의 변환이다.

- 이로 얻을 수 있는 이점은 각 클래스가 하는 일이 명확해진다.

- 상속받은 클래스에서 불필요한 기능들을 상속받지 않을 수 있다.(상속 거부를 안한다)



##### 리팩토링 카탈로그(상속을 위임으로 치환(Replace Inheritance with Delegation))

|이름|상속을 위임으로 치환|
|---|---|
|상황|클래스에 상속 관계가 있음|
|문제|하위 클래스가 상위 클래스 기능의 일부만 사용함(상속 거부), 하위 클래스가 상속 클래스와 IS-A 관계가 아님, 리스코프 치환 원칙 위반, 계약을 지키지 않음|
|해법|위임을 사용해서 상속을 치환함|

- 결과

  o 부적절한 상속 관계를 해소 가능함

  o 클래스에 필요한 기능이 명확해짐

  o 클래스 개선, 기능 추가가 편해짐

  x 위임하는 메서드를 작성해야 함

- 방법
1. 위임용 필드 도입

   1. 하위 클래스에 상위 클래스 타입의 위임용 필드 선언
   2. 생성자 안에서 위임용 필드를 this 로 초기화
   3. 상속받던 메서드를 재작성해서 위임용 필드를 이용하게 함
   4. 컴파일해서 테스트
2. 상속 관계 삭제

   1. 상위 클래스 선언(extends) 삭제
   2. 위임용 필드를 상위 클래스의 인스턴스로 초기화
   3. 지금까지 외부에서 암묵적으로 이용하던 메서드를 명시적으로 선언
   4. 그 메서드를 위임용 필드 경유 호출로 작성
   5. 컴파일해서 테스트

- 관련항목

    - 위임을 상속으로 치환

      역 리팩토링

##### Application
```java
package example_14_replace_inheritance_with_delegation;

public class Application {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
			Dice dice = new Dice();
			for(int i = 0 ; i <10 ;i++)
			System.out.println("주사위는 : "+dice.nextInt());
	}

}
```
##### Dice
```java
package example_14_replace_inheritance_with_delegation;

import java.util.Random;

public class Dice extends Random{


	public Dice() {
		super(314159L);
	}
	public Dice(long seed) {
		super(seed);
	}
	@Override
	public int nextInt() {
		// TODO Auto-generated method stub
		return nextInt(6)+1;
	}
	@Override
	public boolean nextBoolean() {
		// TODO Auto-generated method stub
		throw new UnsupportedOperationException();
	}

	@Override
	public void nextBytes(byte[] arg0) {
		// TODO Auto-generated method stub
		throw new UnsupportedOperationException();
	}

	@Override
	public double nextDouble() {
		// TODO Auto-generated method stub
		throw new UnsupportedOperationException();
	}

	@Override
	public float nextFloat() {
		// TODO Auto-generated method stub
		throw new UnsupportedOperationException();
	}

	@Override
	public synchronized double nextGaussian() {
		// TODO Auto-generated method stub
		throw new UnsupportedOperationException();
	}

}
```

대통령과 국무총리로 하면 좋겠지만 그들의 정확한 권한과 필요한 기능을 모르는 관계로
책에 있는 주사위 예제(길벗 출판, 자바로 배우는 리팩토링 입문)를 가져왔다.

Dice 는 1~6까지 그려져 있는 주사위다.
우리가 원하는 랜덤한 정수를 반환하는 기능은 Random 클래스의 nextInt(int bound)에 구현이 되어있다.

그렇기에 Random 클래스를 상속받았고 메서드들을 오버라이드 했다.
하지만 나머지 메서드들은 필요가 없다. 그렇기에 UnsupportedOperationException 을 던졌다.
실행시 해당 익셉션이 발생하므로 호출을 안하게 될 것이다.

이제 Application 을 실행시키면 정상적으로 10번의 주사위 결과가 출력된다.
하지만 Dice 객체는 불필요한 메서드들이 너무 많이 상속되어있다.

우리는 분명히 nextInt(int bound) 기능만이 필요했는데 이를 Dice 에서 굳이 상속받아야할 이유가 있을까?
동작에는 문제가 없지만 Dice 에 오버라이드된 수많은 메서드들은 외부 사용자가 보기에 혼란스러울것이다.
외부 사용자는 이 코드의 상속구조와 제약조건에 관심이 있는것이 아니라 기능 자체에 관심이 있다.

코드를 다른곳에서 사용하기위해 Dice. 을 친 상황을 생각해보자.
IDE 에서는 왜 들어갔는지도 모르겠는 수많은 메서드들을 추천해줄 것이고 이는 의도치 않은 사용을 발생시킬 수 있다.
물론 우리는 UnsupportedOperationException 을 던지도록 했지만 우리가 지금 오버라이드한 메서드 이외에도 많은 메서드가 존재한다.

그리고 Dice is a Random 은 성립이 안된다.
Random 은 말그대로 랜덤한 난수를 여러타입으로 반환하는 클래스인데 우리는 이 클래스의 아주 일부분이
필요할 뿐이다.

그러므로 이러한 상황에서의 상속은 좋지 않은 선택이다.
일단 상속으로 해결할 때의 문제를 알았으니 리팩토링을 시작해본다.

Random 클래스는 분명 필요하다. 이를 가지는 필드를 하나 생성한다.

##### Dice
```java
package example_14_replace_inheritance_with_delegation;

import java.util.Random;

public class Dice extends Random{

	private final Random random;

	public Dice() {
		super(314159L);
	}
	public Dice(long seed) {
		super(seed);
	}
	@Override
	public int nextInt() {
		// TODO Auto-generated method stub
		return nextInt(6)+1;
	}
	@Override
	public boolean nextBoolean() {
		// TODO Auto-generated method stub
		throw new UnsupportedOperationException();
	}

	@Override
	public void nextBytes(byte[] arg0) {
		// TODO Auto-generated method stub
		throw new UnsupportedOperationException();
	}

	@Override
	public double nextDouble() {
		// TODO Auto-generated method stub
		throw new UnsupportedOperationException();
	}

	@Override
	public float nextFloat() {
		// TODO Auto-generated method stub
		throw new UnsupportedOperationException();
	}

	@Override
	public synchronized double nextGaussian() {
		// TODO Auto-generated method stub
		throw new UnsupportedOperationException();
	}

}
```

random 이라는 변수를 Dice 에 추가하였다.
##### Dice
```java
package example_14_replace_inheritance_with_delegation;

import java.util.Random;

public class Dice extends Random{

	private final Random random;

	public Dice() {
		super(314159L);
		random = this;
	}
	public Dice(long seed) {
		super(seed);
		random = this;
	}
	@Override
	public int nextInt() {
		// TODO Auto-generated method stub
		return nextInt(6)+1;
	}
	@Override
	public boolean nextBoolean() {
		// TODO Auto-generated method stub
		throw new UnsupportedOperationException();
	}

	@Override
	public void nextBytes(byte[] arg0) {
		// TODO Auto-generated method stub
		throw new UnsupportedOperationException();
	}

	@Override
	public double nextDouble() {
		// TODO Auto-generated method stub
		throw new UnsupportedOperationException();
	}

	@Override
	public float nextFloat() {
		// TODO Auto-generated method stub
		throw new UnsupportedOperationException();
	}

	@Override
	public synchronized double nextGaussian() {
		// TODO Auto-generated method stub
		throw new UnsupportedOperationException();
	}

}
```
Dice 객체는 하나의 Random 객체만 가지면 되며 Random 객체가 변할일은 없기에 final 로 선언함에 따라
random 은 객체 생성시에 초기화 되어야한다.
아직까지는 Random 을 Dice 에서 상속받고 있기에 this 를 통해 초기화가 가능하다.

이제 random 을 가지고 있기에 random.nextInt(int bound) 가 가능하다.
이를 이용하여 Dice 의 nextInt()를 수정한다.

##### Dice
```java
@Override
	public int nextInt() {
		// TODO Auto-generated method stub
		return random.nextInt(6)+1;
	}
```
컴파일 해서 돌려보면 문제없이 돌아가는걸 확인할 수 있다.
여기에서 잠깐 한가지 확인해보자. 위에서 우리는 Random 과 Dice 는 IS-A라는 상속 관계에 부합하지 않는다고 머리로 생각했다.
이를 좀 더 상세히 확인할 수 있는 방법이 있는데 리스코프 치환 원칙에 부합하는지 확인하면된다.

**리스코프 치환원칙은 A 가 Object 를 상속받을 때 Object 타입의 변수로 A를 인스턴스화 했을 때에도 문제없이 사용가능해야한다는 것이다.**

```java
Random random = new Dice();
random.nextBoolean();
```

즉 위와 같은 코드가 문제없이 동작해야한다는 이야기인데 우리의 Dice 는 정상적으로 동작하는게 맞는가?

random 은 UnsupportedOperationException 을 뱉을 것이다.
물론 Dice 에서 오버라이드를 해서 throw 했기 때문이지만 이렇게 한 이유는 우리에게 필요가 없기때문이었다.
즉 리스코프 치환 원칙(계약 = 기대했던 동작)을 깨는 구조이기에 적절치 못하다고 판단할 수 있다.

그럼 여러모로 좋지 않음을 다시 한번 깨달았으므로 마저 리팩토링을 진행한다.
필드로 Random 인스턴스를 가지고 있으므로 우리는 굳이 상속을 받을 필요가 없다.
상속관계를 제거한다.

##### Dice
```java
package example_14_replace_inheritance_with_delegation;

import java.util.Random;

public class Dice{

	private final Random random;

	public Dice() {
		random = new Random(314159L);
	}
	public Dice(long seed) {
		random = new Random(seed);
	}

	public int nextInt() {
		// TODO Auto-generated method stub
		return random.nextInt(6)+1;
	}

}
```
상속관계를 제거함에 따라 오버라이드는 받지 않는다.
대신 위임용 필드인 random 의 .nextInt(int bound)를 호출하는 메서드가 필요하기에 nextInt()를 그대로 둔다.

여기까지 하면 불필요한 오버라이드는 일어나지 않게 된다.
후에 이 코드를 다시 사용할 사람에게도 덜 혼란스러운 딱 필요한 기능만을 가지게 되었다.

다 끝났지만 Dice 의 생성자를 봐보자.
new Random(long) 같은 코드의 형태가 반복된다. Random 이 난수를 생성하기 위해서 seed 값을 이용하게 되는데
물론 초기값을 주지않을 경우에는 내부적으로 생성시 계산한 시드값을 이용한다.

우리는 Random 의 시드 초기값을 결정하였으므로 전달해줘야한다.
또한 Dice 의 생성자에는 seed 를 받는 생성자가 있다. 생성자 연쇄라는 패턴을 통해 해결할 수 있다.

##### Dice
```java
package example_14_replace_inheritance_with_delegation;

import java.util.Random;

public class Dice{

	private final Random random;

	public Dice() {
		this(314159L);
	}
	public Dice(long seed) {
		random = new Random(seed);
	}

	public int nextInt() {
		// TODO Auto-generated method stub
		return random.nextInt(6)+1;
	}

}
```

다음 내용은 대리자 은폐(Hide Delegate)이다.
