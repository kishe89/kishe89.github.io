---
layout: post
title:  "DB 파티셔닝과 샤딩. 그리고 적용."
date:   2026-01-11 04:00:00
author: 김지운
cover:  "/assets/instacode.png"
categories: DB
---

### 들어가며

데이터베이스의 데이터가 증가하면서 단일 서버로는 처리하기 어려운 상황이 발생한다. 이때 데이터를 분산하여 저장하고 관리하는 기법이 필요하다. 파티셔닝(Partitioning)과 샤딩(Sharding)은 대규모 데이터베이스를 효율적으로 관리하기 위한 핵심 기술이다.

이번 글에서는 파티셔닝과 샤딩의 개념, 차이점, 그리고 실제 적용 방법에 대해 알아보겠다.

### 파티셔닝(Partitioning)이란?

파티셔닝은 하나의 데이터베이스 내에서 테이블을 논리적 또는 물리적으로 분할하는 기법이다. 같은 데이터베이스 서버 내에서 데이터를 여러 파티션으로 나누어 저장한다.

#### 파티셔닝의 종류

##### 1. 수평 파티셔닝(Horizontal Partitioning)

행(Row) 단위로 데이터를 분할하는 방식이다. 같은 스키마를 가진 여러 테이블로 나누어 저장한다.

**예시:**
```typescript
// TypeORM Entity - 연도별 파티션 테이블
// 주의: TypeORM은 파티셔닝을 직접 지원하지 않으므로,
// 마이그레이션에서 파티셔닝 설정을 추가해야 합니다.

@Entity('users_2023')
export class User2023 {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ type: 'varchar', length: 100 })
  name: string;

  @Column({ type: 'date' })
  createdAt: Date;
}

@Entity('users_2024')
export class User2024 {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ type: 'varchar', length: 100 })
  name: string;

  @Column({ type: 'date' })
  createdAt: Date;
}

@Entity('users_2025')
export class User2025 {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ type: 'varchar', length: 100 })
  name: string;

  @Column({ type: 'date' })
  createdAt: Date;
}
```

##### 2. 수직 파티셔닝(Vertical Partitioning)

열(Column) 단위로 데이터를 분할하는 방식이다. 자주 사용하는 컬럼과 자주 사용하지 않는 컬럼을 분리한다.

**예시:**
```typescript
// TypeORM Entity - 수직 파티셔닝
// 자주 조회하는 컬럼
@Entity('users_basic')
export class UserBasic {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ type: 'varchar', length: 100 })
  name: string;

  @Column({ type: 'varchar', length: 100 })
  email: string;
}

// 자주 조회하지 않는 컬럼
@Entity('users_detail')
export class UserDetail {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ type: 'text', nullable: true })
  bio: string;

  @Column({ type: 'varchar', length: 255, nullable: true })
  profileImageUrl: string;

  @Column({ type: 'json', nullable: true })
  settings: Record<string, any>;
}
```

#### 파티셔닝의 장점

- **쿼리 성능 향상**: 특정 파티션만 조회하여 전체 테이블 스캔을 방지
- **인덱스 효율성**: 각 파티션별로 인덱스가 작아져 관리가 용이
- **유지보수 용이**: 오래된 데이터 파티션만 백업/삭제 가능
- **병렬 처리**: 여러 파티션을 동시에 처리 가능

#### 파티셔닝의 단점

- **복잡도 증가**: 파티션 키 선택과 관리가 복잡
- **조인 비용**: 파티션 간 조인 시 성능 저하 가능
- **트랜잭션 제약**: 여러 파티션에 걸친 트랜잭션 처리 복잡

### 샤딩(Sharding)이란?

샤딩은 데이터를 여러 데이터베이스 서버에 분산하여 저장하는 기법이다. 각 샤드는 독립적인 데이터베이스 서버이며, 전체 데이터의 일부를 담당한다.

#### 샤딩의 종류

##### 1. 범위 기반 샤딩(Range-based Sharding)

데이터의 범위를 기준으로 샤드를 분할한다.

**예시:**
- 샤드 1: user_id 1~1000000
- 샤드 2: user_id 1000001~2000000
- 샤드 3: user_id 2000001~3000000

##### 2. 해시 기반 샤딩(Hash-based Sharding)

해시 함수를 사용하여 데이터를 샤드에 분배한다.

**예시:**
- 사용자 ID를 해시 함수로 변환하여 샤드 인덱스 결정
- `shard_index = hash(user_id) % shard_count`
- 데이터가 고르게 분산되어 핫스팟 방지에 유리

##### 3. 디렉토리 기반 샤딩(Directory-based Sharding)

샤드 키를 기반으로 샤드 위치를 조회하는 별도의 디렉토리 서비스를 사용한다.

#### 범위 기반 vs 해시 기반 샤딩 비교

| 구분 | 범위 기반 샤딩 | 해시 기반 샤딩 |
|------|--------------|--------------|
| **데이터 분산** | 범위별로 연속된 데이터 저장 | 해시 함수로 고르게 분산 |
| **핫스팟 발생** | 특정 범위에 집중 시 발생 가능 | 상대적으로 적음 |
| **범위 쿼리 성능** | 범위 쿼리에 유리 (단일 샤드 조회 가능) | 범위 쿼리 시 여러 샤드 조회 필요 |
| **재샤딩 비용** | 범위 재조정으로 일부 데이터만 이동 | 해시 함수 변경 시 전체 재분배 필요 |
| **확장성** | 새 샤드 추가 시 범위 재조정 필요 | 샤드 수 변경 시 재해싱 필요 |
| **구현 복잡도** | 상대적으로 간단 | 해시 함수 선택 및 관리 필요 |
| **데이터 지역성** | 범위별로 데이터가 연속적 | 데이터가 무작위로 분산 |
| **적용 사례** | 시간 기반 데이터, 순차적 ID | 사용자 ID, 무작위 키 |

#### 샤딩의 장점

- **수평 확장성**: 서버를 추가하여 용량과 성능 확장 가능
- **부하 분산**: 여러 서버에 부하를 분산
- **장애 격리**: 한 샤드의 장애가 다른 샤드에 영향 없음
- **지역별 배치**: 지역별로 샤드를 배치하여 지연 시간 감소

#### 샤딩의 단점

- **복잡한 운영**: 여러 서버 관리 및 모니터링 필요
- **조인 제약**: 샤드 간 조인 불가능
- **재샤딩 비용**: 데이터 재분배 시 높은 비용
- **트랜잭션 제약**: 샤드 간 트랜잭션 처리 어려움

### 파티셔닝 vs 샤딩

| 구분 | 파티셔닝 | 샤딩 |
|------|---------|------|
| **범위** | 단일 데이터베이스 내 | 여러 데이터베이스 서버 |
| **위치** | 같은 서버 | 다른 서버 |
| **확장성** | 수직 확장(서버 성능 향상) | 수평 확장(서버 추가) |
| **복잡도** | 상대적으로 낮음 | 높음 |
| **트랜잭션** | 파티션 간 트랜잭션 가능 | 샤드 간 트랜잭션 어려움 |
| **조인** | 파티션 간 조인 가능 | 샤드 간 조인 불가능 |

### 실제 적용 방법

#### MySQL 파티셔닝 예시 (TypeORM)

```typescript
// 범위 파티셔닝 - 주문 테이블
// 마이그레이션에서 PARTITION BY RANGE 설정 필요
@Entity('orders')
export class Order {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ type: 'int' })
  userId: number;

  @Column({ type: 'date' })
  orderDate: Date;

  @Column({ type: 'decimal', precision: 10, scale: 2 })
  amount: number;
}

// 마이그레이션 예시
// ALTER TABLE orders PARTITION BY RANGE (YEAR(order_date)) (
//   PARTITION p2023 VALUES LESS THAN (2024),
//   PARTITION p2024 VALUES LESS THAN (2025),
//   PARTITION p2025 VALUES LESS THAN (2026),
//   PARTITION p_future VALUES LESS THAN MAXVALUE
// );

// 해시 파티셔닝 - 사용자 테이블
@Entity('users')
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ type: 'varchar', length: 100 })
  name: string;

  @Column({ type: 'varchar', length: 100 })
  email: string;
}

// 마이그레이션 예시
// ALTER TABLE users PARTITION BY HASH(id) PARTITIONS 4;

// 리스트 파티셔닝 - 판매 테이블
@Entity('sales')
export class Sale {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ type: 'varchar', length: 50 })
  region: string;

  @Column({ type: 'decimal', precision: 10, scale: 2 })
  amount: number;
}

// 마이그레이션 예시
// ALTER TABLE sales PARTITION BY LIST COLUMNS(region) (
//   PARTITION p_north VALUES IN ('서울', '경기'),
//   PARTITION p_south VALUES IN ('부산', '경남'),
//   PARTITION p_etc VALUES IN (DEFAULT)
// );
```

#### PostgreSQL 파티셔닝 예시 (TypeORM)

```typescript
// PostgreSQL 범위 파티셔닝 - 주문 테이블
@Entity('orders')
export class Order {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ type: 'int' })
  userId: number;

  @Column({ type: 'date' })
  orderDate: Date;

  @Column({ type: 'decimal', precision: 10, scale: 2 })
  amount: number;
}

// 마이그레이션 예시
// CREATE TABLE orders (
//     id SERIAL NOT NULL,
//     user_id INTEGER NOT NULL,
//     order_date DATE NOT NULL,
//     amount DECIMAL(10,2)
// ) PARTITION BY RANGE (order_date);
//
// CREATE TABLE orders_2023 PARTITION OF orders
//     FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');
//
// CREATE TABLE orders_2024 PARTITION OF orders
//     FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
//
// CREATE TABLE orders_2025 PARTITION OF orders
//     FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
```

### 적용 시 고려사항

#### 1. 파티션/샤드 키 선택

- **균등 분산**: 데이터가 고르게 분산되도록 선택
- **쿼리 패턴**: 자주 사용하는 쿼리 조건에 맞게 선택
- **핫스팟 방지**: 특정 파티션/샤드에 집중되지 않도록 주의

#### 2. 모니터링

- 각 파티션/샤드의 데이터 크기 모니터링
- 쿼리 성능 및 부하 분산 상태 확인
- 디스크 사용량 및 메모리 사용량 추적

#### 3. 재파티셔닝/재샤딩 전략

- 데이터 증가에 따른 재분배 계획 수립
- 다운타임 최소화 방안 고려
- 백업 및 복구 전략 수립

#### 4. 애플리케이션 레벨 처리

- 파티션/샤드 라우팅 로직 구현
- 실패 처리 및 재시도 메커니즘
- 트랜잭션 범위 고려

### 실제 적용 사례

#### 사례 1: 차량 이동 경로(GPS) 데이터 시간 기반 파티셔닝 (TypeORM)

차량의 GPS 이동 경로 데이터를 일별로 파티셔닝하여 대용량 위치 데이터를 효율적으로 관리하고, 오래된 데이터는 별도 스토리지로 이동

```typescript
// TypeORM Entity - 차량 GPS 이동 경로
@Entity('vehicle_gps_tracks')
export class VehicleGpsTrack {
  @PrimaryGeneratedColumn({ type: 'bigint' })
  id: number;

  @Column({ type: 'int' })
  vehicleId: number;

  @Column({ type: 'decimal', precision: 10, scale: 7 })
  latitude: number;

  @Column({ type: 'decimal', precision: 10, scale: 7 })
  longitude: number;

  @Column({ type: 'timestamp' })
  recordedAt: Date;

  @Column({ type: 'decimal', precision: 5, scale: 2, nullable: true })
  speed: number;

  @Column({ type: 'int', nullable: true })
  heading: number;

  @Column({ type: 'int', nullable: true })
  altitude: number;
}

// 마이그레이션에서 파티셔닝 설정
// CREATE TABLE vehicle_gps_tracks (
//     id BIGINT NOT NULL AUTO_INCREMENT,
//     vehicle_id INT NOT NULL,
//     latitude DECIMAL(10,7) NOT NULL,
//     longitude DECIMAL(10,7) NOT NULL,
//     recorded_at TIMESTAMP NOT NULL,
//     speed DECIMAL(5,2),
//     heading INT,
//     altitude INT,
//     PRIMARY KEY (id, recorded_at),
//     INDEX idx_vehicle_recorded (vehicle_id, recorded_at),
//     INDEX idx_recorded_at (recorded_at)
// ) PARTITION BY RANGE (DATE(recorded_at));

// TypeORM 마이그레이션으로 자동 파티션 생성
import { MigrationInterface, QueryRunner } from 'typeorm';

export class CreateGpsPartitionForToday1234567890 implements MigrationInterface {
  public async up(queryRunner: QueryRunner): Promise<void> {
    const today = new Date();
    const partitionName = `p${today.getFullYear()}${String(today.getMonth() + 1).padStart(2, '0')}${String(today.getDate()).padStart(2, '0')}`;
    const nextDay = new Date(today);
    nextDay.setDate(nextDay.getDate() + 1);
    const nextDayStr = nextDay.toISOString().split('T')[0];

    await queryRunner.query(`
      ALTER TABLE vehicle_gps_tracks 
      ADD PARTITION (
        PARTITION ${partitionName} 
        VALUES LESS THAN ('${nextDayStr}')
      )
    `);
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    // 파티션 삭제 로직
  }
}

// 사용 예시: 특정 차량의 특정 날짜 이동 경로 조회
// 파티셔닝으로 해당 날짜의 파티션만 조회하여 성능 향상
export class VehicleGpsService {
  constructor(
    private gpsRepository: Repository<VehicleGpsTrack>
  ) {}

  async getVehicleTracksByDate(
    vehicleId: number, 
    date: Date
  ): Promise<VehicleGpsTrack[]> {
    const startOfDay = new Date(date);
    startOfDay.setHours(0, 0, 0, 0);
    const endOfDay = new Date(date);
    endOfDay.setHours(23, 59, 59, 999);

    return await this.gpsRepository.find({
      where: {
        vehicleId,
        recordedAt: Between(startOfDay, endOfDay)
      },
      order: {
        recordedAt: 'ASC'
      }
    });
  }
}
```

#### 사례 2: 차량 ID 기반 샤딩 (TypeORM)

차량 ID를 해시하여 여러 샤드에 분산. 차량 정보와 해당 차량의 GPS 이동 경로 데이터를 같은 샤드에 저장하여 조인 성능 향상

```typescript
// TypeORM Entity - 차량
@Entity('vehicles')
export class Vehicle {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ type: 'varchar', length: 50 })
  vehicleNumber: string;

  @Column({ type: 'varchar', length: 100 })
  model: string;

  @Column({ type: 'varchar', length: 50, nullable: true })
  driverName: string;

  @Column({ type: 'timestamp', default: () => 'CURRENT_TIMESTAMP' })
  createdAt: Date;
}

// TypeORM Entity - 차량 GPS 이동 경로
@Entity('vehicle_gps_tracks')
export class VehicleGpsTrack {
  @PrimaryGeneratedColumn({ type: 'bigint' })
  id: number;

  @Column({ type: 'int' })
  vehicleId: number;

  @Column({ type: 'decimal', precision: 10, scale: 7 })
  latitude: number;

  @Column({ type: 'decimal', precision: 10, scale: 7 })
  longitude: number;

  @Column({ type: 'timestamp' })
  recordedAt: Date;

  @Column({ type: 'decimal', precision: 5, scale: 2, nullable: true })
  speed: number;

  @Column({ type: 'int', nullable: true })
  heading: number;
}

// 샤드 라우팅 서비스
import { DataSource } from 'typeorm';

export class VehicleShardService {
  private shardCount = 4;
  private dataSources: Map<number, DataSource> = new Map();

  constructor() {
    // 각 샤드에 대한 DataSource 초기화
    for (let i = 0; i < this.shardCount; i++) {
      const dataSource = new DataSource({
        type: 'mysql',
        host: `shard${i}.example.com`,
        port: 3306,
        username: 'user',
        password: 'password',
        database: 'vehicle_db',
        entities: [Vehicle, VehicleGpsTrack],
      });
      this.dataSources.set(i, dataSource);
    }
  }

  // 샤드 결정 함수 - 차량 ID 기반
  getShardIndex(vehicleId: number): number {
    return vehicleId % this.shardCount;
  }

  // 샤드별 DataSource 가져오기
  getDataSource(vehicleId: number): DataSource {
    const shardIndex = this.getShardIndex(vehicleId);
    return this.dataSources.get(shardIndex)!;
  }

  // 차량 조회
  async getVehicle(vehicleId: number): Promise<Vehicle | null> {
    const dataSource = this.getDataSource(vehicleId);
    const vehicleRepository = dataSource.getRepository(Vehicle);
    return await vehicleRepository.findOne({ where: { id: vehicleId } });
  }

  // 차량 생성
  async createVehicle(vehicle: Partial<Vehicle>): Promise<Vehicle> {
    const vehicleId = vehicle.id || Math.floor(Math.random() * 1000000);
    const dataSource = this.getDataSource(vehicleId);
    const vehicleRepository = dataSource.getRepository(Vehicle);
    return await vehicleRepository.save({ ...vehicle, id: vehicleId });
  }

  // GPS 이동 경로 저장
  async saveGpsTrack(track: Partial<VehicleGpsTrack>): Promise<VehicleGpsTrack> {
    const dataSource = this.getDataSource(track.vehicleId!);
    const trackRepository = dataSource.getRepository(VehicleGpsTrack);
    return await trackRepository.save(track);
  }

  // 차량과 이동 경로 함께 조회 (같은 샤드에 있어 조인 가능)
  async getVehicleWithTracks(
    vehicleId: number,
    startDate: Date,
    endDate: Date
  ): Promise<{ vehicle: Vehicle; tracks: VehicleGpsTrack[] }> {
    const dataSource = this.getDataSource(vehicleId);
    const vehicleRepository = dataSource.getRepository(Vehicle);
    const trackRepository = dataSource.getRepository(VehicleGpsTrack);

    const vehicle = await vehicleRepository.findOne({ where: { id: vehicleId } });
    if (!vehicle) {
      throw new Error('Vehicle not found');
    }

    const tracks = await trackRepository.find({
      where: {
        vehicleId,
        recordedAt: Between(startDate, endDate)
      },
      order: {
        recordedAt: 'ASC'
      }
    });

    return { vehicle, tracks };
  }
}
```

### 마무리

파티셔닝과 샤딩은 대규모 데이터베이스를 효율적으로 관리하기 위한 필수 기술이다. 각각의 특성과 장단점을 이해하고, 시스템의 요구사항에 맞게 선택하여 적용해야 한다.

#### 핵심 요약

- **파티셔닝**: 단일 데이터베이스 내에서 데이터 분할, 상대적으로 간단
- **샤딩**: 여러 데이터베이스 서버에 데이터 분산, 높은 확장성
- **적용 시**: 파티션/샤드 키 선택, 모니터링, 재분배 전략이 중요

#### 마지막으로

파티셔닝과 샤딩은 데이터베이스 성능과 확장성을 위한 강력한 도구이지만, 복잡도가 증가한다. 신중한 계획과 지속적인 모니터링이 필요하다. 작은 규모에서 시작하여 점진적으로 확장하는 것이 좋다.

### 참고 자료

- [MySQL Partitioning](https://dev.mysql.com/doc/refman/8.0/en/partitioning.html)
- [PostgreSQL Partitioning](https://www.postgresql.org/docs/current/ddl-partitioning.html)
- [TypeORM Documentation](https://typeorm.io/)

