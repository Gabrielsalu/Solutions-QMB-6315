#!/usr/bin/python
"""
##################################################
# 
# QMB 6315: Python for Business Analytics
# 
# Using Databases with SQLite3
# 
# Lealand Morin, Ph.D.
# Assistant Professor
# Department of Economics
# College of Business Administration
# University of Central Florida
# 
# April 12, 2025
# 
# Sample Program for Assignment 3
# 
##################################################
"""


##################################################
# Import Modules.
##################################################


import os # To set working directory
import pandas as pd # To read and inspect data

import sqlite3 # To pass SQL queries to a database


##################################################
# Set Working Directory.
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



##################################################
# Python Commands and SQL Queries
##################################################

#--------------------------------------------------
### Question 1: Population, Area and Population Density 
###     of US States and Territories
#--------------------------------------------------

# In this example, we will create a table 
# to store the population and land area of the states and
# territories of the United States. 


# a. Create a new database called population.db.

# You would import some kind of API 
# to interact with the database
# We will continue using sqlite3
import sqlite3 as dbapi
con = dbapi.connect('population_USA.db')



# b. Make a database table called Density that will 
# hold the name of the state or territory (TEXT), 
# the population (INTEGER), 
# and the land area (REAL). 


cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Density (State TEXT,
    Population INTEGER, Area REAL)''')
con.commit()


# c. Insert the data from the table above. 

# The hard way, which we did in class:
# table = [
#  ('Alaska', 123, 45678),
#  ...
#  ('Wyoming', 123, 45678),
# ]

# The easy way:


density_df = pd.read_csv('US_state_pop_area.csv')

# Take a look at the individual types of columns in the data frame.
density_df.dtypes


# Inspect a few rows of data.
density_df.head(3)
density_df.tail(3)

# Check the dimensions of the data.
density_df.index
density_df.columns

# Loop through the rows of the dataframe to INSERT the VALUES.
for row in density_df.index:
   cur.execute('INSERT INTO Density VALUES (?, ?, ?)', 
               (str(density_df['state_terr'][row]), 
                int(density_df['population'][row]), 
                float(density_df['area'][row]) ))
con.commit()



#--------------------------------------------------
# Fill in the following queries.
#--------------------------------------------------

# d. Retrieve the contents of the table.

cur.execute('SELECT * FROM Density')
for row in cur.fetchall():
 print(row)


# e. Retrieve the populations. 

cur.execute('SELECT Population FROM Density')
for row in cur.fetchall():
 print(row)



# f. Retrieve the states that have populations of less than one million. 


cur.execute('SELECT State FROM Density WHERE Population < 1000000')
for row in cur.fetchall():
 print(row)


# g. Retrieve the states that have populations of less than one million
# or greater than five million. 


cur.execute('SELECT State FROM Density WHERE Population < 1000000 OR Population > 5000000')
for row in cur.fetchall():
 print(row)


# h. Retrieve the states that *do not* have populations of less than one million
# or greater than five million. 


cur.execute('SELECT State FROM Density WHERE Population BETWEEN 1000000 AND 5000000')
for row in cur.fetchall():
 print(row)




#--------------------------------------------------
### Example 2: Population of Capital Cities
#--------------------------------------------------

# Now add a new table called Capitals to the database. 
# Capitals has three columns: 
# state/territory (TEXT),
# capital (TEXT), and population (INTEGER). 

# We are continuing from above
# but if we started another session, 
# we would have to reopen and reconnect to the database.
# import sqlite3 as dbapi
# con = dbapi.connect('census.db')
# cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS Capitals")
cur.execute('''CREATE TABLE Capitals(State TEXT,
 Capital TEXT, Population INTEGER)''')
con.commit()

# Load the table from a spreadsheet.

capitals_df = pd.read_csv('US_cap_cities_pop.csv')
    
# Take a look at the individual types of columns in the data frame.
capitals_df.dtypes


# Inspect a few rows of data.
capitals_df.head(3)
capitals_df.tail(3)

# Check the dimensions of the data.
capitals_df.index
capitals_df.columns

# Loop through the rows of the dataframe to INSERT the VALUES.
for row in capitals_df.index:
 cur.execute('INSERT INTO Capitals VALUES (?, ?, ?)', 
               (str(capitals_df['state'][row]), 
                str(capitals_df['capital'][row]), 
                int(capitals_df['population'][row]) ))
con.commit()



# a. Retrieve the contents of the table. 


cur.execute('SELECT * FROM Capitals')
for row in cur.fetchall():
 print(row)


# b. Retrieve the populations of the states and capitals 
# (in a list of tuples of the form 
# [state_population, capital_population]). 

# INNER JOIN with WHERE clause
cur.execute('''SELECT Density.Population, Capitals.Population
 FROM Capitals INNER JOIN Density
 WHERE Capitals.State = Density.State''')
for row in cur.fetchall():
 print(row)


cur.execute('''SELECT State
 FROM Density''')
cur.fetchall()

cur.execute('''SELECT State
 FROM Capitals''')
cur.fetchall()

# INNER JOIN with ON clause
cur.execute('''SELECT Density.Population, Capitals.Population
 FROM Capitals INNER JOIN Density
 ON Density.State = Capitals.State''')
for row in cur.fetchall():
 print(row)

# Answer to j in the in-class example:

# LEFT JOIN with Capitals ON the LEFT table
cur.execute('''SELECT Density.Population, Capitals.Population
 FROM Capitals LEFT JOIN Density
 ON Density.State = Capitals.State''')
for row in cur.fetchall():
 print(row)

# LEFT JOIN with Density ON the LEFT table
cur.execute('''SELECT Density.Population, Capitals.Population
 FROM Density LEFT JOIN Capitals
 ON Density.State = Capitals.State''')
for row in cur.fetchall():
 print(row)


# Notice the None values for territories, 
# which are not listed in the other table. 


#--------------------------------------------------
# Fill in the following queries.
#--------------------------------------------------


# c. Retrieve the land area of the states whose capitals 
# have populations greater than 100,000. 

cur.execute('''SELECT Density.Area
 FROM Density
 JOIN Capitals ON Density.State = Capitals.State
 WHERE Capitals.Population > 100000''')
for row in cur.fetchall():
 print(row)



# d. Retrieve the states with land densities
# greater than ten people per square kilometer
# and capital city populations more than 500,000. 



cur.execute('''SELECT Density.State
 FROM Density
 JOIN Capitals ON Density.State = Capitals.State
 WHERE (Density.Population / (Density.Area * 2.58999)) > 10
 AND Capitals.Population > 500000
''')
for row in cur.fetchall():
 print(row)


# e. Retrieve the total land area of the USA. 


cur.execute('SELECT SUM(Area) FROM Density')
print(cur.fetchone())


# f. Retrieve the average population of the capital cities. 


cur.execute('SELECT AVG(Population) FROM Capitals')
print(cur.fetchone())


# g. Retrieve the lowest population of the capital cities. 


cur.execute('SELECT MIN(Population) FROM Capitals')
print(cur.fetchone())


# h. Retrieve the highest population of the states or territories. 

cur.execute('SELECT MAX(Population) FROM Density')
print(cur.fetchone())




##################################################
# Commit changes and close the connection
##################################################


# The commit method saves the changes. 
con.commit()


# Close the connection when finished. 
con.close()

# Then we can continue with this file when you have time
# to work on it later.



##################################################
# Extra code snippets
##################################################

# In case things go wrong, you can always drop the table
# and start over:
# cur.execute('DROP TABLE Density')
# cur.execute('DROP TABLE Population')

# This can get the schema of the table,
# cur.execute("PRAGMA table_info('Density')").fetchall()
# cur.execute("PRAGMA table_info('Capitals')").fetchall()
# which states the names of the variables and the data types.



##################################################
# End
##################################################
