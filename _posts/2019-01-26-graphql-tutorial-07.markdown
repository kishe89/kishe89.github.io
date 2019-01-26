---
layout: post
title:  "Grphql Tutorial 7"
date:   2019-01-26 18:38:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Javascript
---
### 들어가며
---
이전 포스팅에서는 email을 통해서 인증에 필요한 토큰을 포함한 링크를 보내고 처리 해봤다.

이번 포스팅에서는 이전에 구현에서 빠진 비밀번호 암호화를 진행해본다.

비밀번호 암호화하는데는 여러가지 방법들이 있는데 우리는 [bcrypt] 를 이용하도록한다.

많이 사용되는 암호화 방식 및 각각의 장단점에 대한 내용은 [안전한 패스워드 저장]에 잘 정리 되어있다.

[bcrypt]의 work factor는 높을 수록 생성에도 공격에도 많은 리소스가 필요해진다.

2의 work factor 승수 만큼의 처리 과정을 가지게 되는데 이 값은 해당 시점에 컴퓨팅 파워에 따라 적절하게 조절해줘야한다.

그리고 따로 지정을 할때는 항상 모듈이나 라이브러리에 세팅되어있는 디폴트값보다 낮은 값을 사용하지 않도록 하자.

bcrypt의 해싱함수를 통해 나오는 다이제스트 값의 형태를 봐보면

`$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy` 이란 값을 봐보자

맨 처음 `$2a$` 부분은 
- $1$: MD5
- $2$: Bcrypt
- $sha1$: SHA-1
- $5$: SHA-256
- $6$: SHA-512
등이 들어 들어가 있을 건데 어떤 해시함수를 이용했는지 나타낸다.

물론 `$2a$`도 들어갈 수 있는데 이도 Bcrypt를 나타낸다.

그다음 나오는 `10`은 비용 변수이다. 그리고 솔트 가 나타나고 솔트를 넣고 돌린 해싱 값이 나타난다.

대략적인 내용은 봤으니 [bcrypt]를 이용해 실제 코드 구현을 해보자.
##### package.json
```typescript
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
    "@types/jsonwebtoken": "^8.3.0",
    "@types/bcrypt": "^3.0.0"
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
    "jsonwebtoken": "^8.4.0",
    "bcrypt":"^3.0.3"
  },
  "keywords": [
    "vs"
  ],
  "author": "kishe56@gmail.com",
  "license": "MIT"
}
```
devDependencies 에는 `"@types/bcrypt": "^3.0.0"`을 dependencies 에는 `"bcrypt":"^3.0.3"`를 추가하였다.

인스톨을 해주고 이제 signUp과 signIn을 수정해본다.

일단 UserResolver 와 그곳에 있는 signUp 함수를 먼저 수정하도록 한다.

UserResolver에 `import bcrypt from 'bcrypt'` 로 [bcrypt]를 로드하도록 한다.

그리고 signUp 함수에 다음과 같이 추가 한다.
```typescript
    @Mutation(returns => User, { nullable: false, description: 'Create User' })
    async signUp(@Arg('user') user: InputUser): Promise<User> {
        const encryptedPassword = await bcrypt.hash(user.password,14)
        user.password = encryptedPassword
        const savedUser = await this.users.create({ ...user })
        return savedUser.toObject()
    }
```
기존 함수에서 입력으로 받은 user의 password를 이용해서 먼저 패스워드를 bcrypt를 이용해서 암호화(해싱)하고 그 값을

입력으로 받은 user 의 password에 대입하고 그 다음은 이전과 동일하다.

[bcrypt]모듈은 동기 방식과 비동기 방식의 함수를 모두 지원하는데 권장하길 비동기 함수의 이용을 권장한다.

비동기 함수는 그냥 genSalt, hash, compare 로 호출하면 되고 동기 함수는 뒤에 Sync를 붙여주면 된다.

hash(string, string|number, callback)을 인자로 받는데

첫 인자에 암호화할 값을 넣어주면 되고 두번째에는 salt 혹은 salt를 생성하는데 사용할 work factor값을 넣어주면 되고 마지막으로 결과를 받을 콜백을 넣어주면 되는데 콜백으로 안받을 때는 위와 같이 구현하면 된다.

나머지 함수들도 마찬가지이다.

이제 signIn함수를 수정하도록 하자.

```typescript
  @Query(returns => String, { nullable: true, description: 'Find One User' })
  async signIn(@Arg('id') id: String,
    @Arg('password') password: String,
    @Ctx() apolloContext: ApolloContextInterface): Promise<String> {
    const user = await this.users.findOne({ id })
      .select(['_id', 'id', 'email', 'name', 'emailVerificationStatus'])
      .lean()
    const verified = await bcrypt.compare(password,user.password)
    if(!verified){
      throw new ApolloError('Invalid Password')
    }
    const token = await apolloContext.jwt.sign(user, apolloContext.JWT_SECRET_KEY)
    return token
  }
```
signIn 함수에서는 입력받는 인자를 password란 이름으로 하나 추가하고 중간에 아래와 같은 코드가 추가 되었다.

```typescript
const verified = await bcrypt.compare(password,user.password)
if(!verified){
  hrow new ApolloError('Invalid Password')
}
```
bcrypt.compare 함수의 리턴값은 Promise<Boolean> 으로 위와 같이 작성해주면 true, false로 비교 결과가 넘어온다.

false인 경우는 동일한 값이 아니므로 비밀번호가 유효하지 않다고 에러를 throw하도록 하였다.

자 이제 실행 해서 signUp, signIn까지 한번 해보도록 하자.

혹시 사용하는 node 버전과 bcrypt 버전에 따라 `dyld: Symbol not found 뭐라뭐라` 에러가 발생할 수 있다.

호환성 문제가 약간 있었는데 이를 해결하기 위해서는 bcrypt 모듈을 다시 빌드 해줘야한다.

`npm rebuild bcrypt --build-from-source` 명령을 실행 시켜서 다시 빌드하고 시작해보도록 한다.

![Alt text](/assets/Posts/graphql_tutorial_7_1.png)

![Alt text](/assets/Posts/graphql_tutorial_7_2.png)

위와 같이 정상적으로 보일 것이다.

현재는 보기 위해서 password 필드를 쿼리할 수 있게 해놨는데 사실 클라이언트에게 이걸 볼 수 있게 해줘야할 이유가 없기에 제거 하도록 하자.


##### 이전 포스팅
1. [Graphql Tutorial 1]
2. [Graphql Tutorial 2]
3. [Graphql Tutorial 3]
4. [Graphql Tutorial 4]
5. [Graphql Tutorial 5]
6. [Graphql Tutorial 6]


[안전한 패스워드 저장]:https://d2.naver.com/helloworld/318732
[bcrypt]:https://www.npmjs.com/package/bcrypt
[nodemailer]:https://nodemailer.com/about/
[mongodb-connect]:https://kishe89.github.io/bluemix(ibm)/2018/02/15/mongodb-connect.html
[mlab]:https://mlab.com
[typescript-handbook]:https://www.typescriptlang.org/docs/handbook/tsconfig-json.html
[Graphql Tutorial 1]:https://kishe89.github.io/javascript/2019/01/01/graphql-tutorial-01.html
[Graphql Tutorial 2]:https://kishe89.github.io/javascript/2019/01/07/graphql-tutorial-02.html
[Graphql Tutorial 3]:https://kishe89.github.io/javascript/2019/01/13/graphql-tutorial-03.html
[Graphql Tutorial 4]:https://kishe89.github.io/javascript/2019/01/19/graphql-tutorial-04.html
[Graphql Tutorial 5]:https://kishe89.github.io/javascript/2019/01/23/graphql-tutorial-05.html
