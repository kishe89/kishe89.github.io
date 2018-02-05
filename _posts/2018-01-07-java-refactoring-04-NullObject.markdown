---
layout: post
title:  "Java Refactoring Null Object"
date:   2018-01-07 20:39:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Java
---

1일 1포스팅의 5번째이다.
오늘은 본격적으로 예제와 내용을 보기전에 정리된 카탈로그 표를 먼저 본다.

##### 리팩토링 카탈로그(널 객체 도입)

|이름|널 객체 도입(Introduce Null Object)|
|---|---|
|상황|객체를 다룸|
|문제|null 확인이 너무 많음|
|해법|null을 나타내는 특별한 객체를 도입해 '아무것도 안 함' 이라는 처리를 함|
|결과|null 확인이 줄어듬|

### 방법
---
1. 널 객체 클래스 작성
   1. 널 객체 클래스 작성
       - 기존 클래스(null)을 확인하는 클래스의 하위 클래스로 작성
   2. isNull 메서드 작성
       - 기존 클래스는 false 반환
       - 널 객체 클래스는 true 반환
   3. 컴파일
2. null 치환하기
   1. null 을 널 객체로 치환
   2. null 확인을 isNull 메서드 호출로 치환
   3. 컴파일에서 테스트
3. 널 객체 클래스를 재정의해서 조건 판단 삭제하기
   1. isNull 메서드를 사용하는 조건 판단에서 다음과 같은 코드를 찾기
   ```java
   if (obj.isNull()) {
   	//TODO null 동
   } else {
   	obj.doSomething();
   }
   ```
   2. 널 객체 클래스에서 doSomething 메서드를 오버라이드함, 이 메서드에는 Null 동작을 작성함.
   3. 조건 판단 삭제
   ```java
   obj.doSomething();
   ```
   4. 컴파일해서 테스트

### 관련 항목
---
- 어서션 도입
- 널 객체 패턴
- 싱글톤 패턴
- 팩토리 메서드 패턴

널 객체의 도입으로 인한 코드 변화는 ex1 -> ex2로 볼 수 있다.
##### ex1
```java
if( _name != null){
    _name.display();
}
```
##### ex2
```java
_name.display();
```

일단 리팩토링 되지 않은 클래스 2개를(Person, Label) 만든다. 그리고 실행 진입점이 될 Main클래스를 만든다.

##### Person.java
```java
package example_5_nullobject;

import example_5_nullobject.Label;

public class Person {
	private final Label _name;
	private final Label _mail;
	public Person(Label _name, Label _mail) {
		super();
		this._name = _name;
		this._mail = _mail;
	}
	public Person(Label _name) {
		this(_name,null);
	}
	public void display() {
		if(_name != null) {
			_name.display();
		}
		if(_mail != null) {
			_mail.display();
		}
	}
	public String toString() {
		String result = "[ Person:";
		result += " name=";
		if(_name == null) {
			result += "\"(none)\"";
		} else {
			result += _name;
		}

		result += " mail=";
		if(_mail == null) {
			result += "\"(none)\"";
		} else {
			result += _mail;
		}
		result += "]";
		return result;
	}
}

```

##### Label.java
```java
package example_5_nullobject;

public class Label {
	private final String _label;

	public Label(String _label) {
		super();
		this._label = _label;
	}
	public void display() {
		System.out.println("display : "+_label);
	}
	public String toString() {
		return "\""+ _label +"\"";
	}
}
```

##### Main.java

```java
package example_5_nullobject;

public class Main {
	public static void main(String[] args) {
		Person[] people = {
				new Person(new Label("Alice"), new Label("alice@example.com")),
				new Person(new Label("Bobby"), new Label("bobby@example.com")),
				new Person(new Label("Chris")),
		};
		for(Person p : people) {
			System.out.println(p.toString());
			p.display();
			System.out.println();
		}
	}
}

```

Person클래스의 display와 toString 메서드를 보면 필드의 null여부를 체크하기위해 if( _name == null)형태처럼
보이는 if문들이 보인다.

처음에 ex1에서 ex2로의 변화를 Person코드를 통해 보도록 하겠다.

처음 해야할 일은 널 객체를 작성하는 것이다. 그리고 isNull메서드를 작성하고 컴파일 해서 테스트 한다.

##### Label.java(isNull메서드 추가)
```java
package example_5_nullobject;

public class Label {
	private final String _label;

	public Label(String _label) {
		super();
		this._label = _label;
	}
	public void display() {
		System.out.println("display : "+_label);
	}
	public boolean isNull() {
		return false;
	}
	public String toString() {
		return "\""+ _label +"\"";
	}
}

```

##### NullLabel.java
```java
package example_5_nullobject;

public class NullLabel extends Label{

	public NullLabel() {
		super("(none)");
		// TODO Auto-generated constructor stub
	}

	@Override
	public boolean isNull() {
		// TODO Auto-generated method stub
		return true;
	}

}

```

Label클래스에 isNull메서드를 추가하고 Label의 isNull이 호출 되려면 Label은 null이 아니므로 false를 반환하도록 작성한다.
NullLabel클래스의 isNull은 Label을 상속받아 Label의 isNull을 오버라이드하고 널 객체이니 true를 반환하도록 작성한다.

이상태로 컴파일을 해본다. 정상적으로 컴파일 될 것이다.

Null객체(NullLabel)를 만들었으니 Person의 null을 우리가 만든 Null객체로 치환하도록 한다.
x == null 형태의 null체크 코드는 _name.isNull(), _mail.isNull()메서드로 치환하도록 한다.

##### Person.java(null을 NullLabel로 치환, null체크를 isNull메서드로 치환)
```java
package example_5_nullobject;

import example_5_nullobject.Label;

public class Person {
	private final Label _name;
	private final Label _mail;
	public Person(Label _name, Label _mail) {
		super();
		this._name = _name;
		this._mail = _mail;
	}
	public Person(Label _name) {
		this(_name,new NullLabel());
	}
	public void display() {
		if(_name != null) {
			_name.display();
		}
		if(_mail != null) {
			_mail.display();
		}
	}
	public String toString() {
		String result = "[ Person:";
		result += " name=";
		if(_name.isNull()) {
			result += "\"(none)\"";
		} else {
			result += _name;
		}

		result += " mail=";
		if(_mail.isNull()) {
			result += "\"(none)\"";
		} else {
			result += _mail;
		}
		result += "]";
		return result;
	}
}
```

Main.Java에서 우리는 dummy데이터로 3개의 Person인스턴스를 생성했다.
alice, bobby, chris를 생성했는데 alice와 bobby는 mail주소를 가지고 있지만 chris는 mail이 없다.

##### ex3
```java
public Person(Label _name) {
		this(_name,new NullLabel());
	}
```
chris는 위 ex3 즉 Person의 생성자중 하나의 Label 객체만을 파라미터로 하는 생성자로 생성되었다.
_name은 정상적으로 셋될것이고 두번째 파라미터인 mail은 입력안되어서 우리가 NullLabel인스턴스를 셋해줬다.
chris는 _mail이 NullObject인 것이다.

컴파일 하게되면 우리가 toString에서 _mail.isNull()을 호출한 부분에서 true를 반환(NullObject이니까)
반환할 result에 "(none)"을 append할것이다.

일단 우리는 조건식에서 null을 삭제했다.
하지만 아직 ex2의 형태는 아니다.

조건문에서 null일 때의 동작을 보면 result += "\\"(none)\\"" 를 수행하는데 Person객체의 입장에서 중요한건
가지고 있는 Label객체의 값을 display하는 것이지 Label이 null일 때의 동작을 관리할 필요는 없을 것이다.
또한 Label객체가 본인의 값을 display하는 것처럼 NullLabel이 null일 때의 값을 display하는것이 아무 행위를 안하는 것보다 좋을것같다.
NullLabel에 Label의 display를 override하여 아래처럼 작성해보자.
##### Person.java(조건식 변경 및 null동작을 null객체에 이관)
```java
package example_5_nullobject;

import example_5_nullobject.Label;

public class Person {
	private final Label _name;
	private final Label _mail;
	public Person(Label _name, Label _mail) {
		super();
		this._name = _name;
		this._mail = _mail;
	}
	public Person(Label _name) {
		this(_name,new NullLabel());
	}
	public void display() {
		_name.display();
		_mail.display();
	}
	public String toString() {
		return "[ Person: name="+_name+" mail="+ _mail+"]";
	}
}
```
##### NullLabel(display함수 override해서 null동작 작성)
```java
package example_5_nullobject;

public class NullLabel extends Label{

	public NullLabel() {
		super("(none)");
		// TODO Auto-generated constructor stub
	}


	@Override
	public void display() {
		// TODO Auto-generated method stub

	}


	@Override
	public boolean isNull() {
		// TODO Auto-generated method stub
		return true;
	}

}

```
Person객체의 행동(화면에 필드의 내용을 출력(display)하고, 콘솔에 필드의 내용을 보여주는(toString)) 자체에
대한 코드만이 남게 되었다. 행위 자체를 읽는데 있어서 불편하게 만들던 검사 구문들이 제거 되어서 Person의 행동에 대해 더 쉽게 볼 수 있을것이다.
하지만 클래스가 늘어났으며 NullLabel객체자체 가하는 일이라곤 isNull호출시 true를 반환하는 것인데 chris와 같이 mail이 널인 객체의 생성마다
NullLabel객체의 새로운 인스턴스가 하나씩 추가된다.

NullLabel은 어떠한 상태도 가지지 않는다. 물론 Label의 이름만을 가지는 생성자로 "(none)"문자열을 _name에 가지게되지만
모든 NullLabel은 같은 값을 가지며 이 값은 어떠한 수정도 일어나지 않는다.

이럴 때 사용 할 수 있는 패턴이 싱글톤 패턴이다. 또한 싱글톤 객체를 가지고 오기위해 팩토리 메서드 패턴을 이용한다.

##### Person(NullLabel 생성부분 getInstance메서드로 변경)
```java
package example_5_nullobject;

import example_5_nullobject.Label;

public class Person {
	private final Label _name;
	private final Label _mail;
	public Person(Label _name, Label _mail) {
		super();
		this._name = _name;
		this._mail = _mail;
	}
	public Person(Label _name) {
		this(_name,NullLabel.getInstance());
	}
	public void display() {
		_name.display();
		_mail.display();
	}
	public String toString() {
		return "[ Person: name="+_name+" mail="+ _mail+"]";
	}
}
```

##### NullLabel(private한 singleton 인스턴스 필드 추가 및 반환 메서드 getInstance추가)
```java
package example_5_nullobject;

public class NullLabel extends Label{

	private static final NullLabel instance = new NullLabel();

	public static Label getInstance() {
		return instance;
	}

	public NullLabel() {
		super("(none)");
		// TODO Auto-generated constructor stub
	}


	@Override
	public void display() {
		// TODO Auto-generated method stub

	}


	@Override
	public boolean isNull() {
		// TODO Auto-generated method stub
		return true;
	}

}
```
NullLabel의 필드인 instance변수는 컴파일시 최초 NullLabel 인스턴스가 할당되고 그 이후 변경되지 않는다.
Person은 _name만을 가지는 경우에 이전에 new NullLabel로 항상 새로운 NullLabel인스턴스를 생성하던것에서
이미 생성되있는 싱글톤 객체인 instance를 참조하게 된다.
결론적으로 NullLabel함수는 여러개의 Person 인스턴스가 생성되더라도 하나만 생성되어 불필요한 메모리 사용을 방지 할 수 있다.

NullLabel자체가 상태를 가지지 않고 상태의 변경이 없기에 가능한 방법이며 singleton을 사용할 때는 상태의 공유가 일어나진 않는지 확인하고 사용하여야 한다.
또한 reflection등을 이용하여 해당 클래스를 동적으로 생성할 경우 원래 우리의 목적이었던 하나의 인스턴스가 아닌 여러개의 인스턴스가 생성될 수 있으니 체크하고 사용하여야한다.

클래스의 갯수가 많아진 것을 해결하기 위해선 inner class로 NullLabel객체를 만드는 방법이 있다.
일단 inner class로 만들기 전에 주의할 것은 OOP에서 결국에는 누군가(어떤 class)는 해야할 일을 우리는 각자의 역할과 책임에 맞게 분배하고 매핑하게 된다는 것이다.
즉 결국 어딘가에서는 행해야한다.
Person이 해야할 일이 별로 많지 않고 필드의 타입이 많지 않기때문에 지금 상황에서 NullLabel을 inner class로 정의하는것은 좋다.
하지만 이런 inner class가 많아진다면 오히려 코드의 구조에 악영향을 끼칠 수 있다. 또한 inner class로 작성시 다른 인스턴스에서 재사용이 불가 할 수 있다.

##### Label.java(NullLabel을 inner class로 작성 및 getInstance메서드 추가)
```java
package example_5_nullobject;

public class Label {
	private final String _label;

	public Label(String _label) {
		super();
		this._label = _label;
	}
	public void display() {
		System.out.println("display : "+_label);
	}
	public boolean isNull() {
		return false;
	}
	public String toString() {
		return "\""+ _label +"\"";
	}
	public static Label getInstance() {
		return NullLabel.getInstance();
	}
	private static class NullLabel extends Label{

		private static final NullLabel instance = new NullLabel();

		public static Label getInstance() {
			return instance;
		}

		public NullLabel() {
			super("(none)");
			// TODO Auto-generated constructor stub
		}


		@Override
		public void display() {
			// TODO Auto-generated method stub

		}


		@Override
		public boolean isNull() {
			// TODO Auto-generated method stub
			return true;
		}

	}

}

```

##### Person.java(NullLabel.getInstance()->Label.getInstance()로 변경)
```java
package example_5_nullobject;

import example_5_nullobject.Label;

public class Person {
	private final Label _name;
	private final Label _mail;
	public Person(Label _name, Label _mail) {
		super();
		this._name = _name;
		this._mail = _mail;
	}
	public Person(Label _name) {
		this(_name,Label.getInstance());
	}
	public void display() {
		_name.display();
		_mail.display();
	}
	public String toString() {
		return "[ Person: name="+_name+" mail="+ _mail+"]";
	}
}
```

NullLabel을 Label의 inner class로 작성함으로써 우리는 Person.java, Label.java, Main.java3개의 java파일과
좀 더 간결한 Person을 작성하였습니다.
팩토리 메서드 패턴을 이용하지 않고 NullLabel을 Label의 필드로 사용 할 수도 있습니다.

만약 위와 같이 기존 클래스에 수정을 가할 수 있는 상황이 아니라면 Null인터페이스를 만들어서 사용 할 수 있습니다.
Null인터페이스는 비어있으며 obj.isNull()대신 obj instanceof Null 표현식을 사용합니다.

이러한 인터페이스를 마커 인터페이스(Marker interface)라고 부르며 java.io.Serializable인터페이스 등이
마커 인터페이스입니다.

다음 포스팅은 코드의 반복적인 동작 및 너무 긴 코드를 메서드로 추출하는 방법에 대해 공부하고 올리겠습니다.
