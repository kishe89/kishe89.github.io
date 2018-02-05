---
layout: post
title:  "Java Refactoring Replace type code with SubClass"
date:   2018-01-13 04:39:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Java
---

이전 포스팅에서 분류 코드를 클래스로 치환 하는 방법에 대해 알게 되었다.
글 마지막에 이야기 했듯이 단순 분류를 하는 것 이상으로 그 이후의 동작이(메소드)
필요하다면 단순 클래스로 치환보다는 하위 클래스로 치환 하는 것이 쉽게 해결할 수 있는 방법이다.
개인적인 생각으론 단순 분류 코드는 enum 을 이용한 정리가 더 의미상 깔끔하지 않을까 싶다.


##### 리팩토링 카탈로그(분류 코드를 하위 클래스로 치환)

|이름|분류 코드를 하위 클래스로 치환|
|---|---|
|상황|분류 코드마다 객체가 다른 동작을 함|
|문제|switch 문을 써서 동작을 구분함|
|해법|분류 코드를 하위 클래스로 치환해서 다형적 메서드를 작성함|

- 결과

  o 동작이 클래스별로 나뉨

  x 클래스 개수가 늘어남

- 방법
1. 분류 코드에 대응하는 하위 클래스 작성

    1. 분류 코드를 자기 캡슐화

        - 분류 코드를 나타내는 필드를 직접 보여주는 게 아니라 게터 메서드를 통해 보여주기

          자기 캡슐화 필드
    2. 분류 코드를 바탕으로 인스턴스를 작성하고 있다면 팩토리 메서드 작성

        - 생성자를 팩토리 메서드로 치환
    3. 분류 코드 값마다 하위 클래스 작성

        - 하위 클래스에서 분류 코드 게터 메서드를 오버라이드

          메서드 내리기
        - switch 문에 적힌 동작을 하위 클래스로 이동

          메서드 내리기
    4. 컴파일해서 테스트
2. 불필요한 필드 삭제

    1. 분류 코드 필드 삭제
    2. 기존 클래스의 분류 코드 게터 메서드를 추상 메서드로 만들기
    3. 컴파일해서 테스트
- 관련항목

    - 분류 코드를 클래스로 치환.

        동작이 규정되어 있지 않을 때 사용.
    - 자기 캡슐화 필드

        분류 코드를 나타내는 필드용으로 게터 메서드 작성
    - 메서드 내리기

        게터 메서드를 하위 클래스로 이동할 때나 switch 문에 적힌 동작을 하위 클래스로 이동할 때 사용
    - 생성자를 팩토리 메서드로 치환

        분류 코드를 기반으로 객체를 작성할 때 사용

##### Article.java
```java
package example_9_replace_typecode_subclass;

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
Article 지난 포스팅에서 작성한 Article class 이다. type code 를 클래스로 치환한 상태인데
Article 은 지금 타입 과 상관없이 동일한 print 양식으로 print 하고있다.
헌데 Article 이 각 타입별로 다르게 print 해주는 기능이 있는 Article 이라면
어떤 코드가 나타날까?

#####Article.java(타입 별 print)
```java
package example_9_replace_typecode_subclass;

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
		switch(articleType.getTypecode()) {
			case 0:
				System.out.println("MyArticle\n - title : "+title
						+"\ncontent : "+content
						+"\nauthorName : "+this.getAuthor().getAuthorName()
						+"\nauthorMail : "+this.getAuthor().getAuthorName()
						+"\nCreatedAt : "+this.postedAt.getCreatedAt()
						+"\nUpdatedAt : "+this.postedAt.getUpdatedAt()+"\n");
				break;
			case 1:
				System.out.println("Shared Article\n - title : "+title
						+"\ncontent : "+content
						+"\nauthorName : "+this.getAuthor().getAuthorName()
						+"\nauthorMail : "+this.getAuthor().getAuthorName()
						+"\nCreatedAt : "+this.postedAt.getCreatedAt()
						+"\nUpdatedAt : "+this.postedAt.getUpdatedAt()+"\n");
				break;
			case 2:
				System.out.println("Advertisement Article\n- title : "+title
						+"\n- content : "+content
						+"\n- nauthorName : "+this.getAuthor().getAuthorName()
						+"\n- nauthorMail : "+this.getAuthor().getAuthorName()
						+"\n- nCreatedAt : "+this.postedAt.getCreatedAt()
						+"\n- nUpdatedAt : "+this.postedAt.getUpdatedAt()+"\n");
				break;
			default: throw new IllegalArgumentException("typecode = "+articleType.getTypecode());
		}
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
앞에서 분류 코드를 ArticleType 클래스로 치환한 것이 오히려 print 를 작성하는데
안좋은 코드가 나오게 되었다. case 구문에는 상수가 와야하는데 상수를 정의하자니 이미 ArticleType에 정의 해놓았는데
또 해야하는 결과가 생기고 또한 키워드도 마땅치 않다.

일단 저 switch 문은 동작에는 문제가 없다. 하지만 화면은 자주 바뀌는 부분중 하나기에 출력 양식은
추가되거나 삭제되거나 하는 일이 분명히 많이 발생한다.
다시 초심으로 돌아가 type code 로 역 리팩토링을 진행해본다.

##### Article.java(typecode 다시 추가)
```java
package example_9_replace_typecode_subclass;

public class Article {
	private String title;
	private String content;
	private String password;
	private Author author;
	private PostedAt postedAt;
	public static final int MYARTICLE = 0;
	public static final int SHAREDARTICLE = 1;
	public static final int ADARTICLE = 2;
	private final int typecode;

	public Article() {
		super();
		this.typecode = MYARTICLE;
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
		switch(typecode) {
			case MYARTICLE:
				System.out.println("MyArticle\n - title : "+title
						+"\n- content : "+content
						+"\n- authorName : "+getAuthor().getAuthorName()
						+"\n- authorMail : "+getAuthor().getAuthorName()
						+"\n- CreatedAt : "+postedAt.getCreatedAt()
						+"\n- UpdatedAt : "+postedAt.getUpdatedAt()+"\n");
				break;
			case SHAREDARTICLE:
				System.out.println("Shared Article\n - title : "+title
						+"\ncontent : "+content
						+"\nauthorName : "+getAuthor().getAuthorName()
						+"\nauthorMail : "+getAuthor().getAuthorName()
						+"\nCreatedAt : "+postedAt.getCreatedAt()
						+"\nUpdatedAt : "+postedAt.getUpdatedAt()+"\n");
				break;
			case ADARTICLE:
				System.out.println("Advertisement Article\n- title : "+title
						+"\n- content : "+content
						+"\n- nauthorName : "+getAuthor().getAuthorName()
						+"\n- nauthorMail : "+getAuthor().getAuthorName()
						+"\n- nCreatedAt : "+postedAt.getCreatedAt()
						+"\n- nUpdatedAt : "+postedAt.getUpdatedAt()+"\n");
				break;
			default: throw new IllegalArgumentException("typecode = "+getTypecode());
		}
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
ArticleManager 와 Application 코드도 ArticleType 을 사용하지 말고
다시 분류코드를 기호상수로 치환한 코드를 이용하도록 변경한다.

switch 의 case 문에 기호 상수를 이용할 수 있게 되어 동일 의미의 기호상수로 전체를 묶는데는 아까
타입코드를 클래스로 치환한 코드보다는 보기 좋다.
하지만 결국 우리가 앞에서 분류 코드를 클래스로 치환 함으로써 해결했던 문제들이 다시 발생할 수 있다.

범위가 넘어가는 분류 코드가 넘어왔을 때 실행 시점에 알아차리게 되는 문제, 타입 분별이 안되는 문제 등이 발생할 수 있다.
분류는 필요하다 분명 이전에 분류코드를 치환한 코드는 분류된 객체가 다른 동작이 필요치 않은 경우 였다.
하지만 분류한 객체별 다른 동작이 필요하다면 서브클래스로의 치환을 고려해볼만 하다.

순서대로 해보자. 첫번째로는 분류 코드를 자기 캡슐화 할 것이다.

##### Article.java(switch(typecode) -> switch(getTypecode())
```java
package example_9_replace_typecode_subclass;

public class Article {
	private String title;
	private String content;
	private String password;
	private Author author;
	private PostedAt postedAt;
	public static final int MYARTICLE = 0;
	public static final int SHAREDARTICLE = 1;
	public static final int ADARTICLE = 2;
	private final int typecode;

	public Article() {
		super();
		this.typecode = MYARTICLE;
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
		switch(getTypecode()) {
			case MYARTICLE:
				System.out.println("MyArticle\n - title : "+title
						+"\n- content : "+content
						+"\n- authorName : "+getAuthor().getAuthorName()
						+"\n- authorMail : "+getAuthor().getAuthorName()
						+"\n- CreatedAt : "+postedAt.getCreatedAt()
						+"\n- UpdatedAt : "+postedAt.getUpdatedAt()+"\n");
				break;
			case SHAREDARTICLE:
				System.out.println("Shared Article\n - title : "+title
						+"\ncontent : "+content
						+"\nauthorName : "+getAuthor().getAuthorName()
						+"\nauthorMail : "+getAuthor().getAuthorName()
						+"\nCreatedAt : "+postedAt.getCreatedAt()
						+"\nUpdatedAt : "+postedAt.getUpdatedAt()+"\n");
				break;
			case ADARTICLE:
				System.out.println("Advertisement Article\n- title : "+title
						+"\n- content : "+content
						+"\n- nauthorName : "+getAuthor().getAuthorName()
						+"\n- nauthorMail : "+getAuthor().getAuthorName()
						+"\n- nCreatedAt : "+postedAt.getCreatedAt()
						+"\n- nUpdatedAt : "+postedAt.getUpdatedAt()+"\n");
				break;
			default: throw new IllegalArgumentException("typecode = "+getTypecode());
		}
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

이미 이전에 private final로 감추고 getter를 만들었기에 switch문만 수정했다.

두번째로 분류 코드를 바탕으로 인스턴스를 작성하는 팩토리 메서드를 작성하겠다.
ArticleManager 에게 Article 의 생성, 조회, 검색, 삭제 등을 맡겼기 때문에
ArticleManager 에 다음과 같이 createArticle 을 수정한다.

##### ArticleManager(createArticle(Article 팩토리 메서드) typecode에 따라 인스턴스 생성으로 수정)
```java
package example_9_replace_typecode_subclass;

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
	public Article createArticle(String title, String content, String authorName, String authorMail, int articleType) {
		switch(articleType) {
			case Article.MYARTICLE:
				this.list.add(new Article(title, content, authorName, authorMail, articleType));
				break;
			case Article.SHAREDARTICLE:
				this.list.add(new Article(title, content, authorName, authorMail, articleType));
				break;
			case Article.ADARTICLE:
				this.list.add(new Article(title, content, authorName, authorMail, articleType));
				break;
			default:
				throw new IllegalArgumentException("typecode : "+articleType);
		}
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

현재는 분류 코드에 따라 switch문에서 분기하여도 전부 Article을 생성하는데 이제 세번째로 분류 코드별로 하위 클래스를 작성한다.
그리고 switch문에서 해당 클래스를 생성하도록 변경한다.
##### MyArticle.java(Article extend, 다른 동작만 오버라이드)
```java
package example_9_replace_typecode_subclass;

public class MyArticle extends Article{


	public MyArticle(String title, String content, String authorName, String authorMail, int typecode) {
		super(title, content, authorName, authorMail, typecode);
		// TODO Auto-generated constructor stub
	}

	@Override
	public void print() {
		// TODO Auto-generated method stub
		System.out.println("MyArticle\n - title : "+getTitle()
				+"\n- content : "+getContent()
				+"\n- authorName : "+getAuthor().getAuthorName()
				+"\n- authorMail : "+getAuthor().getAuthorName()
				+"\n- CreatedAt : "+getPostedAt().getCreatedAt()
				+"\n- UpdatedAt : "+getPostedAt().getUpdatedAt()+"\n");
	}

	@Override
	public int getTypecode() {
		// TODO Auto-generated method stub
		return Article.MYARTICLE;
	}
}
```

##### SharedArticle
```java
package example_9_replace_typecode_subclass;

public class SharedArticle extends Article{


	public SharedArticle() {
		super();
		// TODO Auto-generated constructor stub
	}

	public SharedArticle(String title, String content, String authorName, String authorMail, int typecode) {
		super(title, content, authorName, authorMail, typecode);
		// TODO Auto-generated constructor stub
	}

	@Override
	public void print() {
		// TODO Auto-generated method stub
		System.out.println("Shared Article\n - title : "+getTitle()
				+"\ncontent : "+getContent()
				+"\nauthorName : "+getAuthor().getAuthorName()
				+"\nauthorMail : "+getAuthor().getAuthorName()
				+"\nCreatedAt : "+getPostedAt().getCreatedAt()
				+"\nUpdatedAt : "+getPostedAt().getUpdatedAt()+"\n");
	}

	@Override
	public int getTypecode() {
		// TODO Auto-generated method stub
		return Article.SHAREDARTICLE;
	}

}
```

##### AdArticle
```java
package example_9_replace_typecode_subclass;

public class AdArticle extends Article{


	public AdArticle(String title, String content, String authorName, String authorMail, int typecode) {
		super(title, content, authorName, authorMail, typecode);
		// TODO Auto-generated constructor stub

	}

	@Override
	public void print() {
		// TODO Auto-generated method stub
		System.out.println("Advertisement Article\n- title : "+getTitle()
				+"\n- content : "+getContent()
				+"\n- nauthorName : "+getAuthor().getAuthorName()
				+"\n- nauthorMail : "+getAuthor().getAuthorName()
				+"\n- nCreatedAt : "+getPostedAt().getCreatedAt()
				+"\n- nUpdatedAt : "+getPostedAt().getUpdatedAt()+"\n");
	}

	@Override
	public int getTypecode() {
		// TODO Auto-generated method stub
		return Article.SHAREDARTICLE;
	}

}
```

##### Article.java(abstract로 추상화)
```java
package example_9_replace_typecode_subclass;

public abstract class Article {
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

	public Article(String title, String content, String authorName, String authorMail, int typecode) {
		super();
		this.title = title;
		this.content = content;
		this.author = new Author(authorName, authorMail);
		this.postedAt = new PostedAt();
		this.typecode = typecode;
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
	public int getTypecode() {
		return typecode;
	}
	public boolean isNull() {
		return false;
	}

}
```

##### ArticleManager.java(typecode 별로 MyArticle,SharedArticle,AdArticle 생성)
```java
package example_9_replace_typecode_subclass;

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
	public Article createArticle(String title, String content, String authorName, String authorMail, int articleType) {
		switch(articleType) {
			case Article.MYARTICLE:
				this.list.add(new MyArticle(title, content, authorName, authorMail, articleType));
				break;
			case Article.SHAREDARTICLE:
				this.list.add(new SharedArticle(title, content, authorName, authorMail, articleType));
				break;
			case Article.ADARTICLE:
				this.list.add(new AdArticle(title, content, authorName, authorMail, articleType));
				break;
			default:
				throw new IllegalArgumentException("typecode : "+articleType);
		}
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

자 마지막으로 상위 클래스인 Article을 abstract로 추상화 하며 동작이 다른 즉 서브클래스에서 정의해야할 기능부분은
abstract method로 만들어 주고 해당 구현을 서브클래스에 맡겼다.
실행시켜보면 이전과 동일하게 동작함을 알 수 있다. 우리는 print라는 동작에서 switch를 제거 했는데
이 와중에 ArticleManager 의 팩토리 메서드에 switch 문이 추가 되었다.
사실 생성부분이고 생성 자체가 복잡해지거나 하는 일은 쉽게 일어나지 않고 또한
여기서 더 진행하면 물론 제거는 가능하겠지만 코드가 필요 이상으로 복잡해 질 수 있다.
그래도 한단계 더 나가서 제거해보자.
방법은 팩토리메서드를 팩토리 클래스로 치환하면 된다. 이번 포스팅의 내용 그대로 쭉 해보자.

##### ArticleFactory
```java
package example_9_replace_typecode_subclass;

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

##### ArticleManager.java
```java
package example_9_replace_typecode_subclass;

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
	public Article createArticle(String title, String content, String authorName, String authorMail,ArticleFactory factory) {
		this.list.add(factory.create(title, content, authorName, authorMail));
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

##### Application.java
```java
package example_9_replace_typecode_subclass;

public class Application {

	private static ArticleManager articlemanager;

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		articlemanager = ArticleManager.getInstance();
		articlemanager.createArticle("title1", "Hello World!", "alice", "alice@gmail.com", ArticleFactory.SharedArticleFactory.getInstance());
		articlemanager.createArticle("title2", "Hello World!!", "bobby", "bobby@gamil.com", ArticleFactory.MyArticleFactory.getInstance());
		articlemanager.createArticle("title3", "Hello World!!!", "bobby", "bobby@gamil.com", ArticleFactory.MyArticleFactory.getInstance());
		articlemanager.createArticle("title4", "Hello World!!!!", "bobby", "bobby@gamil.com", ArticleFactory.MyArticleFactory.getInstance());
		articlemanager.createArticle("title5", "Hello World!!!!!", "alice", "alice@gmail.com", ArticleFactory.SharedArticleFactory.getInstance());
		articlemanager.createArticle("AD", "Hello facebook", "facebook", "facebook@gmail.com", ArticleFactory.AdArticleFactory.getInstance());
		articlemanager.createArticle("???", "???????", "unknown", "unknown@gmail.com", ArticleFactory.AdArticleFactory.getInstance());

		articlemanager.printCurrentArticle();

	}
}

```

ArticleFactory에서 보면 각 Article들을 만들어내는 곳을 유심히 보자.
사실 Factory가 종류별로 준비 되었는데 분류 코드를 가지고 있을 필요는 없다.
굳이 확인해야 한다면 getTypecode()메서드를 이용하면 되니 생성자와 필드는 삭제해도 된다.
또한 팩토리를 던져줘야 하기 때문에 범위를 넘어가는 수치등으로 처리할 일도 사라졌다.
하지만 Application.java 코드를 보면 상당히 Factory호출 부분이 거슬린다.
그리고 클래스 갯수도 무지막지하게 늘어났다. 처음에 Article, ArticleType, ArticleManager, Application, NullArticle, Author, PostedAt
7개였던 클래스가 지금은 12개로 늘어났다. 단지 switch 문을 하나 없애자고 일어난 일이다.
물론 코드를 보는것과 앞으로 추가가 일어난다는 가정하에 좀 더 좋은 코드가 되긴 했다.
하지만 일어나지 않을일을 예단해서 과한 리팩토링을 하는건 극단적으로 이야기하면 지구 종말론을 믿으며 하루하루를 방탕하게 보내는 멍청이와 다름이없다.
특정 지점의 복잡정도는 줄어들 수 있지만 그만큼 구조적인 복잡정도가 올라가기때문에
리팩토링을 어디까지 해야할지는 프로젝트가 가지는 포커스에 따라 달라진다.
다음 포스팅은 분류 코드를 상태/전략 패턴으로 치환하는 것을 보겠다.
