Title: SWIFT -- Supply Chain Data Modeling
Date: 2023-11-08
Category: Project
Author: Yoga
Password: project

## Business Value

The Ultimate Supply Chain Planning Experience

SWIFT = Scenario and What If analysis enabled Flexibility and Transparency in Supply Chain

Our Goal is to create capabilities for Global and Regional Planners that predict and analyze the changing needs and disruptions in SC by improving end to end visibility and responsiveness from source to customer for MedTech SC in the ASPAC region. ​ 

Project SWIFT is focused on delivering a MVP solution for a Digital Twin Control Tower for the Endo-mech business from Manufacturing / Distribution Center to the Distributors.

The pilot seeks to provide end-to-end visibility of products within the supply chain through creation of a network digital twin, scenario planning capabilities and timely responsiveness to help better predict and assess changing needs and supply chain disruptions, escalate decision making and improve resiliency.

## Network Lead Time

A graphical network view shows digital representations of supply chain networks. Tabular view to show the lead time by Lane.

lead time一般指前置时间。 前置时间是指从受订到出货所间隔的时间，通常以天数或小时计算。前置时间的减少会使生产商和零售商平均库存水平得到减少。

Shipments which were supposed to arrive (GR date is null) in current date (Shipment ETA). 
Planned Shipments (Shipment ETA) is calculated using GI date + transport Lead time from gdm transport for particular SKU in the lane. 

https://yogagii.github.io/neo4j.html

## User Generated Event

**Event Type**:

- Demand: Model changes to demand 需求变化
- Supply: Model changes to inventory levels 库存变化

**SS Level:** Average safety stock level for event timeline

**Loss Sale Value**: Estimated sum of loss from sales that cannot be carried out- ex. customer moves to a competitor

**Cost**: Estimated sum of cost to carry out solution

**BO Value**

* Start BO value: the BO value of each SKU, site, in the start week of the event.
* End BO value: the BO value of each SKU, site, in the end week of the event.
* POST BO value: inventory of the end week + (end week demand - adjust demand of end week). display the negative value is BO value and 0 if it is positive.
* BO Change: (POST BO - End BO) / End BO * 100
* Safety Stock % by week: new_cal_inventory / safety_stock * 100;

**Event Forecast**

* Scenario 1: If previous week (W-1) inventory is Initial Inventory
* Scenario 2: If previous week (W-1) inventory is not Initial Inventory and is future bucket
* Scenario 3: If previous week (W-1) inventory is not Initial Inventory and is NOT future bucket

Need to calculate event forecast week by week!

## Modeled Solution

**Solution Type:**

1. Standard Node to Node Transfer: uses the standard transportation mode in system suggested lane
2. Expedited Node to Node Transfer: uses a faster alternative transportation mode in system suggested lane
3. Mod Substitution
4. Alternative Code Substitution: Alternate Code Substitution adjusts what % of demand can be replaced with an alternative SKU of the planner's choice

**Periods:** 

periods just correspond to time periods (of length 1 week) in the planning horizon, starting with the current week which is period 1

- transfer_period - this is the week number where the suggested transfer will take place relative to the current week (period 1)
- transfer_week - This is the week-year combination date where the transfer will take place
- transfer_lt - the number of periods (i.e. weeks) it will take for the transfer to arrive at the destination node
- arrival_period - the period (week) where the transferred inventory will arrive at the destination node and actually change the inventory values at the destination

transfer_period + transfer_lt = arrival_period

**Databricks Job:**

1. Scenario Planning for existing event
2. Scenario Planning for user generated event
3. Solution Forecast with applied transfer

Remodel: Display Alert and Action when solutions modeled are past a time threshold where solution may no longer be accurate

https://yogagii.github.io/databricks-api.html

**BO Value:**

- **Pre-Model BO** is calculated in the UI from user-generated event forecast. Pre-Model BO only needs to be updated if the solution is re-modelled or adjusted.
- **Post-Model BO** from DS
    - for each transfer (if I were to apply one transfer)
    - for each solution (if I were to apply ALL transfers in standard/expetited N2N Transfer)

## Email Notification

1. User share user generated event
2. User share model solution
3. Solution ready notification
4. Solution forecast ready notification
5. Feedback required
6. Review SKU notification
7. Weekly Activity Report Summary

## User Preference

1. Content Preference
2. Threshold Preference (Default / Custom SKU)
  These custom preferences will determine the colour coding on the PSI table. Depending on the alert timeframe set by the user, the colour coding will be reflected as needed. customizable by different user id, custom threshold always has more priority compared to default
3. Email Preference

## Web Analytics

* Google Analytics
* Microsoft Clarity

## CICD

https://yogagii.github.io/cicd-pipeline.html

## UI Shared Component

UI developer workflow:

1. Check if the common repo already has a component that fits with the user story
2. If nothing exists, they should add it, PR it
3. Then in the reliability hub (RH) repo, import that shared component from the shared repo (once published in artifactory)
4. If they want to alter an existing shared component, there should be a conversation with the Lead Developers on all squads, to ensure not to make a breaking change that affects another project
5. If for some reason the story has something that shouldn't be added to the shared lib, then add it directly into the RH repo (however this should be rare).
