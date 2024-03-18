Title: Snyk
Date: 2024-03-18
Category: Programming
Author: Yoga


注册: https://snyk.io/

Install Snyk CLI

```bash
npm install -g snyk
```

```bash
curl https://static.snyk.io/cli/latest/snyk-macos -o snyk
chmod +x ./snyk
mv ./snyk /usr/local/bin/ 
```

Authenticate your machine

```bash
snyk auth
```

Scan for security issues

```bash
snyk test --all-projects
# open-source packages
snyk monitor --all-projects --org=771080d9-f4f9-42f5-b535-bd9bd76d9984
# Containers
snyk container monitor <repository>:<tag> --org=771080d9-f4f9-42f5-b535-bd9bd76d9984
```

Enable Code Test: 
https://docs.snyk.io/snyk-cli/scan-and-maintain-projects-using-the-cli/snyk-cli-for-snyk-code

```bash
# Source code
snyk code test
snyk code test --org=771080d9-f4f9-42f5-b535-bd9bd76d9984
```

Snyk Preview

https://jenkins.eat.jnj.com/[project-key]/job/[repo-name]/job/[branch]/1/artifact/snyk-scan-id-sast.html

Snyk Ignore: .snyk

```yaml
exclude:
 global:
   - packages/shared/config
```

Snyk CICD: manifest.yaml

```yaml
staticAnalysis:
  enabled: false
  type: multi
  stages:
    sonar: ...
    snyk:
      enabled: true
      type: snyk
      failBuild: false # disable
      snykIacAnalysis: false
      snykSastAnalysis: true
      snykCredentials: xxx
      gitCredentialsId: sourcecode-bitbucket
```
