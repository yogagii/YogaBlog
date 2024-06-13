Title: Azure Cli
Date: 2024-06-13
Category: Cloud
Tags: Azure
Author: Yoga

* clouds

```bash
# list available clouds
az cloud list --output table
# China Azure
az cloud set --name AzureChinaCloud
```

* login

```bash
# login service account
az login --service-principal --tenant xxx -u xxx -p xxx

# local
az login

# vm无法使用浏览器，强制使用设备代码流 
az login --use-device-code
# https://microsoft.com/deviceloginchina
```

* 访问 aks

```bash
az aks get-credentials --resource-group xxx --name xxx
```

* get token

```bash
az account list

az account get-access-token --resource https://ossrdbms-aad.database.chinacloudapi.cn --output tsv --query accessToken
az account get-access-token --resource-type oss-rdbms --output tsv --query accessToken
```

* mysql

```bash
mysql -h xxx.mysql.database.chinacloudapi.cn \
	--user xxx@xxx.com.cn \
	--enable-cleartext-plugin \
	--password=`az account get-access-token --resource-type oss-rdbms --output tsv --query accessToken`
 # user 大小写敏感
```

