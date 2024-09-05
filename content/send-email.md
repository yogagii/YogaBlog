Title: Email Service
Date: 2024-09-05
Category: Backend
Tags: Express
Author: Yoga

### 生成邮件模板并发送邮件

```ts
async function sendEmail(
  email: string,
  filename: string,
  content: Buffer,
  subject = "材料下载"
) {
  const htmlTemplate = await generateHtmlForFileDownload();
  const attachment = {
    filename,
    content,
  };
  if (currentFileName.includes(".csv")) {
    attachment.contentType = "text/csv; charset=utf-8";
  }

  await emailService({
    subject,
    to: email,
    html: htmlTemplate,
    text: htmlTemplate,
    attachments: [attachment],
  });
  return "success";
}

export async function generateHtmlForFileDownload(templateName = "template") {
  const { environment } = await getConfig();

  const filePathRemote = `/public/${templateName}.html`;
  const filePathLocal = `/../../public/${templateName}.html`;
  const templateFile = environment === "local" ? filePathLocal : filePathRemote;
  return fs.readFileSync(__dirname + templateFile, "utf8");
}

export const emailService = async (options: EmailOptions): Promise<void> => {
  const config = await getConfig();

  const toEmails = (options.to || "")
    .split("|")
    .filter((email: string) => /^[^@\s]+@its\.jnj\.com$/i.test(email));

  const errors = [];

  for (const server of config.email.relayServers) {
    const transporter = createTransport(server); // NOSONAR
    const mailOptions = {
      from: options.from || config.email.defaultFromEmail,
      to: toEmails.join(", "),
      subject: options.subject,
      text: options.text,
      html: options.html,
      attachments: options.attachments,
    };

    try {
      await transporter.sendMail(mailOptions);
      Logger.info(`Email sent: ${options.subject} to ${options.to}`);
      return;
    } catch (err) {
      errors.push(err);
    } finally {
      transporter.close();
    }
  }

  throw new Error(
    "All relay servers are unavailable. Error details: " + errors.join(", ")
  );
};
```

### 数据生成 csv 并作为附件发送

Excel 在打开 CSV 文件时，默认采用 ANSI 编码，而不是 UTF-8。当文件包含中文或其他非 ASCII 字符时，直接用 Excel 打开可能会出现乱码

```ts
async function sendDataEmail(
	email: string,
	data: Record<string, string>[],
	fileName: string
) {
	const blobCsvString = unparse(data);
  // 在CSV文件的开头添加一个Byte Order Mark (BOM)，Excel就能正确识别为UTF-8编码。
	const BOM = "\uFEFF";
	const fileData = Buffer.from(BOM + blobCsvString, "utf-8");

	return sendEmail(email, fileName, fileData);
}

const fileData = trackingList.map((item) => ({
  标题: item.title,
  ...,
  时间: formatUTCDate(item.sign_in_date.toISOString()),
}));
return Attachment.sendDataEmail(email, fileData, "数据导出.csv");
```

### 将 blob 中的文件作为附件发送

```ts
async function sendAttachmentEmail(email: string, attachmentUrl: string) {
  const urlArr = attachmentUrl.split("/");
  const [, , , , fileName] = urlArr;
  const [filename] = fileName.split("?size=");
  const fileData = await downloadFile(attachmentUrl);

  return sendEmail(email, filename, fileData);
}

export async function downloadFile(attachmentUrl: string) {
  const urlArr = attachmentUrl.split("/");
  const [, , destination, fileType, fileName] = urlArr;
  const [file] = fileName.split("?size=");
  const encodedFilename = encodeURIComponent(file);
  const { content } = await getFileFromBlob(
    `${destination}/${fileType}/${encodedFilename}`,
    fileType as FileType
  );
  return new Promise<Buffer>((resolve, reject) => {
    const chunks: Buffer[] = [];
    if (content) {
      content.on("data", (chunk: Buffer) => {
        chunks.push(chunk);
      });

      content.on("end", () => {
        resolve(Buffer.concat(chunks));
      });

      content.on("error", (err) => {
        reject(err);
      });
    } else {
      reject(new Error("No content received"));
    }
  });
}

export const getFileFromBlob = async (
  fileName: string,
  fileType: FileType,
  rangeStart = 0,
  rangeEnd?: number
) => {
  const blockBlobClient = await getContainerClientByFileName(fileName);
  const count = rangeEnd ? rangeEnd - rangeStart + 1 : undefined;
  const downloadBlockBlobResponse = await blockBlobClient.download(
    rangeStart,
    count
  );
  const splits = fileName.split(".");
  const suffix = splits.pop();
  const contentType = getContentType(fileType, suffix);

  return {
    contentType,
    content: downloadBlockBlobResponse.readableStreamBody,
  };
};

export async function getContainerClientByFileName(fileName: string) {
  const containerClient = new ContainerClient(
    `https://${azure[blob].storageAccount}.${azure[blob].sasDomain}/${azure[blob].blobContainer}?${azure[blob].sasToken}`
  );
  return containerClient.getBlockBlobClient(fileName);
}
```
