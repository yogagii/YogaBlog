Title: Microsoft Azure Adminstrator
Date: 2022-04-13
Category: Cloud
Tags: Azure
Author: Yoga

## Azure Active Directory

用户和组身份：身份验证 + 访问授权

https://portal.azure.com/

https://portal.azure.com/#blade/Microsoft_AAD_IAM/LicensesMenuBlade/Overview

新建并切换域名：

Azure Active Directory -> Manage tenants -> create

创建用户：

Users -> New User

User Test 1: Aa123456

Bob: Caqu2794

Alice: myPassword1234

创建组：

Groups -> New Group -> 添加用户

Devices -> Device Settings -> 指定用户

Join Type: Azure AD joined / register

Azure DNS: 不能实现域名注册，只提供域名解析服务

---

## Azure PowerShell

Azure PowerShell 是一组 cmdlet，用于直接从 PowerShell 管理 Azure 资源。 

### 安装

Azure PowerShell 服务管理模块仅适用于 Windows PowerShell。 它与 PowerShell 6 或更高版本不兼容,并且不在 Linux 或 macOS 上运行.

在vm上打开Edge浏览器（不支持ie），登录v-账号，确保域名在whitelist

登录到 Azure 中国世纪互联
```PowerShell
Connect-AzAccount -Environment AzureChinaCloud
```

安装 Az.Storage 模块版本
```PowerShell
Install-Module -Name Az.Storage -RequiredVersion 5.4.1
```

```PowerShell
# Initialize these variables with your values.
$rgName = "<resource-group>"
$accountName = "<storage-account>"
$containerName = "<container>"
$blobName = "<archived-blob>"

# Get the storage account context
$ctx = (Get-AzStorageAccount `
        -ResourceGroupName $rgName `
        -Name $accountName).Context

echo $ctx

# Get blob
$blob = Get-AzStorageBlob -Container $containerName -Blob $blobName -Context $ctx
```

将 Blob 解除冻结到同一存储帐户
```powershell
# Copy the source blob to a new destination blob in hot tier with Standard priority.
Start-AzStorageBlobCopy -SrcContainer $srcContainerName `
    -SrcBlob $srcBlobName `
    -DestContainer $destContainerName `
    -DestBlob $destBlobName `
    -StandardBlobTier Hot `
    -RehydratePriority Standard `
    -Context $ctx
```

通过更改 Blob 层解除冻结 Blob
```powershell
# Change the blob's access tier to hot with Standard priority.
$blob.BlobClient.SetAccessTier("Hot", $null, "Standard")
```

批量解冻
```powershell
$folderName = "<folder>/"
$blobCount = 0
$Token = $Null
$MaxReturn = 5000

do {
  $Blobs = Get-AzStorageBlob -Context $ctx -Container $containerName -Prefix $folderName -MaxCount $MaxReturn -ContinuationToken $Token
  if($Blobs -eq $Null) { break }
  #Set-StrictMode will cause Get-AzureStorageBlob returns result in different data types when there is only one blob
  if($Blobs.GetType().Name -eq "AzureStorageBlob")
  {
      $Token = $Null
  }
  else
  {
    $Token = $Blobs[$Blobs.Count - 1].ContinuationToken;
  }
  $Blobs | ForEach-Object {
    if(($_.BlobType -eq "BlockBlob") -and ($_.AccessTier -eq "Archive") ) {
      $_.BlobClient.SetAccessTier("Hot", $null, "Standard")
    }
  }
}
While ($Token -ne $Null)
```
