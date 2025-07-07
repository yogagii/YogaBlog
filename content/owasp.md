Title: Secure Code
Date: 2025-07-07
Category: Javascript
Tags: Security
Author: Yoga

‌OWASP（开放式 Web 应用程序安全项目）是一个全球性非营利组织，致力于提升 Web 应用程序安全性，通过开源项目、工具开发和标准制定（如 OWASP Top 10）提供无商业偏见的应用安全解决方案。

‌OWASP Top 10‌：列举当前最严重的 Web 安全漏洞（如注入、失效身份认证），并提供防御方案

### Vulnerabilities from untrusted source

```html
<script
  src="https://example.com/script.js"
  integrity="sha384-oqVuAfXRKap7fdgcCY5cn6M2YGR7fGjgL+Q0/9f0s++/0euutpTE6YvpoDNV9gL4"
  crossorigin="anonymous"
></script>
```

- crossorigin: 当你不需要在请求中发送任何凭证（例如 Cookies 或 HTTP 认证信息），并希望确保请求被服务器安全处理时，可以使用 crossorigin="anonymous"。这有助于提高安全性，通常在从 CDN 加载字体或脚本时使用。被请求的资源必须具备正确的 CORS 头部(如 Access-Control-Allow-Origin)，以指定该资源可以被你的域访问。
- integrity: 通过提供一个哈希值，浏览器可以在下载资源时计算该资源的哈希，如果计算得出的哈希与提供的哈希不匹配，则浏览器会拒绝加载该资源。这确保了即使 CDN 上的文件被攻击者替换，用户也不会加载到恶意版本。

### Sensitive user data exposure

### Code injection

```ts
const parsedInfo: any = eval("(" + info.info + ")");
```

By dynamically evaluating untrusted data, an attacker could be able to inject code that will be executed inside the application context to carry out unauthorized operations.

It is recommended to avoid the use of functions (like eval and Function) that allow dynamic code execution. Any data coming from an untrusted source (like local storage) should not be passed to those functions.

### Improper authentication

- Don't expose session IDs in the URL
- Implement multi-factor authentication
- Don't use user IDs or predictable sequential values as session
  IDs. Instead, use a secure server-side session manager that generates a random session ID with high entropy

### Sensitive data storage

Bcrypt is accepted as one of the stronger hashing algorithms. The hashing algorithm incorporates a salt, this makes it so that the hashed version of identical security answers are still different and a table of hashes cannot be used to discover the security answer.

```js
import bcrypt from "bcryptjs";

const salt = bcrypt.genSaltSync(10);
const secretHash = bcrypt.hashSync(secret, salt);
```
