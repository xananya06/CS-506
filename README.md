# CS-506

This is the project repository for CS 506: Computational Tools for Data Science


## Link to Presentation

https://youtu.be/2GusWFGZqok

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

### **_Dataset 3 : Field Interrogation and Observation_**


**_1.Filtering :_**
The dataset was preprocessed by removing duplicate records and unnecessary columns, ensuring that only relevant information remains. A year column was added to distinguish records from different files when combining multiple datasets. Additionally, invalid or inconsistent entries in categorical and numerical fields were cleaned and standardized.

**_2. Missing values :_**
Columns with missing values were filled with NaN where appropriate. For categorical fields like weather, missing values were retained as NaN to indicate no recorded information. In numerical fields, values were converted to proper data types, and records with excessive missing data were reviewed.

**_3. Features :_**
Several new features were engineered to enhance the analysis. These include day of the week, time of day, stop duration category, whether the stop occurred on a weekend, and whether it was a vehicle interaction. Other features like total contacts per area and supervisor involvement were also derived to support further exploration. These new variables help in analyzing trends and behavior patterns.

**_4. Text Classification :_**
The contact_reason column, which contains text descriptions of why an interaction occurred, was processed using text classification techniques to categorize common reasons. To extract keywords from the "contact_reason" column and create a new column, used a keyword-based approach with regular expressions. Define categories with associated keywords, match them against the text, and assign all relevant categories to each record. This method transforms the detailed narratives into concise, actionable reasons, enabling you to produce graphs and explore correlations effectively.

### **_Dataset 4 : Overtime Details_**

**_1. Consolidation :_**

The dataset consisted of multiple duplicate columns for the same information (ID, officer names, ranks) spread across 66 original columns. Columns were consolidated by priority order, with multiple ID columns merged into a single Employee_ID field with 100% coverage, reducing to 28 columns while preserving key information.

**_2. Missing values :_**

Missing values were prevalent across multiple fields. The most critical field (officer identification) was addressed by consolidating four different ID columns (ID, Emp_No, Emp. ID, IDNO6) with coverage rates ranging from 3.4% to 73.8%, resulting in a combined field with 100% coverage.

**_3. Datatypes :_**

Temporal data including overtime_date was interpreted as "Object" datatype. These columns were converted to datetime format to enable extraction of year, month, and day components for time-based analysis. Additionally, the rank field showed mixed datatypes with numerical ranks (3.0-9.0) averaging 400-500 hours versus text ranks (Ptl, Det, Sergt) averaging only 4-5 hours, indicating inconsistent coding systems.

## Outlier Detection :

### **_Dataset 1 : Operating Budgets_**

![alt text](Plots/Outlier.png)

InterQuartile Range (IQR) was used to detect the outliers. Each of the numerical feature columns 3rd Quartile and 1st Quartile were obtained and then the values exceeding the quartile and the IQR*1.5 combined were identified. Post that, Manual eyeballing of the data to confirm if indeed the presented values were outliers was used. 

### **_Dataset 2 : Employees Earnings Data_**

![alt text](./Plots/OutliersEmployees.png)

Similarly, for the second dataset the same approach was followed using IQR. This process was followed for the numerical features, and was also only used for entries which did not contain 0 values, as many columns had a large amount of rows which were 0. No extreme outliers had been identified that had to be removed or adapted.

### **_Dataset 3 : Field Interrogation and Observation_**

![alt text](./Plots/outliers_violin.png)

I used violin plot as it combines a box plot and a density plot, showing the distribution, median, quartiles, and outliers. The width represents data frequency, while whiskers and points outside indicate outliers. Unlike box plots, it visualizes skewness and multiple peaks, providing a clearer view of data spread. This makes it ideal for detecting outliers and understanding distribution patterns in dataset.

### **_Dataset 4 : Overtime Details_**

![alt text](Plots/yearly_avg_hours.png)

The yearly breakdown shows significant variation:<br/>

2012-2013: Very low average hours (around 5-6 hours)<br/>
2014-2017: High average hours (up to 581 hours)<br/>
2018-2022: Moderate but still significant hours (350-527 hours)<br/>

The script found only 16 outliers (0.003% of the sample), with the highest being 1800 hours, mostly associated with overtime type "C" (which appears to be a standard code) and "Z".

## Visualization and Insights :

### **_1: Operating Budgets_**

Boston Police Department has undergone varying shifts between the years 2022 and 2025. While the overall budget has indeed increase between the given time frames, there are certain expense categories and intra-department allocations that have experienced significant fluctuations and changes. 



**_1. General Trends :_**

The overall budget has increased from 2022 to 2025 for most of the departments. This suggests an increased emphasis on most of the department activities. The increase has been seen on various expense categories ranging from equipments to personnel across which the trend is overall increasing however with notable fluctuations.

The below diagram highlights the increase/decrease in budgets across departments between 2022-2025 (X-axis Scaled 0-1)

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

The below diagram highlights the increase/decrease in budgets across departments between 2024-2025 (X-axis Scaled 0-1)

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


### **_4: Field Interrogation and Observation_**

**_1. Frequency of Primary Reasons:_**

The bar chart of primary reasons reveals that "Drug-Related" stops dominate the dataset, followed by "Traffic Violation" and "Weapons violation." This suggests a strong focus on drug enforcement within BPD’s FIO activities, with over half of all interactions potentially linked to narcotics. Less frequent reasons like "Warrant Check" or "Prostitution" indicate targeted rather than routine policing efforts. The distribution highlights resource allocation priorities, with drug-related issues as a central concern.

![alt text](./Plots/Fio_Primary_Reason.png)

**_2. Summons Issued by Primary Reason:_**

The stacked bar chart shows that "Drug related" stops have the highest summons issuance rate, often exceeding 30%, due to clear legal violations. In contrast, "traffic violation" stops, despite their frequency, result in fewer summons—less than 20%—suggesting observation or investigation over immediate enforcement. The reamining issues rarely leads to summons, indicating these stops are precautionary. This variation reflects differing enforcement strategies across reasons.

![alt text](./Plots/Summons_Issued.png)

**_3. Time of Day Patterns:_**

The bar chart of time-of-day patterns indicates that "Night" stops are the most common, comprising nearly 40% of interactions, likely tied to nightlife or low-visibility conditions. "Evening" and "Afternoon" follow, with "Morning" stops being the least frequent, under 15%. This suggests heightened police activity during darker hours, possibly targeting drug or disorderly conduct issues. The pattern underscores temporal resource deployment in BPD operations.

![alt text](./Plots/time_of_day_stops.png)

**_4. Vehicle Type Involvement:_**
The bar chart of vehicle types shows "SUV (Sport Utility Vehicle)" and "Passenger car (Sedan)" as the most frequently involved, each accounting for over 30% of vehicle-related stops. "Pickup" and "Van" appear less often, under 10% combined, reflecting common vehicle ownership in the area.This distribution suggests a focus on typical civilian vehicles rather than specialized ones.

![alt text](./Plots/top10_vehicletypes.png)

**_5. Top 10 cities by fio stops:_**
The top 10 cities by FIO stops are dominated by Boston and its neighborhoods, with Boston itself leading at over 13,000 stops, followed by Dorchester and Roxbury with 5,467 and 3,234 stops, respectively. This concentration reflects higher police activity in densely populated urban areas, likely tied to crime hotspots or population density. Neighborhoods like Jamaica Plain and East Boston, with 903 and 836 stops, show significant but lower activity, suggesting varied enforcement focus. The prevalence of urban areas in the top 10 aligns with the dataset’s urban/suburban classification, emphasizing BPD’s focus on city-center interactions.

![alt text](./Plots/top10_city_stops.png)

**_6.Primary Reason Trends Over Time:_**
The stacked area plot tracks reasons over months, showing "Traffic violations" stops consistently leading, with periodic spikes (eg: mid-2020) suggesting targeted operations. "Drug related" peaks intermittently, possibly tied to seasonal campaigns, while "Suspicious Behavior" remains steady but lower. Fluctuations in less common reasons like "Warrant Check" indicate sporadic enforcement focus. This temporal view reveals evolving policing priorities over the dataset’s timeframe.

![alt text](./Plots/Primary_Reason_trends.png)

### **_5: Overtime Details_**

**_1. Monthly Overtime Payments by Year:_**

This line graph shows the month-by-month overtime payment patterns across three consecutive years. 2020 shows extreme volatility with peaks in January and October and dramatic drops in April and November. 2021 had its highest payments in March (~$33 million), while 2022 shows generally lower, more stable payment patterns with less variation between months.

![alt text](Plots/monthly_overtime_by_year.png)

**_2. Overtime Budget vs. Actual Payments :_**

This bar chart compares budgeted overtime amounts against actual expenditures across three years. In 2020 and 2021, actual overtime payments significantly exceeded budgeted amounts by approximately $40 million each year, indicating consistent underbudgeting. By 2022, this pattern reversed, with actual payments coming in under budget, suggesting improved budget planning or reduced overtime utilization.

![alt text](Plots/budget_vs_actual.png)

**_3. Distribution of Overtime Hours Worked:_**

This histogram reveals a bimodal distribution of overtime hours with two distinct peaks. The highest frequency occurs at very low hours (0-50), representing over 150,000 instances, while a second significant cluster appears between 450-750 hours. This pattern suggests two different overtime usage behaviors: occasional/minimal overtime for most personnel versus a substantial subset working extensive overtime hours.

![alt text](Plots/hours_distribution.png)





### **_6: Responsive Record_**
1. Data Information :

There are 2229 details of police officers with 1457 white officers followed by 485 black officers. There are only 308 female officers in comparision to 1921 male officers. The dataset is highly imbalanced and must be taken into consideration before modeling.

2. Datatypes :

Numerical columns contain hourly values and the categorical values contain job title, union code, ethnic group and sex.

**Are certain officers more likely than others to have lower worked-to-paid ratios?**


![image](https://github.com/user-attachments/assets/961256c5-5700-40bb-9886-e6c3fa9723b1)

White and Black officers are more likely to earn higher paid to worked ratios than asian and hispanic officers. The reason for it being more white and black officers are at higher positions. With respect to male and female officers, they earn the same on average. The pay of student officers is an anomaly with them earning signifficantly less for an hour when compared to other officers. Supn In Chief, Bureau Admin and Technology, Bureau of Professional Standards, Bureau of Professional Development, Night Commands earn the most per hour with them over $100/hr. Hispanic officers work over 160 hours more than White officers for an year. This could be a direct effect of more white officers being at higher level when compared to Hispanic officers.

![image](https://github.com/user-attachments/assets/ccafbcd4-bb1e-4269-8a9e-92ea6e730731)

Number of hours per month worked is higher for the same officers that get paid the highest with them working under 165 hrs/month with the rest working at the rate of 170 hrs/month.

## Modelling :


 ### 1: Overtime Prediction

 One of the questions we wanted to answer was given previous overtime data, can we predict the amount of overtime paid for the next year and how does this prediction compare with the budget allocation for the BPD?

Firstly, overtime prediction for the following year as well as the total earnings prediction for the following year which will be compared with the budget of the BPD for 2025. For this problem, we relied on 3 different models to give us 3 different predictions and to choose a optimal range to report. Due to having limited data, only from the years 2011 to 2024, this does give us many data points to use for predictions, thus 3 models were chosen to ensure that are results can be seen as reasonably accurate. 

 These models consisted of a simple linear regression model, and two time series models. The first time series, [Prophet](https://facebook.github.io/prophet/), developed by Meta, is based on a additive model where non-linear trends are fit for data. The second time series model we chose to fit, was Holt-Winters. Since we are wworking with time series data, the train/validation and test split had to be sequential. The years 2011-2021 was chosen as training data, 2022-2023 as validation, and then 2024 as test data. Finally, after the model is trained, a future prediction will be made on the year 2025 which will be compared to the budget. 

 The modelling results and plots can be seen below. For Linear Regression and Holt Winters, there were no hyperparameters to be tuned and the validation set wasn't used. For Pophet, hyperparameter optimization was run to find the optimal hyperparameters of the model. These included finding the hyperparameters for the prior values as well as the type of seasonility. A gridsearch was performed and the parameters with lowest validation MAE was chosen as the final parameters. 
 
 As we can see from the model performance, Prophet had the lowest mean absolute error on our validation set, but Holt Winters performed better than Prophet and LR on the test set. From these models, we can see the forecasted total overtime for 2025 is between $95 million and $100 million. 

| Metric                              | Linear Regression       | Prophet                                                                                     | Holt-Winters       |
|-------------------------------------|-------------------------|---------------------------------------------------------------------------------------------|--------------------|
| Validation MAE (2022–2023)            | $3,356,105.65           |  $3,348,817.53    | $8,036,913.93      |
| Test MAE (2024)                     | $11,469,111.15          | $11,396,486.70         | $5,593,698.32      |
| Forecasted Overtime for 2025        | $95,294,581.17          | $95,334,902.95                                                                              | $101,764,065.97    |

<img src="Plots/LROvertime.png" width="300"/> <img src="Plots/ProphetOvertimeHyper.png" width="300"/> <img src="Plots/holtwintersOvertime.png" width="300"/>


Since Prophet performed the best on the validation set, we also plotted a 95% confidence interval for the future prediction, to give a range of values the model predicts with a 95% certainty that the overtime will be in that range for the year 2025. For the 95% confidence interval range, the values range from $86 million to $104 million. This value range also agrees with the other 2 models we used while predicting a single value, so we can assume this will be a reasonably accurate prediction for 2025. Although the prediction of our test case from 2024 falls outside the 95% confidence interval range, as mentioned in the previous data exploration section this was an anomaly and we believe this will still be accurate for 2025. 

TODO: Compare with budget from Yuri.

![alt text](Plots/ProphetCI.png)






