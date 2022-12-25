Title: Linkmed BST Project Data
Date: 2022-12-24
Category: Project
Tags: Next, Nest
Author: Yoga

## Authentication

> JWT TOKEN = JWT头.有效载荷.签名

* JWT头：一个描述JWT元数据的JSON对象
```json
{
  "alg": "HS256", // 签名使用的算法，默认为HMAC SHA256
  "typ": "JWT" // 令牌的类型
}
```

* 有效载荷：JWT的主体内容部分，也是一个JSON对象，包含需要传递的数据，指定七个默认字段，默认未加密的，任何人都可以解读其内容。

```
{
  iss：发行人
  exp：到期时间
  sub：主题
  aud：用户
  nbf：在此之前不可用
  iat：发布时间
  jti：JWT ID用于标识该JWT
}
```

* 签名：对上面两部分数据签名，通过指定的算法生成哈希，以确保数据不会被篡改。指定一个密码（secret）保存在服务器中，不能向用户公开。

HMACSHA256(base64UrlEncode(header) + "." + base64UrlEncode(payload),secret)

**Authentication 身份验证**

https://yogagii.github.io/nestjs.html

[POST] /auth

Get Token

**Request**

* Params
None
* Headers
None
* Body
```json
{
  "username": "xxx", "password": "xxx"
}
```

**Response**

* Body
```json
{
  "access_token": "xxxxxx.xxxx.xxxx"
}
```
**Data 数据接口**

[GET] /users

Get User list

**Request**

* Params
None
* Headers
```json
{
  "Authorization": "Bearer <token>"
}
```
* Body
None

**Response**

* Body
```json
[{
  ...
}]
```

## Cache

Promise.race() 承诺列表中寻找第一个履行或拒绝的承诺；

Promise.any() 是从承诺列表中查找第一个履行的承诺。

判断是否存在缓存，缓存中有数据直接返回，缓存中无数据 -> 从数据库获取。

缺点：1. 缓存数据不更新，2.不能并发

Promise.race 在cacheGet中reject导致拒绝，无法返回数据库获得数据，Promise.any 在cacheGet中reject不影响，会返回数据库数据

优势：1. 用缓存数据直接相应接口，解决504，同时读取数据库更新缓存，保证接口每次获得最新数据，2. 读缓存和度数据库可并发

```ts
async cacheGet(key: any): Promise<any> {
    return new Promise((resolve, reject) => {
      this.cacheManager.get(key, (error, result: any) => {
        if (result) {
          resolve(JSON.parse(result));
        }
        reject(error);
      });
    });
  }
```

```ts
const [examlist, userlist]: [Pagination<ExamDto>, Pagination<UserDto>] =
  await Promise.all([
    Promise.any([
      this.examsService.getBehaviorList(),
      this.cacheService.cacheGet("examlist"),
    ]),
    Promise.any([
      this.usersService.getUserList(),
      this.cacheService.cacheGet("userlist"),
    ]),
  ]);
```
tsconfig.json
```json
{
  "compilerOptions": {
    "target": "es2021",
  }
}
```

## TypeORM

https://yogagii.github.io/typeorm.html

join table时间复杂度太高，接口容易超时

```ts
export const joinKey = <T>(item: T, fields: StringKeyof<T>[]) => {
  return fields
    .map((it) => {
      return item[it];
    })
    .join('-');
};

/**
 * 生成映射
 * @param list
 * @param field
 * @param options
 * @returns
 */
export const createMap = <
  T extends Record<string, any>,
  R extends { type: 'one' | 'many' } | undefined,
>(
  list: T[],
  field: StringKeyof<T> | StringKeyof<T>[],
  options?: R,
): CreateMapReturn<T, R> => {
  const map: Record<string, T[] | T> = {};

  list.forEach((item) => {
    const str = Array.isArray(field)
      ? joinKey(item, field)
      : item[field as string];
    if (options?.type === 'many') {
      if (!map[str]) {
        map[str] = [];
      }
      map[str].push(item);
    } else {
      map[str] = item;
    }
  });

  return map as CreateMapReturn<T, R>;
};
```

## Export EXCEL

```ts
import { writeFileSync } from 'fs';
import * as json2xls from 'json2xls';

interface Option {
  path: string;
  filename: string;
  data: Array<object>;
}

export default function saveExcel(option: Option) {
  const { filename, data, path } = option;
  const xls = json2xls(data);
  writeFileSync(`${path}${filename}`, xls, 'binary');
}
```
邮件发送成功后删除源文件
```js
import { existsSync, rmSync } from 'fs';

if (existsSync(filepath)) {
  rmSync(filepath);
}
```

## Export CSV

```ts
const jsonToCSV = (data: ExcelDataType[]) => {
  let str = "";
  data.forEach((table: ExcelDataType) => {
    str += table.title + "\n";
    str += table.head.join(",") + "\n";
    table.data.forEach((row) => {
      str += Object.values(row).join(",") + "\n";
    });
    str += "\n";
  });

  return `data:text/csv;charset=utf-8,\ufeff${encodeURIComponent(str)}`;
};
```
```jsx
<a href={jsonToCSV(data)} download="FILENAME.csv">
  <Button>Export CSV</Button>
</a>
```
## Export PDF
```js
const onrendered = async (canvas) => {
  var contentWidth = canvas.width;
  var contentHeight = canvas.height;

  var pageHeight = (contentWidth / 592.28) * 841.89;
  var leftHeight = contentHeight;
  var position = 0;
  var imgWidth = 595.28;
  var imgHeight = (592.28 / contentWidth) * contentHeight;

  var pageData = canvas.toDataURL("image/jpeg", 1.0);

  const jsPDF = (await import("./jspdf.debug")).default;
  var pdf = new jsPDF("", "pt", "a4");

  if (leftHeight < pageHeight) {
    pdf.addImage(pageData, "JPEG", 0, 0, imgWidth, imgHeight);
  } else {
    while (leftHeight > 0) {
      pdf.addImage(pageData, "JPEG", 0, position, imgWidth, imgHeight);
      leftHeight -= pageHeight;
      position -= 841.89;
      if (leftHeight > 0) {
        pdf.addPage();
      }
    }
  }
  pdf.save("FILENAME.pdf");
};

export default async function () {
  const html2canvas = (await import("./html2canvas")).default;
  const target = document.getElementById("main");
  target.style.fontFeatureSettings = '"liga" 0';
  html2canvas(target, {
    allowTaint: true,
    scale: 2,
    height: target.scrollHeight,
    width: target.scrollWidth,
    background: "rgb(242, 245, 249)",
    onrendered,
  });
}
```
## G2

https://yogagii.github.io/antv-g2.html

## Adaptive Card

https://yogagii.github.io/adaptive-card.html

JSON 转 CSV: https://www.bejson.com/json/json2excel/

EXCEl 转 JSON: http://www.esjson.com/exceltojson.html