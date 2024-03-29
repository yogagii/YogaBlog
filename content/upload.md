Title: 文件上传
Date: 2024-03-29
Category: Backend
Tags: Express
Author: Yoga

解析 Content-Type: multipart/form-data

- formidable

```js
const form = new formidable({ multiples: true });

form.parse(req, async (err, fields, files) => {
  if (err) {
    res.status(400).json({ error: `Invalid request: ${err}` });
    return;
  }

  const file = files.file;
  const fileType = fields.fileType; // 表单中除文件外的其他字段
  const { originalName, size, path } = request.file;

  // Check file size
  if (size > 5 * 1024 * 1024) {
    res.status(400).json({ error: `File size is too large` });
    return;
  }
  // Read the file into buffer
  const fileBuffer = fs.readFileSync(path);
});
```

- Multer

```js
import multer from "multer";

const upload = multer({
  limits: {
    fileSize: 5 * 1024 * 1024, // 限制文件大小为 5 MB
  },
});

express.Router().post("/upload", upload.single("file"), uploadRequestHandler);

const { originalname, size, buffer } = request.file;

// request.file:  {
//  fieldname: 'file',
//  originalname: 'pic.png',
//  encoding: '7bit',
//  mimetype: 'image/png',
//  buffer: <Buffer 89 50 4e 47 0d 66 69 ... 21271 more bytes>,
//  size: 21321
//  }
```

_踩坑：
"MultipartParser.end(): stream ended unexpectedly: state = START_BOUNDARY" 错误通常发生在客户端发送的 multipart/form-data 请求被异常终止或格式不正确的情况下。
express-http-proxy 会尝试解析请求体，因为它需要知道请求体的大小来设置 "content-length" 头部。_

解决：
在代理函数中设置了 parseReqBody: false（这在处理大文件或流数据时是推荐的做法）

```js
proxy(`${hosts.businessFileUpload}`, {
  proxyReqPathResolver: () => `/api/file/${fileType}?destination=xxx`,
  parseReqBody: false,
})(request, response, next);
```

Frontend
```js
import { Button, message, Upload } from 'antd';
const props = {
  name: 'file',
  action: 'https://localhost:8543/api/internal-course/upload/image?destination=xxx',
  headers: {
    // "Content-Type": "multipart/form-data", // 当用户上传文件时，浏览器自动设置正确的 'Content-Type' 头部和 'boundary' 参数。不需要手动设置 'Content-Type'。
  },
  onChange(info) {...},
};
const App = () => (
  <Upload {...props}>
    <Button icon={<UploadOutlined />}>Click to Upload</Button>
  </Upload>
);
export default App;
```