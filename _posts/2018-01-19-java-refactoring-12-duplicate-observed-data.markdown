---
layout: post
title:  "Java Refactoring Duplicate Observed Data"
date:   2018-01-19 18:41:00
author: 김지운
cover:  "/assets/instacode.png"
---

소프트웨어에서 어떤 객체에서 일어나는 일들(관측 데이터)을 다른 객체에게 알려줘야 하는 상황들이 빈번하게 일어난다.
우리는 ArticleManager 가 Article 들을 전부 관리하도록 했습니다. ArticleManager 가 관리하고 있는 Article 들이
업데이트(변경)이 이루어질 때 print 를 해줘야 하는데 print 할 device 가 바쁘다면 ArticleManager 가 그저 print 를 호출하는건 옳바른 동작을 보장할 수 없을것이다.
print 될 device 를 관리하는 객체에서 바쁘지 않을 때(실행 가능할 때) print 를 하는 것이 올바른 동작일 것이다.
데이터의 update 이벤트가 발생하는 지에 대해서 print 할 device 객체인 B 에서 확인할 수 있어야 한다.
이를 위해 관찰자 패턴(Observer pattern)이나 이벤트 리스너가 필요해진다.
이전까진 Article 자체가 print 를 하도록 했지만 예를 위해서 console 에 print 를 행할 객체를 하나 만들도록 한다.
그 이후 리팩토링을 진행해본다.


##### 리팩토링 카탈로그(관측 데이터 복제(Duplicate Observed Data))

|이름|관측 데이터 복제|
|---|---|
|상황|데이터를 표시하는 클래스가 있음|
|문제|모델과 뷰가 한 클래스 안에 뒤섞여 있음|
|해법|양쪽을 분리하고 관찰자 패턴 또는 이벤트 리스너로 동기화하|

- 결과

  o 클래스 역할이 확실해짐

  o 여러 뷰를 가지거나 뷰를 전환하기 쉬워짐

  x 클래스 숫자가 늘어남

  x 주의하지 않으면 동기화 이벤트가 무한히 발생할 수 있음

- 방법
1. 모델을 나타내는 클래스 작성

   1. 클래스 추출
   2. 뷰:뷰에서 모델 참조
   3. 뷰:모델을 메서드로 조작
   4. 컴파일해서 테스트
2. 통지 관련 클래스와 인터페이스 작성

   1. 통지 내용을 나타내는 이벤트 선언
   2. 통지 관련 인터페이스 선언
   3. 통지를 받는 메서드를 뷰에 선언
   4. 컴파일해서 테스트
3. 뷰 등록과 뷰 통지

   1. 모델:뷰를 모델에 등록 가능하게 만듦
   2. 뷰:뷰를 모델에 등록
   3. 모델:모델을 변경하면 뷰에 통지하는 코드 작성
   4. 뷰:통지를 받는 메서드 안으로 표시 갱신 처리를 이동
   5. 컴파일해서 테스트

- 관련항목

    - 클래스 추출

      모델과 뷰가 뒤섞인 클래스에서 모델이 되는 클래스 추출
    - 자기 캡슐화 필드

      필드를 직접 다루던 코드에서 게터 메서드나 세터 메서드를 이용하도록 수정
    - 프레젠테이션과 도메인 분리

      관측 데이터 복제와 비슷한 문제를 다루지만 더 큰 리팩토링

##### ConsoleView
```java
package example_13_duplicate_observed_data;

import java.util.ArrayList;

public abstract class ConsoleView {
	public String header;
	public String footer;
	public abstract void print(Article article);
	public interface UpdateListener{
		public boolean OnUpdate(ArrayList<Article> articles);
	}
	public String getHeader() {
		return header;
	}
	public String getFooter() {
		return footer;
	}
	public void setHeader(String header) {
		this.header = header;
	}
	public void setFooter(String footer) {
		this.footer = footer;
	};

}
```

ConsoleView 라는 클래스를 하나 작성하였다.

물론 이미 있는 GUI 라이브러리들을 사용하거나 하는 방법도 괜찮지만 공부를 위함이므로 하나 만들자.
ConsoleView 는 앞으로 생성할 MyArticleView, SharedArticleView, AdArticleView 의 상위 클래스로
console 에 view 마다 띄워줄 header, footer String 을 가지며 view 에 실제 print 를 요청할 인터페이스 UpdateListener
를 가진다.
그리고 이벤트가 OnUpdate 메서드를 통해 전달되면 실제 console 에 print 하는 print 메서드를 구현하도록 강제하였다.

Article 에서는 print 메서드가 필요가 없다 우리는 view 객체를 만들어서 해당 view 에게 print 할 책임을 줄것이다.
그러므로 Article 의 print 메서드를 삭제하고 일단 ConsoleView 를 상속받는 MyArticleView 를 하나 만든다.

##### MyArticleView
```java
package example_13_duplicate_observed_data;

import java.util.ArrayList;

public class MyArticleView extends ConsoleView implements ConsoleView.UpdateListener{

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

	@Override
	public boolean OnUpdate(ArrayList<Article> articles) {
		// TODO Auto-generated method stub
		if(articles != null) {
			for(Article article : articles) {
				print(article);
			}
			return true;
		}
		return false;
	}

	@Override
	public String getHeader() {
		// TODO Auto-generated method stub
		return super.getHeader();
	}

	@Override
	public String getFooter() {
		// TODO Auto-generated method stub
		return super.getFooter();
	}

	@Override
	public void setHeader(String header) {
		// TODO Auto-generated method stub
		super.setHeader(header);
	}

	@Override
	public void setFooter(String footer) {
		// TODO Auto-generated method stub
		super.setFooter(footer);
	}


}
```

전체 흐름은 Application 에서 뷰 객체 생성, Article 생성 -> ArticleManager 의 setUpdateListener 를 통해 listener 설정 -> ArticleManager 의 notifyDataSetChanged() 를 호출하여 업데이트 이벤트 발생
-> MyArticleView 는 OnUpdate 를 통해 전달받은 이벤트 객체를 print

이다.

##### ArticleManager
```java
package example_13_duplicate_observed_data;

import java.util.ArrayList;

import example_13_duplicate_observed_data.ConsoleView.UpdateListener;

public class ArticleManager {
	private static final ArticleManager instance = new ArticleManager();
	private ArrayList<Article> list = new ArrayList<>();
	private UpdateListener listener;

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
	public ManagedArticle removeArticle() throws NullPointerException {
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
	public void setList(ArrayList<Article> list) {
		this.list = list;
	}
	public ArrayList<Article> getList() {
		return list;
	}
	public void notifyDataSetChanged() {
		if(listener == null) {
			throw new NullPointerException("listener is null. please call setUpdateListener method");
		}

		if(!this.listener.OnUpdate(list)) {
			System.out.println("update denied");
		}
	}
	public void setUpdateListener(UpdateListener listener) {
		this.listener = listener;
	}

}
```
ArticleManager 에는 notifyDataSetChanged(), setUpdateListener(), listener 가 새로 정의되었다.

##### Application
```java
package example_13_duplicate_observed_data;

public class Application {

	private static ArticleManager articlemanager;

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		articlemanager = ArticleManager.getInstance();
		MyArticleView view = new MyArticleView();
		articlemanager.createArticle("title1", "Hello World!", "alice", "alice@gmail.com", ArticleTypeEnum.SharedArticle );
		articlemanager.createArticle("title2", "Hello World!!", "bobby", "bobby@gamil.com", ArticleTypeEnum.MyArticle);
		articlemanager.createArticle("title3", "Hello World!!!", "bobby", "bobby@gamil.com", ArticleTypeEnum.MyArticle);
		articlemanager.createArticle("title4", "Hello World!!!!", "bobby", "bobby@gamil.com", ArticleTypeEnum.MyArticle);
		articlemanager.createArticle("title5", "Hello World!!!!!", "alice", "alice@gmail.com", ArticleTypeEnum.MyArticle);
		articlemanager.createArticle("AD", "Hello facebook", "facebook", "facebook@gmail.com", ArticleTypeEnum.AdArticle);
		articlemanager.setUpdateListener(view);
		articlemanager.notifyDataSetChanged();
	}
}
```
Application 에서는 위와 같이 동작하게 된다.
동작을 해보면 문제를 느낄 것이다. 바로 view 의 타입을 바꾸게 되면 전부 바뀌게 되는 문제점인데
이제 이를 해결해본다.
Article 의 타입에 따라 ConsoleView 를 생성해줘야하는데 그렇다면 Article 의 갯수만큼의 ConsoleView 객체가 필요할 것이다.
또한 articleManager 는 이러한 사항들을 모두 알고있어야한다.

이를 알고 있을 ArticleAdapter 를 만든다.

##### ArticleAdapter
```java
package example_13_duplicate_observed_data;

import java.util.ArrayList;

public class ArticleAdapter implements AdapterUpdateListener{
	private ArrayList<ConsoleView> row;

	public ArticleAdapter() {
		super();
		row = new ArrayList<>();
	}

	@Override
	public void updateData(ArrayList<Article> articles) {
		// TODO Auto-generated method stub
		for(Article article : articles) {
			createView(article);
		}
	}
	@Override
	public void createView(Article article) {
		// TODO Auto-generated method stub
		ConsoleView view = article.getType().createView();
		row.add(view);
		bindData(view, article);
	}

	@Override
	public void bindData(ConsoleView view,Article article) {
		// TODO Auto-generated method stub
		view.setBody(article);
		print(view);
	}

	@Override
	public void print(ConsoleView view) {
		// TODO Auto-generated method stub
		view.print();
	}
}
```
##### AdapterUpdateListener
```java
package example_13_duplicate_observed_data;

import java.util.ArrayList;

public interface AdapterUpdateListener {
	public void updateData(ArrayList<Article> articles);
	public void createView(Article articles);
	public void bindData(ConsoleView view, Article articles);
	public void print(ConsoleView view);
}
```
##### ArticleManager
```java
package example_13_duplicate_observed_data;

import java.util.ArrayList;

public class ArticleManager {
	private static final ArticleManager instance = new ArticleManager();
	private ArrayList<Article> list = new ArrayList<>();
	private AdapterUpdateListener adapter;
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
	public ManagedArticle removeArticle() throws NullPointerException {
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
	public void setList(ArrayList<Article> list) {
		this.list = list;
	}
	public ArrayList<Article> getList() {
		return list;
	}
	public void notifyDataSetChanged() {
		if(adapter == null) {
			throw new NullPointerException("listener is null. please call setUpdateListener method");
		}
		this.adapter.updateData(list);
	}
	public void setAdapter(AdapterUpdateListener adapter) {
		this.adapter = adapter;
	}
}
```

##### ArticleTypeEnum
```java
package example_13_duplicate_observed_data;

public enum ArticleTypeEnum {
	MyArticle{

		@Override
		public ConsoleView createView() {
			// TODO Auto-generated method stub
			return new MyArticleView();
		}

	},
	SharedArticle{

		@Override
		public ConsoleView createView() {
			// TODO Auto-generated method stub
			return new ShareArticleView();
		}

	},
	AdArticle{

		@Override
		public ConsoleView createView() {
			// TODO Auto-generated method stub
			return new AdArticleView();
		}

	};
	public abstract ConsoleView createView();
}
```


ArticleManager 의 notifyDataSetChanged 를 호출하게 되면 set 되어있는 adapter 에게
updateData 메서드를 통해 이벤트를 발생시키는데 이때 변경된 DataSet 인 list 를 전달하고
adapter 에서는 전달된 list 의 article 을 가지고 createView 를 호출하여
ConsoleView 를 생성한다.(실제 타입에 맞는 view)

##### MyArticleView
```java
package example_13_duplicate_observed_data;

public class MyArticleView extends ConsoleView {

	@Override
	public void print() {
		// TODO Auto-generated method stub
		System.out.println("MyArticle\n - title : "+super.body.getTitle()
		+"\n- content : "+super.body.getContent()
		+"\n- authorName : "+super.body.getAuthor().getAuthorName()
		+"\n- authorMail : "+super.body.getAuthor().getAuthorName()
		+"\n- CreatedAt : "+super.body.getPostedAt().getCreatedAt()
		+"\n- UpdatedAt : "+super.body.getPostedAt().getUpdatedAt()+"\n");
	}

	@Override
	public String getHeader() {
		// TODO Auto-generated method stub
		return super.getHeader();
	}

	@Override
	public String getFooter() {
		// TODO Auto-generated method stub
		return super.getFooter();
	}

	@Override
	public void setHeader(String header) {
		// TODO Auto-generated method stub
		super.setHeader(header);
	}

	@Override
	public void setFooter(String footer) {
		// TODO Auto-generated method stub
		super.setFooter(footer);
	}
}
```

각각의 뷰는 위 MyArticleView 와 같은 형태이다.
createView 에서는 view 를 생성하고 bindData 를 호출 하는데
bindData 에서는 실제 데이터를 view 에 등록해준다. 그 후 print 를 호출하는데
이 때 xxxView.print() 를 호출하게 된다.

우리는 ArticleManager 를 수정하고 ArticleAdapter 를 만들고 xxxView 를 만들어서 실행했지만
결과는 이전과 동일하다.
그러나 이러한 작업을 통해서 역할을 나누고 책임을 나누어서 각각의 수정 및 추가가 쉽게 되었다.
예를 들어서 새로운 양식의 Article 뷰를 만들고 싶으면 ConsoleView 를 상속받는 다른 view 만 작성하고 ArticleTypeEnum 에 추가만 해주면된다.
Article 을 관리하는데 있어서 새로운 기능 rangeUpdate 등을 구현하는 것은 ArticleManager 에 구현하면된다.
또한 뷰의 타입문제도 해결이 되었다.
네이밍은 약간 수정해야 겠지만 유연성은 확실히 좋아졌다.
다음 포스팅에서는 상속을 위임으로 치환하는 방법에 대해서 쓰겠다.
