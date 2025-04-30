# -*- coding: utf-8 -*-
"""
##################################################
#
# QMB 6315: Python for Business Analytics
#
# Name: Gabriel Baradel
#
# Date: 4/29/2025
#
##################################################
#
# Sample Script for Final Examination:
# Obtaining Data from a Database
# and Building Predictive Models
#
##################################################
"""

##################################################
# Import Required Modules
##################################################

import os 
import sqlite3

import pandas as pd 
from sklearn.linear_model import LogisticRegression
import numpy as np
import statsmodels.formula.api as smf 
import statsmodels.api as sm 

import matplotlib.pyplot as plt  
import seaborn as sns 
sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)


##################################################
# Set up Workspace
##################################################



print(os.path.dirname(os.path.realpath(__file__)))

os.chdir(os.path.dirname(os.path.realpath(__file__)))


os.getcwd()




##################################################
# Question 1: Connect to a Database
#     and Obtain Applications Data
##################################################


#--------------------------------------------------
# a. Connect to the database called customers.db
#     and obtain a cursor object.
#--------------------------------------------------


con = sqlite3.connect("customers.db") # Code goes here

cur = con.cursor() # Code goes here


#--------------------------------------------------
# b. Submit a query to the database that obtains
#    the sales data.
#--------------------------------------------------

query_1 = """
SELECT income, homeownership, purchases, credit_limit
FROM Applications;
"""
print(query_1)
cur.execute(query_1)

#--------------------------------------------------
# c. Create a data frame and load the query
#     results into a dataframe.
#--------------------------------------------------

# Code goes here
purchase_app = pd.DataFrame(cur.fetchall(), columns=["income", "homeownership", "purchases", "credit_limit"])
purchase_app["homeownership"] = purchase_app["homeownership"].astype("category")

# Could use a loop with a pd.concat() command.


# Describe the contents of the dataframe to check the result.
purchase_app.describe()

purchase_app.columns



#--------------------------------------------------
# Fit a regression model to check progress.
#--------------------------------------------------

reg_model_app = smf.ols(formula = 
                           "purchases ~ income + C(homeownership) + credit_limit", 
                           data=purchase_app).fit()


# Display a summary table of regression results.
print(reg_model_app.summary())




##################################################
# Question 2: Obtain CreditBureau Data
##################################################




#--------------------------------------------------
# a. Submit a query to the database that obtains
#    the Application data joined with CreditBureau data.
#--------------------------------------------------

query_2 = """
        SELECT a.income, a.homeownership, a.purchases, a.credit_limit,
        b.fico, b.num_late, b.past_def, b.num_bankruptcy
        FROM Applications a
        JOIN CreditBureau b ON a.ssn = b.ssn;
        """
print(query_2)
cur.execute(query_2)




#--------------------------------------------------
# b. Create a data frame and load the query
#     results into a dataframe.
#--------------------------------------------------



# Code goes here
purchase_app_bureau = pd.DataFrame(cur.fetchall(), columns=[
    "income", "homeownership", "purchases", "credit_limit",
    "fico", "num_late", "past_def", "num_bankruptcy"]) 

# Could use a loop with a pd.concat() command.



# Describe the contents of the dataframe to check the result.
purchase_app_bureau.describe()
purchase_app_bureau.columns



#--------------------------------------------------
# Fit another regression model.
#--------------------------------------------------

reg_model_app_bureau = smf.ols("""
                     purchases ~ income + C(homeownership) + credit_limit +
                    fico + num_late + past_def + num_bankruptcy
                    """, data=purchase_app_bureau).fit()


# Display a summary table of regression results.
print(reg_model_app_bureau.summary())




##################################################
# Question 3: Obtain Demographic Data
##################################################



#--------------------------------------------------
# a. Submit a query to the database that obtains
#    the Application data joined with CreditBureau data.
#    and then joined with the Demographic data.
#--------------------------------------------------

query_3 = """
        SELECT a.income, a.homeownership, a.purchases, a.credit_limit,
       b.fico, b.num_late, b.past_def, b.num_bankruptcy,
       d.avg_income, d.density
        FROM Applications a
        JOIN CreditBureau b ON a.ssn = b.ssn
        JOIN Demographic d ON a.zip_code = d.zip_code;
        """
print(query_3)
cur.execute(query_3)




#--------------------------------------------------
# b. Create a data frame and load the query.
#--------------------------------------------------



# Code goes here
purchase_full = pd.DataFrame(cur.fetchall(), columns=[
    "income", "homeownership", "purchases", "credit_limit",
    "fico", "num_late", "past_def", "num_bankruptcy",
    "avg_income", "density"])

# Could use a loop with a pd.concat() command.



# Check to see the columns in the result.
purchase_full.describe()

purchase_full.columns


#--------------------------------------------------
# Fit another regression model.
#--------------------------------------------------

reg_model_full = smf.ols("""
                 purchases ~ income + C(homeownership) + credit_limit +
                 fico + num_late + past_def + num_bankruptcy +
                  avg_income + density
                """, data=purchase_full).fit()


# Display a summary table of regression results.
print(reg_model_full.summary())



##################################################
# Question 4: Advanced Regression Modeling
##################################################

#--------------------------------------------------
# Parts a-c with utilization.
#--------------------------------------------------


# Create a variable for credit utilization.

# Code goes here.




#--------------------------------------------------
# Fit another regression model.
#--------------------------------------------------


# Code goes here.




#--------------------------------------------------
# Parts a-c with log_odds_util.
#--------------------------------------------------


# Create a variable for credit utilization.

purchase_full["utilization"] = purchase_full["purchases"] / purchase_full["credit_limit"]
print(purchase_full["utilization"].describe())


#--------------------------------------------------
# Fit another regression model.
#--------------------------------------------------


reg_utilization = smf.ols("""
    utilization ~ income + C(homeownership) + fico + num_late +
    past_def + num_bankruptcy + avg_income + density
""", data=purchase_full).fit()
print(reg_utilization.summary())



purchase_full["log_odds_util"] = purchase_full["utilization"] / (1 - purchase_full["utilization"])
purchase_full["log_odds_util"] = purchase_full["log_odds_util"].apply(lambda x: np.nan if x <= 0 else np.log(x))
print(purchase_full["log_odds_util"].describe())


reg_log_odds_util = smf.ols("""
    log_odds_util ~ income + C(homeownership) + fico + num_late +
    past_def + num_bankruptcy + avg_income + density
""", data=purchase_full).fit()
print(reg_log_odds_util.summary())







##################################################
# Commit changes and close the connection
##################################################


# The commit method saves the changes. 
# con.commit()
# No changes were necessary -- only reading.

# Close the connection when finished. 
con.close()

# Then we can continue with this file when you have time
# to work on it later.



##################################################
# Extra code snippets
##################################################

# In case things go wrong, you can always drop the table
# and start over:
# cur.execute('DROP TABLE Applications')
# cur.execute('DROP TABLE CreditBureau')
# cur.execute('DROP TABLE Demographic')

# This can get the schema of the table,
# cur.execute("PRAGMA table_info('Applications')").fetchall()
# cur.execute("PRAGMA table_info('CreditBureau')").fetchall()
# cur.execute("PRAGMA table_info('Demographic')").fetchall()
# which states the names of the variables and the data types.


##################################################
# End
##################################################
