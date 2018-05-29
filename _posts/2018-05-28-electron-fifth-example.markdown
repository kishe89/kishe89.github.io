---
layout: post
title:  "Electron & Socket.io 를 이용한 챗봇 개발기5"
date:   2018-05-26 16:14:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Electron
---

이번 포스팅에서는 클라이언트 코드 부분을 보도록한다.

본격적인 포스팅에 앞서 약을 약간 팔자면 이번 프로젝트를 하면서 기술적인 목표를 몇가지 잡은게 있는데

아래와 같다.

1. Web frontend 공부
2. electron 공부
3. react 공부
4. react-native 공부

각각의 단계에서 지금 과정은 1~2번이다.

굳이 react를 Web frontend 공부에서 분리한 이유는 부족한 Web frontend의 기초를 다지며

facebook이 거쳐온 과정과 비슷하게 진행해보는걸로 react 자체에 대해서 기술적인 필요성을 몸으로 느끼기 위해서이다.

일부러 JQuery의 사용 또한 배제하고 있다.

해서 지금의 코드는 상당히 지저분하며 올바르지 못한 코드일 가능성이 높다는 점을 먼저 약을판다.

ㅜ.ㅜ

일단 이전 포스팅들중
- [Electron & Socket.io 를 이용한 챗봇 개발기1]
- [Electron & Socket.io 를 이용한 챗봇 개발기2]

위 두 포스팅에 대한 내용들은 보고 이 포스팅을 보길 바란다.

처음 볼 코드는 로그인 화면이다.

### Login window

일단 로그인 화면을 구성할 html 문서를 보도록 한다.

##### login.html
```HTML
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>배틀그라운드 마스터</title>
    <link rel="stylesheet" type="text/css" href="./app/css/login.css">
</head>
<body>
<div class="background"></div>
<div class = "login-form-container">
    <div id="lottie"></div>
    <h3 class="page-title">Please Sign In</h3>
    <div class="SignInButton" id="SignInButton">
        Sign In
    </div>
    <div class="SignUpButton" id="SignUpButton">
        Sign Up
    </div>
</div>
</body>
<script src="https://cdn.socket.io/socket.io-1.2.0.js"></script>
<script src="./app/services/login.js"></script>
</html>
```

많은 내용은 없고 login을 위한 SignIn 버튼과 SignUp 버튼이 있다.

[Electron]에서 화면을 그릴 때 html을 이용하여 그릴 수 있는데 BrowserWindow 객체의 load 함수를 이용하여 그릴 수 있다.
`
앱의 시작을 의미하므로 프로젝트의 루트디렉토리에 main.js 라고 이름 붙인 js 파일을 만들고 아래와 같은 코드를 작성한다.

##### main.js

```javascript
const electron = require('electron');
const {app, BrowserWindow, ipcMain} = electron;
const path = require('path');
const url = require('url');
const fs = require('fs');
const axios = require('axios');
const FB = require('fb');
const FBManager = require('./main/fbmanager');
const fbManager = new FBManager(app,axios,path,fs,FB);

let win;
let locale;

function createAuthWindow() {
  fbManager.login(win,BrowserWindow);
};

function createLoginWindow() {
  const {width,height}= electron.screen.getPrimaryDisplay().workAreaSize;
  locale = app.getLocale();
  const webPreference = {
    affinity:true
  };

  // Create the browser window.
  win = new BrowserWindow({
    width: width/2>600? width/2 : 600,
    minWidth:width/2>600? width/2 : 600,
    height: height/2>600? height/2 : 600,
    minHeight:height/2>600? height/2 : 600,
    resizable:false,
    fullscreenable:false,
    fullscreenWindowTitle:false,
    webPreferences:webPreference
  });

  // and load the index.html of the app.
  win.loadURL(url.format({
    pathname: path.join(__dirname, 'login.html'),
    protocol: 'file:',
    slashes: true
  }));
  win.webContents.openDevTools();
  win.on('enter-full-screen',(event)=>{
    console.log('win : enter-full-screen');
  });
  win.on('maximize',(event)=>{
    console.log('win : maximize');
  });
  win.on('enter-html-full-screen',(event)=>{
    console.log('win : enter-html-full-screen');
  });
  // Emitted when the window is closed.
  win.on('closed', () => {
    // Dereference the window object, usually you would store windows
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    console.log('window closed');
    win = null;
    app.quit();
  });
};

app.on('ready', createLoginWindow);
// Quit when all windows are closed.
app.on('window-all-closed', () => {
    // On macOS it is common for applications and their menu bar
    // to stay active until the user quits explicitly with Cmd + Q
    console.log('All Closed');
    if (process.platform !== 'darwin') {
        app.quit()
    }
});

app.on('activate', () => {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    console.log('activate');
    if (win === null) {
        createLoginWindow();
    }
});

ipcMain.on('login',(event,args)=>{
  /**
   * @TODO validation logic
   */
  win.webContents.send('login_success',args);
});
ipcMain.on('fb-authenticate',(event,args)=>{
  /**
   * @TODO validation logic
   */
  createAuthWindow();
});

```

순서대로 보면 일단 electron 모듈에서 우리가 필요한 클래스 및 함수들을 가지고 와야한다.

```javascript
const electron = require('electron');
const {app, BrowserWindow, ipcMain} = electron;
```

물론 위 3가지 이외에도 제공해주는 것들은 더 많다.

하지만 현재 우리가 로그인 화면을 띄우는 데 필요한것은 위 3가지면 충분하다.

일단 Application의 라이프사이클을 관리하는 app

화면을 나타내는 API들을 가지고 있는 BrowserWindow

그리고 BrowserWindow로 생성된 뷰 프로세스와 ipc 를 이용한 통신을할 ipcMain 객체이다.

내가 검색해본 결과(깃헙에서) 보통 Angular를 이용한 싱글페이지 앱으로 작업한 프로젝트들이 많이 보였다.

하지만 굳이 싱글페이지 앱일 필요는 없다.

얼마든지 BrowserWindow로 차일드 프로세스들을 생성할 수 있고 또한 뷰관련이 아니더라도 프로세스는 생성할 수 있다.

일단 [Electron] Application이 실행 준비되면 `'ready'` 이벤트가 발생되며 이를 app 객체를 통해서 받을 수 있다.

`'ready'` 이벤트는 정말 중요한데 왜냐하면 아래와 같은 코드들이 정상동작을 하는데 필요한 상태이기 때문이다.

```javascript
app.getLocale();
```

어플리케이션의 locale 값을 가지고 오는 코드이다. app 이 ready 상태가 아닐 때도 이 함수는 동작을 한다.

항상 디폴트값인 'en-US' 값을 반환하면서...

처음에 에러없이 동작하길래 정상동작을 하는줄 알았지만 아니었다.(덕분에 다른코드에서 타임존변환 잘못한줄알고 30분동안 삽질)

환경에 관련된 함수들은 app이 `'ready'`에 이르러야만 우리가 생각하는 정상적인 값을 반환하게 된다.

꼭 기억하고 나와 같은 실수를 하지 않길 바란다.

다시 화면 그리는것으로 이야기를 돌리자면 `'ready'` 가 되면 아래처럼 BrowserWindow 를 생성하는 콜백을 던져주면 된다.

```javascript
const path = require('path');
const url = require('url');
const fs = require('fs');
let win;
app.on('ready', createLoginWindow);
```

`createLoginWindow` 함수는 아래와 같다.

```javascript
function createLoginWindow() {
  const {width,height}= electron.screen.getPrimaryDisplay().workAreaSize;
  locale = app.getLocale();
  const webPreference = {
    affinity:true
  };

  // Create the browser window.
  win = new BrowserWindow({
    width: width/2>600? width/2 : 600,
    minWidth:width/2>600? width/2 : 600,
    height: height/2>600? height/2 : 600,
    minHeight:height/2>600? height/2 : 600,
    resizable:false,
    fullscreenable:false,
    fullscreenWindowTitle:false,
    webPreferences:webPreference
  });

  // and load the index.html of the app.
  win.loadURL(url.format({
    pathname: path.join(__dirname, 'login.html'),
    protocol: 'file:',
    slashes: true
  }));
  win.webContents.openDevTools();
  win.on('enter-full-screen',(event)=>{
    console.log('win : enter-full-screen');
  });
  win.on('maximize',(event)=>{
    console.log('win : maximize');
  });
  win.on('enter-html-full-screen',(event)=>{
    console.log('win : enter-html-full-screen');
  });
  // Emitted when the window is closed.
  win.on('closed', () => {
    // Dereference the window object, usually you would store windows
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    console.log('window closed');
    win = null;
    app.quit();
  });
};
```

한줄 한줄 보도록 한다.

`createLoginWindow` 함수의 첫 라인을 보면
```javascript
const {width,height}= electron.screen.getPrimaryDisplay().workAreaSize;
```
와 같은 코드가 있다.

현제 주 디스플레이의 화면 사이즈를 가지고오는 속성으로 width, height 는 pixel 단위이다.


```javascript
locale = app.getLocale();

```

두번째라인의 위 코드는 app이 실행중인 환경의 locale 정보를 가지고 오는 함수이고 이를 locale 변수에 할당한 것이다.

locale을 가지고 온 이유는 앱의 타임존변경 및 추후 다국어 지원을 위해서이다.

위에서 이야기 했듯이 app의 ready 이후의 흐름에서 실행해야 정상동작한다.

이제 3번라인을 보도록 한다.

```javascript
const webPreference = {
    affinity:true
  };
```

webPreference 는 [BrowserWindow] 클래스에서 웹의 특징들을 설정하는 옵션이다.

```javascript
win.webContents.openDevTools();
```
와 같이 화면에 개발자도구를 키는 함수가 있다.

이렇게 [BrowserWindow]는 web의 기능들을 이용할 수 있는데 이러한 기능의 사용여부 및 동작에 관련한 옵션들이다.
세션을 이용하는 규칙, 스크립트의 로드시 특정스크립트를 먼저 로드하는등의 옵션들을 지정할 수 있다.

이중 devTools 옵션이 있는데 기본값을 `true`이고 이를 false로 세팅하게 되면 openDevTools()는 사용할 수 없다.

`affinity`는 [BrowserWindow]를 생성하여 렌더할때 각각의 rendererProcess를 사용하는게 아니라 기존 rendererProcess를 재사용한다.

그래서 특정 webPreference 옵션들은 공유될 수 있다.

딱히 웹콘텐츠의 동작순서가 영향을 미치지 않기때문에 다른 옵션들은 손대지 않고 일단은 같이 공유하도록한다.

그 아래라인을 보도록 한다.

```javascript
// Create the browser window.
  win = new BrowserWindow({
    width: width/2>600? width/2 : 600,
    minWidth:width/2>600? width/2 : 600,
    height: height/2>600? height/2 : 600,
    minHeight:height/2>600? height/2 : 600,
    resizable:false,
    fullscreenable:false,
    fullscreenWindowTitle:false,
    webPreferences:webPreference
  });
```

[BrowserWindow]의 생성부분이다.

로그인 화면의 크기를 지정해주고 크기를 조절가능하게 할지, 전체화면을 가능하게할지, 전체화면모드에서 타이틀바에 타이틀을 보여줄지 여부

그리고 마지막으로 webPreferences 를 세팅해주었다.

width와 height 그리고 minWidth, minHeight 는 전체화면의 크기를 가지고온 후 절반이 600pixel 이상일경우에만

화면해상도를 기준으로 화면을 그리고 아닌 경우는 600 x 600으로 고정하였다.

이유는 login.html 를 그리는데 필요한 최소 픽셀이어서 그렇다.(디자인에 따라 다르게 잡으면 되겠다.)


그 다음 코드를 본다.

```
// and load the index.html of the app.
  win.loadURL(url.format({
    pathname: path.join(__dirname, 'login.html'),
    protocol: 'file:',
    slashes: true
  }));
```

생성한 [BrowserWindow] 객체의 화면을 그릴 때 어떤 html 을 사용할지 셋하는 부분이다.

nodejs 의 url 모듈을 이용하였는데 최신버전은 object를 파라미터로 하지 않고 url, options 객체를 인자로 한다.

일단 지금 사용한 이전버전의 api를 보면 아래의 구조와 같다.
```javascript
{
  protocol: 'https',
  hostname: 'example.com',
  pathname: '/some/path',
  query: {
    page: 1,
    format: 'json'
  }
}
```

만들 url String의 protocol 위 예에서는 https 프로토콜을 이용하여 가지고 오기때문에 https이다.

반환값은 만들어진 url String 이다.

우리의 코드로보면 file:///프로젝트루트/login.html 과 같은 형태가 될것이다.

내경우는`file:///Users/kjw/ElectronWorkspace/FirstExample/login.html` 가 나오게 된다.


해서 로드할 html 파일의 위치까지 알려줘서 로드하게된다.

그럼 html을 로드하게 되고 html에서 load 하는 javascript, css 등도 로드가 되게 된다.

개발자 도구를 키는 라인은 넘어간다 위에서 설명했으니.

그 아래는 화면의 제어에 대한 이벤트 몇가지에 대해서 리스너를 등록해놓은 것이다.

```javascript
win.on('enter-full-screen',(event)=>{
    console.log('win : enter-full-screen');
  });
  win.on('maximize',(event)=>{
    console.log('win : maximize');
  });
  win.on('enter-html-full-screen',(event)=>{
    console.log('win : enter-html-full-screen');
  });
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

일렉트론은 native와 web의 화면에 대한 특성을 제어한다.

예를들어서 확대등에 대한 일반적인 웹의 속성들도 지원한다.

나머진 문서를 참고하도록 하고 closed에 대해서만 본다.

윈도우는 여러개 일 수 있다. 이 때 메인 윈도우가 종료되면 앱이 종료되는 흐름은 일반적일 것이다.

그외 서브 윈도우들의 종료는 앱의 종료로는 이어지면 안된다. 이를 제어하는 곳이다.


android 로 치면 Activity의 OnDestroy 와 같은 부분으로 보면 될듯하다.

해서 지금 현제 로그인 윈도우만 떠있고 이를 사용자가 닫는다면 앱은 종료되어야 할것이다.


해서 [BrowserWindow]객체를 할당받은 win 변수를 null로 초기화해주고 app의 종료함수인 quit() 함수를 호출해준다.

이로써 기본적인 window 생성법에 대해서 봤다.


webPreferences 에는 webGl의 사용여부 등과 같은 중요한 속성들이 더 있다.

이에 대해서는 사용하게 되면 점진적으로 정리해나간다.


css 와 js 는 정리가 되면 올리도록 하겠다.


다음 포스팅에서는 facebook Oauth 를 연동하는 과정을 정리하도록 하겠다.

아래는 발디자인으로 디자인한 화면이다.

![Alt text](/assets/Electron/sc1.png)


[Electron & Socket.io 를 이용한 챗봇 개발기1]:https://kishe89.github.io/electron/2018/03/29/electron-first-example.html
[Electron & Socket.io 를 이용한 챗봇 개발기2]:https://kishe89.github.io/electron/2018/04/04/electron-second-example.html
[emit-cheatsheet]:https://socket.io/docs/emit-cheatsheet/
[axios]:https://github.com/axios/axios
[socket.io]:https://socket.io/
[mongoose]:http://mongoosejs.com/
[Electron]:https://electronjs.org/
[BrowserWindow]:https://electronjs.org/docs/api/browser-window

