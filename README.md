# CS-506

This is the project repository for CS 506: Computational Tools for Data Science

## DESCRIPTION

The Police Overtime project for Spring 2025 conducts an extensive investigation into the Boston Police Department's financial expenses through an evaluation of overtime cost registration and allocation. The BPD handles an annual budget worth more than $400 million which requires detailed examination of its financial distributions. This research examines police financing patterns while investigating inefficiencies that may occur through overtime remunerations within budgetary frameworks. The project establishes financial transparency for law enforcement operations because policing remains exposed to sensitive political influences.

The analysis dedicates substantial time to studying overtime payments along with other aspects of police payroll. The research will examine both base compensation and overtime pay while investigating any time discrepancy between recorded work hours and received payments as it affects different officer groups depending on their rank and time in service and background demographics. The research utilizes historical data from 2011 to 2023 and makes projections about future overtime spending up until and beyond 2024. Statistical analysis combined with visualization tools allows the project to demonstrate whether overtime utilization delivers useful results or provides a cover for unneeded expenses.

The study gathers information from three primary data points which consist of employee earnings reports and BPD field activity records together with the City of Boston’s operating budget data. A geospatial data analysis through Python, Power BI and ArcGIS will process and visualize the information to reveal essential insights. We as a team will issue three main deliverables consisting of both statistical reports and visualized displays that present overtime spending patterns in the police force. Stakeholders including policymakers and advocacy organizations will use the obtained findings to make informed choices focusing on budget allocating and oversight capabilities.

The project promotes additional studies on extension topics that analyze systemic inequalities in police departments as well as environmental and political dimensions of police vehicle idling and funding sources. Research findings will achieve public transparency while directing policy decisions to establish equal public safety funding governance.

## Goals

Budget Analysis Goals

1. Year-Over-Year Budget Trends:

   - Analyze how the Boston Police Department (BPD) budget has changed annually, identifying key growth or reduction areas.
   - Examine overall and intra-departmental shifts in funding allocations.

2. Interdepartmental Funding Shifts:
   - Assess how funding has shifted between BPD and other city departments over time, such as reallocations to public health, education, or community programs.

Payroll and Compensation Goals

3. Paycheck Trends:

   - Evaluate changes in BPD paychecks year-over-year, comparing average salaries with non-BPD Boston city employees.
   - Breakdown pay structures into regular pay, overtime pay, and other components (e.g., detail pay, bonuses).

4. Overtime Cost Predictions:

   - Predict future overtime expenditures using historical data and compare these forecasts with budget allocations for the upcoming fiscal year.

5. Injury Pay Analysis:
   - Quantify the portion of BPD officer pay attributed to injury claims and calculate the percentage of officers receiving injury pay annually.

Overtime Efficiency Goals

6. Worked vs. Paid Overtime Discrepancies:

   - Compare overtime hours worked versus paid to identify financial discrepancies year-over-year.
   - Calculate the financial impact of these discrepancies on the department's budget.

7. Demographic Analysis of Overtime Ratios:

   - Investigate whether specific demographics (e.g., race, age, gender, tenure, or rank) are associated with lower worked-to-paid overtime ratios.

8. Outlier Detection in Overtime Ratios:
   - Analyze the distribution of overtime worked versus paid ratios to identify outliers and patterns that may indicate inefficiencies or misconduct.

Deliverables and Insights

9. Visualization and Reporting:

   - Create detailed visualizations (e.g., charts, graphs) to support findings on budget trends, payroll analysis, and overtime discrepancies.
   - Provide actionable insights for stakeholders to improve budget transparency and efficiency.

10. Policy Recommendations:
    - Develop evidence-based recommendations for optimizing resource allocation within BPD.
    - Suggest reforms to address inefficiencies in overtime spending and promote equitable compensation practices.

## Data

The data used in this project is collected and provided by the City of Boston. As the nature of this project is to determine how the Boston Police Department distributes its money, especially related to overtime, these are the datasets and data dictionaries that will be used in the project.
[Employees Earnings Data](https://data.boston.gov/dataset/employee-earnings-report), [Payroll Categories](https://data.boston.gov/dataset/employee-earnings-report/resource/609a6014-5ab0-49d9-8c38-1389e7bf0d41), [Boston Police Department's Field Interrogation and Observation (FIO) program](https://data.boston.gov/dataset/boston-police-department-fio), [BPD Roster](https://drive.google.com/drive/u/1/folders/1WKuP3SyeyBEHhnNi1O8e6vXMTk3cmaCj),[Overtime details](https://drive.google.com/drive/folders/1MCvI3iUbNnPE3an9tLKMfshEGwOvv52o) and [the entire operating budget of the city of Boston](https://data.boston.gov/dataset/operating-budget). All these datasets were provided in the Spark Project outline.

This dataset contains all government employees' earnings for the City of Boston. We are specifically interested in the earnings of the employees of the Boston Police Department (BPD), to evaluate how the BPD spends their funds. A data dictionary is also provided explaining the different payment types of the BPD, and how overtime and regular pay are calculated. Another dataset contains the records from the Boston Police Department's Field Interrogation and Observation (FIO) program. This program documents interactions between police officers and individuals, including stops, observations, and interrogations, which can be relevant as to when overtime is paid and for which reason to certain individuals. Finally, a dataset containing the overtime details is provided, to help with analysis and inference.

These datasets will be explored and cleaned for our use case. During the project's duration, new datasets can be added or existing datasets can be removed if necessary.

## Modeling

Modeling is a crucial part of the data processing pipeline to extract meaningful insights from clean and pre-processed data. It helps us to better understand and predict current and future trends based on past information. We plan on doing the following:

1. To identify trends that are not stationary and it's dependence on features, we plan on using variations of ARIMA that explain trends over time

2. We plan on using correlation analyses to identify how one factor might affect or depend on another

3. Statistical analysis ( ex t-test ) based feature selection for modeling and grouping the data based on significance.

4. Linear Regression ( Lasso and Ridge ) to fit current trends and apply it to future data.

5. Decision trees and Random Forests to model decisions where explainability is key.

6. Principal and Canonical Component analysis to understand variability in the features.

7. Outlier Detection by observing clusters in the data that may point to inefficiencies or misconduct.

By using different types of models (SVC, Logistic Regression, LSTM, Gradient Boosting, Model Stacking) where appropriate improving the metrics of prediction ( Accuracy, f1, precision, recall, ROC-AUC ) depending on the situation. Cross Validation would be done to ensure the model is robust on multiple seeds.

This would be done across multiple tools including python, seaborn and powerBI.

## Visualization

The need for visualization is paramount for this project. Visualization is one of the key steps as it helps us quickly identify any outliers, patterns, and information of significance.

We aim to use a mixture of tools for visualization. This includes, but is not limited to, native Python libraries such as Seaborn, dedicated visualization tools like Tableau, and using an external repo to keep track of the experimentation. The latter part focuses more on the visualization of the modeling experiments.

Our primary objective would be to uncover patterns, and for this, we may involve a multitude of plots such as box plots, violin plots, scatter plots, and more. The former (box plots) would be crucial to our analysis in figuring out what sort of outliers exist. Detecting the presence of outliers would be essential as it would help us uncover abnormalities and anomalies within the dataset. Standard plotting methodologies like scatter plots, pie charts, line charts, and the likes of it can be used to visualize the dependency of multiple features against each other.

For example:

1. We could utilize a department-wise plotting of overtime pay. This could be achieved with the help of a bar plot.
2. Another approach would be to check the percentage of overpayment given to various buckets of regular pay. This could be achieved with the help of a pie chart.

Overall, our objective of uncovering insights and patterns remains paramount, and we aim to identify interesting trends within the dataset.

## Test Plan

We aim to perform testing in a multitude of ways to prevent both bias and overly optimistic predictions. We approach the testing process as a multi-step procedure.

1. To analyze the effectiveness of overtime payments, one approach that could be deployed during the testing process is to derive an actual figure concerning the expected overtime payments. The prediction process could be conducted separately for each department to prevent the introduction of outliers and to avoid the strain of one model attempting to capture patterns across all departments. By utilizing this testing methodology, we can capture the differences in payments and assess their significance.
2. The testing process will not follow a standard 80-20 or 60-30-10 split. Instead, it will continuously utilize historical data to predict future information in segments. For example, we may use the last two months of data to predict two weeks into the future and repeat the process iteratively. Part of the testing phase experimentation will involve evaluating how well a mixture of experts model performs compared to a single model for all data. We aim to use metrics that capture discrepancies, such as MSE (which penalizes larger errors). MSE is particularly relevant since larger payment discrepancies correspond to higher financial losses.
3. Beyond the supervised training phase, we also plan to utilize unsupervised methodologies like clustering. This will help us understand the various natural groupings within the dataset and determine if these clusters correlate with other feature distributions. The testing aspect of this will involve assessing the quality of clustering, which can be easily measured using metrics like the silhouette score.

The testing phase is a crucial part of our project, as it dictates the overall quality of the output and the confidence in the deliverables we aim to present.
