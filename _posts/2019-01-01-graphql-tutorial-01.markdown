---
layout: post
title:  "Grphql Tutorial 1"
date:   2019-01-01 20:19:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Javascript
---

### Why [Graphql]?
우리가 기존에 웹 어플리케이션을 개발하면 화면의 디자인, 동작을 담당하는 프론트엔드 영역과
프론트엔드에서 요청하는 데이터들 혹은 페이지를 전달해주는 백엔드 영역을 개발하게 된다.

최근 개발되는 거의 모든 백엔드 영역은 RESTful 하게 개발되어진다.

RESTful 한 API는 현재까지도 유용한 API 개발 방법이다. 잘 설계된 API들은 직관적이며 사용하기 편리하다.

어떠한 기능을 하고 하는데 부족하지는 않다.

그럼에도 불구하고 Graphql이란건 왜 나온걸까 한번 생각해보자.

일단 RESTful API의 경우 API 자체에 대해서 어떠한 스키마나 타입정의가 없다.

백엔드 개발자 입장에서 이는 쉽게 추가하고 지울 수 있는 장점이 있지만 프론트엔드 입장에서 생각해보면 서로간에 약속된 내용이거나

**swagger**와 같은 툴을 이용해 작성된 문서가 없다면 내가 호출하는 API endpoint가 존재하고 내가 보내는 요청이 올바른 양식이길
눈감고 기도하며 개발하는 것과 다를바 없을 것이다.

이 부분은 문서화를 최대한 자동화하고 업데이트를 잘하면 해결될 수도 있는 문제일 수 있으나 어쨋든 생각보다 많은 노력이 필요하다.

자 그럼 한가지 주제는 생각해봤으니 다음으로 넘어가보자

앞에서 프론트엔드 개발자의 기도가 통해서 API의 호출이 성공적으로 이루어졌고 정상적으로 데이터를 받아서 렌더했고

그 외에 100여개의 API 호출에 대한 처리도 다 해서 개발을 완료 했다고 생각해보자.

헌데 갑자기 새롭고 아름다운 UI&UX가 머리 속에서 떠올라서 적용을 하기로 결정하였는데

이때 프론트엔드 개발자와 백엔드 개발자에게는 무슨일이 생길까?
정리해보자.

- 기존 API들로 새로운 UI&UX를 커버할 수 있는지 검토
    1. 커버 가능일 때
        1. 그냥 프론트엔드 개발만 하면됨.
    2. 단일API론 안되지만 기존 API 여러개 묶으면 커버가능일 때
        1. 프론트엔드가 책임지고 복잡한 API 묶어서 처리
        2. 백엔드에서 기존 API 여러개 wrapping 해서 API 엔드포인트 추가
        3. 새로 만들기
    3. 커버 불가일 때
        1. 새로 만들기

위와 같이 될것이다. 차라리 새로 만드는거면 좋겠지만 상황상 추가적으로 백엔드 개발이 불가할 수도 있는 경우도 있을것이고

백엔드에서 처리를 안하고 프론트엔드에서 처리를 하더라도 프론트엔드 개발 복잡도는 상당히 올라갈 것이다.

애시당초 API 설계시 새로운 UI&UX를 고려하여 설계한것이 아니기때문에 API콜 이후 반환되는 데이터들에 대해서

병합하는등의 후처리들이 들어갈 것이다.

더 많은 상황들이 있겠지만 위 2가지만 생각해봐도 백엔드 개발자건 프론트엔드 개발자건 짜증이 날것이다.

자 이러한 짜증나는 상황에 대해서 좀 더 유연하게 대처할 방법으로 나온 것이 [Graphql]이다.

일단 [Graphql]은 SDL(Schema Definition Language)를 이용해서 요청에 대한 Schema를 작성하는걸로 시작한다.

즉 백엔드 개발당시에 요처에 대한 Schema를 작성하게 되어 타입등을 작성하게 된다는 것이다.
### Graphql 예제

아래 코드를 보자.
##### Schema 정의
```typescript
// Construct a schema, using GraphQL schema language
  const typeDefs = gql`
  type Query {
    hello: String
  }
  `;
```
[Graphql]은 Query, Mutation, ... 으로 요청을 받고 보내는데

**Query**는 조회.

**Mutation**은 생성, 수정, 삭제와 같은 동작을 생각하면된다.

즉 위 코드는 **Query**를 생성하는데 **Query**에는 hello가 있고 요청에 대한 반환 타입이 String이란 것이다.

위에서 정의한 Schema에 대해서 실제 조회,생성,수정,삭제를 행하는건 Resolver란 코드가 필요하다.

Resolver는 아래와 같이 작성한다.
##### Resolver
```typescript
const resolvers = {
    Query: {
      hello: () => 'hello world'
    }
  };
```

Schema를 Query에는 hello가 있고 이는 타입이 String이라고 하였다.

Resolver는 hello의 동작을 정의하는데 hello wolrd 문자열을 반환하도록 하였다.

전체 코드 실행 이전에 일단 위와같이 정의한 Schema와 Resolver로 Graphql 서버를 띄운 결과를 본다.

![Alt text](/assets/Posts/graphql_tutorial01.png)
위 화면이 실행한 결과를 볼 수 있는 화면인데 [playground](Postman 생각하면됨)라는 툴을 이용하여 결과를 확인할 수있다.

지금 사용중인 [apollo-server-express] 은

[playground] 를 포함하고 있는 graphql 서버 제작용 오픈소스이다.

[playground] 는 electron 으로 개발된 데스크탑용 앱도 제공한다.

자 좀 더 이해하기 쉽게 사람을 나타내는 데이터를 반환하는 Schema와 Resolver를 작성해보겠다.

##### Schema
```typescript
// Construct a schema, using GraphQL schema language
  const typeDefs = gql`
  type Query {
    hello: String
    people: [Person]
  }
  type Person{
    name: String
    age: Int
  }
  `;
```
##### Resolver
```typescript
  // Provide resolver functions for your schema fields
  const resolvers = {
    Query: {
      hello: () => 'hello world',
      people: () => {
        return [{
          name: "Davidkim",
          age: 18
        },{
          name: "Alice",
          age: 18
        }]
      }
    }
  };
```
Schema에는 Query에 people이라는 요청과 그에 따를 응답값의 타입인 `[Person]`을 작성하였고
```typescript
type Person{
    name: String
    age: Int
  }
```
으로 Person 타입을 정의했다.

Person은 name(String타입), age(Int타입)을 가지는 타입이다.

Resolver에서는 people Query가 호출되었을 때 Davidkim, Alice 두명의 정보를 반환하도록 하였다.

결과 화면부터 또 보도록 하겠다.
![Alt text](/assets/Posts/graphql_tutorial02.png)
```
{
  "data": {
    "hello": "hello world",
    "people": [
      {
        "name": "Davidkim",
        "age": 18
      },
      {
        "name": "Alice",
        "age": 18
      }
    ]
  },
  "extensions": {}
}
```
위와 같은 응답을 받은걸 볼 수 있다.

처음 디자인할때 위와같은 데이터가 필요했지만 위에서 age 는 필요가 없는 다른 화면을 작성하려고한다.

그냥 REST API 로 작업을 했다면 endpoint에 v1, vX, vN 과같잉 버저닝을 해서 새로 작성하던가

아니면 그냥 그대로 쓰되 렌더링만 안하는 방법이 있을것이다.

하지만 위에 **Why Graphql?** 에서 이러한 상황에 유연하게 대처할 수 있게 하기위해 Graphql이 나왔다고 했다.

새로운 API를 작성하거나 필요없는 필드를 계속해서 받을 필요가 없다.

아래 [playground] 화면을 본다.
![Alt text](/assets/Posts/graphql_tutorial03.png)

그저 우리가 보내는 쿼리의 요청에 age 필드를 제거만 하면 된다.

서버에서 제공하는 스키마에서 존재하는 필드들에 대해서는 클라이언트에서 선택을 할 수 있기때문이다.

Backend 에서는 새로운 API endpoint를 작성해야할 필요가 없고

Frontend 에서도 새로운 API 호출이 필요치 않다. 또한 불필요한 데이터를 계속 받을 필요도 없다.

그저 기존 호출에서 받기위해 요청한 속성만 제거하면된다.

### REST vs Graphql

이건 정답이 정해져있는게 아니고 상황에 따라 다르다고 생각된다.

일단 위에서는 Graphql의 장점을 이야기 했는데 이와 비교 했을때 REST의 장점도 있기때문이다.

개인적으로 Graphql 보다 REST 가 더 좋게 느껴진 점은 보일러플레이트가 적다는 것이다.

일단 Graphql의 경우는 정확한 Schema가 설계 되어야 하며 응답할 정확한 인터페이스가 정의되어야한다.

물론 이점은 REST도 마찬가지지만 코드로 정의를 제공 하지 않더라도 REST는 문제가 없지만 Graphql의 경우는 제공이 되어야한다.

사실 위에서 **Why Graphql** 에서 이야기한 상황들은 어디까지나 가정이기 때문이다.

그래도 Graphql은 좋은 개발 도구가 될 수 있다고 생각한다.

REST로 빠르게 잘 만들 수 있으면 REST

Graphql로 빠르게 잘 만들 수 있으면 Graphql로 하는게 바랍직해보인다.

[Graphql]:https://graphql.org/
[apollo-server-express]:https://github.com/apollographql/apollo-server/tree/master/packages/apollo-server-express
[playground]:https://github.com/prisma/graphql-playground
