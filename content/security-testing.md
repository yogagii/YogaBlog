Title: Application Security Testing
Date: 2025-02-07
Category: Programming
Tags: Security
Author: Yoga

### SAST（Static Application Security Testing）静态应用程序安全测试
    
* 定义：SAST是一种在软件开发过程中对源代码进行分析的安全测试方法（白盒测试）。它通过静态分析技术，检查代码中的潜在安全漏洞。
* 特点：
  * 静态分析：在代码运行之前进行分析，不需要运行代码。
  * 白盒测试：需要访问源代码，通常在开发阶段进行。
  * 自动化程度高：可以集成到开发工具和持续集成/持续部署（CI/CD）流程中。
* 适用场景：适用于开发阶段，帮助开发人员在代码编写过程中发现和修复安全漏洞。
* 工具：  
  * SonarQube
  * Snyk
    
### DAST（Dynamic Application Security Testing）动态应用程序安全测试

* 定义：DAST是一种在运行时对应用程序进行安全测试的方法（黑盒测试）。它通过模拟攻击来发现应用程序在运行时的安全漏洞。
* 特点：
  * 动态分析：在应用程序运行时进行测试。
  * 黑盒测试：不需要访问源代码，通常在测试阶段或生产环境中进行。
  * 自动化程度高：可以自动化执行测试，但通常需要人工干预来验证发现的漏洞。
* 适用场景：适用于测试阶段和生产环境，帮助发现运行时的安全漏洞。
* 工具： 
  * Qualys 是一家提供云安全和合规解决方案的公司

    Qualys Web Application Scanning (**WAS** 应用程序安全扫描) 是一种基于云的服务，属于DAST的范畴，它提供自动化的Web应用爬取和测试，以识别包括跨站脚本（XSS）和SQL注入在内的漏洞
  * NoName API Security Test：通过模拟攻击场景来检测 API 在运行时的安全漏洞。
    
    In order to run the scan, the tool has to be able to parse these API documents, and the only supported format is OpenAPI documentation. (swagger)
  * DARM（Dynamic Application Runtime Monitoring）Scan 是一种动态应用运行时监控扫描技术


### 渗透测试（Penetration Testing）
* 定义：渗透测试是一种模拟真实攻击场景的安全评估方法，旨在发现系统、网络或应用程序中的安全漏洞。它通常由专业的安全专家手动执行，也可以结合自动化工具进行。
* 特点：
  * 综合性：渗透测试通常涵盖多个层面，包括网络、应用程序、操作系统等。
  * 模拟攻击：通过模拟真实攻击者的手段和方法，发现潜在的安全漏洞。
  * 手动与自动化结合：虽然可以使用自动化工具，但通常需要人工干预来验证和利用漏洞。
* 适用场景：适用于对系统进行全面的安全评估，特别是在系统上线前或重大变更后。

德勤常规CPCS中带的渗透测试大致分为两个部分，第一是漏洞扫描，使用自动化脚本工具对系统进行扫描，会检测出一些漏洞。第二是手动测试，在逻辑漏洞这一块会比较侧重，例如越权问题（水平越权和垂直越权）。

部分进行测试的测试场景：
  * 跨站点脚本（CSS，Cross Site Scripting）
  * SQL注入（SQL Injection）
  * 破损的认证和会话管理 （Broken authentication and session management）
  * 文件上载缺陷 （File Upload flaws）
  * 缓存服务器攻击 （Caching Servers Attacks）
  * 安全错误配置（Security Misconfigurations）
  * 跨站点请求伪造（Cross Site Request Forgery）
  * 密码破解（Password Cracking）

### Malware scan 恶意软件扫描

* 定义：Malware Scan 是一种安全检测技术，旨在识别和清除计算机系统、网络或应用程序中的恶意软件（Malware）。恶意软件是指任何未经授权的、有害的软件，包括病毒、木马、蠕虫、间谍软件、广告软件、勒索软件等
* 工具：TrendMicro on VM

The policy what action to take depending on the type of malware that is found. Use custom actions：

- Virus: Clean 清除病毒，安全软件将尝试移除病毒而不删除被感染的文件
- Trojans: Quarantine  将木马隔离，将木马移动到一个安全的位置，防止它们对系统造成进一步的伤害
- Packer: Quarantine 将打包程序（可能用于加密恶意软件）隔离
- Spyware:  Quarantine 将间谍软件隔离
- CVE Exploit:  Quarantine  将CVE漏洞隔离
- Aggressive Detection Rule 激进检测规则: Pass 放行
- Cookie: Delete 删除，清除恶意或可疑的cookies
- Other Threats: Clean 清除其他类型的威胁

Testfile: https://www.eicar.org/download-anti-malware-testfile/
https://docs.trendmicro.com/all/ent/de/v1.5/en-us/de_1.5_olh/ctm_ag/ctm1_ag_ch8/t_test_eicar_file.htm

```bash
curl --request GET --url 'https://raw.githubusercontent.com/Da2dalus/The-MALWARE-Repo/refs/heads/master/Virus/Melissa.doc' >> Melissa.doc
curl --request GET --url 'https://raw.githubusercontent.com/Da2dalus/The-MALWARE-Repo/refs/heads/master/Banking-Malware/Zloader.xlsm' >> Zloader.xlsm

wget -O eicar.com https://www.eicar.org/download/eicar-com/?wpdmdl=8840&refresh=672dc91e4dc701731053854

vi test # X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*
```
