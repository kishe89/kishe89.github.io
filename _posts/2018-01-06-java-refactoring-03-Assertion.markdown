---
layout: post
title:  "Java Refactoring Assertion"
date:   2018-01-06 18:57:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Java
---

1일 1포스팅의 4번째이다.

Assertion은 우리의 프로그램에 필요한 조건들에 대한 검증을 뜻합니다.

예를 들어서 우리의 java프로그램이 ex1처럼 arguments로 값을 받아야하는데 꼭 하나 이상은 받아야 하는 프로그램이 있다.

##### ex1
```java
package example_4_assertion;

import java.util.ArrayList;

public class Application{

	public static void main(String args[]) {
		ArrayList<String> dummyList = new ArrayList<>();
		for(String item:args) {
			dummyList.add(item);
		}
		print(dummyList);
	}

	private static void print(ArrayList<String> arg) {
		for(String item: arg) {
			System.out.println(item);
		}
	}
}
```

ex1에 arguments로 값을 받아야하는데 꼭 하나 이상은 받아야 한다는게 지금은 없어서 코드만 봐서는 알 수 없다.

이를 알리기 위해 우리는 ex2처럼 코드에 주석을 달 수 있을 것이다.

##### ex2
```java
package example_4_assertion;

import java.util.ArrayList;

public class Application{

	public static void main(String args[]) {
		/**
		 *실행시에 argument를 꼭 전달해주세요
		 */
		ArrayList<String> dummyList = new ArrayList<>();
		for(String item:args) {
			dummyList.add(item);
		}
		print(dummyList);
	}

	private static void print(ArrayList<String> arg) {
		for(String item: arg) {
			System.out.println(item);
		}
	}
}
```

일단 코드를 본다는 전제하에 의미를 전달을 하긴 했다. 하지만 argument가 전달이 되건 안되건 실행이 될 것이다.

또한 코드를 봐야만 알 수 있다.
그럼 코드를 안봐도 알 수 있게 하려면 어떻게 해야할까?

##### ex3
```java
package example_4_assertion;

import java.util.ArrayList;

public class Application{

	public static void main(String args[]) throws Exception {
		/**
		 *실행시에 argument를 꼭 전달해주세요
		 */
		if(args.length == 0) {
			throw new Exception("실행시에 argument를 꼭 전달해주세요");
		}
		ArrayList<String> dummyList = new ArrayList<>();
		for(String item:args) {
			dummyList.add(item);
		}
		print(dummyList);
	}

	private static void print(ArrayList<String> arg) {
		for(String item: arg) {
			System.out.println(item);
		}
	}
}
```

ex3처럼 args가 전달안된 경우 Exception을 발생시켜주면 코드를 보지 않더라도 실행시에 발생하는 Exception으로 인해
코드를 사용하는 이에게 의미와 필요한 것을 전달할 수 있을것이다.

하지만 좀 더 이 필요조건이 시스템상에서 발생한 예외가 아닌 사용자에게 의미 전달만을 위한 코드 및 문서로의 역할을 할 수 없을까?

그 방법중 하나가 Assertion을 도입하는 것이다.

##### ex4
```java
package example_4_assertion;

import java.util.ArrayList;

public class Application{

	public static void main(String args[]) throws Exception {
		/**
		 *실행시에 argument를 꼭 전달해주세요
		 */
		assert isNotEmpty(args);
		ArrayList<String> dummyList = new ArrayList<>();
		for(String item:args) {
			dummyList.add(item);
		}
		print(dummyList);
	}

	private static boolean isNotEmpty(String[] args){
		if(args.length == 0) {
			return false;
		}
		return true;
	}

	private static void print(ArrayList<String> arg) {
		for(String item: arg) {
			System.out.println(item);
		}
	}
}
```

ex4에는 함수 isNotEmpty를 만들었고
isNotEmpty는 args가 비어있으면 false data가 있으면 true를 반환한다.

이 함수를 assertion에 이용하면 argument를 입력 안할 시
assertion exception이 발생하게 된다.

이는 필요 조건 구문이 충족 안되었다는 내용으로만 사용자에게 전달 될 수있다.

물론 Exception을 확장하여 Custom Exception을 이용한 내용 출력을 통해 의미전달을 하는게 더 보기 좋은 사람도 있고 할 수 있다.
하지만 위에서 이야기 했듯이 시스템에서의 예외와 코드상 스펙에서 필요한 것이 이것이다를 나타내는건 다른 문제라고 생각된다.

또한 assertion을 java에서만 사용하는 것이 아니고 더 나아가서 testcase를 작성시에도 많이 사용게 된다.
주석을 아예 대채할 수 있냐에 대해서는 아니다.
javadoc과 같은 유용한 주석들이 있다.

단 프로그램의 동작에대해 필요조건이 있고 그 필요조건이 무엇인지 실행시점에 사용자에게 알려주는데 있어서 도움이 된다는 것이다.

추가로 java 명령어는 기본적으로 assertion이 비활성화 되어있다.
그렇기 때문에 ex5와 같이 실행시 -ea 옵션으로 지정해야한다.
##### ex5
```
java -ea Application
```

assertion 옵션에 대한 자세한 내용은 [Assertion docs][Assertion docs]를
참조한다.

[Assertion docs]:https://docs.oracle.com/javase/8/docs/technotes/guides/language/assert.html
