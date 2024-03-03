---
layout: post
title:  "Fastlane&SelfHostedRunner"
date:   2023-11-18 19:00:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Javascript
---

### 들어가며

[Fastlane] 과 [Github Self Hosted-Runner] 를 이용한 빌드 및 배포 자동화 정리 글입니다.

[Fastlane]에 대해서 무엇을 하는 것이고 왜 사용하는지 모르시는 분들을 위해 간단하게 이야기하고 진행하도록 하겠습니다.

[Fastlane]은 아래와 같은 일을 위해 사용하는 툴이며 `Ruby`를 이용해 스크립트를 작성합니다.

| 기능      | 내용                             | 설명                                                                                     |
|---------|--------------------------------|----------------------------------------------------------------------------------------|
| 테스트 자동화 | Android&IOS 테스트 스크립트 및 Task 실행 | 이를 통해서 기기(가상&실) 테스트 자동화 및 Meta 정보(스크린샷등) 생성 자동화를 함.                                    |
| 빌드 자동화  | Android&IOS 빌드 스크립트 및 Task 실행  | 이를 통해 중간 배포단계(스토어 track별 배포 및 testFlight&AppDistribution 등에 개발 배포를 통한 버전 관리 및 스테이징 분리. |
| 배포 자동화  | Android&IOS 각 앱스토어에 배포.        | 말 그대로 Build 결과 물 업로드 자동화.                                                              |

기본적으로 `IOS` 앱의 경우는 `OSX`에서 실행 되어야 하므로 `OSX` 이미지를 실행시키고 그 위에서 실행시키거나 실 기기에서 실행 시키는 방법이 있다.

[Github Self Hosted-Runner]에서 사용할 수 있도록 `OSX` 이미지를 제곻하긴 하지만 `Runner`의 실행시간에 곱해지는 [Github Actions Execution Time multiple] 이 다륻게 적용되고  
이는 무료 사용량을 금방 넘어가게 만들 수 있다.

실제 [Fastlane]에 이것저것 `lane`을 작성하고 `lane`에 기능들을 추가하게 되면 실행시간은 상당히 늘어날 수 있는데  
이 때 기본 `실행시간의 * 10` 이라는건 상당한 비용이다.(일반적으로 테스트 돌리는 Ubuntu 에 비하면 그냥 단순 계산해서 10배 비용)  
비용이 무서워서 자주 못 돌리는건 이런 자동화의 큰 장점중 하나인 자주, 막, 겁 없이 코드를 실행해보는 환경구성과는 맞지 않기때문에  
회사 개발팀의 `React-Native` 테스트&빌드&배포는 내 회사 맥북을 호스트로 사용하도록 구성했다.

어차피 유튜브 영상작업 및 외부에 들고 다닐 목적으로 개인적으로 갤럭시 북3 프로 360 를 구매하여서 사용중이기에  
회사 맥북은 들고 다닐일이 없어졌다.  
갤럭시 북3 프로 360은 만약 삼성 제품들 특히 폴드와 갤럭시 태블릿을 주요 모바일 기기로 사용한다면 강추한다.

퀫쉐어, 스크린레코더, 스크린플로우, 세컨드 스크린등 주변 기기와 함께 사용하는데 도움이 되는 기능들을 많이 제공하고 퀄리티도 많이 좋아졌다.

잠시 원래 내용으로 돌아와서 남는 `OSX` 및 `XCODE` 실행 가능한 기기가 있다면 셀프 호스팅 하는게 좀 더 싸게 돌릴 수 있느 방법이다.

대신 조금의 품이 더 들어가는건 어쩔 수 없다.

이제 해야하는 작업들에 대해서 보도록 한다.

### Github Self Hosted Runner 세팅 및 설치.

먼저 Github actions 를 호스팅할  기기에 Runner 세팅을 해줘야한다.

먼저 Runner 를 설치할 유저 계정을 하나 만들어서 분리해준다.(OSX 사용자 계정)

그리고 [Github Self Hosted-Runner] 에서 설명하는대로 필요한 스크립트등을 다운받는다.

1. Github.com 에서 러너를 추가할 조직 resource(조직, 개인 등등) 를 선택한다.
2. 해당 조직 리소스의 Settings 탭을 눌러서 setting 페이지를 띄운다.
3. sidebar 의 actions 를 클릭해서 펜딩된곳에서 Runners 를 선택한다.
4. New Runner 를 클릭하고 New Self-hosted runner 를 선택한다.
5. runner 가 동작할 Os image 및 architecture(x64, arm64, arm32) 를 선택한다. 인텍맥이면 x64 아니면 arm64 or 32 를 선택하면 된다.
6. 다운로드페이지가 뜨거나 다운로드 시작되고 필요한 파일 및 스크립트가 다운로드된다.
7. 터미널을 열어서(윈도우는 관리자 권한으로) 각 스크립트를 실행한다.(윈도우는 c 드라이브에 application-runner 디렉토리로 압축 푸는걸 추천한다.)
8. config 스크립트는 runner application 을 등록한다.(러너를 서비스로 등록하는건 추가적으로 스크립트 실행이 필요하다.)

환경별로 8번은 다르므로 추가적으로 환경별로 적으면 다음과 같다.

일단 압축푼 디렉토리가 `application-runner` 라고 가정하고 한다.
해당 디렉토리에 보면 `svc.sh` 스크립트가 있을거다.

일단 맥, 윈도우, 리눅스 순서로 적는다.
```bash
On Mac
./svc.sh stop
./svc.sh install
./svc.sh start
```
Mac 에서는 위와 같이 먼저 현재 실행중인 runner application 을 중단하고 설치하고 시작한다.
실행중인 runner application 이 없이 초기 설치라면 stop 은 안해도 되지만 아니라면 해주도록 한다.


윈도우에서는 power shell(관리자 권한) 을 이용해서 아래와 같이 등록한다.
```bash
On Windows
Stop-Service "actions.runner.*"
Start-Service "actions.runner.*"
Get-Service "actions.runner.*"
```
해서 마지막 Get-Service 스크립트가 정상 동작해서 동작중인 러너가뜨면 정상 시작 된것이다.

*추가적으로 윈도우의 경우 runner 를 다시 등록하는 경우에는 Github 페이지에서 앞의 1~8 까지를 다시 해서 해야한다.*

리눅스에서는 아래와 같이 등록한다.

```bash
On Linux
sudo ./svc.sh stop
sudo ./svc.sh install
sudo ./svc.sh start
```

마지막으로 만든 OSX 사용자 계정에게 지금 runner 를 등록한 계정 dir에 대한 모든 권한을 주도록 한다.

혹시 설치에 및 실행에 문제가 있었다면 아래를 참고하도록 한다.

```
{User}/Library/Logs/actions.runner.{...}/stderr.log의 내용을 살펴본다.
error log가 Operation not permitted 등 권한 관련 error 라면, bash 터미널의 권한 설정을 확인하고, 권한을 부여한다.
```

### Fastlane 필요 내용 설치.
일단 Fastlane 의 lane 은 ruby 를 이용해 작성하고 실행한다. 이를 위해서 ruby 설치를 먼저 진행한다.
```
Notice
내 환경에서만 발생하는지는 모르겠지만 아래와 같은 이슈가 있었다.
공개된 GitHub action 플러그인중 ruby 설치 action 이 있지만 해당 action 에서 필요한 파라미터중 OSX 의 버전이 있는데 detect 를 못한다.
(runner 와 workflow 그리고 호스트 ENV 세팅해도 detect 안됨)
그래서 Manual 로 설치해야한다.
```

위의 이유로 인해 Github action 사용 하지 않고 manual 로 설치한다.(osx 기본 ruby 는 사용하지 않도록 한다.)

1. 일단 환경 변경의 용이성을 위해 가상 환경을 지원하는 `rbenv` 를 설치한다.
2. `rbenv` 로 프로젝트에서 사용하는 ruby 버전에 맞는 ruby 를 설치한다.

```
# Customize to your needs...
export PATH="$HOME/kimjiwoon/.rbenv/shims:$PATH"
# load rbenv automatically
eval "$(rbenv init -)"
```
각자 사용하는 shell 의 환경설정 파일에 rbenv 실행경로를 추가해주고 `source` 나 각자의 터미널에 맞는 명령어로 환경설정을 다시 로드한다.

3. `openssl@1.1` 을 설치한다.(설치 할 때의 Ruby 버전과 ReactNative 버전 호환성 문제 없는 최신 버전으로)

```
# openSSL
export RUBY_CONFIGURE_OPTS="--with-openssl-dir=/opt/homebrew/opt/openssl@1.1"
```
각자 사용하는 shell 의 환경설정 파일에 openssl 실행경로를 세팅해준다.(위의 경우는 homebrew 로 설치했음.)

4. Fastlane 배포에 사용할 메타 정보를 환경변수로 세팅해준다.

```
# FastLane locale settings
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```

그리고 추가적으로 앱 signing 키, 파베크레덴셜등 민감정보는 프로젝트의 git ignore 로 ignore 시키고

레파지토리 혹은 조직의 Github Secrets 에 등록해서 사용하도록 한다.

키파일은 base64 encoding 해서 올리고 실행 action 에서 다시 디코딩해서 파일출력해서 사용하도록 한다..

### Fastlane 플러그인 설치.

다양한 플러그인들이 있지만 일단 안드로이드 기준으로 아래와 같이 추가한다.

> - [fastlane-plugin-versioning_android]
> - [fastlane-plugin-load_json]
> - [fastlane-plugin-firebase_app_distribution]

각각 안드로이드 스토어 버전정보 가지고 오고 gradle 버전 세팅하는 플러그인.

lane 작성시 필요한 정보들 json 으로 로딩할 떄 사용할 Json 파싱 플러그인.

그리고 Firebase App Distribution 을 이용한 appTester 로 배포 위한 플러그인.

### Fastlane lane 작성

먼저 스토어 업로드 레인 실행전 한번은 스토어에 올려야 한다.

> #### bumpVersionName lane(for android)
>
> ```ruby
>   desc "update versionName"
>   lane :bumpVersionName do
>       android_set_version_name(
>       version_name: version_name
>   )
>   end
> ```
>
> `android build.gradle`(app 수준) 의 `versionName` 을 세팅하는 lane 입니다.
>
> ```gradle
> defaultConfig {
>   applicationId "com.newmetafitrn"
>   minSdkVersion rootProject.ext.minSdkVersion
>   targetSdkVersion rootProject.ext.targetSdkVersion
>   testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
>   versionCode 6
>   multiDexEnabled true
>   versionName "0.0.72"
> }
> ```
>
> 위와 같이 **app 수준의** `build.gradle` 의 `defaultConfig` 의 `versionName` 을 세팅해줍니다.
> version_name 파라미터는 package.json 의 version 을 따라가며 package.json 의 버전은 standard-version 으로 bump 합니다.

> #### bumpVersion lane(for android)
>
> ```ruby
>   desc "update version(All)"
>   lane :bumpVersion do
>       version_code = google_play_track_version_codes(
>           package_name: app_id,
>           track: "internal",
>           json_key: json_key_file_path,
>       )[0]
>       version_code = version_code.to_i > 0 ? version_code.to_i + 1 : 2
>       android_set_version_name(
>           version_name: version_name
>       )
>       android_set_version_code(
>           version_code: version_code
>       )
>   end
> ```
>
> android play store 의 track 버전 코드를 `google_play_track_version_codes` 함수로 가지고 와서 `versionName` 과 `versionCode` 를 세팅 및 bump 해주는 lane 입니다.
> `versionName` 은 **bump** 하지는 않으며 **bumping** 된 `package.json` 의 `version` 을 세팅하며 versionCode 는 스토어에 이전에 배포된 `versionCode` 를 가지고 와서 `+1` 해줍니다.

> #### buildAPK lane(for android)
>
> ```ruby
>   desc "Build APK"
>   lane :buildAPK do
>       gradle(
>           task: "clean assembleRelease"
>       )
>   end
> ```
>
> **Release** 용 **APK** 빌드하는 lane 입니다.

> #### build lane(for android)
>
> ```ruby
>   desc "Build Bundle"
>   lane :build do
>       gradle(
>           task: "bundle",
>           build_type: "Release"
>       )
>   end
> ```
>
> **Release** 용 **AAB** bundle 하는 lane 입니다.

> #### deployInternalDraft lane(for android)
>
> ```ruby
>   desc "Deploy a new version to the Google Play(internal-draft)"
>   lane :deployInternalDraft do
>       version_code = google_play_track_version_codes(
>           package_name: app_id,
>           track: "internal",
>           json_key: json_key_file_path,
>       )[0]
>       version_code = version_code.to_i > 0 ? version_code.to_i + 1 : 2
>       android_set_version_code(
>           version_code: version_code
>       )
>       gradle(
>           task: "clean bundle",
>           build_type: "Release",
>           properties: {
>               'versionName' => version_name,
>               'versionCode' => version_code
>           }
>       )
>       upload_to_play_store(
>           package_name: app_id,
>           version_name: version_name,
>           version_code: version_code,
>           track: 'internal',
>           release_status: 'draft',
>           aab: './app/build/outputs/bundle/release/app-release.aab'
>       )
>       createdTag = git_tag(
>           version_name,
>           version_code,
>           'internal'
>       )
>     slack(
>        message: appName + " App successfully Deploy a new version to the Google Play",
>        channel: "#31-service-qc",  # Optional, by default will post to the default channel configured for the POST URL.
>        success: true,        # Optional, defaults to true.
>        payload: {  # Optional, lets you specify any number of your own Slack attachments.
>            "Platform" => "Android",
>            "Build Date" => Time.new.to_s,
>            "Built by" => "FastLane",
>        },
>        default_payloads: [:git_branch, :git_author], # Optional, lets you specify default payloads to include. Pass an empty array to suppress all the default payloads.
>        attachment_properties: { # Optional, lets you specify any other properties available for attachments in the slack API (see https://api.slack.com/docs/attachments).
>                   # This hash is deep merged with the existing properties set using the other properties above. This allows your own fields properties to be appended to the existing fields that were created using the `payload` property for instance.
>            thumb_url: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT4gb-fCQcI1W9pmVafFhEWE85hlQQPnNRBDdtvLC7LRw&s",
>            fields: [{
>              title: "VersionTag",
>              value: createdTag,
>              short: true
>            },{
>              title: "Publish Track&ReleaseStatus",
>              value: "internal-draft",
>              short: true
>            }]
>        }
>    )
>   end
> ```
>
> android play store 의 내부 테스트 **track** 에 **draft** 상태로 **publish** 하고 **publish** 한 `versionName`, `versionCode`, `track` 을 태그 생성해서 푸시하는 lane
> 업로드는 bundle 해서 AAB 를 올린다.  
> 생성되는 tag 포맷은 `${version_name}-${code}-${track}`이다.  
> draft 로 올라가므로 최종적으로 내부 테스트에 배포하기 위해서는 플레이 콘솔에 가서 직접 배포해주도록 한다.

> #### deployProduction lane(for android)
>
> ```ruby
>   desc "Deploy a new version to the Google Play(production)"
>   lane :deployProduction do
>       version_code = google_play_track_version_codes(
>           package_name: app_id,
>           track: "internal",
>           json_key: json_key_file_path,
>       )[0]
>       version_code = version_code.to_i > 0 ? version_code.to_i + 1 : 2
>       android_set_version_code(
>           version_code: version_code
>       )
>       gradle(
>           task: "clean bundle",
>           build_type: "Release",
>           properties: {
>               'versionName' => version_name,
>               'versionCode' => version_code
>           }
>       )
>       upload_to_play_store(
>           package_name: app_id,
>           version_name: version_name,
>           version_code: version_code,
>           track: 'production',
>           release_status: 'complete',
>           aab: './app/build/outputs/bundle/release/app-release.aab'
>       )
>       createdTag = git_tag(
>           version_name,
>           version_code,
>           'production'
>       )
>     slack(
>        message: appName + " App successfully Deploy a new version to the Google Play",
>        channel: "#31-service-qc",  # Optional, by default will post to the default channel configured for the POST URL.
>        success: true,        # Optional, defaults to true.
>        payload: {  # Optional, lets you specify any number of your own Slack attachments.
>            "Platform" => "Android",
>            "Build Date" => Time.new.to_s,
>            "Built by" => "FastLane",
>        },
>        default_payloads: [:git_branch, :git_author], # Optional, lets you specify default payloads to include. Pass an empty array to suppress all the default payloads.
>        attachment_properties: { # Optional, lets you specify any other properties available for attachments in the slack API (see https://api.slack.com/docs/attachments).
>                   # This hash is deep merged with the existing properties set using the other properties above. This allows your own fields properties to be appended to the existing fields that were created using the `payload` property for instance.
>            thumb_url: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT4gb-fCQcI1W9pmVafFhEWE85hlQQPnNRBDdtvLC7LRw&s",
>            fields: [{
>              title: "VersionTag",
>              value: createdTag,
>              short: true
>            },{
>              title: "Publish Track&ReleaseStatus",
>              value: "production-complete",
>              short: true
>            }]
>        }
>    )
>   end
> ```
>
> android play store 에 production track 에 배포하고 태그 생성하는 lane 이다.  

> #### distribute lane(for android)
>
> ```ruby
>   desc "Firebase distribute"
>   lane :distribute do
>       version_code = google_play_track_version_codes(
>           package_name: app_id,
>           track: "internal",
>           json_key: json_key_file_path,
>       )[0]
>       version_code = version_code.to_i > 0 ? version_code.to_i : 2
>       android_set_version_code(
>           version_code: version_code
>       )
>       gradle(
>           task: "clean assembleRelease",
>           properties: {
>               'versionName' => version_name,
>               'versionCode' => version_code
>           }
>       )
>       firebase_app_distribution(
>           app: "앱아이디",
>           groups: "internal-test",
>           apk_path: "./app/build/outputs/apk/release/app-release.apk",
>           service_credentials_file: json_key_file_path,
>           release_notes: "Lots of amazing new features to test out!"
>       )
>       createdTag = git_tag(
>           version_name,
>           version_code,
>           'internal-app-distribution'
>       )
>     slack(
>        message: appName + " App successfully Deploy a new version to the App Tester",
>        channel: "#31-service-qc",  # Optional, by default will post to the default channel configured for the POST URL.
>        success: true,        # Optional, defaults to true.
>        payload: {  # Optional, lets you specify any number of your own Slack attachments.
>            "Platform" => "Android",
>            "Build Date" => Time.new.to_s,
>            "Built by" => "FastLane",
>        },
>        default_payloads: [:git_branch, :git_author], # Optional, lets you specify default payloads to include. Pass an empty array to suppress all the default payloads.
>        attachment_properties: { # Optional, lets you specify any other properties available for attachments in the slack API (see https://api.slack.com/docs/attachments).
>                   # This hash is deep merged with the existing properties set using the other properties above. This allows your own fields properties to be appended to the existing fields that were created using the `payload` property for instance.
>            thumb_url: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT4gb-fCQcI1W9pmVafFhEWE85hlQQPnNRBDdtvLC7LRw&s",
>            fields: [{
>              title: "VersionTag",
>              value: createdTag,
>              short: true
>            },{
>              title: "Publish Track&ReleaseStatus",
>              value: "internal-draft",
>              short: true
>            }]
>        }
>    )
>   end
> ```

[Fastlane]:https://fastlane.tools
[Github Self Hosted-Runner]:https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners
[Github Actions Execution Time multiple]:https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions#minute-multipliers
[fastlane-plugin-versioning_android]: https://github.com/beplus/fastlane-plugin-versioning_android
[fastlane-plugin-load_json]: https://github.com/KrauseFx/fastlane-plugin-load_json
[fastlane-plugin-firebase_app_distribution]: https://github.com/fastlane/fastlane-plugin-firebase_app_distribution
