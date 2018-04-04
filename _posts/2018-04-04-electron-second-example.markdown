---
layout: post
title:  "Electron & Socket.io 를 이용한 챗봇 개발기2"
date:   2018-04-04 12:56:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Electron
---


[Electron] 에서 **renderer process** 가 화면을 로드할 때

[BrowserWindow] 클래스를 이용한다.

[BrowserWindow] 는 EventEmitter 이므로 각종 화면에 관련한 각종 이벤트를 발생시킬 수 있다.

생성은 `new` 예약어를 사용하여 생성한다.

생성에 필요한 옵션은 다음과 같다.

- options(optional)
  - `width` :  Integer 값이며 화면의 폭이며 pixel 단위이고 기본 폭은 800 pixel 이다.
  - `height` : Integer 값이며  화면의 높이이며 pixel 단위이고 기본 높이는 600 pixel 이다.
  - `x` : Integer 값이며 왼쪽 offset 값으로 기본값은 화면의 중앙값이다. y 값을 사용한다면 같이 사용해야한다.
  - `y` : Integer 값이며 상단 offset 값으로 기본값은 화면의 중앙값이다. x 값을 사용한다면 같이 사용해야한다.
  - `useContents` : Boolean 값이며 true 일 때 웹페이지 width, height 값을 실제 창과 동일하게 사용한다. 기본값은 false 이다.
  - `center` : Boolean 값이며 화면의 중앙에 창을 보여준다.
  - `minWidth` : 최소 width 값이며 width 와 내용은 동일하며 기본값은 0이다.
  - `minHeight`: 최소 height 값이며 height 와 내용은 동일하며 기본값은 0이다.
  - `maxWidth` : 최대 width 값이며 기본값은 no limit 이다.
  - `maxHeight` : 최대 height 값이며 기본값은 no limit 이다.
  - `resizeable` : 창의 크기를 조정 가능하게 할지에 대한 Boolean 값이다. 기본값은 true 이다.
  - `movable` : 창을 이동할 수 있는지에 대한 Boolean 값이다. linux 에는 구현되어 있지 않다. 기본값은 true 이다.
  - `minimizable` : 창을 최소화 할 수 있는지에대한 Boolean 값이다. linux 에는 구현되어 있지 않다. 기본값은 true 이다.
  - `closeable` : 창을 닫을 수 있느지에 대한 Boolean 값이다. linux 에는 구현되어 있지 않다.
  - `focusable` : 창이 focus 를 가질 수 있는지에 대한 Boolean 값이다. 기본값은 true 이며 Window(os)에서는 false 이며 또한 `skipTaskBar` 도 true 로 설정 됨을 의미한다.

    Linux(os) 설정에서 `focusable`을 false로 세팅시 wm과의 상호작용을 멈출 수 있다. 그래서 모든 작업공간에서 최상위에 위치할 수 있다.
  - `alwaysOnTop` : 다른 창들의 위에 항상 떠있는다. 기보값은 false 이다.
  - `fullscreen` : 창이 전체화면으로 떠야할 때 세팅한다. 기본값은 false 인데 MacOS 에서는 false 일 때 전체화면 버튼이 가려지고 비활성화된다.
  - `fullscreenable` : 창을 전체화면 모드로 변경할 수 있는지에대한 Boolean 값이다. 기본값은 true 이다. MacOS 에서는 최대화/확대 버튼과 토글동작을 한다.
  - `simpleFullscreen` : MacOS 에서 Lion(OS 버전명) 이전의 전체화면을 사용한다. 기본값은 false 이다.
  - `skipTaskBar` : 창을 작업표시줄에 보여줄 지 Boolean 값이다. 기본값은 false 이다.
  - `kiosk` : 키오스크 모드로 동작할지 Boolean 값이다.
  - `title` : 창의 제목으로 기본값은 `"Electron"` 이다.
  - `icon` : 창에서 사용할 icon이다. Window 에서는 `ICO`포맷의 icon을 사용하길 추천한다.
  - `show` : 창이 생성되었을 때 보여져야할 지에 대한 Boolean 값으로 기본값은 true 이다.
  - `frame` : flase 로 세팅시 [Frameless Window] 를 생성한다. 기본값은 true 이다.
  - `parent` : 부모 창을 설정한다. 기본값은 null 이다.
  - `modal` : 대화상자 창을 띄울지에 대한 Boolean 값이다. 이 창은 오직 자식 창으로서만 동작 가능하다. 기본값은 false 이다.
  - `acceptFirstMouse` : WebView 에 창을 활성화하는 단일 mouse-down 이벤트만 허용한다. 기본값은 false 이다.
  - `disableAutoHideCursor` : 키보드 타이핑중에 마우스 커서를 감출지에 대한 Boolean 값이다. 기본값은 false 이다.
  - `enableLargerThanScreen` : 창이 화면 크기보다 커질 수 있는지에 대한 Boolean 값이다. 기본값은 false 이다.
  - `backgroundColor` : 창의 배경색이며 16진수 문자열 값이다. ex)#FFF 기본값은 #FFF 이다.
  - `hasShadow` : 창이 그림자를 가져야할지에 대한 Boolean 값이다. 오직 MacOS 에만 구현되어있다. 기본값은 true 이다.
  - `opacity` : 창의 투명도 값으로 0.0 ~ 1.0 까지의 값을 가진다. Window 와 MacOS 에만 구현되어 있다.
  - `darkTheme` : 창에 darkTheme 를 적용한다. GTK+3(GUI 환경을 구성하는데 사용하는 widget toolkit) 환경에서만 동작한다. 기본값은 false 이다.
  - `transparent` : 창을 투명하게 만든다. 기본값은 false 이다.

 나머지는 [BrowserWindow] 문서를 참조한다.

 보면 옵션들중 특정 OS 에서만 동작할 수 있는 것들이 있다. 빌드시에 환경을 체크하는 작업이 필요하다는 의미이다.

 하지만 일단 MacOS 와 Window 환경에 초점을 맞추고 개발하려고 한다.
 BrowserWindow 에서 html 페이지를 로드하게되면 해당 페이지는 webContents 로 취급된다.
 함수는 `loadURL` 이다.
 ```javascript
 onst {width,height}= electron.screen.getPrimaryDisplay().workAreaSize;
 win = new BrowserWindow({width: width/2, height: height/2,modal:true});

 // and load the index.html of the app.
 win.loadURL(url.format({
   pathname: path.join(__dirname, 'login.html'),
   protocol: 'file:',
   slashes: true
 }));

 // Open the DevTools.
 win.webContents.openDevTools();

 // Emitted when the window is closed.
 win.on('closed', () => {
   // Dereference the window object, usually you would store windows
   // in an array if your app supports multi windows, this is the time
   // when you should delete the corresponding element.
   console.log('window closed');
   win = null;
   app.quit();
 });
 ```

위 코드에서는 현제 스크린의 width, height 의 절반만큼의 사이즈로 창을 생성하고 창은 modal 로 띄웠다.

그 창에 login.html 을 로드하고 개발자 도구화면을 같이 띄워줬다.
그리고 창에 closed 이벤트를 리슨하고 처리할 콜백을 등록해줬다.

창이 닫히게 되면 창을 null 로 초기화 해준다. 그리고 `app.quit()` 을 호출하여 앱을 종료시킨다.

물론 실제 로그인 화면이라면 `app.quit()` 을 이곳에서 호출하면 안될것이다.

기본적으로 html 로 작성한 화면을 가지고오는 것은 이런식의 처리가 되고 이외의 기능 부분은 js 를 로드하면 된다.

기존의 웹 페이지 개발과 크게 다르지 않다.

이제 즐겁게 작업을 해본다.

사용할 라이브러리중 대표적인건 socket.io, mongoose, nedb 이다.

[socket.io] 는 실제 채팅 기능을 구현하는데 사용할 것이다.

[mongoose] 는 mongodb 를 좀 더 쉽게 이용하기 위해 사용할 것이다.

[nedb] 는 [Electron] 으로 작업한 클라이언트에 embeded 시킬 nosql db 이다.

[nedb] 의 경우는 [sqllite3] 를 사용할까도 했지만 어차피 서버에 nosql db 를 사용하니 비슷하게 갈 수 있는 db를 찾았다.

작업 순서는 필요한 기능 구현 후 화면 디자인 작업을 하려한다.

그래서 일단 User 모델 설계부터 시작한다. 즉

1. 데이터 모델 설계
2. Message 기능 구현
3. Room 기능 구현
4. 화면 작업
5. Bot 에서 사용할 Dialog interface 설계
6. Bot Dialog interface 관리 화면 작업
7. Desktop App 배포
8. Mobile App 배포

Mobile 퍼스트가 아닌 이유는 만들 챗봇이 모바일보다는 데스크탑에서 활용될 일이 많기 때문이다.

그리고 [Electron] 을 공부하고 싶은 욕심도 있기도 하고 Mobile 을 먼저하다 보면 그냥 native 로 개발하고픈 욕심이 생길거같아서 그렇다.

Web frontend 공부를 하면서 진행할 프로젝트기에 이렇게 진행한다.

[socekt.io]:https://socket.io/
[mongoose]:http://mongoosejs.com/
[nedb]:https://github.com/louischatriot/nedb
[sqllite3]:https://github.com/mapbox/node-sqlite3
[Electron]:https://electronjs.org/
[BrowserWindow]:https://electronjs.org/docs/api/browser-window
[Frameless Window]:https://electronjs.org/docs/api/frameless-window
[Electron-App-Docs]: https://electronjs.org/docs/api/app
[App-list]:https://electronjs.org/apps
