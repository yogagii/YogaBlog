Title: Technical Debt
Date: 2021-10-29
Category: Programming
Author: Zack, Yoga

## What is Technical Debt 

Technical Debt refers to the need to revisit previously written code. Often associated with the practice of relying on temporary easier-to-implement solutions to achieve short-term results at the expense of efficiency in the long run. That’s a metaphor coined by Ward Cunningham for describing the impact of accruing tech issues.

* Principal: The principal is all the work that must be done to modernize the technology stack. 

* Interest: The interest is the complexity tax that project pays. The extra effort that it takes to add new features is the interest paid on the debt. These frictional losses inhibit companies’ long-term velocity and productivity and harm current budgets and returns on investment.

## What causes Technical Debt

There are in general two types of technical debt that we are concerned:

* Intentional tech debt (also called deliberate or active) happens when the team consciously delays the resolution of some issues to yield short term benefit but unsustainable in the longer term. For example, making a release or working on a POC. Keeping in check the awareness of going back to make changes to the design after. 

* Unintentional tech debt (also called inadvertent, accidental, outdated, passive) occurs when the team is doing a subpar job without even knowing it while accruing many issues along the way. There are times when we did not realize the importance of certain activities, or the good practices behind designing certain solutions. As we become wiser and less ignorant of the good practices, we need to capture all those activies as debt. 

## Consequences of Technical Debt

* Pros:
  * We are able to yield short term benefits such as release.
  * Gain competitive advantage by shortening time-to-market.
  * Gain user feedback faster to test out features. 
* Cons:
  * Sacrificing future speed due to debt built up in the application. 
  * Left unchecked, we might arrive at Technical Bankruptcy, which happens when even simple changes of code or extensions become unmanageable. 

## How to measure Technical Debt
### What is our Technical Debt Budget

* Assuming 1 story points is approximately US$ 500
* Development Capacity in a year is ~1200 story points (Assuming stable team with average velocity 48 story points per 2-week sprint)
* AMS Support Story Points is ~200 story points 
* Technical Debt Budget for Vital is approximately 1400 story points per year. (100%)
* As a start, we will adjust our risk tolerance at 50%. Meaning, we should limit the amount of technical debt in Vital to below 700 story points at any point of time.

### What is our Technical Debt Interest 

There are a few metrics that we can use to calculate the weight of interest 

Metric | Interest Rate Calculation
- | -
How frequent is our team going to change | Divide the number of new team members (joined less than 2 months) over total team members as weightage. For example, 2 out of 8 team members are new. The interest rate will be 2/8 = 25%
How frequent is the code going to change | 50% for code that is changing frequently. 25% for code that has moderate change frequency. 0% for code that is not going to change.
What is our code test coverage | 50% for features that does not have good test coverage.
How long has the technical debt exist in the backlog | 5% for every sprint that has passed.

Examples:

Summary | Story Points | Interest Rate | Total Story Points | Remarks
- | - | - | - | -
Remove feature toggle for "Profile" page | 2 | 2 x ( 0% + 25% + 0% + 2 x 5%) = 0.7 | 2 + 0.7 = 2.7 ≅ 3 | Assuming the team is stable - 0%; Assuming the code is not going to change as frequent - 25%; Assuming there are good test coverage on this feature - 0%; Assuming the tech debt has been in backlog for 2 sprints - 2 x 5 %

## Payback Strategy

* The goal is not to reach zero technical debt. Rather, we should work to size, value, and control our tech debt and regularly communicate it within the product team and scrum team.
* Not everything needs refactoring. If it's not critical, or nobody needs to improve its functionality in the next months, or it's just too complicated, consider acknowledging it as tech debt. - Andreas Klinger, Refactoring large Legacy Codebases

### There are a few actions to take to repay technical debt
* Track and Socialise
  * Keep a view of all technical debts in the application and indicate the principal and interest.
  * Avoid reaching technical bankruptcy by using up technical debt budget.
  * Technical Debt should be updated timely by scrum team timely.
  * Product Team and Scrum Team should review the list in story grooming and sprint planning. 
* Prioritise
  * Measure the time horizon to an incident of a technical debt. The shorter the time horizon to an incident, the higher the priority of the item.
  * Measure the proximity of technical debt to a feature in Product Roadmap. Any upcoming product features that has related technical debt should be prioritised. Any technical debt related to a new user story will create friction in the delivery 