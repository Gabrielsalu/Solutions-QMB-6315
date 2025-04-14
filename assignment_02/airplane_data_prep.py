# -*- coding: utf-8 -*-
"""
##################################################
#
# QMB 6315: Python for Business Analytics
#
# Name:
#
# Date:
#
##################################################
#
# Sample Script for Assignment 2:
# Manipulating Data
#
##################################################
"""

##################################################
# Import Required Modules
##################################################

import os
import pandas as pd
import statsmodels.api as sm

##################################################
# Set up Workspace
##################################################


# Find out the current directory.

os.getcwd()

# Get the path where you saved this script.
# This only works when you run the entire script (with the green "Play" button or F5 key).
print(os.path.dirname(os.path.realpath(__file__)))
# It might be comverted to lower case, but it gives you an idea of the text of the path. 
# You could copy it directly or type it yourself, using your spelling conventions. 

# Change to a new directory.

# You could set it directly from the location of this file
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Check that the change was successful.
os.getcwd()
# I got lower case output, even though my folders have some upper case letters.
# But anyway, it works.


##################################################
# Part a) Read Spreadsheet and Sales Data
##################################################

file_path = 'airplane_data.xlsx'

airplane_sales_df = pd.read_excel(file_path, sheet_name='airplane_sales')
print(airplane_sales_df.describe())


#--------------------------------------------------
# Fit a regression model.
#--------------------------------------------------

x = airplane_sales_df[['age']]
y = airplane_sales_df[['price']]
reg_model_sales = sm.OLS(y,x).fit()
print(reg_model_sales.summary())


##################################################
# Part b) Read Specification Data
##################################################



#--------------------------------------------------
# Join the two datasets together.
#--------------------------------------------------

airplane_specs_df = pd.read_excel(file_path, sheet_name='airplane_specs')
airplane_sales_specs = pd.merge(airplane_sales_df, airplane_specs_df, on='sale_id')

print(airplane_sales_specs.head())
print(airplane_sales_specs.describe())


#--------------------------------------------------
# Fit another regression model.
#--------------------------------------------------

x = airplane_sales_specs[['age','passengers','wtop','fixgear','tdrag']]
y = airplane_sales_specs[['price']]

reg_model_sales_specs = sm.OLS(y,x).fit()
print(reg_model_sales_specs.summary())


##################################################
# Part c) Read Performance Data
##################################################



#--------------------------------------------------
# Join the third dataset to the first two.
#--------------------------------------------------

airplane_perf_df = pd.read_excel(file_path, sheet_name='airplane_perf')
airplane_full = pd.merge(airplane_sales_specs, airplane_perf_df, on='sale_id')


#--------------------------------------------------
# Fit another regression model.
#--------------------------------------------------

x = airplane_full[['age','passengers','wtop','fixgear','tdrag','horse','fuel','ceiling','cruise']]
y = airplane_full[['price']]

reg_model_full = sm.OLS(y,x).fit()
print(reg_model_full.summary())

##################################################
# End
##################################################
