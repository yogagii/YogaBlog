Title: ExcelJS
Date: 2023-07-26
Category: Javascript
Author: Yoga

ExcelJS 是一个 Node.js 模块，可用来读写和操作 XLSX 和 JSON 电子表格数据和样式。

```ts
import ExcelJS from 'exceljs';

export async function getXlsx(targetData: object[]) {
  // 获取列名
  const propertyNames = Object.keys(targetData[0]);

  // 创建workbook
  const workbook = new ExcelJS.Workbook();
  // 创建worksheet
  const worksheet = workbook.addWorksheet('My Sheet');

  // 表头样式
  const headerStyle: Partial<ExcelJS.Style> = {
    font: { bold: true, size: 10, color: { argb: '#FF202020' }, name: 'Arial' },
    fill: { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFF4F4F4' } },
    alignment: { horizontal: 'center', vertical: 'middle' },
    border: {
      top: { style: 'thin' },
      left: { style: 'thin' },
      bottom: { style: 'thin' },
      right: { style: 'thin' },
    },
  };

  // 表格数据样式
  const contentStyle: Partial<ExcelJS.Style> = {
    font: { bold: false, size: 8, color: { argb: '#FF63666A' }, name: 'Arial' },
    fill: { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFFFFFFF' } },
    alignment: { horizontal: 'center', vertical: 'middle', wrapText: true },
    border: {
      top: { style: 'thin' },
      left: { style: 'thin' },
      bottom: { style: 'thin' },
      right: { style: 'thin' },
    },
  };

  // 写入表头
  propertyNames.forEach((propertyName: string, i: number) => {
    const curColIndex = i + 1;
    worksheet.getCell(1, curColIndex).value = propertyName;
    worksheet.getCell(1, curColIndex).style = headerStyle;
  });

  // 写入数据
  targetData.forEach((data: any, i: number) => {
    const currentRow = i + 2;
    propertyNames.forEach((propertyName: string, j: number) => {
      const curColIndex = j + 1;
      worksheet.getCell(currentRow, curColIndex).value = data[propertyName];
      worksheet.getCell(currentRow, curColIndex).style = contentStyle;
    });
  });

  // 冻结首行
  worksheet.views = [{ state: 'frozen', ySplit: 1 }];

  // 设置列宽
  for (let j = 1; j <= propertyNames.length; j++) {
    let maxLength = 0;
    for (let i = 1; i <= targetData.length + 1; i++) {
      const cellValue = worksheet.getCell(i, j).value;
      if (cellValue) {
        const cellValueLength = cellValue.toString().length;
        if (cellValueLength > maxLength) {
          maxLength = cellValueLength;
        }
      }
    }
    worksheet.getColumn(j).width = maxLength + 1;
  }

  //return the buffer
  return await workbook.xlsx.writeBuffer();
}
```

controller
```ts
import { Res } from '@nestjs/common';
import { Response } from 'express';

@Get('/download')
async getDownload(
  @Res() res: Response,
) {
  const buffer = await getXlsx(data);
  res.setHeader(
    'Content-Type',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  );
  res.setHeader(
    'Content-Disposition',
    `attachment; filename=custom_thresholds.xlsx`,
  );
  res.send(buffer);
}
```