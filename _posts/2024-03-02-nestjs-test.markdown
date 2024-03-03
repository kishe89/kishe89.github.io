---
layout: post
title:  "NestJS 사용하기"
date:   2024-03-02 19:00:00
author: 김지운
cover:  "/assets/instacode.png"
categories: NestJS
---

### 들어가며

NodeJS 에서 사용하는 웹 프레임 워크는 웹어플리케이션이 수행해야 할 가장 기본적인 기능들만을 포함하고 있는 Express 부터 좀 더 다양한 기능들을 포함하고 있는

NestJS, Hapi, SailsJs 그리고 거의 대부분의 기능을 포함하고 있는 loopback 등이 있다.

이중에 최근 많이 사용되고 있는 NestJS 의 Features 를 알아보며 RDB 설계의 기초에 대해서 학습하도록 한다.

### NestJS With Jest

NestJS 에서는 기본적으로 jest 를 이용한 테스 환경과 유틸리티 코드들을 제공한다.

NestJS 에서 모듈, 프로파이더, 서비스, 컨트롤러, 가드, 인터셉터, 미들웨어등 의 컴포넌트는 서로가

각자 DI 를 통해서 주입 가능한 코드로 작성하는것을 프레임워크에서는 지향하며 이는 테스트에서도 유리한 점이 있다.

어플리케이션을 구성하기 위한 모든 컴포넌트들을 제공하고 NestJS Application 으로 컴파일 하고 이를 사용하는데

이러한 구조로 인해서 이때 주입한 컴포넌트들에 대한 모킹이 단순해진다.

### Example

예시 테스트 코드를 하나 작성해보도록 하겠다.

아래 예시 테스트 코드는 NestJS 에서 StatusService 라고 이름붙인 Service 컴포넌트의 메소드를 테스트하는 코드이다.

```typescript
import { Test, TestingModule } from "@nestjs/testing";
import { StatusService } from "./status.service";
import { statusProvider } from "./status.provider";
import { ConfigModule } from "@nestjs/config";
import { validate } from "../../utils/EnvValidator";
import { DatabaseModule } from "../database/database.module";
import { DataSource, Not, Repository } from "typeorm";
import {
  DATA_SOURCE,
  STATUS_REPOSITORY,
} from "../../constants/ProvideConstants";
import { Status } from "./entities/status.entity";
import { CreateStatusDto } from "./dto/create-status.dto";
import { HealthStatusEnum } from "./enums/health-status-enum";
import { HttpModule } from "@nestjs/axios";
import {
  HTTPModuleDefaultMaxRedirect,
  HTTPModuleDefaultTimeOut,
} from "../../constants/HTTPModuleConstants";
import { AwsModule } from "../aws/aws.module";
import { RemoLoggerModule } from "../../logger/RemoLogger.module";
import {
  HttpStatus,
  InternalServerErrorException,
  Logger,
  NotFoundException,
} from "@nestjs/common";
import { StatusModule } from "./status.module";
import { isErrorNull } from "../../utils/TestUtil";
import { INTERNAL_SERVER_ERROR_RESPONSE_MESSAGE } from "../../httpResponseMessages/responseMessages";
import { addDays } from "date-fns";
import { FindAllStatusDto } from "./dto/find-status.dto";
import { DEFAULT_PAGE_ITEM_COUNT, DEFAULT_PAGE_NO } from "../base/pageNation";
import { DeleteStatusDto } from "./dto/delete-status.dto";
import { generateUUID } from "../../utils/UUIDUtils";
import { UpdateStatusDto } from "./dto/update-status.dto";
import { instanceToPlain } from "class-transformer";

describe("StatusService", () => {
  let service: StatusService;

  const length = 35;
  const totalLength = length * 3;
  let module: TestingModule;
  let datasource: DataSource;
  let statusRepository: Repository<Status>;
  const genParams = (healthStatusEnum: HealthStatusEnum) =>
    Array.from({ length }, (k, v) => {
      const params = new CreateStatusDto();
      params.description = `${healthStatusEnum} - ${v}`;
      params.estimatedCompletionTime = addDays(new Date(), v);
      params.healthStatus = healthStatusEnum;
      return params;
    });
  beforeEach(async () => {
    module = await Test.createTestingModule({
      imports: [
        ConfigModule.forRoot({
          envFilePath: `.${process.env.NODE_ENV}.env`,
          validate,
        }),
        DatabaseModule,
        HttpModule.register({
          timeout: HTTPModuleDefaultTimeOut,
          maxRedirects: HTTPModuleDefaultMaxRedirect,
        }),
        AwsModule,
        RemoLoggerModule.register(new Logger(StatusModule.name)),
      ],
      providers: [...statusProvider, StatusService],
    }).compile();

    service = module.get<StatusService>(StatusService);
    datasource = module.get<DataSource>(DATA_SOURCE);
    statusRepository = module.get<Repository<Status>>(STATUS_REPOSITORY);
  });
  afterEach(async () => {
    jest.clearAllMocks();
    await statusRepository.delete({ parentStatus: Not("") });
    await statusRepository.delete({ uuid: Not("") });
    await datasource.destroy();
    await module.close();
  });
  describe("service.createOperatingNormallyStatus", () => {
    it("should be defined", () => {
      expect(service.createOperatingNormallyStatus).toBeDefined();
    });
    it("should return successfully created status entity(Default case)", async () => {
      const params = new CreateStatusDto();
      params.description = "Operating Normally";
      const status = await service.createOperatingNormallyStatus(params);
      expect(status).toBeDefined();
      expect(status.healthStatus).toEqual(HealthStatusEnum.OperatingNormally);
      expect(status.description).toEqual(params.description);
      expect(status.issuedAt).not.toBeNull();
    });
    it("should return successfully created status entity", async () => {
      const params = new CreateStatusDto();
      params.description = "Operating Normally";
      params.healthStatus = HealthStatusEnum.OperatingNormally;
      const status = await service.createOperatingNormallyStatus(params);
      expect(status).toBeDefined();
      expect(status.healthStatus).toEqual(HealthStatusEnum.OperatingNormally);
      expect(status.description).toEqual(params.description);
      expect(status.issuedAt).not.toBeNull();
    });
    it("should throw InternalServerErrorException", async () => {
      const dummyError = new Error("unknown");
      jest.spyOn(statusRepository, "save").mockImplementation(() => {
        return Promise.reject(dummyError);
      });
      const params = new CreateStatusDto();
      params.description = "Operating Normally";
      params.healthStatus = HealthStatusEnum.OperatingNormally;
      let isError = null;
      try {
        await service.createOperatingNormallyStatus(params);
      } catch (e) {
        isError = e;
      }
      isError = isErrorNull(isError);
      expect(isError).not.toBeNull();
      expect(isError).toBeInstanceOf(InternalServerErrorException);
      expect(isError.message).toEqual(dummyError.message);
      expect(isError.status).toEqual(HttpStatus.INTERNAL_SERVER_ERROR);
    });
  });
});
```

위에서 보면 Testing 용으로 제공되는 TestingModule 에 테스트에 필요한 컴포넌트들을 제공하고 있는 부분이

`BeforeEach()` 부분인데 이 부분을 잘 보면 다음과 같은 코드들이 보인다.

```typescript
service = module.get<StatusService>(StatusService);
datasource = module.get<DataSource>(DATA_SOURCE);
statusRepository=module.get<Repository<Status>>(STATUS_REPOSITORY)
```

테스트하거나 테스트를 위해서 Mocking 이 필요한 코드들의 주입된 인스턴스를 가지고 오는 코드이고 모듈 전체에 대한 모킹이 아니라

부분적으로 모킹하기가 편하다.

부분적으로 모킹하기 편하다는건 테스트 코드를 작성하는데 큰 이점이 있다.

테스트를 작성하면서 큰 코드의 mocking 이 필요한 경우를 매번 겪을 것인데 큰 코드들은

내가 정작 mocking 하기 위한 코드는 일부분임에도 불구하고 내부적으로 가지고 있는 초기화코드

그리고 내부 인스턴스 등등 으로 인해서 내가 mocking 할 코드만 mocking 하기가 쉽지가 않다.

전체 코드중 해당 코드를 타는 부분의 앞단을 전부 mocking 하던가 아니면 모듈 자체를 모킹하는등의 일이 발생하는데

Nest 에서 지향하는바만 지켜준다면 부분 Mocking 이 훨씬 편리해진다.
```typescript
const dummyError = new Error("unknown");
    jest.spyOn(statusRepository, "save").mockImplementation(() => {
        return Promise.reject(dummyError);
});
```

또한 일정부분 AOP(Aspect-oriented programming) 스럽게 작성하는데 용이해진다.

프레임워크에서 강제된다기보다는 유용한 점이 생긴다는 것이니 꼭 따를 필요는 없다.

그리고 이로인해 생기는 단점(순환참조, 모듈 의존성 중복주입으로 인한 문제)들도 있다.

꼭 프레임워크의 구조에 무조건 맞추기보다는 본인의 프로젝트 구조 및 팀 구조가 잘 맞는다 싶은 쪽으로 사용하면 된다.

그리고 혹시 안맞는다면 다른 프레임워크를 찾는게 더 좋은 방법이다.

추가적으로 위에서 매번 module 과 datasource 를 destroy 하고 초기화하는 것은 TypeORM Repository 를

모킹하지 않고 그냥 실제 docker 로 띄워놓은 MySQL 에 쿼리를 날리고 있고 테스트 데이터가 남는것을 방지 하기 위해서(처리 안하는걸 까먹는것 방지) 해놓았다.


[Fastlane]:https://fastlane.tools
[Github Self Hosted-Runner]:https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners
[Github Actions Execution Time multiple]:https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions#minute-multipliers
