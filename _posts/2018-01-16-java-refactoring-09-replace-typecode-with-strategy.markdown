---
layout: post
title:  "Java Refactoring Replace type code with state/strategy pattern"
date:   2018-01-16 18:05:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Java
---

이전 포스팅에서 분류 코드를 서브 클래스로 치환하는 방법 및 경우를 보았다.
우리가 일반적으로 아는 MVC 패턴도 stratergy 패턴의 내용이 포함된 패턴이다.
앞에서 이용한 Sub Class 로 치환을 다시 생각해보면 생성시 객체의 분류가 인스턴스로 결정되었다.
즉 AdArticle -> Article, MyArticle -> Article 은 가능하지만 AdArticle -> MyArticle 은 힘들다.
수평관계에 있는 AdArticle, MyArticle, SharedArticle 끼리는 캐스팅도 불가능 하다.
##### ex1
```java
Article myarticle = new MyArticle("title1", "Hello World!", "alice", "alice@gmail.com");
AdArticle adArticle = (AdArticle)myarticle;
```
ex1 을 동작시켜보면 ClassCastException 이 발생하는 것을 볼 수 있을것이다.

우리가 작성한 ArticleFactory는 각각의 Sub Factory 를 통해서 Article 의 Sub Class 를 생성한다. 당연히
Factory 를 통해 create 한 인스턴스 또한 강제로 캐스팅하려 한다면 같은 익셉션을 발생시킬 것이다.

만약 동적으로 이 Article 의 종류가 변경 되어야 한다면 어떻게 해야할까?

물론 값을 가지고 우리에게 필요한 클래스의 인스턴스를 생성하는 방법도 있을 것이다. 하지만 구조적으로 해결할 순 없을까?
결국 정적인 클래스 명세말고 분류코드가 필요할 것이다.

하지만 여태 우리는 이 분류코드가 가지는 문제들을 공부했고 이 문제를 해결하기 위해 단순 분류만을 위해서는 클래스로 치환하고 분류에 따라 동작이 다른 경우는 서브클래스로 치환을 하였다.
하지만 분류 코드 즉 우리가 앞에서 치환한 클래스, 서브클래스가 동적으로 변하거나 변해야하는 상황이 있을 수 있다.
이런 경우에 대해서 사용할 수 있는 것이 상태/전략 패턴으로의 치환이다.

##### 리팩토링 카탈로그(분류 코드를 상태/전략 패턴으로 치환)

|이름|분류 코드를 상태/전략 패턴으로 치환|
|---|---|
|상황|분류 코드마다 객체가 다른 동작을 함|
|문제|동작을 switch 문으로 나누고 있지만 분류 코드가 동적으로 변하므로 분류코드를 하위 클래스로 치환은 사용 불가|
|해법|분류 코드를 나타내는 새로운 클래스를 작성해서 상태/전략 패턴을 사용함|

- 결과

  o 분류 코드 타입 판별이 가능해짐

  o 분류 코드에 따른 클래스 동작을 다형성으로 해결 가능

  x 클래스 개수가 늘어남

- 방법
1. 상태 객체를 나타내는 클래스 작성

    1. 분류 코드를 자기 캡슐화
    2. 분류 코드를 나타내는 새로운 클래스(상태 클래스) 작성
    3. 분류 코드 값마다 상태 객체의 하위 클래스 작성
    4. 분류 코드를 얻는 추상 메서드를 상태 객체에 작성
    5. 하위 클래스는 추상 메서드를 오버라이드해서 분류 코드를 반환
    6. 컴파일
2. 상태 객체 사용

    1. 분류 코드를 사용하는 클래스에 상태 객체용 필드 추가
    2. 분류 코드를 조사하는 코드를 분류 코드를 얻는 메서드 호출로 치환
    3. 분류 코드를 변경하는 코드를 상태 객체를 변경하는 코드로 치환
    4. 컴파일해서 테스트
- 관련항목

    - 자기 캡슐화 필드
    - 분류 코드를 클래스로 치환
    - 분류 코드를 하위 클래스로 치환


##### Application.java(refactoring before)
```java
package example_trashcode.example_10;

public class Application {

	private static ArticleManager articlemanager;

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		articlemanager = ArticleManager.getInstance();

		articlemanager.createArticle("title1", "Hello World!", "alice", "alice@gmail.com",Article.SHAREDARTICLE );
		articlemanager.createArticle("title2", "Hello World!!", "bobby", "bobby@gamil.com", Article.MYARTICLE);
		articlemanager.createArticle("title3", "Hello World!!!", "bobby", "bobby@gamil.com", Article.MYARTICLE);
		articlemanager.createArticle("title4", "Hello World!!!!", "bobby", "bobby@gamil.com", Article.MYARTICLE);
		articlemanager.createArticle("title5", "Hello World!!!!!", "alice", "alice@gmail.com", Article.SHAREDARTICLE);
		articlemanager.createArticle("AD", "Hello facebook", "facebook", "facebook@gmail.com", Article.ADARTICLE);
		articlemanager.createArticle("???", "???????", "unknown", "unknown@gmail.com", Article.ADARTICLE);

		articlemanager.printCurrentArticle();

	}
}
```
##### Article.java(refactoring before)
```java
package example_trashcode.example_10;

public class Article {
	private String title;
	private String content;
	private String password;
	private Author author;
	private PostedAt postedAt;
	public static final int MYARTICLE = 0;
	public static final int SHAREDARTICLE = 1;
	public static final int ADARTICLE = 2;
	private int typecode;

	public Article() {
		super();
	}

	public Article(String title, String content, String authorName, String authorMail,int typecode) {
		super();
		this.title = title;
		this.content = content;
		this.author = new Author(authorName, authorMail);
		this.postedAt = new PostedAt();
		this.typecode = typecode;
	}

	public void print() {
		switch(getTypecode()) {
		case MYARTICLE:
			System.out.println("MyArticle\n - title : "+getTitle()
			+"\n- content : "+getContent()
			+"\n- authorName : "+getAuthor().getAuthorName()
			+"\n- authorMail : "+getAuthor().getAuthorName()
			+"\n- CreatedAt : "+getPostedAt().getCreatedAt()
			+"\n- UpdatedAt : "+getPostedAt().getUpdatedAt()+"\n");
			return;
		case SHAREDARTICLE:
			System.out.println("Shared Article\n - title : "+getTitle()
			+"\ncontent : "+getContent()
			+"\nauthorName : "+getAuthor().getAuthorName()
			+"\nauthorMail : "+getAuthor().getAuthorName()
			+"\nCreatedAt : "+getPostedAt().getCreatedAt()
			+"\nUpdatedAt : "+getPostedAt().getUpdatedAt()+"\n");
			return;
		case ADARTICLE:
			System.out.println("Advertisement Article\n- title : "+getTitle()
			+"\n- content : "+getContent()
			+"\n- nauthorName : "+getAuthor().getAuthorName()
			+"\n- nauthorMail : "+getAuthor().getAuthorName()
			+"\n- nCreatedAt : "+getPostedAt().getCreatedAt()
			+"\n- nUpdatedAt : "+getPostedAt().getUpdatedAt()+"\n");
			return;
		default: throw new IllegalArgumentException("typecode = : "+getTypecode());
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
	public int getTypecode() {
		return typecode;
	}
	public void setTypecode(int typecode) {
		this.typecode = typecode;
	}
	public boolean isNull() {
		return false;
	}

}
```

[분류 코드를 서브클래스로 치환][07-replace-typecode-with-subclass] 에서 type code 를 sub class 로 치환하기 이전 코드를 보자.

##### print method
```java
public void print() {
		switch(getTypecode()) {
		case MYARTICLE:
			System.out.println("MyArticle\n - title : "+getTitle()
			+"\n- content : "+getContent()
			+"\n- authorName : "+getAuthor().getAuthorName()
			+"\n- authorMail : "+getAuthor().getAuthorName()
			+"\n- CreatedAt : "+getPostedAt().getCreatedAt()
			+"\n- UpdatedAt : "+getPostedAt().getUpdatedAt()+"\n");
			return;
		case SHAREDARTICLE:
			System.out.println("Shared Article\n - title : "+getTitle()
			+"\ncontent : "+getContent()
			+"\nauthorName : "+getAuthor().getAuthorName()
			+"\nauthorMail : "+getAuthor().getAuthorName()
			+"\nCreatedAt : "+getPostedAt().getCreatedAt()
			+"\nUpdatedAt : "+getPostedAt().getUpdatedAt()+"\n");
			return;
		case ADARTICLE:
			System.out.println("Advertisement Article\n- title : "+getTitle()
			+"\n- content : "+getContent()
			+"\n- nauthorName : "+getAuthor().getAuthorName()
			+"\n- nauthorMail : "+getAuthor().getAuthorName()
			+"\n- nCreatedAt : "+getPostedAt().getCreatedAt()
			+"\n- nUpdatedAt : "+getPostedAt().getUpdatedAt()+"\n");
			return;
		default: throw new IllegalArgumentException("typecode = : "+getTypecode());
		}
	};
```

우리의 Article 은 분류 코드(type code)에 따라서 각기 다른 print 동작이 필요하였다.
그래서 우리는 [분류 코드를 서브클래스로 치환][07-replace-typecode-with-subclass]으로 이 문제를 해결하였다.

하지만 앞에서도 이야기 했듯이 동적으로 분류코드로 분류하고자 하는 타입이 변경 될 때에는 유효하지 않은 문제 해결 방법이었다.
카탈로그에서 보인 순서대로 리팩토링을 해보자.

일단 Article 은 사용자의 입력에 의해 AdArticle, MyArticle, SharedArticle 로의 변경이 가능해야한다.
그래서 typecode 에 대한 setter 가 필요하다.
##### Article 의 typecode getter&setter
```java
public int getTypecode() {
	return typecode;
}
public void setTypecode(int typecode) {
	this.typecode = typecode;
}
```

위에서 필요한 상황을 만들기 위해 Article 의 타입을 변경하는 기능을 하나 추가한다.
ArticleManager 가 Article 들을 관리하기로 했으므로 ArticleManager 를 아래와 같이 수정하고, ArticleManager 의 리턴 객체를 하나 새로 정의하겠다.
이름은 MangedArticle 로 필드는 Article 과 index 를 가지도록 하겠다.

##### Application.java
```java
package example_trashcode.example_10;

import example_10_replace_typecode_stratergy.AdArticleType;
import example_10_replace_typecode_stratergy.MyArticleType;
import example_10_replace_typecode_stratergy.SharedArticleType;

public class Application {

	private static ArticleManager articlemanager;

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		articlemanager = ArticleManager.getInstance();

		articlemanager.createArticle("title1", "Hello World!", "alice", "alice@gmail.com",new SharedArticleType() );
		articlemanager.createArticle("title2", "Hello World!!", "bobby", "bobby@gamil.com", new MyArticleType());
		articlemanager.createArticle("title3", "Hello World!!!", "bobby", "bobby@gamil.com", new MyArticleType());
		articlemanager.createArticle("title4", "Hello World!!!!", "bobby", "bobby@gamil.com", new MyArticleType());
		articlemanager.createArticle("title5", "Hello World!!!!!", "alice", "alice@gmail.com", new MyArticleType());
		articlemanager.createArticle("AD", "Hello facebook", "facebook", "facebook@gmail.com", new AdArticleType());
		ManagedArticle mArticle = articlemanager.createArticle("???", "???????", "unknown", "unknown@gmail.com", new AdArticleType());
		System.out.println("---- mArticle ----");
		System.out.println("mArticle index : "+mArticle.getIndex());
		mArticle.getArticle().print();
		System.out.println("---- mArticle ----");
		mArticle.getArticle().changeType(new MyArticleType());

		System.out.println("---- mArticle update----");
		System.out.println("mArticle index : "+mArticle.getIndex());
		mArticle.getArticle().print();
		System.out.println("---- mArticle update----");
		articlemanager.printCurrentArticle();

	}
}
```
##### Article.java
```java
package example_trashcode.example_10;

import example_10_replace_typecode_stratergy.ArticleType;

public class Article {
	private String title;
	private String content;
	private String password;
	private Author author;
	private PostedAt postedAt;
	public static final int MYARTICLE = 0;
	public static final int SHAREDARTICLE = 1;
	public static final int ADARTICLE = 2;
	private ArticleType type;

	public Article() {
		super();
	}

	public Article(String title, String content, String authorName, String authorMail,ArticleType type) {
		super();
		this.title = title;
		this.content = content;
		this.author = new Author(authorName, authorMail);
		this.postedAt = new PostedAt();
		this.type = type;
	}

	public void changeType(ArticleType type) {
		this.type = type;
	}
	public void print() {
		switch(getTypeCode()) {
		case MYARTICLE:
			System.out.println("MyArticle\n - title : "+getTitle()
			+"\n- content : "+getContent()
			+"\n- authorName : "+getAuthor().getAuthorName()
			+"\n- authorMail : "+getAuthor().getAuthorName()
			+"\n- CreatedAt : "+getPostedAt().getCreatedAt()
			+"\n- UpdatedAt : "+getPostedAt().getUpdatedAt()+"\n");
			return;
		case SHAREDARTICLE:
			System.out.println("Shared Article\n - title : "+getTitle()
			+"\ncontent : "+getContent()
			+"\nauthorName : "+getAuthor().getAuthorName()
			+"\nauthorMail : "+getAuthor().getAuthorName()
			+"\nCreatedAt : "+getPostedAt().getCreatedAt()
			+"\nUpdatedAt : "+getPostedAt().getUpdatedAt()+"\n");
			return;
		case ADARTICLE:
			System.out.println("Advertisement Article\n- title : "+getTitle()
			+"\n- content : "+getContent()
			+"\n- nauthorName : "+getAuthor().getAuthorName()
			+"\n- nauthorMail : "+getAuthor().getAuthorName()
			+"\n- nCreatedAt : "+getPostedAt().getCreatedAt()
			+"\n- nUpdatedAt : "+getPostedAt().getUpdatedAt()+"\n");
			return;
		default: throw new IllegalArgumentException("typecode = : "+getTypeCode());
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
	public int getTypeCode() {
		return type.getTypeCode();
	}

	public ArticleType getType() {
		return type;
	}

	public boolean isNull() {
		return false;
	}

}
```
##### ArticleManage.java
```java
package example_trashcode.example_10;

import java.util.ArrayList;

import example_10_replace_typecode_stratergy.ArticleType;

public class ArticleManager {
	private static final ArticleManager instance = new ArticleManager();
	private ArrayList<Article> list = new ArrayList<>();
	public static ArticleManager getInstance() {
		return instance;
	}
	public ArticleManager() {
		super();
	}
	public ManagedArticle createArticle(String title, String content, String authorName, String authorMail,ArticleType type) {
		this.list.add(new Article(title,content,authorName,authorMail,type));
		return new ManagedArticle(this.list.get(this.list.size()-1),this.list.size()-1);
	}
	public ManagedArticle findArticleWithTitle(String query) {
		for(int index = 0; index < this.list.size(); index++){
			if(this.list.get(index).getTitle().equals(query)) {
				return new ManagedArticle(this.list.get(index),index);
			}
		}
		return new ManagedArticle(NullArticle.getInstance());
	}
	public ManagedArticle removeArticle() {
		if(list.size() != 0) {
			return new ManagedArticle(this.list.remove(list.size()-1),list.size()-1);
		}
		return new ManagedArticle(NullArticle.getInstance());
	}
	public ManagedArticle removeArticleWithTitle(String query) {
		for(int index = 0; index < this.list.size(); index++) {
			if(this.list.get(index).getTitle().equals(query)) {
				return new ManagedArticle(this.list.remove(index),index);
			}
		}
		return new ManagedArticle(NullArticle.getInstance());
	}
	public void printCurrentArticle() {
		for(Article article : this.list) {
			article.print();
		}
	}
	public ManagedArticle updateArticle(Article article, int index) {
		if(index > this.list.size()-1 || index == -1) {
			return createArticle(article.getTitle(),
					article.getContent(),
					article.getAuthor().getAuthorName(),
					article.getAuthor().getAuthorName(),
					article.getType());
		}else {
			return new ManagedArticle(this.list.set(index, article),index);
		}
	}

}
```

##### ArticleType
```java
package example_10_replace_typecode_stratergy;

public abstract class ArticleType {

	public abstract int getTypeCode();
}
```
##### MyArticleType
```java
package example_10_replace_typecode_stratergy;

public class MyArticleType extends ArticleType{
	private int type;

	public MyArticleType() {
		super();
		this.type = Article.MYARTICLE;
	}

	@Override
	public int getTypeCode() {
		// TODO Auto-generated method stub
		return this.type;
	}

}
```
##### SharedArticleType
```java
package example_10_replace_typecode_stratergy;

public class SharedArticleType extends ArticleType{
	private int type;

	public SharedArticleType() {
		super();
		this.type = Article.SHAREDARTICLE;
	}

	@Override
	public int getTypeCode() {
		// TODO Auto-generated method stub
		return this.type;
	}

}
```
##### AdArticleType
```java
package example_10_replace_typecode_stratergy;

public class AdArticleType extends ArticleType{
	private int type;


	public AdArticleType() {
		super();
		this.type = Article.ADARTICLE;
	}


	@Override
	public int getTypeCode() {
		// TODO Auto-generated method stub
		return this.type;
	}

}
```
##### ManagedArticle
```java
package example_trashcode.example_10;


public class ManagedArticle {
	private Article article;
	private int index;
	public static final int NULL = -1;
	public ManagedArticle(Article article) {
		super();
		if(article.isNull()) {
			this.index = NULL;
			this.article = article;
		}else{
			throw new IllegalArgumentException("Please Use With NullArticle Object");
		}
	}

	public ManagedArticle(Article article, int index) {
		super();
		this.article = article;
		this.index = index;
	}

	public Article getArticle() {
		return article;
	}

	public int getIndex() {
		return index;
	}
}
```

ManagedArticle 에서 널 처리는 하지 않았다. 복습차원에서 해볼 사람은 해보길 바란다.
ArticleManager 에는 Article 을 업데이트 하는 updateArticle 을 추가하였고 ArticleManager 가 반환하던 형식을 Article 에서 ManagedArticle 로 변경하였으며 ManagedArticle 은 Article 과 해당 Article 의 index 를 가지는 객체이다.
updatedArticle 은 전달된 Article 을 해당 index 에 업데이트 하는데 index 가 유효하지 않으면(즉 없으면) 새로 생성한다.
전달된 index 가 유효하면 해당 index 의 Article 객체를 update 하고 업데이트된 Article, index를 포함한 ManagedArticle 을 반환한다.
Article 의 print 는 ArticleType 의 분류 코드에 의해 동작하며 type 을 변경하는 changeType 이 추가되었다.

변경 중간중간 컴파일 해서 테스트는 진행 해보아야한다.
여기까지 진행하여서 Application 을 실행시켜보면 기존 동작과 변경없이 동작한다.
우리가 만든 ArticleType 은 현재 Article 의 상태를 나타내는 코드로 볼 수 있다.
분류 코드를 치환한 ArticleType 객체의 변경을 통해 위에서 이야기한 문제를 해결할 수 있었다.
하지만 print 부분의 switch 는 아직 악취가 난다. 우리는 앞에서 ArticleType 이라는 상태 객체를 만들었다.

ArticleType 을 아래처럼 변경한다. 우리가 앞에서 했던 작업이다.
각각의 타입클래스들에게 print 동작을 오버라이드 해주고 switch 문의 동작을 이동한다.

##### ArticleType(다형성으로 조건문 분기 치환)
```java
package example_10_replace_typecode_stratergy;

public abstract class ArticleType {

	public abstract int getTypeCode();
	public abstract void print(Article article);
}
```
그러면 아래와 같이 변경 될 것이다.
##### MyArticleType
```java
package example_10_replace_typecode_stratergy;

public class MyArticleType extends ArticleType{
	private int type;

	public MyArticleType() {
		super();
		this.type = Article.MYARTICLE;
	}

	@Override
	public int getTypeCode() {
		// TODO Auto-generated method stub
		return this.type;
	}

	@Override
	public void print(Article article) {
		// TODO Auto-generated method stub
		System.out.println("MyArticle\n - title : "+article.getTitle()
		+"\n- content : "+article.getContent()
		+"\n- authorName : "+article.getAuthor().getAuthorName()
		+"\n- authorMail : "+article.getAuthor().getAuthorName()
		+"\n- CreatedAt : "+article.getPostedAt().getCreatedAt()
		+"\n- UpdatedAt : "+article.getPostedAt().getUpdatedAt()+"\n");
	}

}
```
##### SharedArticleType
```java
package example_10_replace_typecode_stratergy;

public class SharedArticleType extends ArticleType{

	private int type;

	public SharedArticleType() {
		super();
		this.type = Article.SHAREDARTICLE;
	}

	@Override
	public int getTypeCode() {
		// TODO Auto-generated method stub
		return this.type;
	}
	@Override
	public void print(Article article) {
		// TODO Auto-generated method stub
		System.out.println("Shared Article\n - title : "+article.getTitle()
		+"\ncontent : "+article.getContent()
		+"\nauthorName : "+article.getAuthor().getAuthorName()
		+"\nauthorMail : "+article.getAuthor().getAuthorName()
		+"\nCreatedAt : "+article.getPostedAt().getCreatedAt()
		+"\nUpdatedAt : "+article.getPostedAt().getUpdatedAt()+"\n");
	}

}
```
##### AdArticleType
```java
package example_10_replace_typecode_stratergy;

public class AdArticleType extends ArticleType{
	private int type;

	public AdArticleType() {
		super();
		this.type = Article.ADARTICLE;
	}

	@Override
	public int getTypeCode() {
		// TODO Auto-generated method stub
		return this.type;
	}

	@Override
	public void print(Article article) {
		// TODO Auto-generated method stub
		System.out.println("Advertisement Article\n- title : "+article.getTitle()
		+"\n- content : "+article.getContent()
		+"\n- nauthorName : "+article.getAuthor().getAuthorName()
		+"\n- nauthorMail : "+article.getAuthor().getAuthorName()
		+"\n- nCreatedAt : "+article.getPostedAt().getCreatedAt()
		+"\n- nUpdatedAt : "+article.getPostedAt().getUpdatedAt()+"\n");
	}
}
```

##### Article
```java
package example_10_replace_typecode_stratergy;

import example_10_replace_typecode_stratergy.ArticleType;

public class Article {
	private String title;
	private String content;
	private String password;
	private Author author;
	private PostedAt postedAt;
	public static final int MYARTICLE = 0;
	public static final int SHAREDARTICLE = 1;
	public static final int ADARTICLE = 2;
	private ArticleType type;

	public Article() {
		super();
	}

	public Article(String title, String content, String authorName, String authorMail,ArticleType type) {
		super();
		this.title = title;
		this.content = content;
		this.author = new Author(authorName, authorMail);
		this.postedAt = new PostedAt();
		this.type = type;
	}

	public void changeType(ArticleType type) {
		this.type = type;
	}
	public void print() {
		getType().print(this);
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
	public int getTypeCode() {
		return type.getTypeCode();
	}

	public ArticleType getType() {
		return type;
	}

	public boolean isNull() {
		return false;
	}

}
```
이를 클래스로 나타내지 않고 enum 을 이용하여 나타낼 수 있는데 생성한 타입 오브젝트를 enum 으로 매핑한다.

##### ArticleTypeEnum
```java
package example_10_replace_typecode_stratergy;

public enum ArticleTypeEnum {
	MyArticle{

		@Override
		public void print(Article article) {
			// TODO Auto-generated method stub
			System.out.println("MyArticle\n - title : "+article.getTitle()
			+"\n- content : "+article.getContent()
			+"\n- authorName : "+article.getAuthor().getAuthorName()
			+"\n- authorMail : "+article.getAuthor().getAuthorName()
			+"\n- CreatedAt : "+article.getPostedAt().getCreatedAt()
			+"\n- UpdatedAt : "+article.getPostedAt().getUpdatedAt()+"\n");
		}

	},
	SharedArticle{

		@Override
		public void print(Article article) {
			// TODO Auto-generated method stub
			System.out.println("Shared Article\n - title : "+article.getTitle()
			+"\ncontent : "+article.getContent()
			+"\nauthorName : "+article.getAuthor().getAuthorName()
			+"\nauthorMail : "+article.getAuthor().getAuthorName()
			+"\nCreatedAt : "+article.getPostedAt().getCreatedAt()
			+"\nUpdatedAt : "+article.getPostedAt().getUpdatedAt()+"\n");
		}

	},
	AdArticle{

		@Override
		public void print(Article article) {
			// TODO Auto-generated method stub
			System.out.println("Advertisement Article\n- title : "+article.getTitle()
			+"\n- content : "+article.getContent()
			+"\n- nauthorName : "+article.getAuthor().getAuthorName()
			+"\n- nauthorMail : "+article.getAuthor().getAuthorName()
			+"\n- nCreatedAt : "+article.getPostedAt().getCreatedAt()
			+"\n- nUpdatedAt : "+article.getPostedAt().getUpdatedAt()+"\n");
		}

	};
	public abstract void print(Article article);
}

```

##### Article
```java
package example_10_replace_typecode_stratergy;

public class Article {
	private String title;
	private String content;
	private String password;
	private Author author;
	private PostedAt postedAt;
	public static final int MYARTICLE = 0;
	public static final int SHAREDARTICLE = 1;
	public static final int ADARTICLE = 2;
	private ArticleTypeEnum type;

	public Article() {
		super();
	}

	public Article(String title, String content, String authorName, String authorMail,ArticleTypeEnum type) {
		super();
		this.title = title;
		this.content = content;
		this.author = new Author(authorName, authorMail);
		this.postedAt = new PostedAt();
		this.type = type;
	}

	public void changeType(ArticleTypeEnum type) {
		this.type = type;
	}
	public void print() {
		getType().print(this);
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


	public ArticleTypeEnum getType() {
		return type;
	}

	public boolean isNull() {
		return false;
	}

}
```

##### ArticleManager
```java
package example_10_replace_typecode_stratergy;

import java.util.ArrayList;

public class ArticleManager {
	private static final ArticleManager instance = new ArticleManager();
	private ArrayList<Article> list = new ArrayList<>();
	public static ArticleManager getInstance() {
		return instance;
	}
	public ArticleManager() {
		super();
	}
	public ManagedArticle createArticle(String title, String content, String authorName, String authorMail,ArticleTypeEnum type) {
		this.list.add(new Article(title,content,authorName,authorMail,type));
		return new ManagedArticle(this.list.get(this.list.size()-1),this.list.size()-1);
	}
	public ManagedArticle findArticleWithTitle(String query) {
		for(int index = 0; index < this.list.size(); index++){
			if(this.list.get(index).getTitle().equals(query)) {
				return new ManagedArticle(this.list.get(index),index);
			}
		}
		return new ManagedArticle(NullArticle.getInstance());
	}
	public ManagedArticle removeArticle() {
		if(list.size() != 0) {
			return new ManagedArticle(this.list.remove(list.size()-1),list.size()-1);
		}
		return new ManagedArticle(NullArticle.getInstance());
	}
	public ManagedArticle removeArticleWithTitle(String query) {
		for(int index = 0; index < this.list.size(); index++) {
			if(this.list.get(index).getTitle().equals(query)) {
				return new ManagedArticle(this.list.remove(index),index);
			}
		}
		return new ManagedArticle(NullArticle.getInstance());
	}
	public void printCurrentArticle() {
		for(Article article : this.list) {
			article.print();
		}
	}
	public ManagedArticle updateArticle(Article article, int index) {
		if(index > this.list.size()-1 || index == -1) {
			return createArticle(article.getTitle(),
					article.getContent(),
					article.getAuthor().getAuthorName(),
					article.getAuthor().getAuthorName(),
					article.getType());
		}else {
			return new ManagedArticle(this.list.set(index, article),index);
		}
	}

}
```
print 는 ArticleTypeEnum 의 print 를 사용하게 되며 상태 클래스들의 추가로 인한 클래스 갯수 늘어나는 문제도 어느정도 해결할 수 있다.
이번 포스팅 내용은 분류 코드를 하위클래스를 만들어 동작 차이를 오버라이드하는 것 까지는 앞 포스팅과 같지만
이용하는 클래스를 외부에 두는점이 다른 점이다.
다음 포스팅은 에러 코드를 예외로 치환하는 것에 대해 알아보겠다.

분류 코드 치환 관련 포스팅 : [클래스로 치환][07-replace-typecode-with-class], [서브 클래스로 치환][08-replace-typecode-with-subclass], [상태 전략 패턴을 이용한 치환][09-replace-typecode-with-strategy]

[07-replace-typecode-with-class]:https://kishe89.github.io/2018/01/12/java-refactoring-07-replace-typecode-with-class.html
[08-replace-typecode-with-subclass]:https://kishe89.github.io/2018/01/13/java-refactoring-08-replace-typecode-with-subclass.html
[09-replace-typecode-with-strategy]:https://kishe89.github.io/2018/01/16/java-refactoring-09-replace-typecode-with-strategy.html
