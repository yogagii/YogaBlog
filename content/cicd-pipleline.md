Title: CI/CD Pipeline Setup
Date: 2021-10-27
Category: Programming
Tags: CI/CD
Author: Zack, Yoga

## Frontend Structure

* _scm_jenkins
  * install.groovy
  * jenkins.yaml
  * s3Upload.groovy
  * unitTest.groovy
  * version-calculation.groovy
* public
* src
* node_modules
* automation_pipelies.yaml
* environment-mapping.yaml
* Jenkinsfile
* jest.config.js
* manifest-sources.yaml
* manifest.yaml
* sonar-project.propertieis

## Steps

1. Create folder called _scm_jenkins under project root directory.
2. '_scm_jenkins/jenkins.yaml'.

This file is required to trigger pipeline build for CI/CD .
```yaml
- url: https://jenkins.eat.xxx.com/project-name/
  buildFrom:
    - master
    - develop
    - stage
    - preprod
  jobs:
    - jobStyle: multi-branch-pipeline
      jobName: vital-frontend
      jobCredentials: sourcecode-bitbucket
      includeBranches:
        - feature/*
        - bugfix/*
        - hotfix/*
        - master
        - develop
        - stage
        - preprod
```
3. 'automation_pipelines.yaml'

This file is to trigger the pipeline automatically. 
```yaml
# Specify which service to subscribe to. This should not be changed
- service: eat-jenkins
# This is the environemt of automation_piplines not environment of application or Jenkins
environment: Production
teamKey: tavc
jenkinsType: dev
```

4. 'environment-mapping.yaml'

This file is required to determine which branch related to which environment and used as an put for pipeline creation. The file looks like as below.
```yaml
- branchNamePattern: "(feature|bugfix|hotfix)/.*"
  environment: "PREDEV"
- branchNamePattern: "develop"
  environment: "DEV"
- branchNamePattern: "stage"
  environment: "STAGE"
- branchNamePattern: "preprod"
  environment: "PREPROD"
- branchNamePattern: "master"
  environment: "PROD"
```

Pipeline Stage | PREDEV | DEV | STAGE | PROD
- | - | - | - | -
Checkout | Y | Y | Y | Y
Manifest Load | Y | Y | Y | Y
Setup | Y | Y | Y | Y
Unit Test | Y | Y | Y | Y
Lint | Y | Y | Y | Y
Dependency Analysis | Y | Y | Y | Y
Static Annalysis | Y | Y | Y | Y
Release | - | Y | Y | Y
Package | - | Y | Y | Y
Publish | - | Y | Y | Y
Version Calculation | - | Y | Y | Y
Resolve Artifact | - | Y | Y | Y
Deploy | - | Y | Y | Y
Intergration Test | - | TBD | TBD | TBD
Regression Test | - | TBD | TBD | TBD
Hyperion Test Automation | - | TBD | TBD | TBD
Robot Test Automation | - | TBD | TBD | TBD
Sauce Labs | - | TBD | TBD | TBD



5. 'manifest-sources.yaml'

This file defines how many type of manifest file are the project using. There is a two type of manifest are available, common and environment specific. This file is used as an argument during pipeline creation in the jenkinsfile.
```yaml
version: "1.0"
sources:
  - name: common
    location:
      locationType: project
      file: manifest.yaml
    manifest:
      type: simple
      path: common
      required: true
  - name: environment
    location:
      locationType: project
      file: manifest.yaml
    manifest:
      type: by-environment
      path: environments
      required: true
```

6. 'manifest.yaml'

This file holds the configuration related to your file. It has majorly two parts. One is common, Other is Environment type.
```yaml
common:
  pipelineType: node
  debug: true
  npm:
    dockerImage: 'xxx.artifactrepo.xxx.com/jpm/node:14'
  artifactory:
    target: tafn-npm
  customSetup:
    enabled: false
    type: script
    script: project/_scm_jenkins/install.groovy
  unitTest:
    enabled: false
    type: script
    script: project/_scm_jenkins/unitTest.groovy
  lint:
    enabled: false
  buildAnalysis:
    enabled: false
  dependencyAnalysis:
    enabled: false
  staticAnalysis:
    type: sonar
    directory: project
    shortLivedAnalysis: false
    shortLivedBuildResults:
      IGNORE:
        BLOCKER: true
        CRITICAL: true
        MAJOR: true
        MINOR: true
        INFO: true
    longLivedAnalysis: false
    longLivedBuildResults:
      IGNORE:
        BLOCKER: true
        CRITICAL: true
        MAJOR: true
        MINOR: true
        INFO: true
      QUALITY_GATE:
        ERROR: SUCCESS
        WARN: SUCCESS
  release:
    enabled: false
  package:
    enabled: false
    type: zip
    dir: project
    include:
      - dist/**
    versionPackageName: true
    versionFileUpdates:
      - type: 'node-package'
  publish:
    enabled: false
    type: artifactory-upload
  versionCalculation:
    enabled: false
    type: script
    script: project/_scm_jenkins/version-calculation.groovy
    confirmVersion: false
  resolveArtifacts:
    enabled: false
    type: artifactory
    artifactPath: tafn-npm
  deploy:
    enabled: false
    type: multi
    parallel: false
    stages:
      s3Upload:
        enabled: true
        type: script
        script: project/_scm_jenkins/s3Upload.groovy
environments:
  PREDEV:
    customSetup:
      enabled: true
    unitTest:
      enabled: true
  DEV:
    customSetup:
      enabled: true
    unitTest:
      enabled: true
    staticAnalysis:
      longLivedAnalysis: false
    release:
      enabled: true
      type: auto
      updateChangelog: false
      merge: false
      confirmVersion: false
      subDirectory: ''
      branchToRelease: develop
      releaseDestination: develop
    package:
      enabled: true
      name: vital-dev-frontend
    publish:
      enabled: true
      filePattern: vital-dev-frontend-*.zip
    versionCalculation:
      enabled: true
    resolveArtifacts:
      enabled: true
      artifactPattern: vital-dev-frontend-${version}.zip
    deploy:
      enabled: true
      stages:
        s3Upload:
          enabled: true
```

8. 'jenkinsfile'

This file creates the pipeline instance by taking multiple arguments like manifestSourcesFile, EnvironmentMappingFile etc. It uses all the shared library required for pipeline.
```python
#!/bin/groovy
@Library('jpm_shared_lib@1.x') _
import org.xxx.pipelines.*
def args = [:]
args.debug = true
args.manifestSourcesFile = 'manifest-sources.yaml'
args.environmentMappingFile = 'environment-mapping.yaml'
new stdPipeline().execute(args)
```

9. Jenkins configuration in the Jenkins console.

Create a new pipeline job by clicking on the " New Item". Select Multibranch Pipeline and provide name to your pipeline.

After creating pipeline Job select the Job you created. Click on Configure button. In the " Branch Source" section, provide git repo url. Click on Add button to add the credential to access Git. Filter By name section provide master feature/* (All all feature).

Click on the Credentials Manager section in Jenkins, select the Pipeline you want to set the credential. Provide credential Id, Access Key and Secret Key ( Received from AWS console) and click on Save.

10. '_scm_jenkins/s3Upload.groovy'

This is the files responsible for uploading your artifact to S3 in AWS. This file contain S3 credential to upload artifact into S3.The file should looks as below.
```groovy
def run(jobManifest) {
  def jobVars = jobManifest.getJobVars()
  ensure.insideDockerContainer('xxx.artifactrepo.xxx.com/jpm/awscli') {
    dir('project') {
      pPrint.info("Started inside Dir")
      deleteDir()
      unstash jobVars.projectStash
      jobVars.packageStashes.each({ stashName ->
          unstash name: stashName
      })
      def environment = jobVars?.jpmEnvironment
      def awsRegion = "us-east-1"
      def version = jobVars?.calculatedVersion
      def packageName="my-vital-front-end-${version}.zip"
      pPrint.info("PackageName inside Dir"+packageName)
      withEnv(["AWS_DEFAULT_REGION=${awsRegion}"]) {
        withCredentials(...) {
          def keyNotExists = sh(
            script: "aws s3 ls s3://vital-preprod-site-asset/frontend/${packageName}",
            returnStatus: true
          )
          if (keyNotExists) {
            sh "aws s3 cp ./dist/${packageName} s3://vital-preprod-site-asset/frontend/ --sse"
              pPrint.info("S3 upload Done")
          } else {
            pPrint.info("Package already exists in the bucket")
          }
        }
      }
    }
  }
}
 
def expectsManifest() {
    return true
}
 
return this;
```

11. '_scm_jenkins/install.groovy'

This is where all the prerequisite builds happen. 

```groovy
def run(jobManifest) {
  def jobVars = jobManifest.getJobVars()
  ensure.insideDockerContainer('xxx.artifactrepo.xxx.com/jpm/node:14') {
    dir('project') {
      def jpmEnvironment = jobVars?.jpmEnvironment
      def branchEnv = "dev"
      pPrint.info("JPM Environment: " + jpmEnvironment)
      if (jpmEnvironment == "STAGE") {
        branchEnv = "stage"
      } else if (jpmEnvironment == "PREPROD") {
        branchEnv = "preprod"
      } else if (jpmEnvironment == "PROD") {
        branchEnv = "prod"
      } 
      sh "yarn"
      sh "yarn build-${branchEnv}"
    }
  }
}
def expectsManifest() {
  return true
}
return this;
```
