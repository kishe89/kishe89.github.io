---
layout: post
title:  "Java Refactoring Replace typecode with Class"
date:   2018-01-12 19:44:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Java
---

분류 코드는(type code)는 객체의 종류를 나타내는 값을 말한다.
예를 들어서 페이스북의 타임라인을 보면 사용자들의 게시물, 공유 게시물, 광고등의
여러가지 뷰들이 나오는데 이를 구별하여 렌더하기 위해서는 각 데이터들별로 매칭되는
view type code 값이 필요할 것이다.

- 본인 게시물 = 0
- 공유 게시물 = 1
- 광고 - 2

와 같이 분류할 수 있을 것이다.
분류 코드를 이용하여 객체를 구분하는 건 필요 한 일이며 자주 있는 일이다.
하지만 분류 코드로 이용하는 자료형이 기본 자료형만을 이용할 경우 타입 판별이 되지 않거나 또는 타입 세이프가 안지켜질 수 있다.

리팩토링 순서는 다음과 같은 순서로 진행한다.

1. 우선 int를 사용하는 기존 인터페이스(API)를 사용한다.
2. int를 사용하지 않는 새로운 인터페이스(API)로 변경합니다.
3. 마지막으로 기존 인터페이스(API)를 삭제한다.

##### 리팩토링 카탈로그(분류 코드를 클래스로 치환)

|이름|분류 코드를 클래스로 치환|
|---|---|
|상황|객체를 식별하기위한 분류코드가 int와 같은 기본 자료형임|
|문제|타입 판별이 안됨|
|해법|분류 코드를 나타내는 새로운 클래스를 작성|

- 결과

  o 분류 코드의 타입 판별이 가능해짐

  x 클래스 개수가 늘어남

- 방법
1. 새로운 클래스 작성해서 기존 인터페이스(API)에서 사용

    1. 분류 코드를 나타내는 새로운 클래스 작성

        - 호환성을 위해 기본 타입을 사용한 인터페이스를 준비함
    2. 기본 타입을 분류 코드로 사용하는 클래스가 새로운 클래스를 사용하도록 변경

        - 기본 타입을 사용한 기존 인터페이스(API)를 사용
    3. 컴파일 해서 테스트
2. 새로운 인터페이스(API)로 전환

    1. 기본 타입을 사용하지 않는 새로운 인터페이스(API)작성
    2. 기본 타입을 사용한 기존 인터페이스(API)를 새로운 인터페이스(API)로 치환
    3. 치환할 때마다 컴파일해서 테스트
3. 기존 인터페이스(API) 삭제

    1. 기존 인터페이스(API)를 사용하는 클래스가 없어지면 기존 인터페이스(API)삭제
    2. 컴파일해서 테스트
- 관련항목

    - 분류 코드를 하위 클래스로 치환.

        분류 코드에 따른 동작이 지장되었을 때 사용
    - 분류 코드를 상태/전략(strategy) 패턴으로 치환

        분류 코드에 다른 동작이 지정되고 분류 코드를 하위 클래스로 치환을 쓸 수 없을 때 사용
    - 생성자를 팩토리 메서드로 치환

        분류 코드 값에 따라 인스턴스를 작성할 때 팩토리 메서드를 이용 가능.


이전 예제에서 사용한 Article 을 이용해서 보면

##### Article.java(typecode 추가)
```java
package example_8_replace_typecode;

public class Article {
	public static final int MYARTICLE = 0;
	public static final int SHAREDARTICLE = 1;
	public static final int ADARTICLE = 2;
	private String title;
	private String content;
	private String password;
	private Author author;
	private PostedAt postedAt;
	private final int typecode;

	public Article() {
		super();
		typecode = MYARTICLE;
	}
	public Article(String title, String content, String authorName, String authorMail, int typecode) {
		super();
		this.title = title;
		this.content = content;
		this.author = new Author(authorName, authorMail);
		this.postedAt = new PostedAt();
		this.typecode = typecode;
	}
	public void print() {
		System.out.println("Article - title : "+title
				+"\ncontent : "+content
				+"\nauthorName : "+this.getAuthor().getAuthorName()
				+"\nauthorMail : "+this.getAuthor().getAuthorName()
				+"\nCreatedAt : "+this.postedAt.getCreatedAt()
				+"\nUpdatedAt : "+this.postedAt.getUpdatedAt()+"\n");
	}
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
	public boolean isNull() {
		return false;
	}

}
```
Article 의 종류에 대한 분류 코드 typecode 필드가 하나 추가 되었으며
이에 대입될 종류를 나타내는 분류 값이 int 값으로 3개 추가되어있다.
만약 0~2를 벗어나는 값을 집어넣더라도 Article 객체는 생성이 될것이다.

##### Application.java
```java
package example_8_replace_typecode;

public class Application {

	private static ArticleManager articlemanager;

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		articlemanager = ArticleManager.getInstance();
		articlemanager.createArticle("title1", "Hello World!", "alice", "alice@gmail.com", 1);
		articlemanager.createArticle("title2", "Hello World!!", "bobby", "bobby@gamil.com", 0);
		articlemanager.createArticle("title3", "Hello World!!!", "bobby", "bobby@gamil.com", 0);
		articlemanager.createArticle("title4", "Hello World!!!!", "bobby", "bobby@gamil.com", 0);
		articlemanager.createArticle("title5", "Hello World!!!!!", "alice", "alice@gmail.com", 1);
		articlemanager.createArticle("AD", "Hello facebook", "facebook", "facebook@gmail.com", 2);
		articlemanager.createArticle("???", "???????", "unknown", "unknown@gmail.com", 3);

		articlemanager.printCurrentArticle();

	}
}
```

ArticleManager 를 이용해서 Article 을 생성하는데 마지막으로 생성하는 라인을 보면 마지막인자인 typecode 에 0~2를 벗어나는
3이 들어가있다. 하지만 이 코드는 정상적으로 동작하게 된다. 왜냐하면 이 값으로 분류해서 보여주는 화면 리소스가 없이 그냥 내용 자체를 출력하는 코드만 있기때문이다.
만약 뒤에 분류코드에 따라 화면 리소스를 따로 사용한다던가 하는 코드가 들어간다면 리소스를 못찾는 에러가 발생하거나 혹은 원치않는 리소스를 이용한 출력이 이루어질 것이다.
오류가 나면 다행이지만 재수없게도 사용하지 않는 어떤 리소스가 들어가 있어서 동작이 된다면 버그를 찾기는 더욱 힘들어 질 것이다.

정말 별 것 아닌 몇줄의 코드 때문에 밤에 퇴근을 못하는 불상사가 벌어 질 수 있다.

그럼 기본 자료형이 아닌 상태를 나타내는 클래스를 작성하는 것이 어떻게 이 문제를 해결해 줄지 확인해본다.

##### ArticleType.java
```java
package example_8_replace_typecode;

public class ArticleType {
	public static final ArticleType MYARTICLE = new ArticleType(0);
	public static final ArticleType SHAREDARTICLE = new ArticleType(1);
	public static final ArticleType ADARTICLE = new ArticleType(2);
	private final int typecode;


	public ArticleType(int typecode) {
		super();
		this.typecode = typecode;
	}

	public int getTypecode() {
		return typecode;
	}

}
```
##### Article(typecode -> ArticleType 치환)
```java
package example_8_replace_typecode;

public class Article {
	private String title;
	private String content;
	private String password;
	private Author author;
	private PostedAt postedAt;
	private final ArticleType articleType;

	public Article() {
		super();
		articleType = ArticleType.MYARTICLE;
	}
	public Article(String title, String content, String authorName, String authorMail, ArticleType articleType) {
		super();
		this.title = title;
		this.content = content;
		this.author = new Author(authorName, authorMail);
		this.postedAt = new PostedAt();
		this.articleType = articleType;
	}
	public void print() {
		System.out.println("Article - title : "+title
				+"\ncontent : "+content
				+"\nauthorName : "+this.getAuthor().getAuthorName()
				+"\nauthorMail : "+this.getAuthor().getAuthorName()
				+"\nCreatedAt : "+this.postedAt.getCreatedAt()
				+"\nUpdatedAt : "+this.postedAt.getUpdatedAt()+"\n");
	}
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
		return articleType.getTypecode();
	}
	public boolean isNull() {
		return false;
	}

}
```
##### ArticleManager(ArticleType 매개변수 추가)
```java
package example_8_replace_typecode;

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
	public Article createArticle(String title, String content, String authorName, String authorMail, ArticleType articleType) {
		this.list.add(new Article(title, content, authorName, authorMail, articleType));
		return this.list.get(this.list.size()-1);
	}
	public Article findArticleWithTitle(String query) {
		for(Article article : this.list) {
			if(article.getTitle().equals(query)) {
				return article;
			}
		}
		return NullArticle.getInstance();
	}
	public Article removeArticle() {
		if(list.size() != 0) {
			return this.list.remove(list.size()-1);
		}
		return NullArticle.getInstance();
	}
	public Article removeArticleWithTitle(String query) {
		for(int index = 0; index < this.list.size(); index++) {
			if(this.list.get(index).getTitle().equals(query)) {
				return this.list.remove(index);
			}
		}
		return NullArticle.getInstance();
	}
	public void printCurrentArticle() {
		for(Article article : this.list) {
			article.print();
		}
	}

}
```

##### Application.java(타입 미지원으로 인해 에러)
```java
package example_8_replace_typecode;

public class Application {

	private static ArticleManager articlemanager;

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		articlemanager = ArticleManager.getInstance();
		articlemanager.createArticle("title1", "Hello World!", "alice", "alice@gmail.com", ArticleType.SHAREDARTICLE);
		articlemanager.createArticle("title2", "Hello World!!", "bobby", "bobby@gamil.com", ArticleType.MYARTICLE);
		articlemanager.createArticle("title3", "Hello World!!!", "bobby", "bobby@gamil.com", ArticleType.MYARTICLE);
		articlemanager.createArticle("title4", "Hello World!!!!", "bobby", "bobby@gamil.com", ArticleType.MYARTICLE);
		articlemanager.createArticle("title5", "Hello World!!!!!", "alice", "alice@gmail.com", ArticleType.SHAREDARTICLE);
		articlemanager.createArticle("AD", "Hello facebook", "facebook", "facebook@gmail.com", ArticleType.ADARTICLE);
		articlemanager.createArticle("???", "???????", "unknown", "unknown@gmail.com", 3);

		articlemanager.printCurrentArticle();

	}
}
```
아까는 실행되던 마지막 createArticle구문이 실행도 전에 컴파일 시점에 이미 에러로 알 수 있게 나타난다.
Article의 생성자가 받는 type을 나타내는 분류코드는 분류 객체로 변경 되었기에 단순 int형으로는 생성이 불가하다.

ArticleType 에 분류 외의 의미가 없다면 typecode변수 또한 삭제가 가능 할 것이다.

다음은 분류코드를 하위 클래스로 치환하는 방법에 대한 포스팅을 한다.
