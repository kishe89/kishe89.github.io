---
layout: post
title:  "Java Refactoring Hide Delegation"
date:   2018-01-27 11:56:00
author: 김지운
cover:  "/assets/instacode.png"
---

앞에서는 Inheritance 를 Delegaation 으로 치환하는 것에 대해 알아보았다.
잘못된 IS-A 에서 HAS-A 관계로 변경은 어찌보면 당연하다.
하지만 무엇이든 과하면 안좋은 것으로 이러한 위임된 필드들로 인해 문제가 생길 수 있는데
우리가 앞에서 IS-A 를 HAS-A 로 변경할 수 있었던 이유가 무엇일까 생각해보면 우리는 Random 클래스가
해당 기능을 하는 객체이며 내부에서 제공하는 기능들을 알고 있었기에 nextInt(int bound) 외에는 불필요하다는 결론을 내렸다.
그래서 Dice 가 Random 을 Inheritance 하는 것 보다는 위임 필드를 통해 Random 의 nextInt 를 호출하는 것으로 변경하였다.
만약 이러한 관계가 늘어나거나 깊이가 깊어진다 했을 때는 어떤 문제가 발생할 것인가?

수만은 위임필드들로 인해 Dice 는 많은 클래스들과의 관계가 생기게 되고 이는 관계에 의해 불필요한 의존성을 가지게 된다.




##### 리팩토링 카탈로그(대리자 은폐(Hide Delegation))

|이름|대리자 은폐|
|---|---|
|상황|클래스에 위임 관계가 있음|
|문제|클라이언트 클래스가 서버 클래스 뿐만아니라 대리 클래스까지 이용함|
|해법|서버클래스에 위임 메서드를 추가해서 클라이언트 클래스로부터 대리 클래스를 은폐|

- 결과

  o 클래스 사이의 불필요한 관계가 줄고 코드 수정이 쉬워짐

  x 위임하는 메서드를 작성해야 함

- 방법
1. 위임 메서드 작성

   1. 대리 클래스의 메서드에 대응하는 위임 메서드를 서버 클래스에 작성
   2. 클라이언트 클래스는 대리 클래스가 아닌 서버 클래스를 호출하도록 변경
   3. 컴파일해서 테스트
2. 대리 클래스 은폐

   1. 서버 클래스에 있는 대리 클래스의 게터 메서드 삭제
   2. 컴파일해서 테스트

- 관련항목

    - 중계자 제거

      대리자 은폐 결과 서버 클래스의 메서드가 모두 위임 메서드가 되었다면 서버 클래스를 삭제 가능

    - 클래스 인라인화

      대리 클래스가 별다른 일을 하지 않는다면 대리 클래스는 서버 클래스에 인라인화 가능


##### Application
```java
package example_15_hide_delegation;

import java.io.IOException;
import java.util.Enumeration;

public class Application {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		try {
			AddressFile file = new AddressFile("address.txt");
			file.getDatabase().set("alice", "alice@gmail.com");
			file.getDatabase().set("bobby", "bobby@gmail.com");
			file.getDatabase().set("anna", "anna@gmail.com");
			file.getDatabase().update();

			Enumeration<?> e = file.names();
			while(e.hasMoreElements()) {
				String name = (String)e.nextElement();
				String mail = file.getDatabase().get(name);
				System.out.println("name = "+name+", mail = "+mail);
			}
		}catch(IOException e) {
			e.printStackTrace();
		}

	}

}
```
##### AddressFile
```java
package example_15_hide_delegation;

import java.util.Enumeration;

public class AddressFile {
	private final Database database;

	public AddressFile(String filename) {
		super();
		this.database = new Database(filename);
	}
	public Database getDatabase() {
		return this.database;
	}
	public Enumeration names() {
		return database.getProperties().propertyNames();
	}
}
```
##### Database
```java
package example_15_hide_delegation;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Properties;

public class Database {
	private final Properties properties;
	private final String filename;

	public Database(String filename) {
		// TODO Auto-generated constructor stub
		this.filename = filename;
		this.properties = new Properties();
		try {
			properties.load(new FileInputStream(filename));
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	public void set(String key, String value) {
		properties.setProperty(key, value);
	}
	public String get(String key) {
		return properties.getProperty(key, null);
	}
	public void update() throws IOException{
		properties.store(new FileOutputStream(filename), "");
	}
	public Properties getProperties() {
		return this.properties;
	}
}
```

위 예제는 자바로 배우는 리팩토링 입문(길벗 출판, 히로 유키시 지음,서수환 옮김)에서 가져온 예제이다.

Application 을 클라이언트, AddressFile 을 서버, Database 클래스를 대리 라고 한다.

클라이언트를 보면 서버와 대리를 전부 다 호출한다.
일단 서버에서 대리자를 호출하는 부분을 제거해본다.

클라이언트에서 서버.getDatabase 를 통해 set,get,update 를 해야했던 이유는 서버가 대리는 가지고 있지만 대리의 행동을 대신 호출할 위임 메서드가 없었기 때문이다.
대리 의 set,get,update 를 호출할 set,get,update 를 서버에 추가한다.
##### AddressFile
```java
package example_15_hide_delegation;

import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Enumeration;

public class AddressFile {
	private final Database database;

	public AddressFile(String filename) {
		super();
		this.database = new Database(filename);
	}
	public Database getDatabase() {
		return this.database;
	}
	public Enumeration names() {
		return database.getProperties().propertyNames();
	}
	public void set(String key, String value) {
		database.set(key, value);
	}
	public String get(String key) {
		return database.get(key);
	}
	public void update() throws IOException{
		database.update();
	}
}
```
서버에 추가를 하게 되면 위와 같이 변경이 될 것이다.
이 상태에서는 서버.getDatabase 를 클라이언트에서 제거하고 서버.set, 서버.get, 서버.update 를 호출하도록 변경하고 컴파일해서 테스트해본다.
##### Application
```java
package example_15_hide_delegation;

import java.io.IOException;
import java.util.Enumeration;

public class Application {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		try {
			AddressFile file = new AddressFile("address.txt");
			file.set("alice", "alice@gmail.com");
			file.set("bobby", "bobby@gmail.com");
			file.set("anna", "anna@gmail.com");
			file.update();

			Enumeration<?> e = file.names();
			while(e.hasMoreElements()) {
				String name = (String)e.nextElement();
				String mail = file.get(name);
				System.out.println("name = "+name+", mail = "+mail);
			}
		}catch(IOException e) {
			e.printStackTrace();
		}

	}

}
```
클라이언트는 위처럼 변경될것이다. 그럼 한가지 필요없는 코드가 더있다.
서버에서 우리는 이전에 getDatabase 를 통해서 대리를 받아서 대리의 메서드를 호출했지만 지금은
서버에 위임메서드를 만들어 서버에서 대리의 메서드를 호출하도록 하였다.
그러므로 클라이언트는 대리에 대해서 신경쓸 필요도 없고 서버에서도 대리를 반환하는 코드는 필요가 없다.

서버의 getDatabase 메서드를 삭제하고 컴파일 해서 테스트한다.
##### AddressFile
```java
package example_15_hide_delegation;

import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Enumeration;

public class AddressFile {
	private final Database database;

	public AddressFile(String filename) {
		super();
		this.database = new Database(filename);
	}
	public Enumeration names() {
		return database.getProperties().propertyNames();
	}
	public void set(String key, String value) {
		database.set(key, value);
	}
	public String get(String key) {
		return database.get(key);
	}
	public void update() throws IOException{
		database.update();
	}
}
```
정상 동작하는 것을 볼 수 있다.

이러게 하여 Application 과 Database 클래스간의 관계는 끊어졌다.
여기 까지만 해도 대리 클래스의 은폐에 대해서는 설명이 되지만 한번 더 해보자.
아직 이 코드에는 방금전에 끊어냈던 관계와 같은 관계를 가지는 부분이 있다.
서버 코드를 보면 Database 와 Properties 클래스 두개를 사용중이고 Properties 는 대리 클래스이다.

database.getProperties().propertyNames()를 통해서 대리 클래스의 메서드에 접근하고 있다.

이 부분의 관계를 제거해보자 순서는 똑같다.
AddressFile 을 클라이언트, Database 를 서버, Properties 를 대리라 하겠다.

일단 서버 에게 서버.Properties.propertyNames()와 대응되는 위임메서드 keys()를 작성한다.(메서드 이름은 변경)
##### Database
```java
package example_15_hide_delegation;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Enumeration;
import java.util.Properties;

public class Database {
	private final Properties properties;
	private final String filename;

	public Database(String filename) {
		// TODO Auto-generated constructor stub
		this.filename = filename;
		this.properties = new Properties();
		try {
			properties.load(new FileInputStream(filename));
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	public Enumeration keys() {
		return properties.propertyNames();
	}
	public void set(String key, String value) {
		properties.setProperty(key, value);
	}
	public String get(String key) {
		return properties.getProperty(key, null);
	}
	public void update() throws IOException{
		properties.store(new FileOutputStream(filename), "");
	}
	public Properties getProperties() {
		return this.properties;
	}
}
```
이렇게 변경 되면 클라이언트에서는 database.getProperties().propertyNames(); 대신

database.keys() 를 호출하게 되면 된다.

##### AddressFile
```java
package example_15_hide_delegation;

import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Enumeration;

public class AddressFile {
	private final Database database;

	public AddressFile(String filename) {
		super();
		this.database = new Database(filename);
	}
	public Enumeration names() {
		return database.keys();
	}
	public void set(String key, String value) {
		database.set(key, value);
	}
	public String get(String key) {
		return database.get(key);
	}
	public void update() throws IOException{
		database.update();
	}
}
```
그러면 우리는 또 한번 대리 클래스를 리턴하는 메서드가 필요없어진다.
서버의 getProperties 메서드를 제거한다.

##### Database
```java
package example_15_hide_delegation;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Enumeration;
import java.util.Properties;

public class Database {
	private final Properties properties;
	private final String filename;

	public Database(String filename) {
		// TODO Auto-generated constructor stub
		this.filename = filename;
		this.properties = new Properties();
		try {
			properties.load(new FileInputStream(filename));
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	public Enumeration keys() {
		return properties.propertyNames();
	}
	public void set(String key, String value) {
		properties.setProperty(key, value);
	}
	public String get(String key) {
		return properties.getProperty(key, null);
	}
	public void update() throws IOException{
		properties.store(new FileOutputStream(filename), "");
	}
}
```
컴파일을 해서 테스트 해본다. 정상적으로 동작을 하게 된다.

2번의 대리자 은폐 리팩토링을 통해서 우리는 각각의 대리자 응답 메서드를 제거 했으며
각각의 클라이언트 역할을 하던 곳에 있던 의존성도 각 서버만이 가지도록 하였다.

이는 지금 당장은 하지 않아도 되는 리팩토링을 수 있다. 하지만 리팩토링을 하는 이유는 후에 발생할 구조적인 변경등에 대해
유연하게 대처하기 위해 좀 더 구조적으로 나은 코드를 작성하는 것이다.

클라이언트에서 여러 클래스에 의존적일 경우 하나의 수정을 통해 여러 클래스에 미칠 위험을 미연에 방지 할 수 있는 방법이므로
모든 곳에 대리자를 은폐할 필요는 없지만 적정선까지의 은폐는 필요하다.

하지만 이러한 은폐를 하여 관계를 끊었지만 이는 다시 위임메서드에게 해당 관계에 대한 책임을 떠넘긴것으로
위임메서드가 늘어나게 된다.

이러한 위임메서드만을 가진 클래스를 중계자라고 하는데 너무 위임메서드가 많고 하는일이 없다면
중계자를 제거하여 다시 관계를 갖도록 하는 것또한 클래스간의 구조를 개선하는 일이다.
객체지향은 분명 좋은 개념이지만 모든 코드를 전부 객체화 하겠다하는 것은 좋지 않은 생각이다.
예로 System.out.println 을 클라이언트에서 호출하는 것이 좋지 않다고 생각하지 않을것이다.

고작 출력 몇줄 하는 코드를 굳이 객체로 매핑하는 것은 오히려 코드를 망가뜨리는 일이다.
