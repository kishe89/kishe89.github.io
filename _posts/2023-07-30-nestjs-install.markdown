---
layout: post
title:  "NestJS 사용하기"
date:   2023-07-30 22:00:00
author: 김지운
cover:  "/assets/instacode.png"
categories: NestJS
---

### 들어가며

NodeJS 에서 사용하는 웹 프레임 워크는 웹어플리케이션이 수행해야 할 가장 기본적인 기능들만을 포함하고 있는 Express 부터 좀 더 다양한 기능들을 포함하고 있는

NestJS, Hapi, SailsJs 그리고 거의 대부분의 기능을 포함하고 있는 loopback 등이 있다.

이중에 최근 많이 사용되고 있는 NestJS 의 Features 를 알아보며 RDB 설계의 기초에 대해서 학습하도록 한다.

### NestJS

NestJS 의 페이지를 들어가보면 다음과 같이 소개하고 있다
```
A progressive Node.js framework for building efficient, reliable and scalable server-side applications
```

NestJS 뿐만 아니라 위에서 이야기한 다른 프레임워크들도 비슷한 특장점들을 가지고 있다고 소개하는데 실제로 어떤 형태로 이런 특장점들을 가지게 하는지에 대해서는

각 프레임워크의 지향하는 방향에 따라 약간의 차이가 있다.

NestJS 의 경우는 기능 구현을 개별 컴포넌트 단위로 구현하고 컴포넌트들의 집합인 모듈을 정의하고 해당 모듈을 실제 사용할 Nest 프로젝트에서 import 하여 사용하는
형태로 위의 특장점을 구현한다.

### NestJS(Module)

일단 모듈에 대해서 알아보면 모듈은 크게 다음과 같은 기능을 가진다.

- 모듈을 import 할 수 있다.
- Provider(`컴포넌트, 인스턴스등의 Factory 함수등`) 를 제공 받을 수 있다.
- 컴포넌트를 export 할 수 있다.

다른 모듈혹은 컨트롤러를 import 할 수 있으며 이 떄 해당 모듈 혹은 컨트롤러는 Injectable 해야 한다.

우리가 웹 개발을 하면서 자주 사용하게되는 대부분의 라이브러리는 Nest 에서 사용가능한 컴포넌트로 이미 wrapping 되어 있으며

`@Nest` Repo 에 있다(ex: swagger, axios, etc)

Hapi 를 사용해본 사용자를 대상으로 비유하자면 plugin 과 비슷한 포지션을 가지며 AOP(aspect oriented programming, 관점 지향 프로그래밍)에 가까운 모습을 보여준다.

기능단위의 모듈(플러그인) 예를들면 다음과 같은 요구사항의 MyApplication 이라는 프로그램이 있을 때의 모듈의 모습은 다음과 같이 될 것이다.

**요구 사항**

- 계정 시스템을 가진다
- 인증 시스템이 있다.
- 인증은 Email 을 이용한다.
- 게시글을 업로드, 다운로드, 수정, 삭제 할 수 있다.
- 채팅을 할 수 있다.
```mermaid
graph TD;
    AccountModule-->MyApplication;
    AuthenticationModule-->MyApplication;
    EmailModule-->MyApplication;
    ArticleModule-->MyApplication;
    ChatModule-->MyApplication;
```

모듈단위의 모습으로 봤을 때 위 그래프와 같은 형태로 나타 낼 수 있으며 구현 또한 위와 같이 이뤄진다.

### NestJS(Provider)

NestJS 에서 모듈에서 사용할 컴포넌트의 추가는 Provider 를 통해서 제공 된다.

Provider 의 컨셉은 DI(Dependency Injection) 를 통해서 사용할 컴포넌트, 컴포넌트의 factory 등을 provider 에 Provide 하여서

각기 다른 컴포넌트들을 조합 및 재사용 할 수 있도록 하는 것을 목표로 하고있다.

웹 프로젝트를 가정해서 Controller Layer 와 Service Layer 형태의 구현을 기본적인 디자인 패턴으로 채택하며

문서의 예시또한 이를 기준으로 나와 있다.

```typescript
@Injectable()
```

Annotation 을 사용하여 Inject 할 클래스로 만들어주도록 한다.(Guard, Interceptor 등 기타 클래스들도 동일)

Controller Layer 에서는 인증 및 권한에 따른 리소스 라우트 핸들링을 진행하고 비지니스 로직은 Service Layer 에 작성해주도록 한다.

DI 에 대해서 scope 를 제공하며 기본적으로 Application lifecycle 에 의존적이며 이 것이 의미하는 바는

Application 이 시작되면 모든 dependency 들이 resolve 되고 provider 로 제공된 factory, class 등을 이용하여 instance 화 되며 Application 이 종료되면 해당 instance 들이 destroy 된다.

이외에도 Request lifecycle(Express 에서의 미들웨어 lifecycle 과 동일) 및 개별 서비스등의 lifecycle 로도 지정 가능하며

이렇게 instance 화되면 의존하는 lifecycle 동안 SingleTon 으로 인스턴스 관리를 하게 된다.





[Fastlane]:https://fastlane.tools
[Github Self Hosted-Runner]:https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners
[Github Actions Execution Time multiple]:https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions#minute-multipliers
