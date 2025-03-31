# CS-506

This is the project repository for CS 506: Computational Tools for Data Science


## Dataset Preprocessing :

The cleaning process of the data started with the visualization of the data frame. The following points below highlights the steps taken.

### **_Dataset 1 : Operating Budgets_**

**_1. Filtering :_**

The dataset consisted of lots of irrelevant departments that were not necessary for the analysis of BPD (Boston Police department). The dataset was filtered on the BPD prior to the handling of missing values, outliers and other analysis.

**_2. Missing values :_**

The missing values within the dataframe were isolated. The missing values were labelled in the original dataset as “#Missing”. 

**_3. Datatypes :_**

Numerical columns such as Year wise Budget were interpreted as “Object” Datatype. The respective columns were converted into a floating type datapoint for easier analysis and to extract the relevant statistics out of them.  


### **_Dataset 2 : Employees Earnings Data_**


**_1. Aggregation :_**

For the employees earnings data, the datasets were from each year from 2011-2024. These datasets had to be combined into one large dataframe for each year. Secondly, a mapping of column names had to be used to ensure that all the datasets have the same features for the combination. As both BPD and non-BPD is used for the analysis of this dataset, all the different departments were kept. 

**_2. Missing values :_**

The majority of missing values were seen in columns where a employee did not receive pay for a certain category. These were set to be 0 as that is a true reflection of that column as then did not receive overtime, injury or retro pay for that given time period.


**_3. Zip-Code :_**

Finally, the zip codes were adjusted to be all in the same format, which can be used to see difference in average earnings for each zip code in the state of Massachusetts.


## Outlier Detection :

### **_Dataset 1 : Operating Budgets_**

![alt text](Plots/Outlier.png)

InterQuartile Range (IQR) was used to detect the outliers. Each of the numerical feature columns 3rd Quartile and 1st Quartile were obtained and then the values exceeding the quartile and the IQR*1.5 combined were identified. Post that, Manual eyeballing of the data to confirm if indeed the presented values were outliers was used. 

### **_Dataset 2 : Employees Earnings Data_**

![alt text](./Plots/OutliersEmployees.png)

Similarly, for the second dataset the same approach was followed using IQR. This process was followed for the numerical features, and was also only used for entries which did not contain 0 values, as many columns had a large amount of rows which were 0. No extreme outliers had been identified that had to be removed or adapted.


## Visualization and Insights :

### **_1: Operating Budgets_**

Boston Police Department has undergone varying shifts between the years 2022 and 2025. While the overall budget has indeed increase between the given time frames, there are certain expense categories and intra-department allocations that have experienced significant fluctuations and changes. 



**_1. General Trends :_**

The overall budget has increased from 2022 to 2025 for most of the departments. This suggests an increased emphasis on most of the department activities. The increase has been seen on various expense categories ranging from equipments to personnel across which the trend is overall increasing however with notable fluctuations.

The below diagram highlights the increase/decrease in budgets across departments between 2022-2025

![alt text](./Plots/2022_2025_Department_Budget_Change.png)


_**2. Significant areas where budget was reduced :**_

One of the important insights that was derived from this analysis is that of the reduction in the prioritization of intelligence focused spending. 

Bureau of Investigative services saw a cut across various different expense categories between the fiscal years of 2022 and 2025. This signifies the shift from investigative services. 

The police commissioner’s office has reduced the budget for Supplies and Materials by 35% between 2022-2025.

The Bureau of Intelligence & Analysis saw a decreasing trend in its budget from 2022-2023-2024 with a slight recovery (increase) in budget from 2024-2025

![alt text](./Plots/Decrease_Budgets.png)

**_3. Significant areas where budget was increased :_**

Most of the department and expense categories within each department saw an increase in their budgets. The increase in budget was observed across majority of the expense categories with a special focus on the equipments, contractual services and the Current Charges and Obligations.

One of the interesting trends uncovered was that of the expense category “Current Charges and Obligations” under the Bureau of Field Services. It saw a staggering 5523% increase in budget between 2022 and 2025. This suggests a major operational expansion. 

Equipments expenses underneath the Bureau of Community Engagement and Bureau of Professional Development saw a dramatic increase in its budget of 4091% and 2798% respectively. This suggests an increased attempt at public initiatives, and training the personnel with the latest modern technological standards. 

Across many departments, Contractual services have seen sharp rises with the highest being noted for Bureau of Professional Standards. 

One interesting trend that can be observed is that of the Bureau of Community Engagement. Although many expense categories within this department have seen a staggering increase in its budget and the overall trend between 2022 and 2025 also suggest an increase in the budget, between the years of 2024 and 2025, It has faced cuts in funding. 

![alt text](./Plots/Increase_Budgets.png)


**_4. Shifts in Funding between Departments :_**

Most of the department saw an increase in their budgets from 2022 to 2025 except the Bureau of Intelligence and Analysis & Bureau of Investigative Services.

Bureau of Community Engagement saw a growth between 2022-2024 and from 2024-2025, a cut in budget has been observed.

The below diagram highlights the increase/decrease in budgets across departments between 2024-2025

![alt text](./Plots/2024_2025_Department_Budget_Change.png)

The personnel services under the Bureau of Intelligence and Analysis saw a major decrease in its funding. The budget for this department started mildly recovering from 2024.

Bureau of Investigative Services saw a decline in its budget from 2022 to 2025 and also across much of its expense category. It did not see a positive growth even from the fiscal year 2024 unlike the Intelligence and Analysis department. This heavily signifies the reduced emphasis on investigative resources. 

### **_2: BPD Paychecks_**

The second key question that needs answering is how the BPD paychecks have changed year-over-year and how they compare with non-BPD Boston City employees. A detailed analysis of the data was done to answer these two questions.

**_1. Historical Trends of BPD Paychecks :_**

At first, a look into the average pay distribution of BPD employees was done to see how it has changed. The data is available from 2011 to 2024, thus, we can visualize and see the changes over the last 13 years. 

As we can see from the diagram below, the average of regular, overtime and total earnings has been following a similar trend from 2011-2023. The only interesting thing to note from this is the high increase in total earnings from 2023 to 2024. This will be discussed further in the following section.

![alt text](./Plots/BPD%20Average%20Pay%202011-2024.png)

Also, for the year 2024, the members of the Boston Police Department had the largest earnings of all departments within the City of Boston, with more than $5.4 billion in total earnings. This is more than $2 billion more than the department with the second-highest earnings. This just showcases the importance of the BPD and this study in understanding police compensation trends, resource allocation, and the broader impact of law enforcement funding.

![alt text](./Plots/TotalEarnings2024Departments.png)

**_2. Analysis of 2024 and 2023 for BPD :_**

A comparison was made between the average earnings per category of the BPD between 2023 and 2024. From these two charts, we can clearly see that although the average regular earnings increased from $74k to $78k, it resulted in a lower percentage of the average total earnings per employee. Overtime made up a similar percentage of the average total paychecks in 2023 and 2024, with no notable increases in the BPD. This is good as it shows a constant trend.

The largest increases were seen in Retro pay and Detail pay, which increased by more than $10k and increased to 5% more of the total pay distribution. Retro pay, also known as retroactive pay, is for police salary refers to compensation owed to police officers for past work due to delayed contract negotiations, salary increases, or corrections to underpaid wages. An internal investigation will have to be done to see why this large increase in Retro pay occurred from the year 2023 to 2024.

Detail pay refers to compensation police officers receive for working private or special duty assignments outside their regular shifts, such as security at events, traffic control for construction, or private business security. This illustrates that most members of the BPD engaged in more private and special duty assignments compared to 2023. This could be due to the election year taking place in 2024, where more police and security are needed for rallies and events. It is not explicitly mentioned if the pay is coming out of the BPD budget or from third-party sources, but it is usually funded from outside of the BPD.

![alt text](./Plots/BPDDistribution2023-2024.png)

 **_3. Comparing BPD and non-BPD employees :_**

 Finally, a deep dive was done into how the average BPD paycheck compares to the rest of the paychecks from the city of Boston.  In the following two graphs, we can see the average salary of BPD employees compared to the average salary of non-BPD employees, as well as just their overtime earnings. As we can see from 2011 to 2023, both groups followed a similar increasing trend. The large increase in average pay has already been explained by the large increase in Detail Pay and Retro Pay mentioned in the previous section. Other than this, no clear discrepancies between BPD and non-BPD employees can be seen from this graph. The only other notable point is that the BPD had a decrease in average salary from 2020 to 2021, which is most likely due to the Covid-19 pandemic.


 ![alt text](./Plots/BPDvsNonBPD.png)

 In this second plot, we took a look at the difference in percentage increase for each year of BPD employees and non-BPD employees. A moving average was plotted for a smoother visual and to determine if in the long run both sets of employees are receiving the same increase. 

 From this plot we can see that non-BPD employees have had a more consistent increase in total earnings as well a overtime earnings compared to the BPD employees, varying between 0-5% for total earnings and between 0-10% for overtime earnings. While BPD employees experience more volatility with regards to increases and decreases in paycheck,s as seen in the first plot. The overtime increases for BPD employees are more stable and vary only between 3-15%.

 ![alt text](./Plots/moving_average_increases.png)


 ### **_3: Injury Pay_**

 This part of the analysis was to see what trends involving injury pay can be determined, and to see what percentage of BPD employees took injury pay in the current year.

 **_1. Number of employees taking Injury Pay :_**

 The following two graphs show the number of BPD employees which took injury pay in a given year. As we can see, in 2024 32% of employees registered with the BPD took injury pay. This is a extremely large increase relative to the previous year, as seen in the second graph. The second graph illustrates the number of employees who took injury pay and those who did not, from 2011 to 2024. This was the first year when more than 1000 employees took injury pay. This might be a reason to do an internal investigation as to why there is a sudden increase in the number of employees who take injury pay in this given year.


 ![alt text](./Plots/injury_pay_amount_BPD.png)

**_2. How much BPD pay came from injury pay:_**

The second part of this was to investigate the total injury pay across the BPD. As we can see from the graph below, the average and total injury pay follow a similar trend from 2011 to 2024. The only noticeable difference is that in 2024, although there is a slight increase in total injury pay, the average injury pay went down by more than 50%. This is very interesting as we saw from the first point, that more people took injury pay in 2024, but the total increase in injury pay was not significant. This shows that it might not be a cause for concern, as the total injury pay seems relatively normal, but the large number of people taking injury pay might still need to be investigated.

![alt text](./Plots/BPD_injury_pay.png)


### **_5: Responsive Record_**
1. Data Information :

There are 2229 details of police officers with 1457 white officers followed by 485 black officers. There are only 308 female officers in comparision to 1921 male officers. The dataset is highly imbalanced and must be taken into consideration before modeling.

2. Datatypes :

Numerical columns contain hourly values and the categorical values contain job title, union code, ethnic group and sex.

**Are certain officers more likely than others to have lower worked-to-paid ratios?**


![image](https://github.com/user-attachments/assets/961256c5-5700-40bb-9886-e6c3fa9723b1)

White and Black officers are more likely to earn higher paid to worked ratios than asian and hispanic officers. The reason for it being more white and black officers are at higher positions. With respect to male and female officers, they earn the same on average. The pay of student officers is an anomaly with them earning signifficantly less for an hour when compared to other officers. Supn In Chief, Bureau Admin and Technology, Bureau of Professional Standards, Bureau of Professional Development, Night Commands earn the most per hour with them over $100/hr. Hispanic officers work over 160 hours more than White officers for an year. This could be a direct effect of more white officers being at higher level when compared to Hispanic officers.

![image](https://github.com/user-attachments/assets/ccafbcd4-bb1e-4269-8a9e-92ea6e730731)

Number of hours per month worked is higher for the same officers that get paid the highest with them working under 165 hrs/month with the rest working at the rate of 170 hrs/month.


