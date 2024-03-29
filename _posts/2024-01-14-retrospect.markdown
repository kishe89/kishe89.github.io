---
layout: post
title:  "2023년 회고록"
date:   2024-01-14 00:00:00
author: 김지운
cover:  "/assets/instacode.png"
categories: "Posts"
---

### 들어가며

2024년 1월 14일 조금은 뒤 늦은 2023년의 회고록을 작성해본다.

2023년은 개인적으로 직접적인 회사 제품 개발업무보다는 팀원 스킬업에 집중했던 한해였다.

왜 직접하는 개발 업무보다 팀원의 스킬업에 집중했는지는 본문에 회고를 적으며 적도록 하겠다.


>> ### 1. 이거는 무슨 코드죠?
> 2022년 5월 새 회사로 이직하고 처음 7개월은 회사의 마감기한이 얼마 안남은 과제용 제품들을 처내느라 정신없이
> 아무 생각없이 코드를 복붙하는 나날이 이어졌다.
> 
> 기존에 퇴사자가 작업 진행중에 나간 것부터 시작해서 마감기한은 얼마 안남았지만 작업이 완료되지 않은 것들이 있었기에 
> 제품 설계를 다시 진행한다던가 하는 것은 사치에 속하는 프로젝트였다.
> 
> 잘 그리고 유려하게 동작하는 것보다는 무조건 마감 기한내에 적당히 동작하면 되는 성격의 프로젝트들이 대다수여서
> 기존의 설계 및 작업 결과물을 최소한의 유지관리한 정도로 **test** 작성과 문서화정도를 진행하며 작업을 진행 했다.
> 
> 작업 결과물로 어찌 저찌 과제는 넘어갔지만 작업을 진행하면서 이걸 굳이 시간들여서 작업하는게 시간이 아까운 생각이 드는 것은 어쩔 수 없었다.
> 
> 지나고 보니 변명 섞인 이야기지만 조금만 여유가 있었다면 어떘을까 하는 아쉬움이 남는건 어쩔 수 없다.
> 
> 그렇게 과제용 프로젝트 3개정도를 얼 추 마무리 하고 문제가 생기기 시작 했는데...
> 
> 바로 다른 팀원이 내 코드를 이해하지 못하는 상황이었다.
> 
> 코드 자체가 개판이라서가 아니라 팀 구성상 주니어 웹프론트 개발자만 존재하는 상황이었고 android, ios 에 대한 지식이 전무한 상태에서
> 프론트작업을 진행하다보니 내가 작성한 native 코드단을 인수인계를 해줄 수가 없는 상황이 벌어진 것이다.
> 
> 물론 모바일 개발이 재미있는건 맞지만 회사는 조직이고 혼자 모든일을 하기 위한 조직이 아니므로 나에게도 선택과 집중은 필수적인 상황이 었다.
> 
> 최선은 할 수 있는 사람을 뽑자였지만 6개월간 채용을 진행하면서 원하는 인력을 채용하지 못했고 결국 이대로는 안될거같다는 위기의식이 생겼다.
>
>> ### 2. 그래서 이거는 무슨 코드죠? 
> 회사의 이전 기술 스택을 간략하게 소개하면 다음과 같다.
> 
> ***백엔드***
> 1. express
> 2. mysql
> 3. aws
> 
> ***프론트엔드***
> 1. flutter
> 2. react
> 
> 물론 이외에 형상관리용 git 은 gitlab 을 이용중이었고 기타 다른 것이 존재 했지만 사용은 기초적인 부분만 사용중이었다.
> 
> 이 기초라는 것은 현직자라면 이해할 수 있겠지만 팀 by 팀, 회사 by 회사이지만 이 때의 우리팀은 정말 몇개 샘플 프로젝트 진행해보고 
> 해당 프로젝트들에서 학습한 내용만 가지고 프로젝트를 진행하는 수준이었다.
> 
> 가장 큰 문제는 더 딥다이브 하지 않고 알고있는 내용만으로 모든 스펙을 구현하려한 점이다.
> 
> 주니어밖에 없는 팀에서 누군가 기술적 리딩을 해주지 않으면 결국 팀원 개개인들의 열망과 노력에 맡길 수 밖에 없긴 하지만 개인적으로 느끼기에는 조금 심각한 수준이었다.
> 
> 첫 술자리 때(회식은 자주 했지만 팀 분위기가 술마시는걸 좋아하지 않아서 입사 후 반녀정도 지나고) 이렇게 지속되는 것이 신기하다고 이야기한 기억이 난다...
> 
> 어쨋든 신세한탄만 해서 바뀌는건 없기에 당면한 팀의 핏을 맞추는 일은 투트랙(채용과 교육)으로 방향을 잡고 회사 업무 시간과 별개로 교육을 진행하기로 했다.
> 
> ### 3. 그래서 어떻게 해야하죠?
> 
> 1과 2에서 "이거는 무슨 코드죠?" 는 그래도 프론트, 백엔드 각각 3개월 가량 하루에 3시간 정도씩 진행한 교육으로 어느정도 사라졌다.
> 
> 교육은 최대한 공통적으로 사용될만한 지식들과 검색해서 공부할 수 있는 키워드 위주로 진행했다.
> 교육을 진행하며 나 또한 다시 한번 공부만 하고 잊어버린 기억을 되새길 수 있어서 좋긴 했다.
> 
> 아직 어떻게 해야하죠는 나오지만 그래도 여기서부터는 방법론과 스펙의 문제이고 토론거리이기에 지난 1년(6개월이 신입 들어올 때마다 진행됨...)을 보내며
> 팀 전체적인 핏은 어느정도 맞춰졌다고 생각한다.
> 

### 마치며

요즘 부트캠프만 나온 썡신입(개인적으로라도 실제 유저들 어느정도 사용하는 서비스 개발해서 운영해본 분들 제외) 이 많이 쏟아지고 있는걸로 알고 있고

실제로 채용 진행시 경력직은 거의 이미 업무중이고 이제 시작하는 분들만 많은 미스매칭 시장이 이어지는 것 같다.

어느 산업이던 흥망성쇠의 사이클은 존재하고 3D 업종이던(코리안 패치 월화수목금금금의 대표 직업) 소프트웨어 직군이 각광받교 많은 사람들이 참여하게 된것은 해당 업을 하는 사람으로서

기분 좋은 일이다.

하지만 지금 해당업을 평생의 직업으로 결정하고 들어오시는 미래의 동료분들은 이것들은 체크해보고 진로 결정을 하셨으면 좋겠다.

1. 이 분야가 3D 업종이라도 난 좋은가?(사회적인 평판, 금전정인 보상 그리고 워라벨이)
2. 정말 내가 잘 할 수 있는 일인가?
3. 못해도 포기하지 않을 수 있는가?

꼭 개발업이 아니더라도 위 질문은 직업선택에 있어서 가장 기본적인 질문인 것 같다.

소문난 잔치집에 먹을게 없다는 이야기처럼 최근의 기술직이 각광받는 상황이 쏠림이 더 심해지면 결국 어느 쪽은 비게 되고

이로 인해서 빈곳은 또 새로운 틈새시장이 열리게 될것인데(예를 들면 공무원. 이전의 경쟁률과 지금의 경쟁률 비교해보자.) 단지 현재의 장미빛 전망만으로 업을 택하는건 아닌지 진지한 질문이 필요하다고 생각한다.

너무 부정적인 이야기만 적은 것 같아서 마지막으로 긍정적인 이야기를 적으며 마무리 하겠다.

개발업은 컴퓨터가 존재한 이후 사실 한번도 안좋고 힘들었던 적이 없다.

항상 잘 하는 사람들에게는 근 수십년간 기회의 산업이었고 AI 가 여러 직업군을 위협함에도 직업적으로는 어차피 모두가

AI 를 활용하는 개발자적인 업무를 진행하게 될것은 자명할 것이기에 공부의 끈을 놓지 않고 지속적으로 자기개발을 해나간다면 밥벌이가 끊기는 일은 없을거가록 생각한다.

부디 이 글을 보는 모든 동료들이 2024년 용의 해에는 원하는 일을 성취하시길 바라며 이 글을 마무리한다.
