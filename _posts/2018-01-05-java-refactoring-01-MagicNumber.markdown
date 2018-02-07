---
layout: post
title:  "Java Refactoring MagicNumber"
date:   2018-01-05 18:53:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Java
---

1일 1포스팅의 2번째이다.

어제 작성했던 예제 코드를 재탕한다.
일단 우리가 오늘 리팩토링 해볼 내용은 코드내에 하드코딩 되어있는 숫자 혹은 문자열(Magic number) 을 기호 상수(Symbolic Constant)로
치환 해볼 것이다.

Magic number는 코드상에서 if, switch, while, for등 반복, 분기등에서 주로 나타나며 또한 리소스가 필요할 때
리소스 관리는 생각안하고 하드코딩한 곳에서 주로 나타나는데 프로젝트의 코드라인수가 정말 짧고 이러한 상수값들이 많이 사용이 안되서 한 두개의
상수값만이 사용되며 같은 값을 이용하는곳이 한곳이라면 문제는 덜 할 것이다. 하지만 이런 프로젝트는 없다.

예를 들어 안드로이드의 startActivityForResult메서드를 생각해보면 request코드와 result코드값이 있는데 이러한 값이
각 Activity별로 같은 값이어도 나타내는 의미가 다를 수 있으며 그 수도 아주 많은 사항에 따라 100개 이상일 수 있다.
물론 100개까지 가는 것도 문제가 있긴한데 극한 상황을 생각해보면 그럴 수 있다.

이러한 때에 Activity 내의 1이란 요청코드를 다른 값으로 변경 해야할 경우 직접 해당 코드 부분에 가서 바꾸는 방법이 최선일 것이다.
괜히 귀찮다고 tool에서 제공하는 치환기능을 이용했다가 코드내에서 1이 들어간 부분들이 전부 치환 될 수 도 있다.

이러한 문제와 리소스의 재사용성 및 코드에서 상수가 나타내는 의미를 정확히 하기위해서 기호 상수로의 치환을 해야한다.

기호 상수라고 특별한게 아니라 우리 인간이 알아먹기 쉽게 상수의 의미를 나타내는 이름의 변수에 해당 상수값으로 초기화해주고
사용은 기호 상수를 사용하는 것이다.

어제의 예제중 Calculator.java의 subtraction 메소드를 약간 변형해서 value1이 value2보다 작을 경우 음수가 나오는데
음수가 안나오도록 해보자.

물론 굳이 상수를 사용하지 않아도 가능하지만 Magic Number에 대한 리팩토링을 위한 예이다.
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

###### Calculator.java
```java
package example_2_enum;

public class Calculator implements Addition,Subtraction{
	@Override
	public int addition(int value1, int value2) {
		// TODO Auto-generated method stub
		return value1+value2;
	}

	@Override
	public int subtraction(int value1, int value2) {
		// TODO Auto-generated method stub

		if((value1-value2)<0) {
			return (value1-value2)*-1;
		}
		return value1-value2;
	}

}

```
위 Calculator코드의 14번째 line을 보면 조건식이 (value1-value2)<0 인 조건식인데 여기서 0이 Magic Number에
해당한다.

삼항연산자를 이용하면 아래 처럼도 될 것이고 또 다른 방법으로도 Magic Number를 이용안하고 구현할 수 있을것이다.

위에서도 이야기 했지만 해당 부분은 그저 Magic Number에 대한 이야기를 하기위해 억지로 만든 예이다.
```java
package example_2_enum;

public class Calculator implements Addition,Subtraction{
	@Override
	public int addition(int value1, int value2) {
		// TODO Auto-generated method stub
		return value1+value2;
	}

	@Override
	public int subtraction(int value1, int value2) {
		// TODO Auto-generated method stub

		return value1<value2?value2-value1:value1-value2;
	}

}
```

글 처음에 이야기 했듯이 저러한 조건 값들이 여러개 일때 하드 코딩 되어있으면 추후에 유지보수 혹은 기능변경을 할 때
해당 조건으로 인해 예상치 못한 버그를 발생시킬 수 있다.

그렇다면 우리는 어떻게 저 값을 기호 상수로 변경할 수 있을까?

###### Calculator.java
```java
package example_2_enum;

public class Calculator implements Addition,Subtraction{
  private static final int SUBTRACTION_CONDITION = 0;
	@Override
	public int addition(int value1, int value2) {
		// TODO Auto-generated method stub
		return value1+value2;
	}

	@Override
	public int subtraction(int value1, int value2) {
		// TODO Auto-generated method stub

		if((value1-value2)<SUBTRACTION_CONDITION) {
			return (value1-value2)*-1;
		}
		return value1-value2;
	}

}

```

이런식으로 일단 변경 할 수 있을것이다.

일단 SUBTRACTION_CONDITION 변수는 Calculator에서는 초기화가 된 이후
변경도 안되며 이해할 수 있는 문자열로 변경 되었으며 0이 아닌 SUBTRACTION_CONDITION으로 사용 부분을 찾기도 쉬워졌다.

하지만 아래 처럼 OtherCalculator란게 있다 하고 이곳에서의 SUBTRACTION_CONDITION 은 다른 값을 가진다고 생각해보자.
서로 같은 기능을 하는 기호상수임에도 불구하고 값이 다르다.

이럴경우 두개의 클래스의 기호 상수의 이름은 같은데 값은 다른것으로 인해 어떤 문제가 발생할 수 있을까?

###### OtherCalculator.java
```java
package example_2_enum;

public class OtherCalculator implements Addition,Subtraction{
  private static final int SUBTRACTION_CONDITION = 123;
	@Override
	public int addition(int value1, int value2) {
		// TODO Auto-generated method stub
		return value1+value2;
	}

	@Override
	public int subtraction(int value1, int value2) {
		// TODO Auto-generated method stub

		if((value1-value2)<SUBTRACTION_CONDITION) {
			return (value1-value2)*-1;
		}
		return value1-value2;
	}

}

```

우리는 subtraction함수안에 이미 filter역할을 하는 조건문을 적어 놨지만
파라미터로 전달하기전에 더 검사하고 싶어서 Calculator와 OtherCalculator를 작업하고 1년이 지난 후
ex1과 같은 코드를 작성했다고 생각해보자.
##### ex1
```java
Calculator calculator = new Calculator();
OtherCalculator other_calculator = new OtherCalculator();

int value1 = 1;
int value2 = 2;
if((value1-value2)<OtherCalculator.SUBTRACTION_CONDITION){
    // TODO
}
```

고작 각 클래스가 가지고있는 멤버변수의 값 자체를 여러분들이 기억하고 있을 가능성은 희박하다.

그저 우리가 믿을건 우리가 정의 해놓은 기호 상수일 뿐인데 저 if의 조건에서 기호 상수 자체는 맞다. 하지만
기호 상수의 값은 어떤가?

물론 상황에 따라 각자 가지고 있어야할 값도 있을 수 있다. 하지만 조각나있는 기호 상수는 오히려 시간이 지남에 따라
잘못된 믿음으로 인한 버그를 발생 시킬 수 있다.

그렇다면 어떻게 좀 더 우리는 덜 기억해도 되게 기호 상수를 이용할 수 있을까?

그 방법중 하나는 해당 기호 상수를 클래스로 치환하는 방법이 있다.
##### SybolicConstant.java
```java
package example_2_enum;

public class SybolicConstant {
	private static final int CALCULATOR_SUBTRACTION_CONDITION = 0;
	private static final int OTHERCALCULATOR_SUBTRACTION_CONDITION = 123;
}

```
##### ex2
```java
Calculator calculator = new Calculator();
OtherCalculator other_calculator = new OtherCalculator();

int value1 = 1;
int value2 = 2;
if((value1-value2)<SybolicConstant.SUBTRACTION_CONDITION){
    // TODO
}
```

이처럼 치환을 수행하게 되면 우리는 기호 상수를 하나의 클래스에 전부 관리 할 수 있다.

물론 해당 클래스에서 관리하는 기호 상수가 너무 많아지면 이 또한 문제지만 그럴 경우는
enum을 이용하여 그루핑 했을 때 좀 더 이해에 도움을 줄 수 있는 기호 상수들은 따로 관리 할 수 있을 것입니다.

여태 상수값을 코드에 하드코딩하는 것에 대한 문제를 이야기 했습니다.

하지만 꼭 모든 값을 기호 상수로 치환 해야하냐
하면 굳이 그럴 필요 없는 값들이 있습니다. 우리는 자바에서의 배열 인덱스의 최솟값이 0이라는 사실을 이미 알고 있습니다.
그리고 array는 length라는 필드를 가지고 있습니다.

이를 굳이 ARRAY_SIZE와 같은 기호 상수로 치환할 필요는 없습니다.
```java
for(int index = array.length; index>MIN_INDEX; index --){
    // TODO
}
```
와 같은 코드는 오히려 읽는데 불편함을 줄 수 있습니다.
물론 아래 ex3처럼 크기가 정해진 ARRAY를 선언하는 경우등에는 ex4처럼 기호 상수로 치환하는 것이 더 좋은 방법일 것입니다.
##### ex3
```java
int[] height = new int[11];
int[] width = new int[11];
```
##### ex4
```java
private static final int ARRAY_SIZE = 11;


int[] height = new int[ARRAY_SIZE];
int[] width = new int[ARRAY_SIZE];
```

상수들중에는 서로 의존 관계를 가진 것이 있을 수 있습니다.

ex4코드를 기준으로 예를 들어보면 높이와 폭을 가지는 사각형인데
이 사각형은 높이에 대해 폭은 2배여야 한다고 생각해 봅시다.

처음 시작은 ex5와 같이 짤 것입니다.
##### ex5
```java
int[] height = new int[11];
int[] width = new int[22];
```


이를 기호 상수로 치환해보면 ex6처럼 할 수도 있을 것입니다.
##### ex6
```java
private static final int HEIGHT_ARRAY_SIZE = 11;
private static final int WIDTH_ARRAY_SIZE = 22;

int[] height = new int[HEIGHT_ARRAY_SIZE];
int[] width = new int[WIDTH_ARRAY_SIZE];
```

하지만 위 코드는 HEIGHT_ARRAY_SIZE를 변경하게 되면 WIDTH_ARRAY_SIZE 또한 변경 해줘야합니다.
우리는 높이에 대해 폭은 2배라는 규칙을 알고 있습니다.

즉 width = height * 2라는 식을 알고 있습니다.
width는 height라는 변수에 의존적입니다.

이를 기호 상수의 대입식에 표현해보면 ex7과 같이 표현 할 수 있을겁니다.
##### ex7
```java
private static final int HEIGHT_ARRAY_SIZE = 11;
private static final int WIDTH_ARRAY_SIZE = HEIGHT_ARRAY_SIZE*2;

int[] height = new int[HEIGHT_ARRAY_SIZE];
int[] width = new int[WIDTH_ARRAY_SIZE];
```

이런 상호 의존 관계에 있는 상수값들은 따로 따로 만들시 오히려 코드의 관리 측면에서 더 큰 복잡함을 유발할 수 있습니다.

그러므로 최소한 ex7과 같은 형태까지로의 리팩토링 노력은 필요할 것 입니다.

마지막으로 정리하는 표 입니다.

|||
|---|---|
|이름|매직 넘버를 기호 상수로 치환|
|상황|상수를 사용함|
|문제|매직 넘버는 의미를 알기 어려움|
||매직 넘버가 여러 곳에 있으면 변경하기 어려움|
|해법|매직 넘버를 기호 상수로 치환|
|결과|상수의 의미를 알기 쉬워짐|
||기호 상수의 값을 변경하면 상수를 사용하는 모든 곳이 변경됨|
||이해하기 어려운 이름을 사용하면 오해가 생길 수 있음|

오늘 1포스팅 주제였던 Magic number 를 Sybolic Constant로 치환은 여기까지 입니다.

내일은 코드의 처리 흐름을 좀 더 알기 쉽게 하기위해 제어 플래그 삭제를 해보도록 하겠습니다.
