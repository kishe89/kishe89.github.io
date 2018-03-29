---
layout: post
title:  "Electron & Socket.io 를 이용한 챗봇 개발기1"
date:   2018-03-29 13:40:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Electron
---


[Electron] 은 Javascript, HTML, CSS, Node Js runtime 를 이용한 데스크탑용 크로스플랫폼 개발 프레임워크이자 runtime 이다.

장점은 다른 웹기반 크로스플랫폼 개발에 같은 화면을 사용할 수 있다.

[Electron] 을 이용하여 개발된 Application 들은 [App-list]에서 확인할 수 있다.

##### Electron Application Architecture

기본적인 구조에 대해서 보면 **main process** 와 **renderer process** 가 존재하는데
**main process** 는 package.json 의 main 스크립트이다. **main process** 는 GUI 를 웹페이지를 바탕으로 구성할 수 있다.
[Electron]은 하나의 **main process** 를 가진다.

process 들은 물론 여러개 사용 가능하다 **renderer process** 를 제외하고도 process fork 등을 통해서 여러개의 process 를 가질 수 있다.

process 간 통신은 IPC 를 이용하며 이를 이용해야할 상황은 Web 페이지 내에서 OS GUI API 등을 호출해야할 때 **renderer process** 와 **main process** 의 통신을 통해서

**main process** 에서 호출하도록 한다.

process 간 통신에 사용되는 구현체는 `ipcRenderer` 와 `ipcMain` 이다.

[Electron] 에서 화면을 생성하는 것은 **main process** 에서만 가능한데 process 간 통신이 가능하여 **renderer process**  에서 **main process** 에게 요청할 수 있다.
이 때 사용하는 모듈은 `remote` 이다.

```javascript
  const { remote } = require('electron')
  const { BrowserWindow } = remote

  const win = new BrowserWindow()
```

### 설치

```
npm install --save-dev electron
```
설치는 위와 같이 npm 을 이용한다.

### 실행

```javascript
{
    "name": "your-app",
    "version": "0.1.0",
    "main": "main.js"
    "scripts":{
      "start":"electron ."
    }
}

```
package.json 을 정의해준다. 스크립트의 실행은 아래와 같다.

```
npm start [args]
```

### Window 생성

##### main.js
```javascript
const {app, net, BrowserWindow} = require('electron');
const path = require('path');
const url = require('url');
let win;
function createWindow () {
    // Create the browser window.
    win = new BrowserWindow({width: 800, height: 600});

    // and load the index.html of the app.
    win.loadURL(url.format({
        pathname: path.join(__dirname, 'index.html'),
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
        win = null
        app.quit();
    });
    const request = net.request('http://127.0.0.1:3000/users');

    request.on('response', (response) => {
        console.log(`STATUS: ${response.statusCode}`);
        response.on('data', (chunk) => {
            console.log(`BODY: ${JSON.parse(chunk).a}`)
        })
        response.on('error', (error) => {
            console.log(`ERROR: ${JSON.stringify(error)}`);
        });
    });
    request.end();
};

app.on('ready', createWindow);
// Quit when all windows are closed.
app.on('window-all-closed', () => {
    // On macOS it is common for applications and their menu bar
    // to stay active until the user quits explicitly with Cmd + Q
    console.log('All Closed');
    if (process.platform !== 'darwin') {
        app.quit()
    }
})

app.on('activate', () => {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    console.log('activate');
    if (win === null) {
        createWindow()
    }
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.
```

처음으로 할일은 electron 모듈을 로드하는 것이다.

```javascript
const {app, net, BrowserWindow} = require('electron');
```
하나씩 보면 창을 생성하고 창에서 발생하는 이벤트에 대한 API 들을 제공하는 BrowserWindow 클래스

어플리케이션의 생명주기를 관리하는 app 그리고 HTTP/HTTPS 프로토콜로 통신을 할 수 있도록 지원해주는 net library(Node library 는 아니고 chromium 의 native library 이다.)

이다. app 이 시작되면 ready 이벤트가 전달되는데 이 때부터 net 과 BrowserWindow 를 사용할 수 있다.

이전에 호출시 예외를 뱉어낼 것이다.

위 main.js 에서 제어한 app 의 이벤트들만 하나씩 본다.

- ready : app 이 시작할 준비가 될 때 발생하는 이벤트(io API 호출가능)
- activate : app 이 작업표시줄 혹은 dock 바에 내려갔다가 혹은 dock 바에서 클릭시 발생하는 이벤트
- window-all-closed : mac 에서 cmd + Q 로 app 종료시켰을 때 혹은 app 에서 관리하는 window 가 하나도 없을 때 발생하는 이벤트.

이 3개 외에도 다양한 제어가능한 이벤트들을 제공한다. 나머진 [Electron-App-Docs] 를 참고한다.

BrowserWindow 는 창(window) 의 생성자 및 이벤트 관련 API 들을 제공하는데 위에서 사용한 이벤트와 생성자 및 함수들만 본다.

```javascript
win = new BrowserWindow({width: 800, height: 600});
```
pixel 단위의 width, height 를 인자로 생성한다.

```javascript
win.loadURL(url.format({
        pathname: path.join(__dirname, 'index.html'),
        protocol: 'file:',
        slashes: true
    }));
```
생성된 BrowserWindow 객체에 해당 URL 의 문서를 로드한다.
위에서는 index.html 파일을 로딩한다.

```javascript
// Open the DevTools.
    win.webContents.openDevTools();
```

개발 작업시 유용한 함수로 Chrome 개발자도구 창이 뜬다.

```javascript
win.on('closed', () => {
        // Dereference the window object, usually you would store windows
        // in an array if your app supports multi windows, this is the time
        // when you should delete the corresponding element.
        console.log('window closed');
        win = null
        app.quit();
    });
```

창이 닫힐 때 예를들어서 사용자가 타이틀바의 x 를 클릭한다던가 cmd+Q or alt+F4 로 종료시
발생하게 된다. 윈도우를 null 로 초기화 해주도록 한다. 안그러면 메모리릭이 발생할 수 있다.

이제 마지막으로 net 에대해서 보도록한다.

HTTP 요청을 생성할 때는 아래와 같이 사용한다.

```javascript
const request = net.request('http://127.0.0.1:3000/users');
request.end();
```

Node Js 의 HTTP 요청 구문과 상당히 비슷하게 보이는데 도큐먼트에서도 해당 부분에 대해서 비슷하게 하려했다고 적혀있다.

로컬호스트의 3000번 포트로 웹서버를 하나 간단한걸 띄워놓고 호출한것인데 구글 페이지던 뭐 아무거나 써보도록한다.

요청에 대한 응답은 request 객체가 response 이벤트를 핸들링 해줄 수 있도록 listen 해주면 된다.

```javascript
request.on('response', (response) => {
        console.log(`STATUS: ${response.statusCode}`);
        response.on('data', (chunk) => {
            console.log(`BODY: ${JSON.parse(chunk).a}`)
        })
        response.on('error', (error) => {
            console.log(`ERROR: ${JSON.stringify(error)}`);
        });
    });
```
콜백으로 response 인자가 넘어오는데 response 는 header,body,status, ... 등을 포함하는 HTTP 응답 객체이다.
이 부분의 제어는 다른곳에서도 똑같으므로 그냥 한번 슥 보고 넘어간다.

이렇게 기본적인 일렉트론 예제를 한번 봤다.

이제는 열심히 문서를 보면서 필요한 기능을 구현하면 된다.

다음 글은 Socket.io 를 이용하여 기본적인 채팅 기능을 구현할 것이다.

[Electron]:https://electronjs.org/
[Electron-App-Docs]: https://electronjs.org/docs/api/app
[App-list]:https://electronjs.org/apps
