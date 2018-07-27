---
layout: post
title:  "Electron 을 이용한 데스크탑 채팅앱 개발강의 intro"
date:   2018-07-27 20:19:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Electron Lecture
---


##### 강의 제작목적
---

2017년 11월 회사를 퇴사할 때부터 시작한 기술 및 스터디 블로그를 통해서 색다른 기회가 생겼다.

물론 돈으로 직결되지는 않지만 나름의 보람이 있는 일이 될듯하다.

[인프런] 이란 곳에서 강의영상을 제작해볼 생각이 없냐는 제의를 받고 2018년 6월 23일부터 강의를 제작중이다.

강의 주제를 뭘로 할까 고민하다가 제작중인 앱과 비슷한 내용으로 해보면 어떨까 해서 해당 주제로 강의제작을 시작했다.

물론 [Github]에서 검색해보거나 구글링을 해보면 나오는 내용이기도 하다. 그래서 공개된 대다수의 코드들과는 다른 형태로 작업을 하는 방법으로

예제코드를 작성하고 그를 통해 강의를 제작해나가고 있다. 많은 사람들이 봐주고 그를 통해서 나에게도 강의를 봐준분들에게도 새로운 기회가 생겼으면 좋겠다.


##### Intro
---

intro는 [Electron & Socket.io 를 이용한 챗봇 개발기1] 의 내용이다.

강의에서는 위 포스팅의 내용에서 사용하는 NodeJs의 API들에 대한 설명이 추가된 정도이다.

많은 예제 혹은 공개코드가 소켓의 관리를 Renderer Process에서 하는데

내가 생각해봤을때 Socket.io의 튜토리얼 및 샘플앱이 그렇게 작업 되어있기 때문인듯하다.
그리고 사실 큰 문제가 없기도 하다.

거의 대부분의 앱들이 SPA(Single Page Application)로 작성되는데 이러한 앱에서는 저러한 방식의 작업이 더 유리하다.

하지만 웹앱스러운 앱만을 개발할게 아니라면 저 방식은 소켓의 공유를 하는데 있어서 문제가 생길 수 있다.

해서 Main Process에서 소켓 관리를 하고 이를 IPC를 통해서 처리하는 형태로 예제코드를 새로 작성했다.

이렇게 되면 한단계를 분명 더 거쳐야한다.
```
ipcMain -> ipcRenderer or ipcRenderer -> ipcMain 의 형태로 이벤트가 전파되는 과정이 발생한다.
```
물론 이런식으로 작성하지 않더라도 위와 같은 이벤트 전파가 발생해야할 수 있긴한데

**Main Process**에 작업해야할 부분이 적긴하다.

대신 **Renderer Process**에 Socket의 콜백 즉 로직코드의 대부분이 몰리게된다.

간단히 정리하자면 대부분의 예제코드들의 구조는 App의 화면에서 Socket의 로직을 처리하는 구조인데 내가 이번예제로 이야기하고 싶은건

App에서 Socket의 로직을 처리하고 그 결과를 화면들에 표시하는 형태로의 변경을 하는것도 괜찮지 않냐이다.

물론 화면(**Renderer process**)과의 인터랙션을 위해서 연결되는 부분은 있지만

분명한건 **Renderer Process**에서 load해야할 스크립트는 적어진다.

**Electron**이 분명히 웹기술을 이용하여 어플리케이션을 만들 수 있게 도와주는건 맞지만

그렇다고 굳이 웹개발과 동일한 구조로 혹은 컨셉으로 갈 필요는 없다라는게 내 생각이다.

해서 강의에서는 이러한 내 생각과 문서에 근거한 내용으로 설명을 해나가며 모든 설명을 할 순 없더라도 최대한 많은 키워드를 제시하여

혼자서 공부를 해나갈 수 있도록 할것이다.

모든 강의는 라이브 코딩형태로 제작하도록 하겠다.

[Electron & Socket.io 를 이용한 챗봇 개발기1]:https://kishe89.github.io/electron/2018/03/29/electron-first-example.html
[인프런]:https://www.inflearn.com/
[Electron & Socket.io 를 이용한 챗봇 개발기1]:https://kishe89.github.io/electron/2018/03/29/electron-first-example.html
[Electron & Socket.io 를 이용한 챗봇 개발기2]:https://kishe89.github.io/electron/2018/04/04/electron-second-example.html
[emit-cheatsheet]:https://socket.io/docs/emit-cheatsheet/
[axios]:https://github.com/axios/axios
[socket.io]:https://socket.io/
[mongoose]:http://mongoosejs.com/
[Electron]:https://electronjs.org/
[BrowserWindow]:https://electronjs.org/docs/api/browser-window

