---
layout: post
title:  "Java Refactoring Extract class"
date:   2018-01-11 19:44:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Java
---

클래스는 속성을 가지고 행위를 처리하고 책임지는 주체입니다.
이상적인 클래스는 한가지 책임을 지는 클래스 이고 이를 행하기 위해 여러 패턴들이 만들어졌습니다.
하지만 코드가 늘어나고 기능이 추가됨에 따라 어떤 클래스들은 이러한 단일책임원칙을 지키기 어려워질 수 있습니다.
이런 경우 해당 행위를 다른 클래스에게 위임하는 방법이 있습니다.

##### 리팩토링 카탈로그(클래스 추출)

|이름|클래스 추출(Extract Class)|
|---|---|
|상황|클래스를 작성함|
|문제|한 클래스가 너무 많은 책임을 지고 있음|
|해법|묶을 수 있는 필드와 메서드를 찾아 새로운 클래스로 추출|

- 결과

  o 클래스가 작아짐

  o 클래스의 책임이 명확해짐

  x 클래스 개수가 늘어남

- 방법
1. 새로운 클래스 작성

    1. 클래스의 책임을 어떻게 추출할지 결정
    2. 필드 이용

        - 기존 클래스에서 새로운 클래스로 필요한 필드 이동
        - 이동할 때마다 컴파일해서 테스트
    3. 메서드 이동

        - 기존 클래스에서 새로운 클래스로 필요한 메서드 이동
        - 이동할 때 마다 컴파일해서 테스트
    4. 추출한 클래스 검토

        - 복사한 코드에서 입력값으로 사용하는 변수가 있다면 메서드 매개변수로 만든다.
    5. 메서드 반환값 검토

        - 클래스 인터페이스(API)를 줄일 수 있는가
        - 새로운 클래스를 외부에 공개해야 하는가
        - 공개한다면 외부에서 수정 가능하게 할 것인가
- 관련항목

    - 클래스명 변경
    - 필드 이동
    - 메서드 이동


##### Article.java
```java
package example_7_extract_class;

import java.util.Date;

public class Article {
	private String title;
	private String content;
	private String password;
	private String authorName;
	private String authorMail;
	private Date CreatedAt;
	private Date UpdatedAt;
	public Article(String title, String content, String authorName, String authorMail) {
		super();
		this.title = title;
		this.content = content;
		this.authorName = authorName;
		this.authorMail = authorMail;
		this.CreatedAt = new Date(System.currentTimeMillis());
		this.UpdatedAt = new Date(System.currentTimeMillis());
	}
	public void print() {
		System.out.println("Article - title : "+title
				+"\ncontent : "+content
				+"\nauthorName : "+authorName
				+"\nauthorMail : "+authorMail
				+"\nCreatedAt : "+CreatedAt
				+"\nUpdatedAt : "+UpdatedAt+"\n");
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
	public String getAuthorName() {
		return authorName;
	}
	public void setAuthorName(String authorName) {
		this.authorName = authorName;
	}
	public String getAuthorMail() {
		return authorMail;
	}
	public void setAuthorMail(String authorMail) {
		this.authorMail = authorMail;
	}
	public Date getCreatedAt() {
		return CreatedAt;
	}
	public void setCreatedAt(Date createdAt) {
		CreatedAt = createdAt;
	}
	public Date getUpdatedAt() {
		return UpdatedAt;
	}
	public void setUpdatedAt(Date updatedAt) {
		UpdatedAt = updatedAt;
	}
}

```

##### Application.java
```java
package example_7_extract_class;

import java.util.ArrayList;

public class Application {

	public static void main(String[] args) {
		ArrayList<Article> articleList = new ArrayList<>();

		//article 생성
		articleList.add(new Article("Article2","Hello2","bobby","bobby@naver.com"));
		articleList.add( new Article("Article1","Hello","alice","alice@gmail.com"));

		// article 출력
		System.out.println("ArticleList print");
		for(Article article : articleList) {
			article.print();
		}

		// article title 검색
		String query = "Article1";
		Article result;
		for(Article article : articleList) {
			if(article.getTitle().equals(query)) {
				result = article;
				System.out.println("Search Result");
				article.print();
			}
		}

		// article 삭제
		ArrayList<Article> resultList = new ArrayList<>();
		for(int index = 0; index < articleList.size(); index++) {
			if(articleList.get(index).getTitle().equals(query)) {
				Article removedArticle = articleList.remove(index);
				resultList = articleList;
				System.out.println("Removed Article");
				removedArticle.print();
			}
		}
		System.out.println("Remove result");
		for(Article article : resultList) {
			article.print();
		}

	}
}
```

기사를 생성하고 조회하고 검색하고 삭제하는 어플리케이션을 만들기 위해 Article.java와 Application.java를
만들었다.

Article 은 생성시에 입력으로 title, content, authoName, authorMail 을 매개변수로 받는다.
일단 Application.java 를 보자. main 함수에서는 지역변수로 Article 을 관리하는 ArrayList 를 만들어서
Article 의 생성, 조회, 검색, 삭제를 행하고 있다. 주석과 System.out.println 으로 출력해준 String 들이 없다면
코드만 보고 바로 무슨 행위를 하는지 알기 힘들고 보기도 싫어지는 코드다.

이 부분부터 리팩토링을 진행해보자. articleList 는 Application 의 article 을 저장하고 있는 객체다.
Application 은 시작과 종료에 대한 라이프사이클을 책임지는 클래스이다. Application 이
article 의 관리 책임을 가질 이유는 없을 것이다.
그러므로 아래와 같이 Application 이 가지고있던 article 의 관리에 대한 책임을 위임할 수 있을것이다.

##### ArticleManager.java
```java
package example_7_extract_class;

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
	public Article createArticle(String title, String content, String authorName, String authorMail) {
		this.list.add(new Article(title, content, authorName, authorMail));
		return this.list.get(this.list.size()-1);
	}
	public Article findArticleWithTitle(String query) {
		for(Article article : this.list) {
			if(article.getTitle().equals(query)) {
				return article;
			}
		}
		return new NullArticle();
	}
	public Article removeArticle() {
		if(list.size() != 0) {
			return this.list.remove(list.size()-1);
		}
		return new NullArticle();
	}
	public Article removeArticleWithTitle(String query) {
		for(int index = 0; index < this.list.size(); index++) {
			if(this.list.get(index).getTitle().equals(query)) {
				return this.list.remove(index);
			}
		}
		return new NullArticle();
	}
	public void printCurrentArticle() {
		for(Article article : this.list) {
			article.print();
		}
	}

}
```

##### Application.java(Article 관리 책임 ArticleManager에게 위임)
```java
package example_7_extract_class;

public class Application {

	private static ArticleManager articleManager;
	public static void main(String[] args) {
		articleManager = ArticleManager.getInstance();
		articleManager.createArticle("Article2", "Hello2", "bobby", "bobby@naver.com");
		articleManager.createArticle("Article1", "Hello", "alice", "alice@gmail.com");

		articleManager.printCurrentArticle();

		String query = "Article1";
		articleManager.findArticleWithTitle(query).print();
		articleManager.removeArticle().print();
		articleManager.removeArticleWithTitle(query).print();

		articleManager.printCurrentArticle();

	}
}
```
ArticleManager 라고 이름을 붙였다. ArticleManager 는 Application 에서 관리하던 articleList 를 관리하는
책임을 가지고 있는 클래스이다.
필요한 필드는 articleList 로 해당 필드를 ArticleManager 로 이동하면서 이름을 list 로 변경하였다.
list는 ArticleManager 의 속성이며 이에대한 조작은 ArticleManager 가 조작하는 것이 맞으므로 list에 대한
다른 스코프에서 직접적인 접근은 불가하게 private 으로 처리하는게 맞을 것이다.
그리고 Application 에서 처리하던 생성, 조회, 검색, 삭제 동작을 ArticleManager 메서드로 이동하였다.
각 각 createArticle, printCurrentArticle(), findArticleWithTitle(String), removeArticle(), removeArticleWithTitle(String)
으로 이름 붙였다. 이름이 긴것 같지만 의미가 제대로 전달이 안되는 짧은 이름보다는 길더라도 의미가 바로 보이는 이름이 좋다.

Application 은 시스템의 한 부분인 article 에 대한 기능을 하는 ArticleManager 만을 책임 지게 되었다.
기능이 추가 되고 하더라도 해당 기능을 하는 매니저만 추가해주면 될 것이다.

Application 에 대해 리팩토링을 진행하면서 Article 또한 약간의 리팩토링을 거쳤다.
바로 앞에서 배웠던 Null Object를 이용한 Null 처리이다.

Null Object 를 이용하여 리팩토링한 Article 은 아래와 같아 지고 NullArticle 이 생성되었다.

##### Article.java(Null Object 이용한 리팩토링)
```java
package example_7_extract_class;

import java.util.Date;

public class Article {
	private String title;
	private String content;
	private String password;
	private String authorName;
	private String authorMail;
	private Date CreatedAt;
	private Date UpdatedAt;



	public Article() {
		super();
	}
	public Article(String title, String content, String authorName, String authorMail) {
		super();
		this.title = title;
		this.content = content;
		this.authorName = authorName;
		this.authorMail = authorMail;
		this.CreatedAt = new Date(System.currentTimeMillis());
		this.UpdatedAt = new Date(System.currentTimeMillis());
	}
	public void print() {
		System.out.println("Article - title : "+title
				+"\ncontent : "+content
				+"\nauthorName : "+authorName
				+"\nauthorMail : "+authorMail
				+"\nCreatedAt : "+CreatedAt
				+"\nUpdatedAt : "+UpdatedAt+"\n");
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
	public String getAuthorName() {
		return authorName;
	}
	public void setAuthorName(String authorName) {
		this.authorName = authorName;
	}
	public String getAuthorMail() {
		return authorMail;
	}
	public void setAuthorMail(String authorMail) {
		this.authorMail = authorMail;
	}
	public Date getCreatedAt() {
		return CreatedAt;
	}
	public void setCreatedAt(Date createdAt) {
		CreatedAt = createdAt;
	}
	public Date getUpdatedAt() {
		return UpdatedAt;
	}
	public void setUpdatedAt(Date updatedAt) {
		UpdatedAt = updatedAt;
	}
	public boolean isNull() {
		// TODO Auto-generated method stub
		return false;
	}
}
```
##### NullArticle.java(NullObject)
```java
package example_7_extract_class;

public class NullArticle extends Article{

	private static final NullArticle instance = new NullArticle();

	public static NullArticle getInstance() {
		return instance;
	}

	public boolean isNull() {
		return true;
	}

	@Override
	public void print() {
		// TODO Auto-generated method stub
		System.out.println("is Null");
	}
}
```

이제 Application 은 현재로서는 크게 손댈 곳이 없어보인다.
이제 Article 을 손보도록 해보자. 현재의 Article 은 Null에 대한 처리는 NullArticle에게 위임했으므로 그 부분은 제하고 생각해본다.
작성자를 나타내는 authorName, authorMail과 시간 데이터인 CreatedAt, UpdatedAt 필드는 Article의 속성이긴 하지만
하나로 묶을 수 있을 것 같다. 데이터가 가지는 공통 사항이 많은 것들은 데이터 클래스로 추출 해놨을 때 데이터의 이동이 좀 더 용이해진다.
authorName, authorMail 은 Author 클래스로 CreateAt, UpdatedAt 은 PostedAt 클래스로 추출 해보겠다.

##### Author.java
```java
package example_7_extract_class;

public class Author {

	private String authorName;
	private String authorMail;

	public Author(String authorName, String authorMail) {
		// TODO Auto-generated constructor stub
		this.authorName = authorName;
		this.authorMail = authorMail;
	}

	public String getAuthorName() {
		return authorName;
	}

	public String getAuthorMail() {
		return authorMail;
	}
}
```

##### PostedAt.java
```java
package example_7_extract_class;

import java.util.Date;

public class PostedAt {
	private Date CreatedAt;
	private Date UpdatedAt;
	public PostedAt() {
		super();
		CreatedAt = new Date(System.currentTimeMillis());
		UpdatedAt = new Date(System.currentTimeMillis());
	}
	public Date getCreatedAt() {
		return CreatedAt;
	}
	public Date getUpdatedAt() {
		return UpdatedAt;
	}
	public void setUpdatedAt(Date updatedAt) {
		UpdatedAt = updatedAt;
	}
}
```

##### Article.java(Author 와 PostedAt에게 필드 이동)
```java
package example_7_extract_class;

public class Article {
	private String title;
	private String content;
	private String password;
	private Author author;
	private PostedAt postedAt;

	public Article() {
		super();
	}
	public Article(String title, String content, String authorName, String authorMail) {
		super();
		this.title = title;
		this.content = content;
		this.author = new Author(authorName, authorMail);
		this.postedAt = new PostedAt();
	}
	public void print() {
		System.out.println("Article - title : "+title
				+"\ncontent : "+content
				+"\nauthorName : "+this.author.getAuthorName()
				+"\nauthorMail : "+this.author.getAuthorName()
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

	public Author getAuthor() {
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
필드만 이동 했을 뿐인데 지저분하게 널려있던 getter, setter가 많이 줄어들었다.
또한 PostedAt과 같은경우 article 의 업데이트 기능 구현시 해당 시스템 시간으로 업데이트 되어야 할것인데
이것 또한 article의 책임일 수 있지만 article의 기능으로 구현보다는 PostedAt으로 책임을 위임하는 것이
좀 더 간결하고 유연한 코드로 변할 수 있을 것이다.

만약 읽기 전용의 인스턴스로 만들고 싶을 때는 불변 인터페이스(immutable interface)를 이용할 수 있다.
Author 를 보자 작성자가 변경되는 일은 있을 수 없다(일반적으로). 그렇다면 변경이 되는건 이상동작일 가능성이 크고
굳이 변경이 되도록 해놓을 필요도없다.
아래는 불변 인터페이스를 이용한 읽기전용 Author 클래스를 작성한 코드다.
##### ImmutableAuthor(getter만 정의한 interface)
```java
package example_7_extract_class;

public interface ImmutableAuthor {
	public String getAuthorName();
	public String getAuthorMail();
}
```

##### Author(immutable interface 이용한 읽기전용 Author)
```java
package example_7_extract_class;

public class Author implements ImmutableAuthor{

	private String authorName;
	private String authorMail;

	public Author(String authorName, String authorMail) {
		// TODO Auto-generated constructor stub
		this.authorName = authorName;
		this.authorMail = authorMail;
	}

	public String getAuthorName() {
		return authorName;
	}

	public String getAuthorMail() {
		return authorMail;
	}

	public void setAuthorName(String authorName) {
		this.authorName = authorName;
	}

	public void setAuthorMail(String authorMail) {
		this.authorMail = authorMail;
	}

}

```
##### Article(읽기전용 Author 반환하도록 리팩토링)
```java
package example_7_extract_class;

public class Article {
	private String title;
	private String content;
	private String password;
	private Author author;
	private PostedAt postedAt;

	public Article() {
		super();
	}
	public Article(String title, String content, String authorName, String authorMail) {
		super();
		this.title = title;
		this.content = content;
		this.author = new Author(authorName, authorMail);
		this.postedAt = new PostedAt();
	}
	public void print() {
		System.out.println("Article - title : "+title
				+"\ncontent : "+content
				+"\nauthorName : "+this.author.getAuthorName()
				+"\nauthorMail : "+this.author.getAuthorName()
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
	public boolean isNull() {
		return false;
	}
}
```

##### 읽기전용 Author를 이용한 set
```java
articleManager.findArticleWithTitle(query).getAuthor().setAuthorName("kim");
```

ImmutableAuthor interface를 보면 getAuthorName,getAuthorMail처럼 getter만 정의 되어있다.
해당 인터페이스를 Author에 implement하면 해당 메서드는 무조건 구현 해야하는데 이때 setter들은 Author클래스만이 접근가능하고
ImmutableAuthor 에서는 정의가 되지 않았기 때문에 접근이 불가능하다.
그렇기에 Article에서 Author를 반환하는 getter에서 해당 interface를 반환하도록 하면 getter들만이 작성 되어있기에 해당 Author의 getter만이 호출 가능하다.

지금까지 클래스 추출에 대해 봤는데 이 또한 메서드 추출과 같이 너무 과하면 안좋다.
과해서 문제가 생길 경우 inner class로 넣어주던가 아니면 너무 작은 책임들은 해당 책임을 질만한 상위 클래스에 위임하고
삭제하는 역 리팩토링을 진행할 수 있다.
다음 포스팅은 분류 코드를 클래스로 치환하는 것에 대한 것이다.
