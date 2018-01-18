---
layout: post
title:  "Java Refactoring Replace Constructor with Factory Method"
date:   2018-01-18 17:32:00
author: 김지운
cover:  "/assets/instacode.png"
---

일반적으로 클래스를 생성할 때 우리는 new Object() 를 이용하여 클래스를 생성한다.
이 때 Object 에는 생성할 클래스의 이름을 적어주게 되는데 이를 클래스명이 하드코딩 되어있다고 한다.
이 장에서 나올 내용은 앞에서 이미 많이 사용한 내용이다.
팩토리 메서드를 간단히 이야기하면 생성자(Constructor)를 팩토리 메서드(Factory method)로 추상화 한 것이다.
생성할 때 생성자를 호출하여 생성하는 것이 아니라 생성자를 호출하여 생성된 인스턴스를 반환하는 Factory Method 를 호출하여 생성하는 것이다.
이를 통해 얻을 수 있는 장점은 객체의 생성시점에 객체의 타입(클래스) 를 팩토리 메서드 내부에서 결정되게 되는데
이는 반환하는 타입을 이용하여 Factory method 를 호출하는 쪽에서는 그저 Article 을 생성하는 하나의 동작으로 모든 Article 을 생성할 수 있는 것이다.

##### 리팩토링 카탈로그(생성자를 팩토리 메서드로 치환)

|이름|생성자를 팩토리 메서드로 치환|
|---|---|
|상황|인스턴스를 생성함|
|문제|생성하고 싶은 인스턴스가 속한 실제 클래스를 클라이언트에는 숨기고 싶음|
|해법|생성자를 팩토리 메서드로 치환함|

- 결과

  o 어느 클래스 인스턴스를 생성할지를 팩토리 메서드 안에서 정할 수 있음

  o 생성한 인스턴스를 변경해도 클라이언트 쪽은 변경하지 않아도 됨

  x 추상도가 너무 올라가면 코드가 오히려 어려워짐

- 방법
1. 팩토리 메서드 작성

    1. 팩토리 메서드 작성

        - 팩토리 메서드 안에서는 현재 생성자를 호출
    2. 팩토리 메서드 호출

        - 클라이언트에서 생성자를 호출하는 부분을 수정해서 팩토리 메서드를 호출하도록 함
    3. 컴파일해서 테스트
2. 생성자 숨기기

    1. 생성자를 private 로 만든다.

        - 그러면 생성자를 클라이언트에서 실수로 호출하는 걸 막을 수 있어서 팩토리 메서드 호출이 보장됨.
    2. 컴파일
- 관련항목

    - 분류 코드를 하위 클래스로 치환

      생성자를 팩토리 메서드로 치환을 한 후에 이 리팩토링을 할 수 있음.


앞에서 계속 Article 을 리팩토링 했는데 다시 처음으로 돌아가 보자.

##### Application
```java
package example12_replace_constructor_factory;

public class Application {


	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Article article = new Article();
	}
}
```

##### Article
```java
package example12_replace_constructor_factory;

public class Article {
	private String title;
	private String content;
	private String password;
	private Author author;
	private PostedAt postedAt;
	public static final int MYARTICLE = 0;
	public static final int SHAREDARTICLE = 1;
	public static final int ADARTICLE = 2;
	private int type;

	public Article() {
		super();
	}

	public Article(String title, String content, String authorName, String authorMail,int type) {
		super();
		this.title = title;
		this.content = content;
		this.author = new Author(authorName, authorMail);
		this.postedAt = new PostedAt();
		this.type = type;
	}

	public void print() {
		switch(type) {
		case MYARTICLE:
			System.out.println("MyArticle\n - title : "+this.getTitle()
			+"\n- content : "+this.getContent()
			+"\n- authorName : "+this.getAuthor().getAuthorName()
			+"\n- authorMail : "+this.getAuthor().getAuthorName()
			+"\n- CreatedAt : "+this.getPostedAt().getCreatedAt()
			+"\n- UpdatedAt : "+this.getPostedAt().getUpdatedAt()+"\n");
			return;
		case SHAREDARTICLE:
			System.out.println("SharedArticle\n - title : "+this.getTitle()
			+"\n- content : "+this.getContent()
			+"\n- authorName : "+this.getAuthor().getAuthorName()
			+"\n- authorMail : "+this.getAuthor().getAuthorName()
			+"\n- CreatedAt : "+this.getPostedAt().getCreatedAt()
			+"\n- UpdatedAt : "+this.getPostedAt().getUpdatedAt()+"\n");
			return;
		case ADARTICLE:
			System.out.println("AdArticle\n - title : "+this.getTitle()
			+"\n- content : "+this.getContent()
			+"\n- authorName : "+this.getAuthor().getAuthorName()
			+"\n- authorMail : "+this.getAuthor().getAuthorName()
			+"\n- CreatedAt : "+this.getPostedAt().getCreatedAt()
			+"\n- UpdatedAt : "+this.getPostedAt().getUpdatedAt()+"\n");
			return;
		}
	};
	public String getTitle() {
		return title;
	}
	public void setTitle(String title) {
		this.title = title;
	}
	public String getContent() {
		return content;
	}
	public void setContent(String content) {
		this.content = content;
	}
	public String getPassword() {
		return password;
	}
	public void setPassword(String password) {
		this.password = password;
	}

	public ImmutableAuthor getAuthor() {
		return author;
	}
	public PostedAt getPostedAt() {
		return postedAt;
	}


	public int getType() {
		return type;
	}

	public boolean isNull() {
		return false;
	}

}
```

Application 에서 우리는 Article 의 생성자를 호출하여 Article 을 생성하였다.
하지만 Article 이 MyArticle, SharedArticle, AdArticle 로 각각 print 동작이 다른 상황에서
type 에 따라 다른 Article 로 생성하기 위해서는 어떻게 해야할까?
생성자를 호출하는 곳에서 검사구문을 통해 각각의 생성자를 호출해야하는 번거로움이 생길 것이다.
만약 이게 라이브러리라고 하였을 때 그리고 내가 그 라이버르리의 사용자라고 했을 때 Article.print() 로 동작하는 것을 원하지
MyArticle.print(), SharedArticle.print() 를 생각하고 싶지는 않을 것이다.
즉 생성을 어떻게 해야하고 하는 것보단 사용하는데 더 초점을 맞추기 때문에 쓰기 싫은 라이브러리가 될 것이다.

그럼 Constructor 를 Factory method 로 치환 해보자.
앞에서 이야기 했듯이 Factory method 는 단지 생성자를 호출하고 호출된 생성자가 반환하는 인스턴스를 반환하는 method 이다.

##### Article
```java
package example12_replace_constructor_factory;

public class Article {
	private String title;
	private String content;
	private String password;
	private Author author;
	private PostedAt postedAt;
	public static final int MYARTICLE = 0;
	public static final int SHAREDARTICLE = 1;
	public static final int ADARTICLE = 2;
	private int type;
	public static Article create(String title, String content, String authorName, String authorMail,int type) {
		return new Article(title, content, authorName, authorMail, type);
	};
	public Article() {
		super();
	}

	public Article(String title, String content, String authorName, String authorMail,int type) {
		super();
		this.title = title;
		this.content = content;
		this.author = new Author(authorName, authorMail);
		this.postedAt = new PostedAt();
		this.type = type;
	}
  ...
}
```

Article 을 만들어주는 create 라는 Factory method 를 위와 같이 추가한다.
이제 우리는 new Article(), new Article(String,String,String,String,int)
그리고 Article.create(String title, String content, String authorName, String authorMail,int type) 라는 3가지 방법으로 생성할 수 있게 되었다.

하지만 우리가 원하는 생성 방법은 create 를 위해 생성하는 것을 원하며 굳이 Article 의 생성자가 밖으로 공개되야할 이유는 없다.
Article 의 생성자를 protected 으로 변경하여 동일 패키지에서만 호출 가능하도록 변경하자.

##### Article
```java
package example12_replace_constructor_factory;

public class Article {
	private String title;
	private String content;
	private String password;
	private Author author;
	private PostedAt postedAt;
	public static final int MYARTICLE = 0;
	public static final int SHAREDARTICLE = 1;
	public static final int ADARTICLE = 2;
	private int type;
	public static Article create(String title, String content, String authorName, String authorMail,int type) {
		return new Article(title, content, authorName, authorMail, type);
	};
	protected Article() {
		super();
	}

	protected Article(String title, String content, String authorName, String authorMail,int type) {
		super();
		this.title = title;
		this.content = content;
		this.author = new Author(authorName, authorMail);
		this.postedAt = new PostedAt();
		this.type = type;
	}
  ...

}
```
이렇게 되면 Article 외부에서 Article 을 생성할 방법은 Article 의 Factory method 인 create 메서드를 호출하는 수 밖에 없다.
자 그러면 Article 의 type 을 subclass 를 이용해 치환해보자.

1. Article 을 abstract class 로 수정하고 print method 또한 abstract method 로 수정한다.
2. Article 을 상속 받는 MyArticle, SharedArticle, AdArticle 을 작성한다.
3. Article 의 switch 문에 있던 각각의 print 동작을 각 클래스로 이동한다.
4. Article 의 Factory method(create) 에 type 별 생성 구문을 작성한다.
##### MyArticle
```java
package example12_replace_constructor_factory;

public class MyArticle extends Article{

	protected MyArticle() {
		super();
	}
	protected MyArticle(String title, String content, String authorName, String authorMail,int type) {
		super(title, content, authorName, authorMail, type);
	}
	@Override
	public void print() {
		// TODO Auto-generated method stub
		System.out.println("MyArticle\n - title : "+this.getTitle()
		+"\n- content : "+this.getContent()
		+"\n- authorName : "+this.getAuthor().getAuthorName()
		+"\n- authorMail : "+this.getAuthor().getAuthorName()
		+"\n- CreatedAt : "+this.getPostedAt().getCreatedAt()
		+"\n- UpdatedAt : "+this.getPostedAt().getUpdatedAt()+"\n");
	}

}
```
##### SharedArticle
```java
package example12_replace_constructor_factory;

public class SharedArticle extends Article{

	protected SharedArticle() {
		super();
	}
	protected SharedArticle(String title, String content, String authorName, String authorMail,int type) {
		super(title, content, authorName, authorMail, type);
	}
	@Override
	public void print() {
		// TODO Auto-generated method stub
		System.out.println("SharedArticle\n - title : "+this.getTitle()
		+"\n- content : "+this.getContent()
		+"\n- authorName : "+this.getAuthor().getAuthorName()
		+"\n- authorMail : "+this.getAuthor().getAuthorName()
		+"\n- CreatedAt : "+this.getPostedAt().getCreatedAt()
		+"\n- UpdatedAt : "+this.getPostedAt().getUpdatedAt()+"\n");
	}
}
```
##### AdArticle
```java
package example12_replace_constructor_factory;

public class AdArticle extends Article{
	protected AdArticle() {
		super();
	}
	protected AdArticle(String title, String content, String authorName, String authorMail,int type) {
		super(title, content, authorName, authorMail, type);
	}
	@Override
	public void print() {
		// TODO Auto-generated method stub
		System.out.println("AdArticle\n - title : "+this.getTitle()
		+"\n- content : "+this.getContent()
		+"\n- authorName : "+this.getAuthor().getAuthorName()
		+"\n- authorMail : "+this.getAuthor().getAuthorName()
		+"\n- CreatedAt : "+this.getPostedAt().getCreatedAt()
		+"\n- UpdatedAt : "+this.getPostedAt().getUpdatedAt()+"\n");
	}
}
```
##### Article
```java
package example12_replace_constructor_factory;

public abstract class Article {
	private String title;
	private String content;
	private String password;
	private Author author;
	private PostedAt postedAt;
	public static final int MYARTICLE = 0;
	public static final int SHAREDARTICLE = 1;
	public static final int ADARTICLE = 2;
	private int type;
	public static Article create(String title, String content, String authorName, String authorMail,int type) {
		switch(type) {
		case MYARTICLE:
			return new MyArticle(title, content, authorName, authorMail, type);
		case SHAREDARTICLE:
			return new SharedArticle(title, content, authorName, authorMail, type);
		case ADARTICLE:
			return new AdArticle(title, content, authorName, authorMail, type);
		default:
			throw new IllegalArgumentException("type is : "+type);
		}

	};
	protected Article() {
		super();
	}

	protected Article(String title, String content, String authorName, String authorMail,int type) {
		super();
		this.title = title;
		this.content = content;
		this.author = new Author(authorName, authorMail);
		this.postedAt = new PostedAt();
		this.type = type;
	}

	public abstract void print();
	public String getTitle() {
		return title;
	}
	public void setTitle(String title) {
		this.title = title;
	}
	public String getContent() {
		return content;
	}
	public void setContent(String content) {
		this.content = content;
	}
	public String getPassword() {
		return password;
	}
	public void setPassword(String password) {
		this.password = password;
	}

	public ImmutableAuthor getAuthor() {
		return author;
	}
	public PostedAt getPostedAt() {
		return postedAt;
	}


	public int getType() {
		return type;
	}

	public boolean isNull() {
		return false;
	}

}
```
create 가 위와 같이 변경됨에 따라서 Application 에서는 아래 ex1과 같이 사용할 수 있다.

##### ex1
```java
package example12_replace_constructor_factory;

public class Application {


	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Article article1 = Article.create("title1", "Hello World!", "alice", "alice@gmail.com",Article.MYARTICLE);
		Article article2 = Article.create("I want it", "Hello World!", "bobby", "bobby@gmail.com",Article.SHAREDARTICLE);
		article1.print();
		article2.print();
	}
}

```

일단 article 의 팩토리는 만들어지긴 했다. 하지만 create 의 switch 문과 type 은 아직 제거되지 못했다.
Article 을 생성하는 Factory method 를 분리하여 각각의 create method 를 만들어서 변경해보자.

##### Article
```java
package example12_replace_constructor_factory;

public abstract class Article {
	private String title;
	private String content;
	private String password;
	private Author author;
	private PostedAt postedAt;
	public static Article createMyArticle(String title, String content, String authorName, String authorMail) {
		return new MyArticle(title, content, authorName, authorMail);
	}
	public static Article createSharedArticle(String title, String content, String authorName, String authorMail) {
		return new SharedArticle(title, content, authorName, authorMail);
	}
	public static Article createAdArticle(String title, String content, String authorName, String authorMail) {
		return new AdArticle(title, content, authorName, authorMail);
	}
	protected Article() {
		super();
	}

	protected Article(String title, String content, String authorName, String authorMail) {
		super();
		this.title = title;
		this.content = content;
		this.author = new Author(authorName, authorMail);
		this.postedAt = new PostedAt();
	}

	public abstract void print();
	public String getTitle() {
		return title;
	}
	public void setTitle(String title) {
		this.title = title;
	}
	public String getContent() {
		return content;
	}
	public void setContent(String content) {
		this.content = content;
	}
	public String getPassword() {
		return password;
	}
	public void setPassword(String password) {
		this.password = password;
	}

	public ImmutableAuthor getAuthor() {
		return author;
	}
	public PostedAt getPostedAt() {
		return postedAt;
	}

	public boolean isNull() {
		return false;
	}

}
```
분류코드로 사용하던 type 이 제거되고 상수 값들도 제거 되었다 각자의 Factory method 를 호출하면 되기 때문이다. 물론 각 subclass 의 생성자 부분도 변경해줘야한다.
Application 에서는 아래처럼 사용할 수 있다.

##### Application
```java
package example12_replace_constructor_factory;

public class Application {


	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Article article1 = Article.createMyArticle("title1", "Hello World!", "alice", "alice@gmail.com");
		Article article2 = Article.createSharedArticle("I want it", "Hello World!", "bobby", "bobby@gmail.com");
		article1.print();
		article2.print();
	}
}
```

분명 분류코드를 제거하여 불필요한 getter 와 필드 그리고 switch 문을 제거하였는데 결국 createXXX 라는 함수를 호출해야한다.
한단계 더 나아가서 Factory 객체를 만들어보자.

##### ArticleFactory
```java
package example12_replace_constructor_factory;


public abstract class ArticleFactory {
	public abstract Article create(String title, String content, String authorName, String authorMail);
	public static class MyArticleFactory extends ArticleFactory{
		private static final MyArticleFactory instance = new MyArticleFactory();
		public static MyArticleFactory getInstance() {
			return instance;
		}
		@Override
		public Article create(String title, String content, String authorName, String authorMail) {
			// TODO Auto-generated method stub
			return new MyArticle(title, content, authorName, authorMail);
		}

	}
	public static class SharedArticleFactory extends ArticleFactory{
		private static final SharedArticleFactory instance = new SharedArticleFactory();
		public static SharedArticleFactory getInstance() {
			return instance;
		}
		@Override
		public Article create(String title, String content, String authorName, String authorMail) {
			// TODO Auto-generated method stub
			return new SharedArticle(title, content, authorName, authorMail);
		}

	}
	public static class AdArticleFactory extends ArticleFactory{
		private static final AdArticleFactory instance = new AdArticleFactory();
		public static AdArticleFactory getInstance() {
			return instance;
		}
		@Override
		public Article create(String title, String content, String authorName, String authorMail) {
			// TODO Auto-generated method stub
			return new AdArticle(title, content, authorName, authorMail);
		}

	}
}
```
각각의 Article 을 생성하는 ArticleFactory 들을 만듦으로 아래처럼 사용 가능할 것이다.

##### Application
```java
package example12_replace_constructor_factory;

import example12_replace_constructor_factory.ArticleFactory.MyArticleFactory;
import example12_replace_constructor_factory.ArticleFactory.SharedArticleFactory;

public class Application {


	public static void main(String[] args) {
		// TODO Auto-generated method stub
		ArticleFactory myArticlefactory = MyArticleFactory.getInstance();
		ArticleFactory sharedArticlefactory = SharedArticleFactory.getInstance();
		Article article1 = myArticlefactory.create("title1", "Hello World!", "alice", "alice@gmail.com");
		Article article2 = sharedArticlefactory.create("I want it", "Hello World!", "bobby", "bobby@gmail.com");
		article1.print();
		article2.print();
	}
}

```
이제 ArticleFactory 객체의 create 라는 팩토리 메서드로 Article 을 생성할 수 있다. 하지만 위 코드보다는 ArticleManager 를 이용하여 Factory 인스턴스를 받고(의존성 주입(Dependency Injection)) 해당 create를 추상화 하는 것까지가 괜찮은듯 싶다.
지금도 충분히 클래스가 많아졌고 그 이상 추상화를 진행하게되면 오히려 더 복잡한 코드가 될 수 있다.
Factory method 는 유용한 방법이다. 하지만 위에서 이야기 했듯이 용도에 맞게 사용하는 것이 중요하다.
굳이 다형성이 필요하지 않은 곳에 적용할 필요는 없다. new 한줄이면 끝날걸 여러 클래스를 나누는 짓은 멍청한 짓이다.

provider 라는 개념이 있는데 이는 클래스 제공자를 의미합니다.
provider 에 따라 각기 다른 class 를 제공해야하는 class 들은 생성을 주로 factory method 로 제공합니다.
이유는 각기 다른 provider 가 제공하는 클래스를 생성하는데 있어서 클래스형을 미리 정할 수 없기 때문입니다.

다음 포스팅은 관측 데이터 복제에 대한 내용을 포스팅하겠습니다.
