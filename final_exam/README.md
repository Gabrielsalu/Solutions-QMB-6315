# QMB6315: Python for Business Analytics
## Spring 2025

# Final Examination

 Save your scripts and materials in a folder called ```final_exam``` in your GitHub respository.

## Recommended model

Enter the summary statistics from your recommended model in the code block below.


```


                            OLS Regression Results
==============================================================================
Dep. Variable:          log_odds_util   R-squared:                       0.843
Model:                            OLS   Adj. R-squared:                  0.841
Method:                 Least Squares   F-statistic:                     329.8
Date:                Tue, 29 Apr 2025   Prob (F-statistic):          5.14e-192
Time:                        22:09:00   Log-Likelihood:                -894.93
No. Observations:                 500   AIC:                             1808.
Df Residuals:                     491   BIC:                             1846.
Df Model:                           8
Covariance Type:            nonrobust
============================================================================================
                               coef    std err          t      P>|t|      [0.025      0.975]
--------------------------------------------------------------------------------------------
Intercept                    4.1002      0.558      7.346      0.000       3.004       5.197
C(homeownership)[T.Rent]    -2.0981      0.143    -14.655      0.000      -2.379      -1.817
income                   -2.356e-05   3.37e-06     -6.996      0.000   -3.02e-05   -1.69e-05
fico                        -0.0029      0.001     -4.500      0.000      -0.004      -0.002
num_late                     1.0320      0.058     17.852      0.000       0.918       1.146
past_def                     1.7965      0.223      8.062      0.000       1.359       2.234
num_bankruptcy               3.2794      0.220     14.902      0.000       2.847       3.712
avg_income                 2.18e-06   5.75e-06      0.379      0.705   -9.12e-06    1.35e-05
density                      0.0012      0.000     10.207      0.000       0.001       0.001
==============================================================================
Omnibus:                      288.870   Durbin-Watson:                   1.987
Prob(Omnibus):                  0.000   Jarque-Bera (JB):             2461.365
Skew:                           2.423   Prob(JB):                         0.00
Kurtosis:                      12.729   Cond. No.                     7.60e+05
==============================================================================

```