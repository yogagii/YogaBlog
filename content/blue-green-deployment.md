Title: Blue-Green Deployment
Date: 2021-09-03
Category: Programming
Tags: AWS
Author: Yoga

> Blue Green deployments is a technique for rapidly and repeatedly releasing changes to software in production.

1. Go to EC2 instances in AWS and rename environment (EC2(s) in which you want to deploy the code) EC2(s) by appending -Blue in the end of the name of EC2.
2. Create new EC2(s) by using following documentation Set Up - EC2.
3. For new created EC2(s), add -Green in the end of the name of EC2.
4. After provisioning EC2(s) from Step 2, Setup EC2 by using following documentation Set Up - EC2 Instance.
5. Once Step 3 is completed, Now create new Target Group in AWS.
6. Open Infra Set Up page, and look for Create Target Group from AWS console and follow those steps.
7. After creating Target Group, Select newly created Target Group and register your EC2(s) created from Step 3.
8. Now, go to Load Balancers, and select your ALB which is used in your environment infra.
9. After selecting ALB, Go to Listeners tab.
10. Click on View/edit rules under Rules column.
11. Click on Edit icon which is present in page menu bar.
12. Click on Edit icon which is present in the row where Rules are displaying.
13. Click on Edit icon which is present in Then column, left side of Forward to.
14. Select a target group select your new target from dropdown.
15. For the existing Target group assign 100 for traffic distribution and for new Target group assign 0.
16. Expand Group-level Stickiness and enable it for 1 days.
17. Click on Tick icon and then click on Update button.
18. Now go to Target Group, for your newly created Target Group check the Health Status. If it is healthy, then you good for code deployment.