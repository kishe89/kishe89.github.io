---
layout: post
title:  "Grphql Tutorial 5"
date:   2019-01-23 19:32:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Javascript
---
### 들어가며
---
이전 포스팅에 이어서 코드를 작성해보자.

이번 포스팅에서는 이전 포스팅에서 이야기 했듯이 email을 통한 인증코드를 작성해볼것이다.

이전 포스팅들에서 필요한 모듈들은 전부 추가 했고 JWT 생성까지도 작성해봤다.

이전에 했던걸 email로도 비슷하게 해주면된다.

### sendEmail 작성
---
일단 이전에 작성하던 ./src/resolvers/UserResolver.ts 에 이어서 작성한다.

아래와 같이 sendEmail 함수를 작성한다.
```typescript
    @Query(returns => Boolean, { nullable: false, description: 'Email Send' })
    async sendEmail(@Args() { _id }: ArgsUser): Promise<Boolean> {
        const user = await this.users.findOne({_id}).lean()
        const transport = nodemailer.createTransport({
            service: 'Gmail',
            secure: true,
            auth: {
                type: 'OAuth2',
                user: process.env.GMAIL_ID,
                clientId: process.env.GMAIL_CLIENT_ID,
                clientSecret: process.env.GMAIL_CLIENT_SECRET,
                refreshToken: process.env.GMAIL_REFRESH_TOKEN,
                accessToken: process.env.GMAIL_ACCESS_TOKEN,
                expires: 3600
            }
        })
        const sendResult = await transport.sendMail({
            from: {
                name: '인증관리자',
                address: process.env.GMAIL_ID
            },
            subject: '내 서비스 인증 메일',
            to: [user.email],
            text: 'Hello World'
        })
        return sendResult.accepted.length>0
    }
```
메일을 전송하는데 [nodemailer]를 이용할 것이라고 하였는데 이 부분에서 이용한다.

코드를 보면 어떤 변경을 처리하는게 아니기 때문에 `@Query`로 처리 하였다.

그리고 파라미터로 User Document의 ObjectId를 받고 응답은 async 함수이기때문에 `Promise<boolean>`을 응답한다.

처음 하는일은 전달받은 User Document의 ObjectId로 User를 찾는다.

그리고 transport를 생성하는데 이 transport가 메일을 전송하는 역할을 한다.

transport를 생성하는데 사용하는 옵션은 어떤 transport를 생성할 것인지에 따라 달라지는데 일단 우리는 smtp를 이용할 것이다.

service에는 사용할 메일 서비스

secure는 TLS를 이용하는지 여부로 낮은 보안 수준을 이용할때는 사용안해도 상관 없지만 warning이 뜰 수 있다.

그 아래로는 메일전송 계정의 인증 정보가 들어가는데 우리는 Oauth2 로 앞에 [Graphql Tutorial 3] 에서 필요한 준비를 마쳤다.

.env에 입력한 환경변수들을 각각 넣어준다.

|키|값|
|---|---|
|type|인증 방법|
|user|메일계정|
|clientId|메일계정 Oauth 아이디|
|clientSecret|메일계정 Oauth 비밀키|
|refreshToken|토큰 재발행 토큰|
|accessToken|액세스 토큰|
|expires|토큰 만료 시간|

설정에서 자동 리프레시 되도록 설정 해놨기때문에 리프레시는 신경쓰지 않아도 된다.

자 이제 옵션을 전부 맞게 줘서 transport를 정상적으로 생성했으면 transport의 sendMail함수로 메일을 보내면된다.

sendMail의 파라미터는 아래와 같다.

```typescript
from: {
  name: '인증관리자',
  address: process.env.GMAIL_ID
},
subject: '내 서비스 인증 메일',
to: [user.email],
text: 'Hello World'
```
from은 보내는 이의 정보가 들어가는데 보내는 이는 우리가 인증받은 계정이므로 address는 `process.env.GMAIL_ID`를 넣어주면 된다.

name의 경우는 메일보낸이를 나타내는 스트링을 넣어주면 된다.

to는 메일을 받을 계정이 들어가는데 단일로 보낼 수 도 array로 보낼 수 도 있다.

subject는 메일의 제목으로 스트링을 넣어주면 된다.

text는 메일에 표시할 내용인데 스트링을 넣어주면된다.

뒤에서 간단하게 html을 보낼 것인데 이때는 html에 넣어주면된다.

sendMail의 결과로는 전송한 메일에 대한 정보가 넘어오는데

전송수락된 거절된 mail에 대한 정보와 기타 정보들이 넘어온다.

accepted의 길이를 확인해서 우리가 보내야하는 계정이 들어있으면 true를 리턴해주고 아니면 메일전송에 실패 했다고 false를 반환하도록 한다.

자 여기까지 작성 하였으면 빌드하고 실행해서 sendMail Query를 playground에서 실행해보자.

![Alt text](/assets/Posts/graphql_tutorial_5_1.png)

그림과 같이 true를 반환 하면 정상적으로 전송된것이다.

그럼 사용자계정을 생성할 때 입력한 email주소로 들어가서 메일을 확인해보자.

![Alt text](/assets/Posts/graphql_tutorial_5_2.png)

위와 같이 와있는걸 볼 수 있다.

혹시 전송이 안된경우는 sendMail의 반환값을 받아놓은 sendResult를 로그로 확인해보면 내용이 나올 것이다.

자 그럼 의미없는 텍스트말고 토큰을 포함한 인증 링크를 넣어서 보내보자.

일단 인증링크에 들어갈 Query를 하나 더 만든다.

이름은 authEmail 이라고 하겠다.

##### authEmail
```typescript
    @Query(returns => Boolean, { nullable: false, description: 'Modify User' })
    async authEmail(@Arg('token') token: String, @Ctx() {jwt,JWT_SECRET_KEY}: ApolloContextInterface): Promise<boolean> {
        const verified = jwt.verify(token, JWT_SECRET_KEY)
        if(verified){
            return true
        }
        return false
    }
```

위와 같이 token이란 키로 전달받은 jwt를 검사해서 true or false를 반환하도록 한다.

실제론 true일 때 유저에게 어떤 변경을 한다던지 페이지를 redirection 시킨다던지 하면 될것이다.

그럼 이제 html을 작성해본다.

기존 sendMail에서 인증용 토큰을 생성하고 transport.sendMail에 파라미터를 변경할 것이다.

아래 코드를 보자
#####sendMail
```typescript
    @Query(returns => Boolean, { nullable: false, description: 'Email Send' })
    async sendEmail(@Args() { _id }: ArgsUser,@Ctx() {jwt,JWT_SECRET_KEY}: ApolloContextInterface): Promise<Boolean> {
        const user = await this.users.findOne({_id}).lean()
        const token = jwt.sign(user,JWT_SECRET_KEY)
        const encodedToken = encodeURI('"'+token+'"')
        const transport = nodemailer.createTransport({
            service: 'Gmail',
            secure: true,
            auth: {
                type: 'OAuth2',
                user: process.env.GMAIL_ID,
                clientId: process.env.GMAIL_CLIENT_ID,
                clientSecret: process.env.GMAIL_CLIENT_SECRET,
                refreshToken: process.env.GMAIL_REFRESH_TOKEN,
                accessToken: process.env.GMAIL_ACCESS_TOKEN,
                expires: 3600
            }
        })
        const sendResult = await transport.sendMail({
            from: {
                name: '인증관리자',
                address: process.env.GMAIL_ID
            },
            subject: '내 서비스 인증 메일',
            to: [user.email],
            html: '<h3>내 서비스</h3>'+
            '<a href = "http://localhost:3000/graphql?query=query {authEmail(token:'+encodedToken+')}">'+
            'http://localhost:3000/graphql?query=query {authEmail(token:'+encodedToken+')}</a>'
        })
        return sendResult.accepted.length>0
    }
```

일단 토큰을 생성 하고 URI로 encode해준다.

text를 지우고 html에 간단하게 h태그와 a태그를 이용해서 링크 및 내용을 넣었다.

보면 `?query= 쿼리이름(인자키: 값){받을 필드들}` 형태로 이루어진다.

우리는 authEmail이 그냥 boolean만 반환하므로 따로 필드로 지정할건 없다.

호스트는 지금 로컬에서 띄웠기때문에 로컬호스트로 지정하였다.

이제 다시 빌드하고 실행해서 sendMail 쿼리를 playground에서 날려보자.

그리고 메일에 가보면 다음과 같이 와있을 것이다.

![Alt text](/assets/Posts/graphql_tutorial_5_3.png)

그럼 이제 링크를 클릭해보면 playground화면이 뜨고 playground에 내용이 입력되어있을 것이다.

왜 응답이 바로 안왔지? 이러면 안되는데? 라고 생각이 될것이다.

서버를 시작할 때 playground 옵션을 꺼주고 실행해서 다시 링크를 눌러보자.

![Alt text](/assets/Posts/graphql_tutorial_5_4.png)

위와 같이 정상적으로 동작하는걸 볼 수 있다.

일반적으로 제품환경에서는 playground를 끄길 권장한다.

끄고 테스트하기 편하게 하려면 따로 playground 데스크탑 앱을 받아서 사용하는걸 권장한다.

playground를 지원해야한다하면 production은 playground를 끄고 playground client를 따로 지원하는것도 방법이 될 수 있다.

![Alt text](/assets/Posts/graphql_tutorial_5_5.png)

위 화면은 Electron으로 개발된 데스크탑용 playground이다.

playground에 대한 자세한 내용은

https://github.com/prisma/graphql-playground 에서 확인 가능하며 다운도 가능하다.

다음 포스팅에서는 이번에 authEmail에서 true, false로 반환하는 부분을 User 계정에 Email 확인 값을 넣어주는 걸로 변경하고

그에 따라 Email 인증된 유저만이 사용 가능한 Query, mutation을 작성해보도록 한다.

##### 이전 포스팅
1. [Graphql Tutorial 1]
2. [Graphql Tutorial 2]
3. [Graphql Tutorial 3]
4. [Graphql Tutorial 4]

[nodemailer]:https://nodemailer.com/about/
[mongodb-connect]:https://kishe89.github.io/bluemix(ibm)/2018/02/15/mongodb-connect.html
[mlab]:https://mlab.com
[typescript-handbook]:https://www.typescriptlang.org/docs/handbook/tsconfig-json.html
[Graphql Tutorial 1]:https://kishe89.github.io/javascript/2019/01/01/graphql-tutorial-01.html
[Graphql Tutorial 2]:https://kishe89.github.io/javascript/2019/01/07/graphql-tutorial-02.html
[Graphql Tutorial 3]:https://kishe89.github.io/javascript/2019/01/13/graphql-tutorial-03.html
[Graphql Tutorial 4]:https://kishe89.github.io/javascript/2019/01/19/graphql-tutorial-04.html
