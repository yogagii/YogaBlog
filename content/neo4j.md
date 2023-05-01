Title: NEO4J
Date: 2023-04-28
Category: Backend
Tags: database
Author: Yoga

### 安装 Neo4j Desktop

https://neo4j.com/download/

### Nestjs

```bash
npm install neo4j-driver nest-neo4j
```

```ts
// app.module.ts
import { Module } from '@nestjs/common';
import { Neo4jModule } from 'nest-neo4j';

@Module({
  imports: [
    Neo4jModule.forRootAsync({
      imports: [ConfigModule],
      useFactory: () => ({
        scheme: 'neo4j',
        host: 'xxx.xxx.com', // 踩坑：不要带neo4j://
        port: 7687,
        username: process.env.DATABASE_N4_USERNAME,
        password: process.env.DATABASE_N4_PASSWORD,
        database: process.env.DATABASE_N4_DATABASE,
      }),
    }),
  ],
  controllers: [AppController],
  providers: [AppService]
})
export class AppModule {}
```

```ts
import { Injectable } from '@nestjs/common';
import { Neo4jService } from 'nest-neo4j/dist';

@Injectable()
export class SupplyLaneService {
  constructor(private readonly neo4jService: Neo4jService) {}

  findAll() {
    return this.neo4jService
      .read(
        `
          match (o:xx) -[r:xx]->(d:xx) return o,r,d
        `,
      )
      .then((res) => {
        if (!res.records.length) return undefined;
        const row = res.records[0];
        return row;
      });
  }
}

```