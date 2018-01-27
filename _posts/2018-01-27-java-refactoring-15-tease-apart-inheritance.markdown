---
layout: post
title:  "Java Refactoring Tease Apart Inheritance"
date:   2018-01-27 13:51:00
author: 김지운
cover:  "/assets/instacode.png"
---

상속은 더 적은 코드를 가지고 기존보다 많은 기능, 다양한 기능을 구현하는데 좋은 도구이다.
하지만 모든 코드를 계층 구조를 만들면 각각의 클래스는 실제 하는일이 없어진다던가 하여 하는 역할이 모호해질 수 있다.

그러면 아래와 같은 문제가 발생한다.

- 클래스 계층의 어디에 새 기능을 넣어야 할 지 알기 어려움
- 이용하고 싶은 코드가 (부모가 아닌)형제 클래스에 있어서 상속으로 이용할 수 없음

모든 설계는 완벽할 수 없으며 리팩토링은 필수 불가결이다.
아무리 TDD 를 통해서 처음부터 어느정도의 코드품질을 보장하더라도 내가 TDD 를 통해서 코드를 작성할 때의 요구사항과
지금의 요구사항은 달라질 수 있다.

결국 처음부터 개발할 것이 아니면 기존 코드에 대해서 지속적인 리팩토링은 이러한 요구사항의 변경을 따라가기 위해서 필수적으로 해야할 것이다.

이번에는 클래스 계층에서 하는 일을 정리하고 해당 작업, 필드끼리 공통된걸 찾아 새로운 클래스를 작성하여 이임을 써서 클래스의 엉킨 상속을 풀어낸다.


##### 리팩토링 카탈로그(상속 구조 정리(Tease Apart Inheritance))

|이름|상속 구조 정리|
|---|---|
|상황|클래스 계층 하나에 많은 클래스가 존재함|
|문제|클래스 계층 하나에서 다양한 작업을 함|
|해법|상속을 분할하고 필요한 작업은 위임을 사용해 이용함|

- 결과

  o 부적절한 상속 관계를 해소 가능

  o 클래스 개선, 기능 추가가 편해짐

  x 클래스 개수가 늘기도 함

- 방법
1. 어떤 작업을 이동할지 결정

   1. 기존 클래스 계층에서 하던 작업 나열
   2. 이동할 작업 판단
2. 위임 처리

   1. 이동할 작업을 나타내는 클래스를 새로 작성
   2. 기존 클래스 계층에서 클래스 추출
   3. 위임할 필드 작성
3. 새로운 상속 구성

   1. 기존 클래스 계층의 하위 클래스에 대응하는 새로운 클래스의 하위 클래스 작성
   2. 기존 하위 클래스에서 새로운 하위 클래스로 메서드 이동
4. 추가 리팩토링

   1. 하위 클래스에 메서드가 남아 있지 않다면 하위 클래스 작성
   2. 메서드 올리기 또는 메서드 내리기 실시

- 관련항목

    - 클래스 추출

      클래스 계층 내부에서 단위 작업을 추출할 때 사용

    - 클래스 이동

      메서드를 다른 클래스 계층으로 이동할 때 사용
    - 필드 이동

      필드를 다른 클래스 계층으로 이동할 때 사용
    - 메서드 올리기

      하위 클래스에 흩어진 공통 메서드를 상위 클래스에 모을 때 사용
    - 필드 올리기

      하위 클래스에 흩어진 공통 필드를 상위 클래스에 모을 때 사용
    - 상속을 위임으로 치환

      역 리팩토링
    - 브리지(Bridge) 패턴

      상속 구조 정리에 따라 만들어지는 패턴


##### Job
```java
package example_16_tease_apart_Inheritance;

public class Job {

}
```
##### HardJob
```java
package example_16_tease_apart_Inheritance;

public class HardJob extends Job{

}
```
##### SoftJob
```java
package example_16_tease_apart_Inheritance;

public class SoftJob extends Job{

}
```
##### AlphaStyleHardJob
```java
package example_16_tease_apart_Inheritance;

public class AlpahStyleHardJob extends HardJob{

}
```
##### AlphaStyleSoftJob
```java
package example_16_tease_apart_Inheritance;

public class AlphaStyleSoftJob extends SoftJob{

}
```
와 같이 Job 에 대해서 매핑을 했다고 했을 때 Job 의 종류를 상속을 통해 나타낸것 까지는 괜찮아 보인다.
하지만 이러한 Job 의 종류가 늘어나고 Style 이 Alpha, Beta 외에 늘어날 때
이는 중복코드로 이어질 여지가 보인다.

이럴때 Style 객체를 만들어서 Job 이 위임필드로 가지는 상속 구조를 위임으로 치환하게 되면 중복코드가 줄어들 것이다.

이에 대한 예제는 자바로 배우는 리팩토링 입문(길벗 출판, 히로 유키시 지음,서수환 옮김)에서 가져오겠다.

CSV(Comma Separated Value)를 파싱하여 표시하는 프로그램을 만들어 볼것이다.
CSV(Comma Separated Value)는 ,로 값을 구분하는 문서 포맷이다(스프레드 시트 문서, 엑셀 문서등).

처음 만들 클래스들은 아래 표와 같다.

|클래스명|역할|
|---|---|
|CSVReader|CSV를 읽는 추상 클래스|
|CSVStringReader|CSV 문자열을 읽는 클래스|
|CSVFileReader|CSV 파일을 읽는 클래스|
|CSVStringTablePrinter|CSV 문자열을 읽어서 표 형식으로 표시하는 클래스|
|CSVFileTreePrinter|CSV 파일을 읽어서 트리 형식으로 표시하는 클래스|
|Application|동작 확인용 클래스|

표의 클래스명을 봐서는 의미를 파악하고 하는데 문제없는 깔끔한 클래스 같다.
하지만 이름 내에서 중복된 기능을 할거같은 이름들이 보인다.

일단 처음 개발한 프로그램을 본다.

##### CSVReader
```java
import java.io.*;
import java.util.regex.*;

public abstract class CSVReader {
    protected static final Pattern CSV_PATTERN = Pattern.compile("\\s*,\\s*");
    public abstract String[] readCSV() throws IOException;
    public abstract void close() throws IOException;
}
```
##### CSVStringReader
```java
package example_16_tease_apart_Inheritance;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.StringReader;

public class CSVStringReader extends CSVReader{

	private final BufferedReader bufReader;

	public CSVStringReader(String filename) throws IOException{
		bufReader = new BufferedReader(new StringReader(filename));
	}

	@Override
	public String[] readCSV() throws IOException {
		// TODO Auto-generated method stub
		String line = bufReader.readLine();
		if(line == null) {
			return null;
		}else {
			String []item = CSV_PATTERN.split(line);
			return item;
		}
	}

	@Override
	public void close() throws IOException {
		// TODO Auto-generated method stub
		bufReader.close();
	}

}
```
##### CSVFileReader
```java
package example_16_tease_apart_Inheritance;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class CSVFileReader extends CSVReader{

	private final BufferedReader bufReader;

	public CSVFileReader(String filename) throws IOException{
		bufReader = new BufferedReader(new FileReader(filename));
	}

	@Override
	public String[] readCSV() throws IOException {
		// TODO Auto-generated method stub
		String line = bufReader.readLine();
		if(line == null) {
			return null;
		}else {
			String[] item = CSV_PATTERN.split(line);
			return item;
		}
	}

	@Override
	public void close() throws IOException {
		// TODO Auto-generated method stub
		bufReader.close();
	}

}
```
##### CSVFileTreePrinter
```java
package example_16_tease_apart_Inheritance;

import java.io.IOException;

public class CSVFileTreePrinter extends CSVFileReader{

	public CSVFileTreePrinter(String filename) throws IOException {
		super(filename);
		// TODO Auto-generated constructor stub
	}
	public void print() throws IOException{
		String[] prevItem = new String[0];
		for(int row = 0; true; row++) {
			String[] item = readCSV();
			if(item == null) {
				break;
			}
			boolean justprint = false;
			for(int column = 0; column < item.length ; column++) {
				if(justprint) {
					print_line(column,item[column]);
				}else {
					if(prevItem.length <= column || item[column].equals(prevItem[column])) {
						print_line(column,item[column]);
						justprint = true;
					}
				}
				prevItem = item;
			}
		}
		close();
	}
	private void print_line(int indent, String string) {
		// TODO Auto-generated method stub
		for(int i = 0 ; i < indent ; i++) {
			System.out.print("    ");
		}
		System.out.println(string);
	}
}
```
##### CSVStringTablePrinter
```java
package example_16_tease_apart_Inheritance;

import java.io.IOException;

public class CSVStringTablePrinter extends CSVStringReader{

	public CSVStringTablePrinter(String filename) throws IOException {
		super(filename);
		// TODO Auto-generated constructor stub
	}
	public void print() throws IOException{
		System.out.println("<table>");
		for(int row = 0; true; row++) {
			String[] item = readCSV();
			if(item == null) {
				break;
			}
			System.out.println("<tr>");
			for(int column = 0; column < item.length ; column++) {
				System.out.print("<td>");
				System.out.print(item[column]);
				System.out.print("</td>");
			}
			System.out.println("</tr>");
		}
		System.out.println("</table>");
		close();
	}

}
```
##### Application
```java
package example_16_tease_apart_Inheritance;

import java.io.IOException;

public class Application {

	private static final String SAMPLE_CSV_STRING =
			"좋은 아침입니다.,Good morning.\n"
			+"안녕하세요~,Hello.\n"
			+"안녕하세요.,Good evening.\n"
			+"안녕히 주무세요.,Good night.\n";
	private static final String SAMPLE_CSV_FILE = "file.csv";
	public static void main(String[] args) throws IOException{
		// TODO Auto-generated method stub
		new CSVStringTablePrinter(SAMPLE_CSV_STRING).print();
		new CSVFileTreePrinter(SAMPLE_CSV_FILE).print();
	}

}
```
일단 돌아가는 프로그램을 짰다. 우리가 원하는 기능은 정상적으로 돌아간다.

하지만 이프로그램은 몇가지 부분에서 유연하지 못하며 불필요한 중복이 있다.
Printer 들은 출력과 입력(read)가 혼재하고있다. 그리고 File 을 읽던 String 을 읽던
서로간에 출력 Style 을 변경하기 위해서는 각각 Printer 들에 다시 작성해야한다.

이 부분을 리팩토링 해본다.

일단 print 기능을 위임할 CSVPrinter 클래스를 작성한다.
##### CSVPrinter
```java
package example_16_tease_apart_Inheritance;

import java.io.IOException;

public abstract class CSVPrinter {

	protected final CSVReader csvReader;

	public CSVPrinter(CSVReader csvReader) {
		super();
		this.csvReader = csvReader;
	}
	public abstract String[] readCSV()throws IOException;
	public abstract void print()throws IOException;
}
```
CSVPrinter 는 print 에 필요한 내용을 추상하환 추상클래스이다.
이제 출력 클래스를 작성했으니 기존 클래스의 상속을 변경한다.

##### CSVFileTreePrinter
```java
package example_16_tease_apart_Inheritance;

import java.io.IOException;

public class CSVFileTreePrinter extends CSVPrinter{


	public CSVFileTreePrinter(CSVReader csvReader) {
		super(csvReader);
		// TODO Auto-generated constructor stub
	}
	@Override
	public void print() throws IOException{
		String[] prevItem = new String[0];
		for(int row = 0; true; row++) {
			String[] item = readCSV();
			if(item == null) {
				break;
			}
			boolean justprint = false;
			for(int column = 0; column < item.length ; column++) {
				if(justprint) {
					print_line(column,item[column]);
				}else {
					if(prevItem.length <= column || item[column].equals(prevItem[column])) {
						print_line(column,item[column]);
						justprint = true;
					}
				}
				prevItem = item;
			}
		}
		csvReader.close();
	}
	private void print_line(int indent, String string) {
		// TODO Auto-generated method stub
		for(int i = 0 ; i < indent ; i++) {
			System.out.print("    ");
		}
		System.out.println(string);
	}
	@Override
	public String[] readCSV() throws IOException {
		// TODO Auto-generated method stub
		return csvReader.readCSV();
	}
}
```
##### CSVStringTablePrinter
```java
package example_16_tease_apart_Inheritance;

import java.io.IOException;

public class CSVStringTablePrinter extends CSVPrinter{

	public CSVStringTablePrinter(CSVReader csvReader) {
		super(csvReader);
		// TODO Auto-generated constructor stub
	}
	@Override
	public void print() throws IOException{
		System.out.println("<table>");
		for(int row = 0; true; row++) {
			String[] item = readCSV();
			if(item == null) {
				break;
			}
			System.out.println("<tr>");
			for(int column = 0; column < item.length ; column++) {
				System.out.print("<td>");
				System.out.print(item[column]);
				System.out.print("</td>");
			}
			System.out.println("</tr>");
		}
		System.out.println("</table>");
		csvReader.close();
	}

	@Override
	public String[] readCSV() throws IOException {
		// TODO Auto-generated method stub
		return csvReader.readCSV();
	}

}
```
##### Application
```java
package example_16_tease_apart_Inheritance;

import java.io.IOException;

public class Application {

	private static final String SAMPLE_CSV_STRING =
			"좋은 아침입니다.,Good morning.\n"
			+"안녕하세요~,Hello.\n"
			+"안녕하세요.,Good evening.\n"
			+"안녕히 주무세요.,Good night.\n";
	private static final String SAMPLE_CSV_FILE = "file.csv";
	public static void main(String[] args) throws IOException{
		// TODO Auto-generated method stub
		new CSVStringTablePrinter(new CSVStringReader(SAMPLE_CSV_STRING)).print();
		new CSVFileTreePrinter(new CSVFileReader(SAMPLE_CSV_FILE)).print();
	}

}
```
CSVPrinter 에게 print 를 하는 역할을 하도록 하고 Reader 위임필드를 생성하여 Printer 가 Reader 를 상속받는
일 은 없어졌다.
또한 각각의 Reader 를 전달하면서 Reader 를 교체할 수 있는 상황이 되었지만 이름에서 아직 문제가 있다.
일단 이부분은 두고 Reader 들을 본다.

각 Reader 들은 거의 대부분이 중복 코드이다. 그러므로 상위 클래스인 CSVReader 로 메서드와 필드를 올리는 것을 고려할 수 있다.

##### CSVReader
```java
package example_16_tease_apart_Inheritance;
import java.io.*;
import java.util.regex.*;

public class CSVReader {
	protected static final Pattern CSV_PATTERN = Pattern.compile("\\s*,\\s*");
	protected BufferedReader bufReader;
	protected CSVReader(BufferedReader bufReader) {
		this.bufReader = bufReader;
	}
	public String[] readCSV() throws IOException {
		// TODO Auto-generated method stub
		String line = bufReader.readLine();
		if(line == null) {
			return null;
		}else {
			String[] item = CSV_PATTERN.split(line);
			return item;
		}
	}
	public void close() throws IOException {
		// TODO Auto-generated method stub
		bufReader.close();
	}
}
```
##### CSVStringReader
```java
package example_16_tease_apart_Inheritance;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.StringReader;

public class CSVStringReader extends CSVReader{

	protected CSVStringReader(String string) throws IOException {
		super(new BufferedReader(new StringReader(string)));
		// TODO Auto-generated constructor stub
	}
}
```
##### CSVFileReader
```java
package example_16_tease_apart_Inheritance;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class CSVFileReader extends CSVReader{

	protected CSVFileReader(String filename) throws IOException {
		super(new BufferedReader(new FileReader(filename)));
		// TODO Auto-generated constructor stub
	}
}
```
Reader 로 메서드와 필드를 올려서 각각의 Reader 들의 중복코드가 많이 제거 되었다.
그럼에도 동작은 그대로이다.

이제 아까 남겨두었던 Printer 부분을 다시 보자.
우리는 각각의 리더를 전달하여 스타일 변경을 이룰 수 있다. 그러므로 이름을 변경해준다.
각각 CSVStringTablePrinter -> CSVTablePrinter, CSVFileTreePrinter -> CSVTreePrinter 로
변경하면 될 것 같다.

##### Application
```java
package example_16_tease_apart_Inheritance;

import java.io.IOException;

public class Application {

	private static final String SAMPLE_CSV_STRING =
			"좋은 아침입니다.,Good morning.\n"
			+"안녕하세요~,Hello.\n"
			+"안녕하세요.,Good evening.\n"
			+"안녕히 주무세요.,Good night.\n";
	private static final String SAMPLE_CSV_FILE = "file.csv";
	public static void main(String[] args) throws IOException{
		// TODO Auto-generated method stub
		new CSVTablePrinter(new CSVFileReader(SAMPLE_CSV_FILE)).print();
		new CSVTreePrinter(new CSVStringReader(SAMPLE_CSV_STRING)).print();
	}

}
```
변경한 후 Application 에서 호출하는 부분을 변경해서 컴파일 후 테스트 해보면 우리는 Printer 에게 어떤 Reader 를 주냐에 따라
섞어서 출력할 수 있다.

좀 더 나아가보면 Printer 들이 Reader 를 가지고 있을 필요는 없다. 단지 print 할 데이터가 필요한데 이를 Reader 가 가지고있다.
##### CSVPrinter
```java
package example_16_tease_apart_Inheritance;

import java.io.IOException;

public abstract class CSVPrinter {

	public CSVPrinter() {
	}
	public abstract String[] readCSV(CSVReader csvReader)throws IOException;
	public abstract void print(CSVReader csvReader)throws IOException;
}
```
위 CSVPrinter 와 같이 변경하면 print 에 csvReader 를 넘겨주니 위임필드가 필요가 없다.
헌데 이러니 위임메서드인 readCSV 도 굳이 Printer 에 있어야하나 싶다.
또한 CSVReader 를 print 에서 받는 것도 큰 문제는 아니지만 이상하다.
또한 CSVReader 의 Buffer 를 close 해주는걸 print 에서 해주는 것도 이상하다.

이 부분은 CSVReader 에서 데이터를 전부 읽으면 모아서 보내주면 될 것 같다.
묶어서 사용하기 위해 ArrayList 를 이용한다.

##### CSVPrinter
```java
package example_16_tease_apart_Inheritance;

import java.io.IOException;
import java.util.ArrayList;

public abstract class CSVPrinter {

	public CSVPrinter() {
	}
	public abstract void print(ArrayList<ArrayList<String>> itemList)throws IOException;
}
```
##### CSVReader
```java
package example_16_tease_apart_Inheritance;
import java.io.*;
import java.util.ArrayList;
import java.util.regex.*;

public class CSVReader {
	protected static final Pattern CSV_PATTERN = Pattern.compile("\\s*,\\s*");
	protected BufferedReader bufReader;
	protected CSVReader(BufferedReader bufReader) {
		this.bufReader = bufReader;
	}
	public ArrayList<ArrayList<String>> readCSV() throws IOException {
		// TODO Auto-generated method stub
		ArrayList<ArrayList<String>> arr = new ArrayList<>();
		while(true) {
			String line = bufReader.readLine();
			if(line == null) {
				break;
			}else {
				String [] item = CSV_PATTERN.split(line);
				ArrayList<String> subarr = new ArrayList<>();
				for(String s : item) {
					subarr.add(s);
				}
				arr.add(subarr);
			}
		}
		close();
		return arr;
	}
	private void close() throws IOException {
		// TODO Auto-generated method stub
		bufReader.close();
	}
}
```
##### CSVTreePrinter
```java
package example_16_tease_apart_Inheritance;

import java.io.IOException;
import java.util.ArrayList;

public class CSVTreePrinter extends CSVPrinter{


	public CSVTreePrinter() {
		// TODO Auto-generated constructor stub
	}
	@Override
	public void print(ArrayList<ArrayList<String>> itemList) throws IOException{
		ArrayList<String> prevItem = new ArrayList<>();
		for(int row = 0; row < itemList.size(); row++) {
			ArrayList<String>item = itemList.get(row);

			boolean justprint = false;
			for(int column = 0; column < item.size() ; column++) {
				if(justprint) {
					print_line(column,item.get(column));
				}else {
					if(prevItem.size() <= column || item.get(column).equals(prevItem.get(column))) {
						print_line(column,item.get(column));
						justprint = true;
					}
				}
				prevItem = item;
			}
		}
	}
	private void print_line(int indent, String string) {
		// TODO Auto-generated method stub
		for(int i = 0 ; i < indent ; i++) {
			System.out.print("    ");
		}
		System.out.println(string);
	}
}
```
##### CSVTablePrinter
```java
package example_16_tease_apart_Inheritance;

import java.io.IOException;
import java.util.ArrayList;

public class CSVTablePrinter extends CSVPrinter{

	public CSVTablePrinter() {
		// TODO Auto-generated constructor stub
	}
	@Override
	public void print(ArrayList<ArrayList<String>> itemList) throws IOException{
		System.out.println("<table>");
		for(int row = 0; row < itemList.size(); row++) {
			ArrayList<String> item = itemList.get(row);

			System.out.println("<tr>");
			for(int column = 0; column < item.size() ; column++) {
				System.out.print("<td>");
				System.out.print(item.get(column));
				System.out.print("</td>");
			}
			System.out.println("</tr>");
		}
		System.out.println("</table>");
	}
}
```
##### Application
```java
package example_16_tease_apart_Inheritance;

import java.io.IOException;

public class Application {

	private static final String SAMPLE_CSV_STRING =
			"좋은 아침입니다.,Good morning.\n"
			+"안녕하세요~,Hello.\n"
			+"안녕하세요.,Good evening.\n"
			+"안녕히 주무세요.,Good night.\n";
	private static final String SAMPLE_CSV_FILE = "file.csv";
	public static void main(String[] args) throws IOException{
		// TODO Auto-generated method stub
		new CSVTablePrinter().print(new CSVFileReader(SAMPLE_CSV_FILE).readCSV());
		new CSVTreePrinter().print(new CSVStringReader(SAMPLE_CSV_STRING).readCSV());
	}

}
```
최종적으로 위와 같이 작업 되었다. CSVXXXReader 들은 생성자에 저렇게 입력 값을 집어 넣는 것보단
CSV 의 TYPE 을 만들어서 생성자는 타입을 이용한 생성 그에 따라 하위 클래스를 이용한 readCSV()의 구현이 좋을 듯하지만
여기까지만 하도록 한다.

각각의 역할은 명확해 졌으며 불피요한 중복 코드또한 제거 되었다.
앞의 위임필드를 이용해 엉킨 상속관계를 푸는건 브리지 패턴을 만드는 과정이다.
그렇게 분리하다 보니 각가의 역할에 대해서 명확해 졌기에 우리는 이후의 리팩토링을 쉽게 할 수 있었다.
처음 코드에서 바로 하기에는 작은 코드임에도 불구하고 쉽지 않다. 차근차근 기존코드에 영향을 미치는 점은 없는지
컴파일해서 테스트해가며 해야한다.

이걸로 자바로 배우는 리팩토링 입문 책에 대한 포스팅은 끝이다.
다음에는 javascript 에서의 디자인 패턴과 TDD 에 대해서 포스팅해 가고
그 다음에는 Martin.Fowler 의 클린소프트웨어 내용에 대해 포스팅하고
최종적으로 3가지 내용을 묶어서 하나의 프로젝트를 진행하면서 전체를 다뤄보려고 한다.

개인프로젝트의 개발 사이클에 맞춰서 해볼까 싶지만 지금 하고 있는 개인프로젝트는 상당히 많이 지나가서
다음 프로젝트를 예로 들지 싶다.
