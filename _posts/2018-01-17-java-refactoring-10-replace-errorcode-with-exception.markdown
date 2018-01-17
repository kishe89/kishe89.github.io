---
layout: post
title:  "Java Refactoring Replace Error code with Exception"
date:   2018-01-17 18:05:00
author: 김지운
cover:  "/assets/instacode.png"
---

소프트웨어는 에러(의도치 않은 상황)이 발생한다. 사실상 개발자의 제어하에 둘 수 없는 상황이 무조건적으로 생긴다.
그 상황에는 시스템의 파워가 내려가거나 하드웨어의 수명이 다하거나 또는 통신망의 문제 부터 응용소프트웨어의 경우는
돌아가는 Os 에서 다른 소프트웨어들로 인해 메모리가 부족하다거나 컴퓨팅 파워 부족으로 연산이 느려져 화면을 늦게 그리게 된다거나 하는등의
경우들이 에러 이다.
이것들은 위에서 이야기했듯이 본인의 노력만으로 제어가 가능한 부분이 아니다. 그럼에도 소프트웨어는 견고하게 동작해야한다.
하지만 아무리 견고하게 작성한다 하여도 문제는 발생한다. 이 때 프로그램이 그냥 죽는거보단 그래도 어떤 원인으로 지금 동작할 수 없는지
알려주고 다음에 이용하라는 내용을 나타내던지 해결될 시간등을 나타내는것이 좀 더 좋은 방법일 것이다.

이번 포스팅은 이런 처리를 어떻게 하면 좀 덜 복잡하게 코드상에서 구조적으로 나타낼 수 있는지에 대한 내용이다.


##### 리팩토링 카탈로그(에러 코드를 예외(Exception)으로 치환)

|이름|에러 코드를 예외로 치환|
|---|---|
|상황|에러 발생 사실을 에러 코드로 표현함|
|문제|정상처리와 에러 처리가 혼재함, 에러 코드 전파 처리가 넓은 범위에 있음|
|해법|에러 코드 대신에 예외를 사용함|

- 결과

  o 정상 처리와 에러 처리를 명확하게 분리 가능

  o 에러 코드를 반환해서 전파하지 않아도 됨

  o 에러 관련 정보를 예외 객체에 저장 가능

  x 에러 발생 부분과 에러 처리 부분이 분리되기 때문에 알기 어려워지는 경우도 있음

- 방법
1. 에러 종류에 맞는 적절한 예외 작성

    1. 예외 상태가 아니라면 예외를 사용하지 않음.
    2. 복구 가능한 에러라면 검사 예외 선택
    3. 복구 불가능한 에러 또는 프로그래머 실수로 인한 에러라면 비검사 예외 선택
    4. 컴파일
2. 메서드를 호출하는 쪽 변경(검사 예외)

    1. 호출하는 쪽에서 에러를 처리한다면 try-catch 추가
    2. 호출하는 쪽에서 에러를 처리하지 않는다면 thorws 로 처리 책임 전파
    3. 컴파일해서 테스트
- 관련항목

    - 예외를 조건 판정으로 치환(역 리팩토링)

에러 코드를 예외로 치환한다는 것이 에러를 처리하지 않는다는 것은 아니다.
무분별한 에러 코드의 남발로 인한 문제는 앞에서 우리가 분류 코드를 리팩토링하면서 이야기한
문제점들과 비슷한 문제점을 발생시키는데 개발자의 제어 밖에서 발생하므로 더욱 큰 문제를 야기할 수 있다.

##### ex1
```java
public ManagedArticle removeArticle() {
	if(list.size() != 0) {
		return new ManagedArticle(this.list.remove(list.size()-1),list.size()-1);
	}
	return new ManagedArticle(NullArticle.getInstance());
}
```

ex1 을 보자 java 에서 ArrayList 의 size 는 0 아래의 값을 가질 수 없다.
즉 0 이상의 값을 가져야 하는데 그렇지 않을 경우가 있다.
바로 인스턴스화 되지않은 상황이다.

물론 ex1 을 멤버 메서드로 가지고 있는 ArticleManager class 는 생성시 필드로 ArrayList 를 인스턴스로 만들게 되지만
실수로 빼먹는다거나 기능 추가도중 혹여라도 ArticleManager 의 list 필드를 통째로 바꾼다던가 할 때 위 상황은 충분히 실수로 인해서 발생할 수 있다.

##### ex2
```java
ArrayList<Article> list = null;
articleRequest(list);
articlemanager.setList(list);
```

ex2 를 보자. Application 에서는 articleRequest(ArrayList<Article> list) 메서드로
synchronous 하게 동작하는 서버에서 Article 들의 리스트를 반환받는 메서드라고 했을 때
통신문제로 인해 list 는 인스턴스화 되지 않을 수 있다.
이 때 ex1 을 실행한다면 list.size() 는 list 가 null 이므로 Null Object 를 Reference 한다는 NullPointerException 을 발생시킬 것이다.
물론 우리의 removeArticle 에는 그런 예외 상황에대한 어떠한 처리도 없으므로 프로그램은 다운될 것이다.
물론 이러한 상황은 피하도록 해야겠지만 수많은 데이터 변환, 비동기 처리가 일어나는 상황에서 모든 것을 처리할 수는 없을것이다.
분명히 우리는 실수 할 수있으며 이러한 실수와 제어 불가상황에 대한 최소한의 처리가 에러 코드를 처리하는 것인데
많은 에러들을 전부 각자의 에러 코드별로 처리한다는건 좋은 선택이 아니다. 일단 에러 코드들은 무수히 많아질 것이며
그로 인한 처리코드들로 인해 프로그램의 규모에 따라 기하급수적으로 코드는 비대해질 것이다.
또한 각 처리 부분을 찾는 것은 불가능에 가까워질 것이다.

##### ex3
```java
public ManagedArticle removeArticle() {
  if(list == null){
    return new ManagedArticle(NullArticle.getInstance());
  }
	if(list.size() != 0) {
		return new ManagedArticle(this.list.remove(list.size()-1),list.size()-1);
	}
	return new ManagedArticle(NullArticle.getInstance());
}
```
간단한 경우라면 ex3 과 같이 처리할 수 있을 것이다. 하지만 이 경우 우리는
실제 list 상에 삭제하려는 Article 이 없는 것과 list 자체가 없는 경우를 뭉쳐서 처리한 결과로
Article 이 없다는 내용은 분명히 동작은 올바르게 하였지만 모든 Article 이 이미 삭제되었거나 생성된적이 없어서 인 올바른 상황일것이다.
하지만 list 가 없다는 것은 정상적이지 않은 상황이다.
이 구분이 분명하지 않음으로 인해 이 코드에서의 문제 혹은 이 코드를 이용하는 코드에서는 이 반환값을 통해서 에러인지 동작은 올바르게 했는데 Article 이 없는 것인지
판단할 수 없다. 현재 코드는 null 에 대해서 이전에 사용하던 NullObject 를 이용하여 처리 되었는데
이를 아래와 같이 변경할 수 있다.
##### ex4
```java
public ManagedArticle removeArticle() {
  if(list == null){
    throw new IllegalArgumentException("list is null");
  }
	if(list.size() != 0) {
		return new ManagedArticle(this.list.remove(list.size()-1),list.size()-1);
	}
	return new ManagedArticle(NullArticle.getInstance());
}
```

이 때 우리가 던진 IllegalArgumentException 은 분명히 예외상황임을 이코드에서도 분명히 알 수 있고

##### ex5
```java
ArrayList<Article> list = null;
ArrayList<Article> copyCurrentList = articlemanager.getList();
articlemanager.setList(list);
try {
	articlemanager.removeArticle();
}catch(IllegalArgumentException e) {
	System.out.println(e.toString());
	articlemanager.setList(copyCurrentList);
}
articlemanager.printCurrentArticle();
```

이 코드를 이용하는 코드에서는 ex5 와 같이 다시 복원하는 노력을 하거나 혹은 사용자에게 어떠한 연유로 실패했으며 다시 articleRequest
를 호출한다는 내용등에 대한 처리를 할 수 있을 것이다.

예외를 처리하는게 호출한 곳이라면 위와 같이 try~catch 를 이용한 처리를 해주고
예외를 발생 시키는 곳은 에러 코드를 Exception 으로 치환하고 해당 Exception 을 throw 해주는데 해당 Exception에 대한 처리를 Exception이 발생한 곳에서
처리하지 않는다면 throws 를 붙여주게 되면 Exception 을 전파할 수 있고 이에대한 책임은 호출한 곳에 넘길 수 있다.

##### ex6
```java
public ManagedArticle removeArticle() throws NullPointerException {
		if(list.size() != 0) {
			return new ManagedArticle(this.list.remove(list.size()-1),list.size()-1);
		}
		return new ManagedArticle(NullArticle.getInstance());
	}
```
ex6 처럼 우리는 이곳에서 NullPointerException 이 발생할 수 있다는 걸 알고 있다.
그렇기에 발생시 호출한 곳에 NullPointerException 을 던진다는 걸 알려주며 전파할 수 있다.
모든 xxxException 들은 Exception 의 하위클래스들로 다형성을 이용하여 해당 내용에대한 부분들을 전달한다.
그렇기에 간혹 Exception 으로 뭉퉁그려서 처리한 코드들이 있는데 이는 결코 좋지 않다.
하나의 메서드에서 발생할 수 있는 예외들은 하나 이상일 수 있다. 그리고 그에 필요한 처리들은 각 기 다를 수 있다.
예를 들어서 통신 지연으로 인해 문제가 발생 했을 때 캐싱해놓은 데이터를 보여준다던가
화면을 그리는 도중 발생된 문제는 화면을 다시 그린다던가 하는 식의 처리가 이루어 질 수 있는데
이를 Exception 을 발생시키는 곳에서 그저 Exception 으로 전파시키면 처리하는 곳에서 문제가 생길 소지가 있고
코드의 가독성에도 좋지 않다.

예외를 만들때는 예외 또한 다형성을 이용하여 설계 하는 것이 추후 유연한 예외 처리가 가능해진다.

