---
layout: post
title:  "NestJS API 개발 가이드 - RESTful API 구축하기"
date:   2024-12-06 20:00:00
author: 김지운
cover:  "/assets/instacode.png"
categories: NestJS
---

### 들어가며

NestJS 에 대해서는 사용한 경험이 있다는 가정하에 Cursor 를 이용해서 Rule 정의 하는 것을 위주로 알아보도록 하겠습니다.

여기서 정의하는 Rule 은 Agent 로 대부분 Accept 가능한 코드로 작성하는 요령을 익힐 수 있는 Rule 정의방식을 찾아가기 위한 Rule 입니다.

### 가장 중요한 기본 rule 

##### 00-base-rules.mdc
```
---
description: Project Base Rule
globs:
alwaysApply: true
---


- Existing code must **never be deleted**.
- All newly generated code must **always be created separately** from the existing code.
- All code under the src directory must be written with the NestJS framework in mind.
```

기본 Rule 은 기존 코드에 대한 가장 중요한 규칙과 사용하는 프레임워크가 무엇인지에 대해서 나타내도록 합니다.

간혹 버전을 명시적으로 매핑한 rule 들이 있는데 실제 오픈소스 혹은 커뮤니티 기반 라이브러리는 딱딱 버전 호환성이 안 맞거나 버그로 인해 못맞추는 경우가 있을 수 있습니다. 너무 명시적으로 제한하는 경우 차라리 브라우저 검색을 통해서 처리하라고 하는게 더 올바른 결과를 나타 낼 수 있지만 이 경우 Context 의 압박이 있을 수 있습니다.

정확히 호환되는 버전들을 사용 안하거나 deprecated 된 코드를 사용해야하는 경우등 실제로는 다양한 케이스들이 있으므로 엣지케이스는 개발자 본인이 처리한다고 가정하고 너무 상세한 rule 은 작성하지 않도록 합니다.

### 프로젝트 디렉토리 구조 rule

##### 01-handler-directory-rules.mdc
```
# Handler Directory Rules

## Handler Structure
- All NestJS resources (controllers, services, modules) must be implemented under the `src/handler/` directory.
- Each feature should have its own subdirectory under `handler/`.
- Follow the standard NestJS module structure within each handler directory.

## Directory Organization
- Controllers: `src/handler/{feature}/{feature}.controller.ts`
- Services: `src/handler/{feature}/{feature}.service.ts`
- Modules: `src/handler/{feature}/{feature}.module.ts`
- DTOs: `src/handler/{feature}/dto/`
- Entities: `src/handler/{feature}/entities/`
- Types: `src/handler/{feature}/types/`
- Interfaces: `src/handler/{feature}/interfaces/`
- Constants: `src/handler/{feature}/constants/`
- Responses: `src/handler/{feature}/responses/`

## Constants Directory Organization
- Error messages: `src/handler/{feature}/constants/{feature}-error-messages.constant.ts`
- Error codes: `src/handler/{feature}/constants/{feature}-error-codes.constant.ts`
- Error types: `src/handler/{feature}/constants/{feature}-error-types.constant.ts`
- Select fields: `src/handler/{feature}/constants/{feature}-select-fields.constant.ts`
- Other constants: `src/handler/{feature}/constants/{feature}.constant.ts`
- Use descriptive file names with feature prefix for better organization
- Group related constants in separate files for maintainability

## Responses Directory Organization
- Main response DTOs: `src/handler/{feature}/responses/{entity}.response.ts`
- Error response DTOs: `src/handler/{feature}/responses/{operation}-error.response.ts`
- Success response DTOs: `src/handler/{feature}/responses/{operation}-success.response.ts`
- Detail response DTOs: `src/handler/{feature}/responses/{entity}-detail.response.ts`
- List response DTOs: `src/handler/{feature}/responses/{entity}-list.response.ts`
- Use descriptive file names with entity/operation prefix
- All response DTOs must use `@Expose()` decorator for proper serialization
- Include `@ApiProperty()` decorators for Swagger documentation
- Use `@Type()` decorator for nested objects when needed

## Naming Conventions
- Use kebab-case for directory and file names (e.g., `user-emails`, `motion-analysis-measures`)
- Controller files: `{feature}.controller.ts`
- Service files: `{feature}.service.ts`
- Module files: `{feature}.module.ts`
- DTO files: `{feature}.dto.ts` or specific purpose DTOs

## Module Structure
- Each handler should have its own module file
- Import required dependencies in the module
- Export controllers and services that need to be used by other modules
- Use providers for dependency injection when needed

## Example Structure
```
src/handler/
├── users/
│   ├── users.controller.ts
│   ├── users.service.ts
│   ├── users.module.ts
│   ├── dto/
│   │   ├── users.dto.ts
│   │   └── signIn.dto.ts
│   ├── entities/
│   ├── types/
│   ├── constants/
│   │   ├── users-error-messages.constant.ts
│   │   ├── users-error-codes.constant.ts
│   │   └── users.constant.ts
│   └── responses/
│       ├── user.response.ts
│       ├── user-detail.response.ts
│       └── sign-in-error.response.ts
├── programs/
│   ├── programs.controller.ts
│   ├── programs.service.ts
│   ├── programs.module.ts
│   ├── constants/
│   │   └── programs-error-messages.constant.ts
│   └── responses/
│       ├── program.response.ts
│       └── program-execution.response.ts
└── handler.module.ts
```
description: Handler Rule
globs: ["src/handler/**/*"]
alwaysApply: true
---
```

개인 프로젝트가 아니라 팀 프로젝트라면 팀 내에서 같은 프레임워크라도 미리 정의딘 다른 린트 규칙 및 코드 작성 규칙이 있을 겁니다.
해당 프로젝트에 맞는 디렉토리 규칙 및 naming rule 을 작성하도록 합니다.

위 rule 은 제가 주로 작성하는 디렉토리 구조에서 사용하는 디렉토리 설명이며 NestJS 컴포넌트중 `Module` 컴포넌트와 `Controller`
`Business logic service`, `Entity manipulation service` 컴포넌트 등에 대한 디렉토리 구조를 나타냅니다.

해당 경로가 아니더라도 상관은 없지만 저는 주로 REST API Controller 와 이에서 사용될 Service 레이어에 대해서 해당 디렉토리 구조를 대체로 따릅니다.

**여기서 WSController, interceptor 나 middleware 등은 이야기 하지 않습니다.**

globs 로 해당 컴포넌트들의 위치에 대한 제약과 정보를 추가로 제공하도록 합니다.

### 별도 컴포넌트에 대한 Rule(Controller)

##### 컨트롤러 rule
```
---
description: Controller Base Rule
globs: ["src/**/*controller*.ts", "src/**/*Controller*.ts"]
alwaysApply: true
---

# Controller Development Rules

## Controller Structure
- Controller class names must use the `Controller` suffix (e.g., `UserController`, `AuthController`).
- File names must follow the `kebab-case.controller.ts` format (e.g., `user.controller.ts`).
- All controllers must use the `@Controller()` decorator.
- Route paths must follow RESTful API design principles.

## HTTP Method Decorators
- GET requests: `@Get()`, `@Get(':id')`
- POST requests: `@Post()`
- PUT requests: `@Put(':id')`
- PATCH requests: `@Patch(':id')`
- DELETE requests: `@Delete(':id')`

## Request/Response Handling
- Use DTO classes to validate request data.
- Responses must follow a consistent format.
- Errors must return appropriate HTTP status codes.
- File uploads must use the `@UseInterceptors()` decorator.

## Dependency Injection
- Services must be injected via the constructor.
- Use the `@Inject()` decorator when necessary.
- Injected dependencies must be declared as `private readonly`.

## Example Code Structure
```typescript
@Controller('users')
export class UserController {
  constructor(
    private readonly userService: UserService,
    private readonly authService: AuthService,
  ) {}

  @Get()
  async findAll(): Promise<UserResponse[]> {
    const result = await this.userService.findAll();
    return plainToInstance(UserResponse, result, { excludeExtraneousValues: true });
  }

  @Get(':id')
  async findOne(@Param('id') id: string): Promise<UserResponse> {
    const result = await this.userService.findOne(id);
    return plainToInstance(UserResponse, result, { excludeExtraneousValues: true });
  }

  @Post()
  async create(@Body() createUserDto: CreateUserDto): Promise<UserResponse> {
    const result = this.userService.create(createUserDto);
    return plainToInstance(UserResponse, result, { excludeExtraneousValues: true });
  }
}
```

컨트롤러에 rule 에서는 서비스 및 DTO 에 대한 사용례만 간단하게 주도록 합니다.

### 별도 컴포넌트에 대한 Rule(Service)



##### Service Rule
```

# Service Development Rules

## Service Types
Services are divided into two main categories based on their purpose:

### 1. Business Logic Services
- Handle complex business logic and orchestration
- Coordinate between multiple entities and external services
- Implement domain-specific business rules
- Follow the standard service patterns described below

### 2. Entity Manipulation Services
- Extend `EntityServiceBase<T>` for TypeORM entity operations
- Provide standardized CRUD operations for entities
- Handle database transactions and query building
- Implement all abstract methods from `EntityServiceBase`
- Always register new Entity Manipulation Services in `entityServicesProviders` located at `src/group-providers/entity-services.provider`.
- Do not add additional business logic or helper methods directly to the service

## Service Structure
- Service class names must use the `Service` suffix (e.g., `UserService`, `AuthService`).
- File names must follow the `kebab-case.service.ts` format (e.g., `user.service.ts`).
- All services must use the `@Injectable()` decorator.
- Services are responsible for business logic.

## Dependency Injection
- Dependencies such as database connections or external API clients must be injected via the constructor.
- All dependencies must be declared as `private readonly`.
- Use the `@Inject()` decorator when necessary.

## Method Naming
- CRUD operations: `create()`, `findAll()`, `findOne()`, `update()`, `remove()`
- Business logic: `validateUser()`, `processPayment()`, `sendNotification()`
- Utility functions: `generateToken()`, `hashPassword()`, `validateEmail()`

## Error Handling
- Business logic errors must throw custom exceptions.
- Database errors must be properly handled and logged.
- For external API failures, consider implementing retry logic.

## Asynchronous Processing
- All external operations must use async/await.
- Prefer async/await over Promise chaining.
- Use `Promise.all()` for concurrent operations when needed.

## Business Logic Service Example
```typescript
@Injectable()
export class UserService {
  constructor(
    @InjectModel(User.name) private userModel: Model<User>,
    private readonly authService: AuthService,
    private readonly logger: Logger,
  ) {}

  async create(createUserDto: CreateUserDto): Promise<User> {
    try {
      const hashedPassword = await this.authService.hashPassword(createUserDto.password);
      const user = new this.userModel({
        ...createUserDto,
        password: hashedPassword,
      });
      return await user.save();
    } catch (error) {
      this.logger.error('Failed to create user', error);
      throw new UserCreationException('Failed to create user.');
    }
  }

  async findAll(): Promise<User[]> {
    return this.userModel.find().exec();
  }

  async findOne(id: string): Promise<User> {
    const user = await this.userModel.findById(id).exec();
    if (!user) {
      throw new UserNotFoundException('User not found.');
    }
    return user;
  }
}
```

## Entity Manipulation Service Example
```typescript
@Injectable()
export class ExternalCameraAllowDeviceEntityService extends EntityServiceBase<ExternalCameraAllowDevice> {
  constructor(
    @Inject(EXTERNAL_CAMERA_ALLOW_DEVICES_REPOSITORY)
    private readonly repository: Repository<ExternalCameraAllowDevice>
  ) {
    super();
  }

  createQueryBuilder(alias?: string, queryRunner?: QueryRunner) {
    if (queryRunner) {
      return this.repository.createQueryBuilder(alias, queryRunner);
    }
    return this.repository.createQueryBuilder(alias);
  }

  create(
    params:
      | DeepPartial<ExternalCameraAllowDevice>
      | DeepPartial<ExternalCameraAllowDevice>[],
    queryRunner?: QueryRunner
  ) {
    if (queryRunner) {
      if (Array.isArray(params)) {
        return queryRunner.manager.create(ExternalCameraAllowDevice, params);
      }
      return queryRunner.manager.create(ExternalCameraAllowDevice, params);
    }
    if (Array.isArray(params)) {
      return this.repository.create(params);
    }
    return this.repository.create(params);
  }

  save(
    params:
      | DeepPartial<ExternalCameraAllowDevice>
      | DeepPartial<ExternalCameraAllowDevice>[],
    queryRunner?: QueryRunner
  ) {
    if (queryRunner) {
      if (Array.isArray(params)) {
        return queryRunner.manager.save(
          ExternalCameraAllowDevice,
          params
        ) as Promise<ExternalCameraAllowDevice[]>;
      }
      return queryRunner.manager.save(
        ExternalCameraAllowDevice,
        params
      ) as Promise<ExternalCameraAllowDevice>;
    }
    if (Array.isArray(params)) {
      return this.repository.save(params);
    }
    return this.repository.save(params);
  }

  findOne(
    findOneOptions: FindOneOptions<ExternalCameraAllowDevice>,
    queryRunner?: QueryRunner
  ) {
    if (queryRunner) {
      return queryRunner.manager.findOne(
        ExternalCameraAllowDevice,
        findOneOptions
      );
    }
    return this.repository.findOne(findOneOptions);
  }

  find(
    findManyOptions: FindManyOptions<ExternalCameraAllowDevice>,
    queryRunner?: QueryRunner
  ) {
    if (queryRunner) {
      return queryRunner.manager.find(
        ExternalCameraAllowDevice,
        findManyOptions
      );
    }
    return this.repository.find(findManyOptions);
  }

  findAndCount(
    findManyOptions: FindManyOptions<ExternalCameraAllowDevice>,
    queryRunner?: QueryRunner
  ) {
    if (queryRunner) {
      return queryRunner.manager.findAndCount(
        ExternalCameraAllowDevice,
        findManyOptions
      );
    }
    return this.repository.findAndCount(findManyOptions);
  }

  update(
    criteria: criteriaType,
    partialEntity: QueryDeepPartialEntity<ExternalCameraAllowDevice>,
    queryRunner?: QueryRunner
  ) {
    if (queryRunner) {
      return queryRunner.manager.update(
        ExternalCameraAllowDevice,
        criteria,
        partialEntity
      );
    }
    return this.repository.update(criteria, partialEntity);
  }

  remove(
    params: ExternalCameraAllowDevice | ExternalCameraAllowDevice[],
    queryRunner?: QueryRunner
  ) {
    if (queryRunner) {
      if (Array.isArray(params)) {
        return queryRunner.manager.remove(
          ExternalCameraAllowDevice,
          params
        ) as Promise<ExternalCameraAllowDevice[]>;
      }
      return queryRunner.manager.remove(
        ExternalCameraAllowDevice,
        params
      ) as Promise<ExternalCameraAllowDevice>;
    }
    if (Array.isArray(params)) {
      return this.repository.remove(params);
    }
    return this.repository.remove(params);
  }

  softRemove(
    params: ExternalCameraAllowDevice | ExternalCameraAllowDevice[],
    queryRunner?: QueryRunner
  ) {
    if (queryRunner) {
      if (Array.isArray(params)) {
        return queryRunner.manager.softRemove(
          ExternalCameraAllowDevice,
          params
        ) as Promise<ExternalCameraAllowDevice[]>;
      }
      return queryRunner.manager.softRemove(
        ExternalCameraAllowDevice,
        params
      ) as Promise<ExternalCameraAllowDevice>;
    }
    if (Array.isArray(params)) {
      return this.repository.softRemove(params);
    }
    return this.repository.softRemove(params);
  }

  async delete(criteria: criteriaType, queryRunner?: QueryRunner) {
    if (queryRunner) {
      return queryRunner.manager.delete(ExternalCameraAllowDevice, criteria);
    }
    return this.repository.delete(criteria);
  }

  async softDelete(criteria: criteriaType, queryRunner?: QueryRunner) {
    if (queryRunner) {
      return queryRunner.manager.softDelete(
        ExternalCameraAllowDevice,
        criteria
      );
    }
    return this.repository.softDelete(criteria);
  }

  async countBy(
    where:
      | FindOptionsWhere<ExternalCameraAllowDevice>
      | FindOptionsWhere<ExternalCameraAllowDevice>[],
    queryRunner?: QueryRunner
  ) {
    if (queryRunner) {
      return queryRunner.manager.countBy(ExternalCameraAllowDevice, where);
    }
    return this.repository.countBy(where);
  }

  async existsBy(
    where:
      | FindOptionsWhere<ExternalCameraAllowDevice>
      | FindOptionsWhere<ExternalCameraAllowDevice>[],
    queryRunner?: QueryRunner
  ) {
    if (queryRunner) {
      return queryRunner.manager.existsBy(ExternalCameraAllowDevice, where);
    }
    return this.repository.existsBy(where);
  }

  async restore(criteria: criteriaType, queryRunner?: QueryRunner) {
    if (queryRunner) {
      return queryRunner.manager.restore(ExternalCameraAllowDevice, criteria);
    }
    return this.repository.restore(criteria);
  }

  async exists(
    options?: FindManyOptions<ExternalCameraAllowDevice>,
    queryRunner?: QueryRunner
  ) {
    if (queryRunner) {
      return queryRunner.manager.exists(ExternalCameraAllowDevice, options);
    }
    return this.repository.exists(options);
  }

  async count(
    options?: FindManyOptions<ExternalCameraAllowDevice>,
    queryRunner?: QueryRunner
  ) {
    if (queryRunner) {
      return queryRunner.manager.count(ExternalCameraAllowDevice, options);
    }
    return this.repository.count(options);
  }
}
```
```

### Service 컴포넌트 분리 전략

#### 문제점
Service 컴포넌트에서 주로 Repository 조작 및 데이터 가공 코드가 들어가게 되는데, TypeORM 등의 타입 정의는 실제 사용례에서 사용하지 않는 코드에 대한 정의도 포함되어 있습니다.

#### 해결 방안
현재 프로젝트에서 사용되는 코드로 Context를 한정하기 위해 **TypeORM Repository 코드를 래핑하는 Entity Manipulation Service 컴포넌트**로 Service 컴포넌트를 분리하여 사용합니다.

#### 장점
1. **타입 추론 개선**: Generic 등 타입 추론에 방해가 되는 부분을 실제 프로젝트에서 사용되는 Entity 및 메서드 제공으로 타입 단언을 통해 Context를 줄입니다.
2. **일관된 패턴**: 동일한 패턴으로 작성되도록 유도하여 추가 리뷰를 줄입니다.
3. **코드 품질 향상**: 불필요한 타입 정의를 제거하고 실제 사용되는 코드만 포함시킵니다.

### DTO 에 대한 rule

```

---
description: DTO define Rule
globs: ["src/**/*dto*.ts", "src/**/*Dto*.ts", "src/**/responses/*.response.ts"]
alwaysApply: true
---
# DTO Development Rules

## DTO Structure
- DTO class names must use suffixes based on their purpose (e.g., `CreateUserDto`, `UpdateUserDto`, `UserResponseDto`).
- File names must follow these rules:
  - General DTOs: `kebab-case.dto.ts` (e.g., `create-user.dto.ts`)
  - Response DTOs: `kebab-case.response.ts` (e.g., `user.response.ts`)
- All DTOs must use `class-validator` decorators for validation.

## Naming Conventions
- For creation: `Create{Entity}Dto` (e.g., `CreateUserDto`)
- For updates: `Update{Entity}Dto` (e.g., `UpdateUserDto`)
- For responses: `{Entity}ResponseDto` (e.g., `UserResponseDto`)
  - **File name**: Must end with `.response.ts` instead of `.dto.ts`
  - **Location**: Must be placed in the `responses/` directory of the relevant resource (e.g., `src/user/responses/user.response.ts`)
- For queries: `{Entity}QueryDto` (e.g., `UserQueryDto`)
- For controller parameters:
  - Body DTO: `{Entity}BodyDto` (e.g., `UpdateUserBodyDto`)
  - Param DTO: `{Entity}ParamDto` (e.g., `UserIdParamDto`)
  - Query DTO: `{Entity}QueryDto` (e.g., `SearchUserQueryDto`)

## Validation Decorators
- Required fields: `@IsNotEmpty()`, `@IsString()`, `@IsNumber()`
- Optional fields: `@IsOptional()`
- String validation: `@IsEmail()`, `@IsUrl()`, `@Length()`, `@Matches()`
- Number validation: `@IsNumber()`, `@Min()`, `@Max()`
- Array validation: `@IsArray()`, `@ArrayMinSize()`, `@ArrayMaxSize()`
- Enum validation: `@IsEnum()`

## Example Code Structure
```typescript
import { IsEmail, IsNotEmpty, IsOptional, IsString, MinLength } from 'class-validator';

export class CreateUserDto {
  @IsNotEmpty({ message: 'Name is required.' })
  @IsString({ message: 'Name must be a string.' })
  name: string;

  @IsNotEmpty({ message: 'Email is required.' })
  @IsEmail({}, { message: 'Email must be in a valid format.' })
  email: string;

  @IsNotEmpty({ message: 'Password is required.' })
  @IsString({ message: 'Password must be a string.' })
  @MinLength(8, { message: 'Password must be at least 8 characters long.' })
  password: string;

  @IsOptional()
  @IsString({ message: 'Phone number must be a string.' })
  phoneNumber?: string;
}

export class UpdateUserDto {
  @IsOptional()
  @IsString({ message: 'Name must be a string.' })
  name?: string;

  @IsOptional()
  @IsEmail({}, { message: 'Email must be in a valid format.' })
  email?: string;

  @IsOptional()
  @IsString({ message: 'Phone number must be a string.' })
  phoneNumber?: string;
}

## Example Response Dto Structure
import { ApiProperty } from "@nestjs/swagger";
import { Expose, Type } from "class-transformer";
/**
 * 미러 디바이스 응답 DTO
 * 미러 디바이스 정보를 반환할 때 사용
 */
export class MirrorDeviceResponseDto {
  @ApiProperty({
    description: "미러 디바이스 ID",
    example: 1,
  })
  @Expose()
  id: number;

  @ApiProperty({
    description: "미러 디바이스 UUID",
    example: "123e4567-e89b-12d3-a456-426614174000",
  })
  @Expose()
  uuid: string;

  @ApiProperty({
    description: "디바이스 MAC 주소",
    example: "00:11:22:33:44:55",
  })
  @Expose()
  macAddress: string;

  @ApiProperty({
    description: "하드웨어 ID",
    example: "12b449179bd919d3",
  })
  @Expose()
  hwId: string;

  @ApiProperty({
    description: "디바이스 상태",
    example: MirrorDeviceStatusEnum.PENDING,
    enum: MirrorDeviceStatusEnum,
  })
  @Expose()
  status: MirrorDeviceStatusEnum;

  @ApiProperty({
    description: "센터 할당 날짜",
    example: "2024-01-15",
    nullable: true,
  })
  @Expose()
  centerAssignDate?: Date;

  @ApiProperty({
    description: "센터 이름",
    example: "강남점",
    nullable: true,
  })
  @Expose()
  centerName?: string;

  @ApiProperty({
    description: "센터 UUID",
    example: "123e4567-e89b-12d3-a456-426614174000",
    nullable: true,
  })
  @Expose()
  centerUUID?: string;

  @ApiProperty({
    description: "생성일시",
    example: "2024-01-01T00:00:00.000Z",
  })
  @Expose()
  createdAt: Date;

  @ApiProperty({
    description: "수정일시",
    example: "2024-01-01T00:00:00.000Z",
  })
  @Expose()
  updatedAt: Date;

  @ApiProperty({
    description: "삭제일시",
    example: null,
    nullable: true,
  })
  @Expose()
  deletedAt: Date | null;
}
export class CenterCategoryMinimalResponseDto {
  @ApiProperty({
    description: "센터 카테고리 ID",
    example: 1,
  })
  @Expose()
  id: number;

  @ApiProperty({
    description: "센터 카테고리 UUID",
    example: "123e4567-e89b-12d3-a456-426614174000",
  })
  @Expose()
  uuid: string;

  @ApiProperty({
    description: "센터 카테고리 이름",
    example: "아파트",
  })
  @Expose()
  name: string;

  @ApiProperty({
    description: "카테고리 이름 해시값",
    example: "a1b2c3d4e5f6...",
  })
  @Expose()
  nameHash: string;
}

/**
 * 센터 카테고리 기본 응답 DTO
 * 기본적인 카테고리 정보를 포함
 */
export class CenterCategoryResponseDto extends CenterCategoryMinimalResponseDto {
  @ApiProperty({
    description: "생성일시",
    example: "2024-01-01T00:00:00.000Z",
  })
  @Expose()
  createdAt: Date;

  @ApiProperty({
    description: "수정일시",
    example: "2024-01-01T00:00:00.000Z",
  })
  @Expose()
  updatedAt: Date;

  @ApiProperty({
    description: "삭제일시",
    example: null,
    nullable: true,
  })
  @Expose()
  deletedAt: Date | null;
}
export class CenterResponseDto {
  @ApiProperty({
    description: "센터 ID",
    example: 1,
  })
  @Expose()
  id: number;

  @ApiProperty({
    description: "센터 UUID",
    required: true,
    nullable: false,
    format: "uuid",
  })
  @Expose()
  uuid: string;

  @ApiProperty({
    description: "센터 이름",
    required: true,
    nullable: false,
    example: "강남점",
  })
  @Expose()
  name: string;

  @ApiProperty({
    description: "센터 이름 해시값 (고유값)",
    required: true,
    nullable: false,
    example: "a1b2c3d4e5f6...",
  })
  @Expose()
  nameHash: string;

  @ApiProperty({
    description: "센터 카테고리 UUID",
    required: false,
    nullable: true,
    format: "uuid",
  })
  @Expose()
  categoryUUID?: string;

  @ApiProperty({
    description: "센터 메모",
    required: false,
    nullable: true,
    example: "강남 지역 주요 고객 센터입니다.",
  })
  @Expose()
  memoText?: string;

  @ApiProperty({
    description: "관리자 이름",
    required: true,
    nullable: false,
    example: "김관리",
  })
  @Expose()
  managerName: string;

  @ApiProperty({
    description: "연락처",
    required: false,
    nullable: true,
    example: "010-1234-5678",
  })
  @Expose()
  phone?: string;

  @ApiProperty({
    description: "센터 주소",
    required: false,
    nullable: true,
    example: "서울특별시 강남구 테헤란로 123",
  })
  @Expose()
  address?: string;

  @ApiProperty({
    description: "센터에 등록된 미러 디바이스들",
    required: false,
    nullable: true,
    type: () => [MirrorDeviceResponseDto],
  })
  @Expose()
  @Type(() => MirrorDeviceResponseDto)
  mirrorDevices?: MirrorDeviceResponseDto[];

  @ApiProperty({
    description: "센터 유형",
    required: false,
    nullable: true,
    type: () => CenterCategoryResponseDto,
  })
  @Expose()
  @Type(() => CenterCategoryResponseDto)
  category?: CenterCategoryResponseDto;

  @ApiProperty({
    description: "생성일",
    required: true,
    nullable: false,
    format: "date-time",
  })
  @Expose()
  createdAt: Date;

  @ApiProperty({
    description: "수정일",
    required: true,
    nullable: false,
    format: "date-time",
  })
  @Expose()
  updatedAt: Date;

  @ApiProperty({
    description: "삭제일",
    required: false,
    nullable: true,
    format: "date-time",
  })
  @Expose()
  deletedAt?: Date;
}
```

### DTO Rule의 목적과 범위

#### DTO Rule 정의 목적
앞의 컨트롤러, 서비스 관련 Rule에서 정의하지 않은 **DTO 관련 Rule**을 정의합니다. 

#### 포함 내용
1. **Validator 사용법**: `class-validator` 데코레이터 사용례
2. **직렬화/역직렬화**: `class-transformer` 옵션 사용법
3. **샘플 코드**: 파라미터 및 응답 변환용 클래스 예제

### 컨트롤러 Rule에서 직렬화/역직렬화 제외 이유

컨트롤러 Rule에 직렬화, 역직렬화 등에 대한 부분이 포함되지 않은 이유는 다음과 같습니다:

#### 복잡성 고려사항
- **서비스 호출 조합**: 여러 서비스를 조합하여 호출하는 경우
- **트랜잭션 처리 전략**: 전체 성공, 일부 성공 등 다양한 시나리오
- **중간 값 변환**: 트랜잭션 중간 단계에서의 데이터 변환

#### 설계 철학
고정된 변환 패턴보다는 **개발자가 상황에 맞게 적절히 변환하는 것**이 더 유연하고 실용적이라고 판단했습니다.

여기까지 rule 외 Guard, interceptor, middleware 등에 대한 컴포넌트 rule 은 지금까지 작성한 방식으로 작성하면 된다.

그러고 나서 API 작성은 다음 프롬프팅 순서를 따라가면 된다.

1. Entity 작성
  - Entity 의 속성들에 대한 나열 ex(name, id, uuid, createdAt, 등등) 및 제약조건.
  - Entity 의 관계 해소에 대한 방법(ORM 기본 방식을 따를지 혹은 관계해소 Entity 를 만들지 등등)
2. 1에서 만들 Entity 의 Entity Manipulation Service 작성해줘.(Ex: User Entity 의 Entity Manipulation Service 작성해줘)
3. 2에서 만들 Entity Manipulation Service 를 이용해서 실제 비지니스 로직에 맞춰서 비지니스 로직 Service 작성해줘.
  - User 이름 수정하는 setName 메서드 가지는 User 비지니스 로직 서비스 작성해줘.
4. 앞에서 작성한 것들 이용한 Controller 작성.
  - UserController 작성하는데 User 의 이름 수정하는 API 만 작성해줘.



이후는 동일한 방식 및 순서로 비지니스 로직 서술해나가면 경험상 거의 대부분의 경우 accept 해서 바로 사용가능하거나 양식에서 어긋나지 않지만 operter 를 잘못 세팅했다던가 하는정도의 수준으로 코드 생성이 이뤄지게 된다.

응답문서 및 dto 의 경우는 2,3 에서 처리 내역을 기반으로 얼추 맞게 나오고 projection 등을 상세히 해서 orm 등에서 나오는 Entity 의 실제 값에 가깝게 base 객체들을 만들어달라고 하고 거기서부터 시작하면 더 정확한 코드를 얻을 수 있다.