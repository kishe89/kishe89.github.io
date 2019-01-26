---
layout: post
title:  "Grphql Tutorial 6"
date:   2019-01-24 21:53:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Javascript
---
### 들어가며
---
이전 포스팅에 이어서 이제 email 인증을 거친 유저만 이용할 수 있도록 처리를 해본다.

일단 이를 위해서 ./src/schemas/user.ts 에 작성한 UserSchema를 수정한다.

emailVerificationStatus 라고 email 인증 상태를 나타내는 상태값을 하나 추가하도록 한다.

type은 boolean으로 하도록 하겠다.

##### ./src/schemas/user.ts
```typescript
import {Schema, Document} from 'mongoose'

export const UserSchema = new Schema({
    id: {type: String, required: true, unique: true},
    password: {type: String, required: true},
    name: {type: String, required: true},
    email: {type: String, required: false},
    emailVerificationStatus: {type: Boolean, default: false},
    workspace: {type: Schema.Types.ObjectId, ref: 'Workspace'},
    friend: [{type: Schema.Types.ObjectId, ref: 'User'}]
})

export interface IUser extends Document{
    _id: Schema.Types.ObjectId
    id: string
    password: string
    name: string
    email: string
    emailVerificationStatus: boolean
    workspace: Schema.Types.ObjectId
    friend: [Schema.Types.ObjectId]
}
```
자 UserSchema에 `emailVerificationStatus: {type: Boolean, default: false},`

IUser에 `emailVerificationStatus: boolean`을 추가했다.

emailVerificationStatus는 User Document가 생성될 때 default로 false값을 가지므로 입력 안해주어도 된다.

이제 이전에 작성한 UserResolver 에 작성되어있는 authEmail Query를 수정하도록 한다.

##### ./src/resolvers/UserResolver.ts
```typescript
@Query(returns => Boolean, { nullable: false, description: 'Modify User' })
  async authEmail(@Arg('token') token: String, @Ctx() { jwt, JWT_SECRET_KEY }: ApolloContextInterface): Promise<boolean> {
    const verified = jwt.verify(token, JWT_SECRET_KEY)
    if (verified) {
      const user = await this.users.findOneAndUpdate({ _id: verified._id },
        { $set: { emailVerificationStatus: true } },
        { new: true })
        .lean()
      if (!user) {
        throw new ApolloError('Not Found User')
      }
      return true
    }
    throw new ApolloError('Invalid Token. please retry sendEmail')
  }
```
자 이제 DB Schema에 수정한것과 같이 Graphql Schema에도 emailVerificationStatus 를 추가해주도록 한다.

##### ./src/objects/user.ts
```typescript
import { ObjectType, Field } from "type-graphql";
import { IsEmail } from "class-validator";
import { ObjectIdScalar } from "../scalars/ObjectId";
import { ObjectId } from "mongodb";

@ObjectType({ description: 'Represent User Infomation' })
export default class User {
  @Field(() => ObjectIdScalar, { nullable: false, description: 'User Object Id' })
  readonly _id!: ObjectId
  @Field(() => String, { nullable: false, description: 'User Id' })
  id!: string
  @Field(() => String, { nullable: false, description: 'User Password' })
  password!: string
  @Field(() => String, { nullable: false, description: 'User Name' })
  name!: string
  @IsEmail()
  @Field(() => String, { nullable: true, description: 'User Eamil' })
  email?: string
  @Field(() => Boolean, { nullable: false, description: 'User\'s Email verification status'})
  emailVerificationStatus!: boolean 
}
```
자 이제 모두 추가가 되었다.

서버를 실행시키고 playground도 실행해서 한번 정상적으로 동작하는지 보도록 하겠다.

이전에 진행했던 순서대로 호출해보면 된다.

signUp, sendEmail, 메일에 있는 링크 클릭 순으로 하면된다.

그리고 나서 변경된 값을 확인하기 위해 signIn, user 쿼리를 한번 날려서 확인하도록 한다.

##### signUp 호출
![Alt text](/assets/Posts/graphql_tutorial_6_1.png)
##### sendEmail 호출
![Alt text](/assets/Posts/graphql_tutorial_6_2.png)
##### email 링크 클릭
![Alt text](/assets/Posts/graphql_tutorial_6_3.png)
##### signIn 호출
![Alt text](/assets/Posts/graphql_tutorial_6_4.png)
##### user 호출
![Alt text](/assets/Posts/graphql_tutorial_6_5.png)

자 정상적으로 emailVerificationStatus가 변경된걸 볼 수 있다.

##### ./src/resolvers/UserResolver.ts
```typescript
@Query(returns => String, { nullable: true, description: 'Find One User' })
  async signIn(@Arg('id') id: String, @Ctx() apolloContext: ApolloContextInterface): Promise<String> {
    const user = await this.users.findOne({ id })
      .select(['_id', 'id', 'email', 'name', 'emailVerificationStatus'])
      .lean()
    const token = await apolloContext.jwt.sign(user, apolloContext.JWT_SECRET_KEY)
    return token
  }
```
보면 userdocument의 select에 `emailVerificationStatus`을 추가 했다.

해서 앞으로는 토큰에 포함된 `emailVerificationStatus`을 확인하여서 email인증여부를 확인한다.

signIn의 경우는 email 인증이 되어있지 않거나 혹은 email이 정상적으로 정상되지 않았을 수 있기때문에

인증상태와 상관없이 호출은 되어야 사용자에게 이메일 인증을 하라고 페이지를 렌더해준다던가 할 수 있다.

signIn을 창구로 해서 발급받은 토큰이 나머지 Query,mutation들의 입구가 되어줄 것이다.

이제 ./src/validator/AuthChecker.ts 에 작성했던 ApolloAuthChecker를 수정하도록 한다.

##### ./src/validator/AuthChecker.ts
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
  if(!user.emailVerificationStatus){
    throw new ApolloError('Please verified your email','Unverified email')
  }
  return user.emailVerificationStatus
}
```
마지막에 `return true` 이던 부분을 `return user.emailVerificationStatus` 으로 바꿔준다.

우리가 토큰을 발급할 때 emailVerificationStatus를 넣어줬으니

이제 Context에서 verify 하고 decode된 user object 에는 항상 emailVerificationStatus가 담겨 올것이다.

우리가 이전에 `@Authorized`를 적용해놨던 user Query를 계정을 새로 생성하고 email인증을 안한상태에서 날려보자.

##### user 호출
![Alt text](/assets/Posts/graphql_tutorial_6_6.png)

현재 password가 빠져있는데 다음 포스팅에서는 password를 암호화해서 저장하고 필요한 쿼리에 추가하도록 한다.

password암호화에는 [bcrypt] 를 이용하도록 한다.


##### 이전 포스팅
1. [Graphql Tutorial 1]
2. [Graphql Tutorial 2]
3. [Graphql Tutorial 3]
4. [Graphql Tutorial 4]
5. [Graphql Tutorial 5]

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
