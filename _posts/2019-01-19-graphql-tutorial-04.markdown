---
layout: post
title:  "Grphql Tutorial 4"
date:   2019-01-19 19:32:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Javascript
---
### 들어가며
---

이번 포스팅에서는 이전에 이야기한바와 같이 인증관련 작업을 할 것이다.

이를 편하게 하기 위해서 몇가지 작업을 할건데 작업 순서는 다음과 같다.

1. Apollo Context 작성
2. signIn에 JWT 생성 추가
3. type-graphql AuthChecker 구현
4. 권한 확인하기 위해 몇개 쿼리 추가

사용자의 이용 시나리오는 다음과 같이 정의한다.

1. 회원가입.
2. 회원가입 당시 인증메일 전송
3. 인증
4. 로그인
5. 이용

사용자의 권한은 다음과 같이 정의한다.
- Admin
  - Workspace에 Worker 추가, 삭제 권한
  - Workpsace에 게시물 추가,수정,삭제 권한
- Worker
  - 참여중인 Workspace에 게시물 추가,수정,삭제 권한.
### Apollo Context 작성
---
ApolloServer에 매 요청별로 공통으로 사용하거나 처리할 부분은 Context에 전달할 수 있다.

ApolloServer의 생성자에 사용할 Context를 전달해주면 되는데 다음과 같이 작성한다.

첫 번째로 src 아래로 context 라는 디렉토리를 생성해준다.

그리고 생성한 context 디렉토리 안에 ApolloContext.ts를 생성하고 이곳에 아래와 같이 코드를 작성해준다.
##### ./src/context/ApolloContext.ts
```typescript
export const ApolloContext = ({req}) => {
  return {
    Authorization: req.headers.authorization
  }
}
```
ApolloServer로 오는 요청에 대해서 header에 포함된 Authorization 속성을 읽어 올것이다.

토큰을 header에 보낼 때 사용하는 몇개의 일반적인 이름이 있는데 그중하나가 Authorization이다.

물론 본인이 원하는 이름으로 작성해도 되며 클라이언트와 약속만 되어있다면 된다.

우리는 Authorization으로 사용할 것이다.

이렇게 컨텍스트에 포함해놓은 객체, 함수, 값등은 Resolver등에서 사용이 가능하다.

하지만 Context는 들어오는 요청 모두에 생성되므로 특정한 상황에서만 사용되는 것 같은것은 담지 않는것이 

불필요한 리소스를 사용하지 않을 수 있다.

들어갈만 한 것을 예로 몇가지 들면 통신에 필요한 커넥션들, 공통으로 사용하는 키 값 등이 있겠다.

자 위에 작성한 코드는 응답의 타입이 암시적으로 되어있는데 타입을 명시해주자.

이를 위해서 해당 코드 아래로 다음과 같이 인터페이스를 하나 선언하자.

전체 코드는 아래와 같다.
##### ./src/context/ApolloContext.ts
```typescript
export const ApolloContext = ({req}):ApolloContextInterface =>{
  return {
    Authorization: req.headers.authorization
  }
}

export interface ApolloContextInterface{
  Authorization: string | undefined
}
```
예전 포스팅에서 이야기 했지만 인터페이스 등을 붙일때 prefix로 I와 같이 붙이는 스타일을 좋아하는 사람도 있고 아닌 사람도 있다.

협업이라면 약속된 스타일로 아니라면 본인이 편한 스타일로 작성하면 되겠다.

개인적으로는 뭉퉁그려서 I라고 하는것보다는 전체를 붙이는게 좋아보인다.

Authorization 은 없을 수 도 있으므로 string | undefined로 선언했다.

이제 작성한 ApolloContext 함수를 ApolloServer 생성자에 넘겨주도록 한다.

src 아래의 index.ts의 ApolloServer 생성부분에 다음과 같이 추가한다.

##### ./src/index.ts
```typescript
  const apolloServer = new ApolloServer({
    context: ApolloContext,
    schema: resolvers,
    playground: true,
    tracing: true,
  })
```
자 이제 확인을 위해 실행해보자.

콘솔에서 아래와 같이 빌드, 실행 명령을 작성하자.
```
npm run-script build
```
```
npm start
```
정상적으로 실행 되는걸 볼 수 있다.

이제 Context에 전달한 함수가 정상적으로 동작하는지 확인해보아야 하는데 

이전에 작성한 UserResolver.ts의 user Query를 다음과 같이 수정한다.
##### ./src/resolvers/UserResolver.ts
```typescript
    @Query(returns => User, { nullable: true, description: 'Find One User' })
    async user(@Arg('id') id: String, @Ctx() apolloContext: ApolloContextInterface): Promise<User | null> {
        console.log(apolloContext)
        return await this.users.findOne({ id }).lean()
    }
```
코드를 보면 함수의 파라미터 부분에 `@Ctx() apolloContext: ApolloContextInterface` 로 컨텍스트를 받는 부분과

함수의 바디에 `console.log(apolloContext)`로 로그를 찍은 부분이 추가 되었다.

이제 다시 빌드, 스타트를 하여서 playground 화면으로 가보자.

그리고 이전에 작성했듯이 user 쿼리를 날려보자.
![Alt text](/assets/Posts/graphql_tutorial_4_1.png)

그리고 콘솔창을 보면 아래와 같이 로그가 찍힌걸 볼 수 있다.
```
{ Authorization: undefined,
  _extensionStack: GraphQLExtensionStack { extensions: [ [Object], [Object], [Object] ] } }
```
자 우리가 헤더의 Authorization에 아무런 값도 전달하지 않았기 때문에 undefined이 떳고 _extensionStack이란게 찍혀있는데

이 정보는 tracing 정보가 들어있다.

이제 playground의 왼쪽 하단의 HEADERS를 클릭해서 header 입력 창을 연다.

![Alt text](/assets/Posts/graphql_tutorial_4_2.png)

그리고 아래처럼 아무런 텍스트나 입력해준다.

![Alt text](/assets/Posts/graphql_tutorial_4_3.png)

나는 Hello Authorization Header 라고 입력했기 때문에 아래와 같이 로그에 찍혀있는것을 볼 수 있다.
```
{ Authorization: 'Hello Authorization Header',
  _extensionStack: GraphQLExtensionStack { extensions: [ [Object], [Object], [Object] ] } }
```

이제 Authorization에 의미 있는 JWT를 전달해보도록 한다.

일단 JWT를 쉽게 생성하고 검증하기 위해 의존성을 하나 추가한다.

아래와 같이 package.json 의 
dependencies에 `"jsonwebtoken": "^8.4.0"` 를 
devDependencies에 `"@types/jsonwebtoken": "^8.3.0"` 를추가해준다.
##### package.json
```javascript
{
  "name": "graphql",
  "version": "0.0.0",
  "description": "using vs code project",
  "main": "index.js",
  "engines": {
    "node": "^8.9.4",
    "npm": "^5.6.0"
  },
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "build": "tsc",
    "start": "node ./dist/index.js"
  },
  "devDependencies": {
    "@types/express": "^4.16.0",
    "@types/mongoose": "^5.3.7",
    "@types/nodemailer": "^4.6.5",
    "@types/jsonwebtoken": "^8.3.0"
  },
  "dependencies": {
    "apollo-server-express": "^2.3.1",
    "express": "4.16.0",
    "reflect-metadata": "^0.1.12",
    "type-graphql": "^0.16.0",
    "typedi": "^0.8.0",
    "typescript": "3.2.2",
    "mongoose": "^5.4.2",
    "dotenv": "^6.2.0",
    "nodemailer": "^5.1.1",
    "jsonwebtoken": "^8.4.0"
  },
  "keywords": [
    "vs"
  ],
  "author": "kishe56@gmail.com",
  "license": "MIT"
}
```
버전은 물론 그 때 당시에 맞게 적어준다.

그리고 .env 에 다음과 같이 추가해주도록 한다.
##### .env
```
JWT_SECRET_KEY = testkey
```
JWT_SECRET_KEY 에 지금은 testkey와 같이 간단한 스트링을 적었는데 보통 random 문자열을 뽑아서 base64로 encoding한 문자열을 넣어준다.

일단 위와 같이 추가해주고 이제 Context에 추가 작업을 해보자.
##### src/context/ApolloContext.ts
```typescript
import jsonwebtoken from 'jsonwebtoken'
import User from '../objects/user';
import dotenv from 'dotenv'
dotenv.config()
const JWT_SECRET_KEY = process.env.JWT_SECRET_KEY
export const ApolloContext = async ({req}):Promise<ApolloContextInterface> =>{
  let user = undefined
  let verified = undefined
  let error = undefined
  if(req.headers.authorization){
    try{
      verified = await jsonwebtoken.verify(req.headers.authorization,JWT_SECRET_KEY)
    }catch(e){
      error = e
    }
  }
  if(verified){
    user = {
      ...verified
    }
  }
  return {
    jwt: jsonwebtoken,
    invalidToken: error,
    user: user,
    JWT_SECRET_KEY: JWT_SECRET_KEY,
    Authorization: req.headers.authorization
  }
}

export interface ApolloContextInterface{
  jwt: any
  invalidToken: Error
  user: User
  JWT_SECRET_KEY: string
  Authorization: string | undefined
}
```
조금 뭐가 많이 추가된거 같은데 하나하나 보면 많지 않다.

인터페이스에 jwt모듈을 넘길 any 타입의 jwt와 token이 decode된결과로 나올 오브젝트를 User 클래스 형태로 넘길 user

그리고 decode과정중 혹 에러가 발생할 경우 해당 에러를 넘길 Error 타입의 invalidToken 이 추가되었다.
에러를 컨텍스트에서 처리 안한 이유는 컨텍스트에서 에러를 throw하게 되면 어떤 쿼리에서 발생했는지 알기 어려워서 컨텍스트 생성 후 처리를 위해 넘긴다.

굳이 패스등의 정보를 볼 필요가 없다면 컨텍스트에서 처리해도 된다.

자 그리고 ApolloContext 함수는 토큰을 verify하고 decode된 객체를 user 변수에 담았다.

최종적으로 리턴에 JWT_SECRET_KEY를 포함해서 반환하면 된다.

### AuthChecker
AuthChecker는 `type-graphql`에서 제공하는 함수로 데코레이터로 사용가능하며 buildSchema시에 커스텀 함수로 전달 가능한 미들웨어이다.

AuthChecker는 boolean 값을 반환하도록 정의되어있고 false이면 UnAuthorized, true이면 Authorized로 판단된다.

자 이제 AuthChecker를 구현해보도록 하자.

src 디렉토리 아래로 validator 디렉토리를 생성하고 AuthChecker.ts 파일을 생성하고 아래와 같이 작성한다.

##### src/validator/AuthChecker.ts
```typescript
import { AuthChecker } from "type-graphql";
import { ApolloContextInterface } from "../context/ApolloContext";
import { ApolloError } from "apollo-server-express";
export const ApolloAuthChecker: AuthChecker<ApolloContextInterface> = async ({context: {jwt, invalidToken, user}}, roles) => {
  if(invalidToken){
    throw new ApolloError(invalidToken.message, invalidToken.name);
  }
  if(!user){
    return false
  }
  return true
}
```

일단 파라미터 부분을 보면 `{conetxt: {jwt, invalidToken, user}}`는 우리가 전달한 컨텍스트에서 필요한 것들을 받은것이고 

roles는 나중에 우리가 `@Authorized(args)`로 사용할때 args로 던져준 파라미터일 것이다.

해서 로직은 컨텍스트에서 토큰 검증중 발생한 에러가 담긴 invalidToken이 undefined가 아닌 정의가 되어있다면 

해당 에러를 ApolloError로 생성해서 던져주었고 그밑으로는 user 객체의 유무로 true, false를 응답하도록 해놨다.

토큰이 전달되었고 invalidToken이 undefined이라면 user는 항상 존재할 것이다.

user가 없는 경우는 토큰이 전달되지 않은 경우일 것이다.

자 이제 작성한 AuthChecker를 사용해보자.

일단 사용하기 위해서는 schema빌드시 함께 빌드 해줘야하는데

src/index.ts에 resolvers 변수를 초기화하는 부분을 다음과 같이 수정하자

##### src/index.ts
```typescript
const resolvers = await buildSchema({
    resolvers: [UserResolver, WorkspaceResolver],
    scalarsMap: [{ type: ObjectId, scalar: ObjectIdScalar }],
    authChecker: ApolloAuthChecker
  })
```
ApolloAuthChecker 를 import 해주고 buildSchema()의 authChecker에 전달해주면 된다.

AuthChecker의 작성이 완료 되었으니 사용해보자.

UserResolver에서 user 쿼리에 적용해보자.

UserResolver.ts를 아래와 같이 수정한다.
##### src/resolvers/UserResolver.ts
```typescript
    @Authorized()
    @Query(returns => User, { nullable: true, description: 'Find One User' })
    async user(@Arg('id') id: String, @Ctx() apolloContext: ApolloContextInterface): Promise<User | null> {
        return await this.users.findOne({ id }).lean()
    }
```
`@Authorized()`한줄이 추가되었다.

이제 실행해서 확인해보자.

playground에서 user 쿼리를 날려보자

![Alt text](/assets/Posts/graphql_tutorial_4_4.png)

위와 같이 접근이 거절되었다고 에러메시지가 나올 것이다.

요청을 보낼때 유효한 토큰을 보내지 않았기 때문에 당연하다.

자 그러면 이제 토큰을 생성해보도록 하자.

UserResolver의 signIn함수를 약간 수정하자.

##### src/resolvers/UserResolver.ts
```typescript
    @Query(returns => String, { nullable: true, description: 'Find One User' })
    async signIn(@Arg('id') id: String, @Ctx() apolloContext: ApolloContextInterface): Promise<String> {
        const user =  await this.users.findOne({ id })
        .select(['_id','id','email','name'])
        .lean()
        const token = await apolloContext.jwt.sign(user, apolloContext.JWT_SECRET_KEY)
        return token
    }
```
우리는 앞에서 컨텍스트에 jsonwebtoken 모듈을 jwt 키에 담아놨다.

signIn에서는 위와 같이 컨텍스트에 있는 jwt의 sign 함수와 JWT_SECRET_KEY를 이용해서 토큰을 생성하고 반환해주자.

반환 타입도 String으로 전부 변경 해주자.

그럼 이제 다시 빌드하고 실행해서 signIn 쿼리를 날려보자.

![Alt text](/assets/Posts/graphql_tutorial_4_5.png)

위와 같이 토큰이 정상적으로 발급될것이다.

이제 토큰을 복사해서 playground 왼쪽 하단의 HTTP HEADERS에 다음 스크린샷처럼 입력하도록하자.

![Alt text](/assets/Posts/graphql_tutorial_4_6.png)

그리고 쿼리를 실행해보면 다음과 같이 정상적으로 나오는걸 볼 수 있다.

![Alt text](/assets/Posts/graphql_tutorial_4_7.png)

자 그럼 마지막으로 잘못된 토큰을 한번 보내보자.

토큰스트링의 가장 앞글자를 하나지우고 보내보자.

그럼 다음과 같이 우리가 throw한 에러가 나오는걸 볼 수 있다.

![Alt text](/assets/Posts/graphql_tutorial_4_8.png)

자 여기까지 위에서 이야기한 1,2,3인
1. Apollo Context 작성
2. signIn에 JWT 생성 추가
3. type-graphql AuthChecker 구현

을 작성해봤다.

4번인 권한 확인하기 위해 몇개 쿼리 추가는 다음 포스팅에서 email 인증을 작성하면서 보도록 한다.

##### 이전 포스팅
1. [Graphql Tutorial 1]
2. [Graphql Tutorial 2]
3. [Graphql Tutorial 3]


[mongodb-connect]:https://kishe89.github.io/bluemix(ibm)/2018/02/15/mongodb-connect.html
[mlab]:https://mlab.com
[typescript-handbook]:https://www.typescriptlang.org/docs/handbook/tsconfig-json.html
[Graphql Tutorial 1]:https://kishe89.github.io/javascript/2019/01/01/graphql-tutorial-01.html
[Graphql Tutorial 2]:https://kishe89.github.io/javascript/2019/01/07/graphql-tutorial-02.html
[Graphql Tutorial 3]:https://kishe89.github.io/javascript/2019/01/13/graphql-tutorial-03.html
