---
layout: post
title:  "Youtube 자막 쉽게 번역하고 넣기(Feat. Google 번역기)"
date:   2020-02-16 16:53:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Javascript
---
### 들어가며
---
이 포스팅은 제가 유튜브를 시작하며 자막 쉽게 넣기 동영상들을 보다가 사람들이 srt 파일을 메모장을 이용해 txt 파일로 출력하고 구글 번역기에 돌렸을때 문자가 깨져서 파파고나 다른 번역기를 쓰거나 혹은 수작업 하는걸 보고 작성하게 되었습니다.

일단 구글 번역기로 다음과 같은 문자열을 번역시키면
```
1
00:00:00-->00:00:44
안녕하세요 김지운입니다.

2
00:00:44-->00:00:56
안녕하세요 다다다다.

```

아래와 같이 나오게 됩니다.

```
One
00:00:00-> 00:00:44
Hello, this is Kim Ji-un.

2
00:00:44-> 00:00:56
Hello there.
```

보면 몇개 문자열들이 원래 양식대로 나오지 않는걸 볼 수 있습니다. 자막 순서 번호와 시간값의 양식이 달라지게 됩니다. 원래 없던 공백이 들어가고 있던 하이픈이 사라지고 1은 2로 번역이 되었습니다.

일반인들은 이걸 다른 번역기를 돌린다던가 손으로 수정하겠지만 우린 프로그래머니까 프로그램을 만들어보겠습니다.

막 거창한거 아니고 그냥 정말 저 원본과 달라진 문자열을 정상적인 srt포맷으로 변경할 수 있는 프로그램입니다.

### 소스작성
---
혹시 소스가 먼저 필요하신 분들은 [srcUtil] 에서 받아서 사용하시면 됩니다.

일단 프로젝트 디렉토리를 생성하고(저는 YOUTUEBECHARACTERCONVERT 라고 생성했습니다.) 다음과 같이  npm 초기화를 하도록합니다.

`npm init`

해서 차례대로 진입점과, 작성자, 라이센스, 레파지토리등 기타 정보들 입력해서 초기화 해주시고 생성된 package.json 에 필요한 모듈의존성을 아래와 같이 추가하도록 합니다.
##### package.json
```
{
  "name": "character_convert",
  "version": "0.0.0",
  "description": "change valid result from google translator output",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "start": "node ./index"
  },
  "keywords": [
    "regexp",
    "youtube",
    "google",
    "translator"
  ],
  "author": "Ji Woon Kim",
  "license": "MIT",
  "dependencies": {
    "fs": "0.0.1-security",
    "util": "^0.12.1"
  }
}
```
저는 index.js를 메인스크립트로 지정하고 start 스크립트를 `node ./index`로 index.js 를 실행하도록 하였습니다.

해서 우리가 원하는 기능의 코드를 index.js 아래와 같이 작성해봅니다.
##### index.js
```javascript
const fs = require('fs')
const util = require('util')
const path = require('path')
const writeFile = util.promisify(fs.writeFile)
const readFile = util.promisify(fs.readFile)
const readdir = util.promisify(fs.readdir)
const PATH_DIR_INPUT = './input'
const PATH_DIR_OUTPUT = './output'
const ENG_ESCAPE_STR = 'One'
const PREFIX_LOG = '-------'
const regexp = new RegExp('(([0-9])\\n)(([0-9])\\w+)', 'g')
const whiteSpace = new RegExp(' ','g')
const engExp = new RegExp('One\\n([0-9]){0,2}\\w+ :')
const extenstion = '.srt'
function isEmptyDirectory(inputFileList){
  if(inputFileList === null || inputFileList === undefined){
    throw new Error('isEmptyDirectory function invalid parameter(inputFileList). inputFileList should not null or undefined')
  }
  return inputFileList.length === 0
}
function convertString(src){
  let result = src
  const term = 2
  if(engExp.exec(src)){
    result = '1' + result.slice(engExp.lastIndex + ENG_ESCAPE_STR.length, result.length)
  }
  while (regexp.exec(result) !== null) {
    const slicedString = result.slice(regexp.lastIndex - term, regexp.lastIndex + 26)
    const removedWhiteSpaceString = slicedString.replace(whiteSpace, '')
    const convertTimeLineString = removedWhiteSpaceString.replace('->', '-->')
    const start = result.match(slicedString).index
    const end = start + slicedString.length
    const cursor = regexp.lastIndex - 4
    let agoString = ''
    if(cursor !== 0){
      agoString = result.slice(0, cursor)
    }
    const preFixStr = result.slice(cursor, start)
    const postFixStr = result.slice(end, result.length)
    result = agoString + preFixStr + convertTimeLineString + postFixStr
  }
  return result
}
async function start(){
  const inputFileList = await readdir(PATH_DIR_INPUT)
  if(isEmptyDirectory(inputFileList)){
    throw new Error('You must provide File or Files in input directory')
  }
  const contents = await Promise.all(inputFileList.map((file) => readFile(path.join(PATH_DIR_INPUT, file),{encoding: 'utf-8'})))
  const convert_Contents = contents.map((content) => convertString(content))
  const outpufFilesList = inputFileList.map((file) => path.join(PATH_DIR_OUTPUT, file.slice(0, file.length - 4) + '_convert' + '_' + Date.now() + extenstion))
  await Promise.all(inputFileList.map((file, index) => writeFile(outpufFilesList[index], convert_Contents[index])))
  return outpufFilesList
}

start()
.then((FileNameList) => {
  const fileNameListString = FileNameList.join('\n')
  console.log(`${PREFIX_LOG}Result Block Start${PREFIX_LOG}`)
  console.log(`${fileNameListString}`)
  console.log(`${PREFIX_LOG}Result Block End${PREFIX_LOG}`)
})
.catch((error) => console.log(error.toString()))
```
프로젝트에 `input` 디렉토리와 `output` 디렉토리를 생성해놓고 실행해보도록 합니다. 그냥 정규식으로 대충 패턴을 찾아서 해당 문자열을 치환해서 파일로 출력 해주는 내용이 전부입니다.

단 구글 번역기에서 영어로 번역시 처음 시퀀스 넘버가 1 에서 One으로 번역되는데 그 부분만 예외적으로 처리하도록 추가 해놨으며(다른 언어에서는 발견 못함) 다른 언어로 번역시에 해당 언어로 번역되는 부분이 있다면 추가해주면 되겠습니다.

그리고 작업 내역을 알 수 있게 콘솔에 파일이름등을 찍어준게 이 프로그램의 전부입니다.

이걸 이제 ui를 입혀서 복붙 가능하게 만들면 조금 더 편하고 많은 사람이 이용할 수 있겠죠?

해서 다음 글에서는 웹 사이트와 데스크탑 클라이언트 프로그램을 만들어 보도록 하겠습니다.


[srcUtil]:https://github.com/kishe89/srtUtil