---
layout: post
title:  "Electron App 에 NFC 카드리더기 연동하기1"
date:   2019-07-09 18:38:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Electron
---
### 들어가며
---
데스크탑앱 개발중에 NFC 카드리더기 연동 요청이 있어서 연동하며 작성한 보일러 플레이트를 튜토리얼로 공유해본다.

일단 데스크탑 앱 개발 도구로 [Electron] 을 사용한다.

그리고 NFC 카드리더기 연동에는 [nfc-pcsc] 를 이용할것이다.

NFC 카드에 데이터를 쓰는 작업이 필요 없다면 [simple-pcsc] 를 사용해도 된다.

[nfc-pcsc]에는 NFC 에 카드를 쓰는 작업또한 지원하므로 선택해서 사용하면 될것같다.


### 프로젝트 생성.
---

항상 그렇듯이 처음으로 할일은 프로젝트 생성. 의존성 주입. 빌드스크립트 작성이다.

처음으로 프로젝트를 생성한다.

디렉토리 이름은 편의상 pcsc_tutorial 로 하겠다.

그리고 콘솔에 `npm init` 명령을 실행해준다.

콘솔에 차례대로 필요한 내용들을 입력해주는데 편의상 entry 만 main.js 라고 동일하게 입력해준다.

그러면 프로젝트에 *package.json* 파일이 생성되어있을 것이다.

이제 필요한 의존성을 *package.json* 에 추가해준다.

아래 명령어를 차례대로 실행하여 의존성을 추가한다.

`npm install electron --save`
`npm install nfc-pcsc --save`

혹시라도 문제가 없다면 다행인데 `nfc-pcsc` 와 같이 native-platform(bcrypt, sharp, ...) 라이브러리를 이용하는 모듈들은
설치된 플랫폼에 맞게 재빌드하는 작업이 필요할 수 있다.

문제가 생기면 해당 모듈은 재빌드 해주도록 하고 그래도 안되면 캐시 삭제하고 재빌드 하고

그래도 정말정말로 안된다면 삭제하고 다시 설치하도록 한다.

### 코드 작성.

본격적인 코드 작성에 앞서 일단 [simple-pcsc] 와 [nfc-pcsc]의 보일러플레이트 코드를 본다.

##### simple-pcsc
```javascript
'use strict';

const PCSC = require('simple-pcsc');
const nfc = new PCSC();

nfc.on('reader', reader => {

    console.log(`NFC (${reader.reader.name}): device attached`);

    reader.on('card', card => {
        console.log(`NFC (${reader.reader.name}): card detected`, card.uid);
    });

    reader.on('error', err => {
        console.log(`NFC (${reader.reader.name}): an error occurred`, err);
    });

    reader.on('end', () => {
        console.log(`NFC (${reader.reader.name}): device removed`);
    });
});

nfc.on('error', err => {
    console.log('NFC: an error occurred', err);
});
```

읽기 동작에 대해서 보일러 플레이트코드로 복잡하지 않다.

NFC 리더기가 연결되면 nfc에 `reader` 이벤트가 발생하게 된다.

reader 이벤트 발생시 콜백으로 reader 객체가 넘어오게 되는데 이게 각각의 device 객체이다.

reader(NFC device)로는 `card`, `error`, `end` 이벤트가 발생되며 이에 대한 이벤트 핸들러를 등록 해주면 된다.

`card` 이벤트는 NFC 카드가 읽히면 카드에 대한 정보를 card 객체로 전달한다.

`error` 이벤트는 각종에러(버퍼,stream, etc)가 발생시 해당 error객체를 전달한다.

`end` 이벤트는 NFC device가 제거되면 발생한다.


##### nfc-pcsc
```javascript
const {
  NFC
} = require('nfc-pcsc');

const nfc = new NFC(); // optionally you can pass logger

nfc.on('reader', reader => {

  // disable auto processing
  reader.autoProcessing = false;
  console.log(`${reader}  device attached`);
  console.log(`${reader.aid}  device aid attatched`);

  reader.on('card', async card => {

    // card is object containing following data
    // String standard: TAG_ISO_14443_3 (standard nfc tags like MIFARE Ultralight) or TAG_ISO_14443_4 (Android HCE and others)
    // String type: same as standard
    // Buffer atr

    console.log(`${reader.reader.name}  card inserted`, card);
    console.log();
    console.log(`card detected`, card);

    // example reading 12 bytes assuming containing text in utf8
    try {

      // reader.read(blockNumber, length, blockSize = 4, packetSize = 16)
      const data = await reader.read(4, 12); // starts reading in block 4, continues to 5 and 6 in order to read 12 bytes
      console.log(`data read`, data);
      const payload = data.toString(); // utf8 is default encoding
      console.log(`data converted`, payload);

    } catch (err) {
      console.error(`error when reading data`, err);
    }

    // example write 12 bytes containing text in utf8
    try {

      const data = Buffer.allocUnsafe(12);
      data.fill(0);
      // const text = (new Date()).toTimeString();
      const text = 'hello world'
      data.write(text); // if text is longer than 12 bytes, it will be cut off
      // reader.write(blockNumber, data, blockSize = 4)
      await reader.write(4, data); // starts writing in block 4, continues to 5 and 6 in order to write 12 bytes
      console.log(`data written`);

    } catch (err) {
      console.error(`error when writing data`, err);
    }
    // you can use reader.transmit to send commands and retrieve data
    // see https://github.com/pokusew/nfc-pcsc/blob/master/src/Reader.js#L291

  });

  reader.on('card.off', card => {
    console.log(`${reader.reader.name}  card removed`, card);
  });

  reader.on('error', err => {
    console.log(`${reader.reader.name}  an error occurred`, err);
  });

  reader.on('end', () => {
    console.log(`${reader.reader.name}  device removed`);
  });

});

nfc.on('error', err => {
  console.log('an error occurred', err);
});
```
코드가 조금 더 길지만 앞에서 본 [simple-pcsc] 코드에 write 기능만 추가된 모양이다.

읽기 부분이벤트는 동일하며 추가적으로 `card.off` 이벤트를 리슨하는 모양이다.

읽기 부분의 처리로직을 보면 데이터를 읽는 부분을 추가했는데 ut8 인코딩 문자열을 읽어들여서 로그를 찍고

그 아래로 데이터를 쓰는 부분이 있다.

12바이트 버퍼를 할당하고 버퍼값을 초기화 해준 이후에 데이터를 쓰는 모습이다.

주석과 로그가 추가 되서 좀 더 길어보이지만 실제 코드량은 얼마 안되므로 읽는데 문제가 없을 것이다.

NFC 데이터 구조에 대해서는 안알아봐서 정확하진 않지만 앞에 블럭은 아마 uid등의 데이터가 쓰여지는 영역으로 사용하는듯하다.

아무리 간단한 코드라도 일단 돌아간다는걸(본인 눈혹은 테스트코드) 확인하지 않은상태에서 다른 코드 작업을 하면
문제가 생겼을때 엉뚱한곳에서 찾을 수 있으므로 위 코드들을 먼저 작성해보고 확인후에 이후 작업을 하는게 좋을것같다.

[Electron]과의 연결은 다음 포스팅에서 이어서 하도록 하겠다.



[Electron]:https://electronjs.org/
[nfc-pcsc]:https://github.com/pokusew/nfc-pcsc#readme
[simple-pcsc]:https://www.npmjs.com/package/simple-pcsc
