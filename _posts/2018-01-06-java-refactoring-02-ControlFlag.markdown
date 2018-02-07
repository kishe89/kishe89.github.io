---
layout: post
title:  "Java Refactoring Control Flag"
date:   2018-01-06 18:52:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Java
---

1일 1포스팅의 3번째이다.

플래그(Flag)란 원래 '깃발'이란 뜻인데, 프로그래밍에서는 '상태를 기록하고 처리 흐름을 제어하기 위한 boolean 변수'를 의미합니다.
제가 고등학생 때 AVR, 8051, PIC 칩 제어용 프로그램을 작성할 때 정말 많이 사용했던 기억이 나네요.

busy(LCD, memory, etc) flag, 그 외 프로그램의 흐름을 제어할 목적으로 정말 많은 플래그들을 만들어서 사용했었습니다.

물론 필요하기에 만들어진 것이고 쓰는 것 자체가 나쁜건 아닙니다. 하지만 과하면 없는 것만 못한 경우들이 생깁니다.

boolean은 true, false를 나타내는 정말 단순한 타입의 변수입니다.

예를 들어 보겠습니다.
##### ex1
```java
package example_3_controlflag;

public class Application{

	public static void main(String args[]) {
		boolean IS_APPLICATION_PLAYING = true;
		int CONDITION = 101;
		int count = 1;
		int sum = 0;
		while(IS_APPLICATION_PLAYING) {
			if(count<CONDITION) {
				sum += count;
			}else {
				IS_APPLICATION_PLAYING = false;
			}
			count++;
		}
		System.out.println("sum = "+sum);
	}
}

```

ex1은 단순히 1~100까지의 합을 구하는 프로그램입니다. 여기서 IS_APPLICATION_PLAYING이 제어 플래그입니다.

물론 지금 이 프로그램은 정말 조그만 기능을 하는 프로그램입니다. 그렇기에 제어플래그의 값을 변경하는 부분은 else문
단 한부분입니다.

일단은 정말 필요한 상황을 설명하기 전에 제어 플래그를 삭제한다는게 어떤 행위인지 보도록 하겠습니다.

ex1의 제어플래그인 IS_APPLICATION_PLAYING을 제거해서 ex2를 만들어보겠습니다.
##### ex2
```java
package example_3_controlflag;

public class Application{

	public static void main(String args[]) {
		int CONDITION = 101;
		int count = 1;
		int sum = 0;
		while(true) {
			if(count<CONDITION) {
				sum += count;
			}else {
				break;
			}
			count++;
		}
		System.out.println("sum = "+sum);
	}
}

```

자 어플리케이션의 지속적인 실행을 관리하는 while은 그저 계속 실행중입니다.

단 count가 CONDITION과 같아지면 break로 인해 루프를 탈출하게 될 것입니다. 다시 이야기하지만 리팩토링은 외부에서 보는 동작의 변화없이 코드의 구조를 개선하는 행위입니다.

자 우리의 Application의 종료조건은 count<CONDTION 한가지밖에 없습니다.

이것만으론 왜 제어플래그 삭제를 해야하는지 잘 와닿지 않습니다. 굳이 리팩토링 해야되나 싶기도 합니다.

우리가 자주 하는 게임을 예로 생각해보겠습니다.

게임클라이언트는 사용자가 실행을 시킨 시점부터 많은 이벤트를 체크하며 그에 따른 반응을 하게됩니다.

어떤 키들은 클릭이벤트에 따라서 우리의 IS_PLAYING_APPLICATION을 false로 바꿀 수 있을 것이며
네트워크 오류 혹은 메모리 할당 오류등 다양한 시스템 오류까지 모두 IS_PLAYING_APPLICATION이라는 제어플래그를
이용하여 전체 어플리케이션의 생명주기를 관리한다면 그 코드의 흐름이 눈에 보일까 생각해봅시다.

또한 굳이 사용하지 않아도 되는 변수를 사용하여 불필요한 코드 라인수 증가를 발생시킵니다.

##### ex3
```java
boolean flag = true;
if(flag){
  //TODO
  return flag;
}else{
  //TODO
  return flag;
}

```

##### ex4
```java
boolean flag = true;
if(flag){
  //TODO
}else{
  //TODO
}
return flag;
```

ex3과 같은 형태의 코드 형태도 존재 할 수 있는데 이 코드의 문제를 생각 해보자.

결국 flag 는 true아니면 false 이며 이에 따라 모두 return flag를 호출하게 된다.

이러한 경우는 해당 스코프를 벗어나는 출구를 공통된 하나의 출구로 묶는것이 좀 더 나은 표현과 가독성을 가질 수 있다.

##### ex5
```java
private boolean isEmpty(ArrayList arg) {
		boolean flag = false;
		if(arg.size()==0) {
			flag = true;
		}else {
			flag = false;
		}
		return flag;
}
```

ex5와 같은경우도 생각해보자 바꿔 본다면 ex6와 같이 변경될 것이다.

##### ex6
```java
private boolean isEmpty(ArrayList arg) {
		if(arg.size()==0) {
			return true;
		}
		return false;
}
```

굳이 모든 참 거짓에 이름을 붙일 필요는 없다. 오히려 true, false로만 표현하는 것이 간결하고 좋을 때도 있다.
또한 제공되는 API들을 잘 이용하는 것도 불필요한 제어플래그를 제거하는데 도움이 된다.

예를들어 ArrayList에서 제공하는 isEmpty()등의 함수들은 메서드의 이름 자체로 이미 모든것을 표현하고 있다.
굳이 EmptyFlag와 같은 변수들을 만들어서 체크할 필요가 없다.

다음은 주저리 주저리 떠드는 주석을 제거할 수 있는 리팩토링 방법에 대해서 보겠습니다.
