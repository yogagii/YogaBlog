Title: Azure Key Vault
Date: 2025-02-07
Category: Cloud
Tags: Microsoft
Author: Yoga

### AZ-Cli

#### Secret

```Bash
az login --use-device-code
# https://microsoft.com/deviceloginchina

# 需要 Key Vault Reader
az keyvault secret list --vault-name xxx

# 需要 Key Vault Secrets Officer
az keyvault secret show --vault-name xxx --name Test
# {
#   "attributes": {
#     "created": "2024-09-29T09:57:21+00:00",
#     "enabled": true,
#     "expires": "2099-09-29T09:56:45+00:00",
#     "notBefore": null,
#     "recoveryLevel": "Recoverable",
#     "updated": "2024-09-29T09:57:21+00:00"
#   },
#   "contentType": null,
#   "id": "https://xxx.vault.azure.cn/secrets/Test/***",
#   "kid": null,
#   "managed": null,
#   "name": "Test",
#   "tags": {},
#   "value": "Test"
# }

# 创建
az keyvault secret set --name Test --vault-name xxx --value Test --expires 2025-11-01
az keyvault secret set --name rsa-private-key-2048-pkcs8 --vault-name xxx --file "rsa_private_key_2048_pkcs8.pem" --expires 2025-11-01

# delete
az keyvault secret delete --name rsa-private-key-2048-pkcs8 --vault-name xxx 
# Secret rsa-private-key-2048-pkcs8 is currently in a deleted but recoverable state, and its name cannot be reused; in this state, the secret can only be recovered or purged.
az keyvault secret recover --name rsa-private-key-2048-pkcs8 --vault-name xxx

az keyvault secret show --vault-name xxx --name rsa-private-key-2048-pkcs8
```

#### Key

私钥应该存储在Azure Key Vault中以保护其安全，公钥可以安全地公开，因为它不用于解密或签名，而是用来加密数据或验证签名。将私钥和公钥分开存储可以减少安全风险。

https://learn.microsoft.com/en-us/cli/azure/keyvault/key?view=azure-cli-latest#az-keyvault-key-import

```bash
az keyvault key import --vault-name "ContosoKeyVault" --name "rsa-public-key-2048" --pem-file "rsa_public_key_2048.pem"

az keyvault key list --vault-name xxx
az keyvault key import --vault-name "xxx" --name "rsa-private-key-2048-pkcs8" --pem-file "rsa_private_key_2048_pkcs8.pem"  --expires 2025-11-01
az keyvault key import --vault-name "xxx" --name "rsa-private-key-2048-pkcs8-2" --pem-file "rsa_private_key_2048_pkcs8.pem"  --expires 2025-11-01 --exportable
az kubectl create secret generic my-private-key --from-file=rsa_private_key_2048_pkcs8.pem

az keyvault key show --vault-name xxx --name rsa-private-key-2048-pkcs8

az keyvault set-policy --name "xxx" --secret-permissions get

# 下载公钥
az keyvault key download --vault-name "xxx" --name "rsa-private-key-2048-pkcs8" --file "public_key.pem"
# 如果私钥可导出，则下载私钥，默认情况下不允许导出私钥，但可以导出公钥
az keyvault key download --vault-name "xxx" --name "rsa-private-key-2048-pkcs8" --file "private_key.pem"
```

当您使用 `az keyvault key import` 命令将私钥导入到 Azure Key Vault 时，Key Vault 会存储整个密钥对，包括私钥和公钥。这是因为 Key Vault 设计为管理整个密钥生命周期，包括使用密钥进行加密、解密、签名和验证等操作。因此，即使您只提供了私钥，Key Vault 也会生成相应的公钥。

如果您在使用AKS 并通过 Helm 将密钥挂载到虚拟机 (VM) 上时，发现挂载的信息变成了公钥，这可能是因为 Key Vault 默认提供了公钥

### Mount into vm

service1-deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
spec:
  template:
    spec:
      containers:
          volumeMounts:
            - name: {{ .Values.secretProviderClass.name }}
              mountPath: {{ .Values.mountPath }}
              readOnly: true
      volumes:
        - name: {{ .Values.secretProviderClass.name }}
          csi:
            driver: secrets-store.csi.k8s.io
            readOnly: true
            volumeAttributes:
              secretProviderClass: {{ .Values.secretProviderClass.name }} 
```

secret-provider-class.yml
```yaml
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: {{ .Values.secretProviderClass.name }}
  namespace: {{ .Values.env }}
spec:
  provider: azure
  parameters:
    cloudName: AzureChinaCloud
    tenantId: {{ .Values.secretProviderClass.tenantId }}
    useVMManagedIdentity: "true"
    userAssignedIdentityID: {{ .Values.secretProviderClass.userAssignedIdentityID }}
    keyvaultName: {{ .Values.secretProviderClass.keyvaultName }}
    objects:  |
      array:
        - |
          objectName: SECRET1
          objectType: secret
        - |
          objectName: SECRET2
          objectType: secret
```

验证
```bash
kubectl get services --all-namespaces

kubectl exec -it service/service1 -n dev -- ls /mnt/secrets
kubectl exec -it service/service1 -n dev -- cat /mnt/secrets/SECRET1
```

### Read Secret with Java

https://docs.azure.cn/zh-cn/key-vault/secrets/quick-create-java?tabs=azure-cli

https://learn.microsoft.com/en-us/java/api/overview/azure/identity-readme?view=azure-java-stable#authenticating-with-defaultazurecredential

1. VM → Identity → system assigned → status: On
2. Key vaults → Access control → add role assignment → members → Managed Identity → VM

```java
public Result<Integer> getSecret(@RequestParam(value = "apikey", required = true) String apikey) {
  String keyVaultUri = "https://xxx.vault.azure.cn/";
  ManagedIdentityCredential defaultCredential = new ManagedIdentityCredentialBuilder().build();
  
  HttpClient httpClient = new NettyAsyncHttpClientBuilder()
          .responseTimeout(Duration.ofSeconds(120))
          .build();

  SecretClient secretClient = new SecretClientBuilder()
          .vaultUrl(keyVaultUri)
          .credential(defaultCredential)
          .httpClient(httpClient)
          .buildClient();

  KeyVaultSecret secret = secretClient.getSecret("SECRET1");
  String apikeyValue = secret.getValue();
  System.out.println("apikeyValue: " + apikeyValue);

  return ResultGenerator.success(0);
}
```

Read Secret with Python
```python
import os
from azure.identity import ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient
 
# 设置存储账户和Key Vault的名称
storage_account = "xxx"
key_vault_name = "xxx"
secret_name = storage_account
 
# 构建Key Vault的URL
key_vault_url = f"https://{key_vault_name}.vault.azure.cn/"
 
# 使用托管标识获取凭据
credential = ManagedIdentityCredential(authority="https://login.chinacloudapi.cn")
 
# 创建SecretClient
secret_client = SecretClient(vault_url=key_vault_url, credential=credential)
 
# 获取秘密值
secret = secret_client.get_secret(secret_name)
secret_value = secret.value
 
# 打印秘密值
print(f"Secret Value: {secret_value}")
```
