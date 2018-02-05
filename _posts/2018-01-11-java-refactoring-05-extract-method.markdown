---
layout: post
title:  "Java Refactoring Extract method"
date:   2018-01-11 16:37:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Java
---

필드 혹은 멤버변수 가 어떤 객체가(dog,cat,person,...,etc) 가지는 속성(age,sex,height,width,sound,...,etc)이라면
메서드(method)는 객체들의 행동을(run,play,stop,increase,...,etc) 매핑하는 것이다.

우리가 일반적으로 생각하는 행동들을 코드로 매핑하기위해서 작성하다 보면 행동들을 준비하기 위해서라거나 혹은 행동의
결과를 정제 한다던가 하는 행동들이 필요해질 수 있다.

이러한 작업들은 주로 반복되기 마련인데 코드상의 반복되는 코드들을 다시 행동으로 나타내게 되면 중복 코드를 줄일 수 있다.

##### 리팩토링 카탈로그(메서드 추출)
|이름|메서드 추출(Extract Method)|
|---|---|
|상황|메서드를 작성함|
|문제|메서드 하나가 너무 길다.|
|해법|기존 메서드에서 묶을 수 있는 코드를 추출해 새로운 메서드를 작성함|

- 결과

  o 각 메서드가 짧아짐

  x 메서드 개수가 늘어남

- 방법
1. 새로운 메서드 작성

    1. 새로운 메서드에 적절한 이름 붙이기
        - 메서드가 무엇을 하는지 잘 알 수 있는 이름을 붙임
        - 메서드에서 실제로 어떻게 처리하는지 뜻하는 이름은 붙이지 않음
        - 적당한 이름을 붙일 수 없다면 적절한 메서드가 아님
    2. 기존 메서드에서 새로운 메서드로 코드 복사
    3. 메서드 내부의 지역 변수 검토

        - 메서드 내부의 지역 변수 검토
    4. 메서드 매개변수 검토

        - 복사한 코드에서 입력값으로 사용하는 변수가 있다면 메서드 매개변수로 만든다.
    5. 메서드 반환값 검토

        - 복사한 코드에서 변경되는 변수가 있는지 조사
        - 변경된 변수가 여러 개 있다면 리팩토링을 계속하기 어려움
        - 변경된 변수가 하나뿐이라면 메서드 반환값으로 쓰기에 적당한지 검토

          - 적당하다면 메서드 반환값으로 사용
          - 적당하지 않다면 리팩토링을 계속하기 어려움
    6. 컴파일
2. 새로운 메서드 호출

    1. 기존 메서드에서 앞서 코드를 복사한 부분을 새로운 메서드 호출로 치환
    2. 기존 메서드에서 더는 사용하지 않는 지역 변수가 있으면 삭제
    3. 컴파일해서 테스트

- 관련항목

    - 임시 변수 분리. 메서드 추출 전에 임시 변수 분리부터 하는게 좋을 때가 있음
    - 질의로 임시 변수 치환. 메서드 추출 전에 질의로 임시 변수 치환부터 하는게 좋을 때가 있음
    - 메서드 인라인화. 역 리팩토링


##### ex1
```java
package example_6_extract_to_method;

public class Main {

	private static String _content = "1234567890";

	public static void main(String[] args) {
		print(0);
	}

	private static void print(int times) {
		// TODO Auto-generated method stub

		// 테두리 출력
		System.out.print("+");
		for(int i = 0 ; i < _content.length(); i++) {
			System.out.print("-");
		}
		System.out.println("+");

		// 내용 출력
		for(int i = 0 ; i < times; i++) {
			System.out.println("|"+_content+"|");
		}

		// 테두리 출력
		System.out.print("+");
		for(int i = 0 ; i < _content.length(); i++) {
			System.out.print("-");
		}
		System.out.println("+");
	}

}

```

##### ex2
```java
package example_6_extract_to_method;

public class ExtractMain {

	private static String _content = "1234567890";

	public static void main(String[] args) {
		print(0);
	}

	private static void print(int times) {
		// TODO Auto-generated method stub

		// 테두리 출력
		printBorder();

		// 내용 출력
		printContent(times);

		// 테두리 출력
		printBorder();
	}

	private static void printContent(int times) {
		for(int i = 0 ; i < times; i++) {
			System.out.println("|"+_content+"|");
		}
	}

	private static void printBorder() {
		System.out.print("+");
		for(int i = 0 ; i < _content.length(); i++) {
			System.out.print("-");
		}
		System.out.println("+");
	}
}

```

일반적으로 메서드 추출 리팩토링이 필요한 코드인 ex1을 먼저 보면 print 메서드에서 우리가 출력하는 것은 테두리 출력과
내용 출력 두 부분으로 나누어질 수 있으며 심지어 테두리 출력 코드는 아예 같은 코드다.
출력을 하는 메서드 내에서도 출력할 내용에 따라 계산 수식등이 달라질 수 있는데 이중에는 분명히 중복되는 내용도 있을 것이다.
이런 중복 작업을 다시 한번 메서드로 묶는 작업을 통해 ex2와 같은 코드로 변경 될 수 있다.

우리가 객체로 만들것이 배너이고 배너는 위와 같이 border 출력, content 출력 기능을 가지고 있다.
Banner 객체는 아마 아래의 Banner.java 와 같이 작성 될 것이고
Baaner 를 이용한 어플리케이션은 Application.java 와 같이 작성 될 것이다.
##### Banner.java
```java
package example_6_extract_to_method;

public class Banner {
	private final String _content;

	public Banner(String _content) {
		super();
		this._content = _content;
	}

	public void print(int times) {
		// 테두리 출력
		System.out.print("+");
		for(int i = 0 ; i < _content.length(); i++) {
			System.out.print("-");
		}
		System.out.println("+");

		// 내용 출력
		for(int i = 0 ; i < times; i++) {
			System.out.println("|"+_content+"|");
		}

		// 테두리 출력
		System.out.print("+");
		for(int i = 0 ; i < _content.length(); i++) {
			System.out.print("-");
		}
		System.out.println("+");
	}
}
```

##### Application.java
```java
package example_6_extract_to_method;

public class Application {

	private static final int PRINTCOUNT = 3;

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Banner banner = new Banner("Hellow, World!!");
		banner.print(PRINTCOUNT);
	}

}
```

물론 ex2를 통해 알게 된 내용을 통해서 이미 Banner의 print를 다르게 작성할 수 있을것이다.
하지만 연습을 위해 다시 한번 작성해본다.

print 함수에서 처음 테두리 출력 부분을 먼저 보자. 여기에 필요한 입력은 없고 반환 해야할 변수도 없다.
##### 테두리(border) 출력(print)부분
```java
System.out.print("+");
for(int i = 0 ; i < _content.length(); i++) {
	System.out.print("-");
}
System.out.println("+");
```

테두리(border) 출력(print)은 print 함수가 호출된 후 처음 실행되고 내용을 출력한 다음에 같은 코드가 반복된다.
입력 변수는 매개변수로, 그리고 지역변수 중 적합한 리턴값이 있는지 판단했을때 딱히 보이지 않는다.
굳이 이 코드가 반환해야할 값이 있다면 print 의 성공여부 정도일 것이다. 하지만 어떤 입력도 없는 상태에서 큰 의미는 없다.

그렇다면 이 코드를 메서드로 변경한다면 반환할 값이 보이지 않기 때문에 반환형을 void 일것이고 Application 에서 Banner 만이 사용하는 기능이니
접근제어 지시자는 private 으로 설정하는 것이 적합하다. 그리고 입력받을 매게변수는 없다(_content는 객체의 속성).

메서드의 접근제어 지시자, 반황형, 매게변수까지 결정이 되었다. 코드의 내용은 변경이 없다.
그럼 메서드의 이름은 어떻게 지어야 할까?
위에서 계속 메서드는 행동이라고 이야기 했다. 일반적으로 메서드의 이름을 결정하는 방법은 행위(동사)+무엇(명사)로 결정한다.
메서드의 이름에는 공백이 들어갈 수 없기에 printborder 가 될것인데 별로 보기 안좋으며 읽기 힘들다.
그래서 보통 printBorder의 형태로 작성하게된다. _(underbar, underscore,밑줄)을 중간에 넣은 print_border, print_Border 등의 이름도 종종 있을 수 있는데
보통 _는 리소스 정의시 많이 사용하게 된다. coding style 은 혼자라면 편한대로 사용하면 되지만 이왕이면 혼자 하더라도 표준 규약을 따르는 것이 좋다.
이런 규약을 전부 알기 어려울 수 있는데 그럴 때는 lint 툴들을 이용한다.

메서드로 추출(extract)하는 방법을 봤는데 뭐든 너무 과하면 좋은 결과로 이어지지 않는다.
메서드 추출을 너무 많이 하게 될경우 객체내의 메서드 갯수가 증가하면서 관리가 어려워 질 수 있다.
간단한 기능들은 굳이 메서드로 추출까지 할 필요는 없다. 혹시 했다면 역으로 메서드 인라인화를 고려할 수 있다.
혹은 추출된 메서드들을 인터페이스등을 이용하여 그루핑하거나 하는식의 방법이 있을 수 있다.
