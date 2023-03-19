---
layout: post
title:  "Fastlane&SelfHostedRunner"
date:   2023-03-19 21:48:00
author: 김지운
cover:  "/assets/instacode.png"
categories: Javascript
---

### 들어가며

"이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다."

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
회사 개발팀의 `React-Native` 테승트&빌드&배포는 내 회사 맥북을 호스트로 사용하도록 구성했다.

어차피 유튜브 영상작업 및 외부에 들고 다닐 목적으로 개인적으로 갤럭시 북3 프로 360 를 구매하여서 사용중이기에  
회사 맥북은 들고 다닐일이 없어졌다.  
갤럭시 북3 프로 360은 만약 삼성 제품들 특히 폴드와 갤럭시 태블릿을 주요 모바일 기기로 사용한다면 강추한다.

퀫쉐어, 스크린레코더, 스크린플로우, 세컨드 스크린등 주변 기기와 함께 사용하는데 도움이 되는 기능들을 많이 제공하고 퀄리티도 많이 좋아졌다.

잠시 원래 내용으로 돌아와서 남는 `OSX` 및 `XCODE` 실행 가능한 기기가 있다면 셀프 호스팅 하는게 좀 더 싸게 돌릴 수 있느 방법이다.

대신 조금의 품이 더 들어가는건 어쩔 수 없다.

이제 해야하는 작업들에 대해서 보도록 한다.

### Github Self Hosted Runner 세팅 및 설치.

먼저 Github actions 를 호스팅할  기기에 Runner 세팅을 해줘야한다.



[Fastlane]:https://fastlane.tools
[Github Self Hosted-Runner]:https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners
[Github Actions Execution Time multiple]:https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions#minute-multipliers
