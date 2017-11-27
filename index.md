### 1일 1작업 및 스터디 정리 페이지.
- Multer Storage Engine(for ObjectStorage)

    node js에서 http multipart/form-data 처리를 위해 많이 사용하는 multer모듈에서 사용하기 위한 ObjectStorage 클라이언트 인터페이스

    [ObjectStorageEngine](./open/README.md)

- MyWay(개인프로젝트)

    2017-11-15 ~ 지금
    
    지도 공유 플랫폼 프로젝트. [MyWayApi](https://github.com/kishe89/MyWayApi)

- StampTour(스탬프투어 플랫폼)

    (주)댓츠잇에서 2015.9.1 ~ 2017.11.31까지 작업 내용
    
    직위 : 사원
    
    앱 설명 : 디바이스 gps 정보 기반으로 일정 범위 내의 장소 들어갈 시 도장 찍기. 종이로 하던 스탬프투어를 대체하기 위해 만듬.
    
    관심 가졌던 문제들 : App패키지 용량, 다국어 지원, 개발 공수는 조금 들어가면서 좀 더 다양하게 경험을 사용자에게 줄 방법.
    
    업무 내용 :
    전체 Database 테이블 및 도큐먼트 설계(RDBMS:MySQL, NoSQL: Mongodb, Store(key-value): Redis) 및 REST API 작업 CloudFoundry(Bluemix) App으로 주로 작업, 
    
    내부 필요 유틸리티 툴 개발(Excel Parsing & Json Converter, QR code 생성),
    
    팀 빌딩(인력 충원 및 감축)
    
    협업 관련 툴 학습 및 교육(git, github, bluemix toolchain, slack, trello)
    
    위치 기반 스탬프투어
    
    |장소    |앱 이름  |작업 내용|   	
    |---	|---	|---	|	
    |신안   	|신안스탬프|Android(Java)클라이언트 100%,Backend(node js) 100%|   	
    |보성   	|보성 스탬프투어|Android(Java)클라이언트 90%,Backend(node js) 100%|
    |보령   	|보령 스탬프투어|Android(Java)클라이언트 90%,Backend(node js) 100%|
    |목포   	|목포 스탬프투어|Android(Java)클라이언트 90%,Backend(node js) 100%|
    |사천   	|사천 스탬프투어|Android(Java)클라이언트 90%,Backend(node js) 100%|
    |서산   	|서산 스탬프투어|Android(Java)클라이언트 90%,Backend(node js) 100%|
    |포천   	|포천 스탬프투어|Android(Java)클라이언트 90%,Backend(node js) 100%|
    |영광   	|영광 스탬프투어|Android(Java)클라이언트 90%,Backend(node js) 100%|
    |여주   	|여주 스탬프투어|Android(Java)클라이언트 90%,Backend(node js) 100%|
    |경주   	|뉴경주 스탬프투어|Android(Java)클라이언트 90%,Backend(node js) 100%|
    |공주   	|공주 스탬프투어|Android(Java)클라이언트 90%,Backend(node js) 100%|
    |남원   	|남원 스탬프투어|Android(Java)클라이언트 90%,Backend(node js) 100%|
    |홍천   	|홍천 스탬프투어|Android(Java)클라이언트 90%,Backend(node js) 100%|
    |코리아트레일|코리아트레일 스탬프투어|Android(Java)클라이언트 90%,Backend(node js) 100%|
    
    QR코드 스탬프투어
    
    |장소|앱 이름|작업 내용|
    |---|---|---|
    |농어촌공사|농촌여행|Android(Java)클라이언트 90%,Backend(node js) 100%, ios(Swift) 50%|
    |댓츠잇|축제 스탬프투어|Android(Java)클라이언트 5%,Backend(node js) 100%|
    
    연구 과제
    
    개인 정보를 받지 않고 중복없는 개인 식별에 대한 방법
    
    아이디어 : One tiem password를 발급 해주고 이에 대해서 Database에서는 Unique한 식별 값을 인식자로 가지고있고 사용자는 손으로 해당 OTP를 적어서 카메라로 찍으면 인식
    
    - 처음 시도 방법 : 서버에서 svm과 mnist 제공 손글씨 데이터를 이용하여 학습된 데이터를 통한 예측으로 전송된 이미지의 값 체크
    - 문제점 : 클라이언트에서 아무런 처리를 하지않은 이미지는 의미가 없음. object detection(여기선 숫자)를 해서 해당 영역들에 대한 정보 혹은 잘라낸 이미지 전송 필요.
    - 다음 시도 방법: OCR 라이브러리 이용 클라이언트 측에서 처리
    - 문제점 : OCR 라이브러리 의존성 큼. 원한만큼 성능이 안나옴
    