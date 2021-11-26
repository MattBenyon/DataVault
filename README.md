# Group 9 Data Warehousing project
Version correct to 26/11/2021

# Table of contents
1. [Introduction](#introduction)
2. [Instructions](#instructions)
    1. [Creatting a PostgreSQL user and database](#instructions1)
3. [Another paragraph](#paragraph2)

## Introduction <a name="introduction"></a>


## Instructions <a name="instructions"></a>
The following content is instructions to execute the python scripts for this project succesfully

### Creatting a PostgreSQL user and database <a name="instructions1"></a>

To create the database, the user MUST execute the follwing commands in the PostgreSQL shell. (PostgreSQL is available at https://www.postgresql.org/download/)

`CREATE USER <username> WITH PASSWORD '<pasword>' CREATEDB;` where the username and password are the choice of the user.

`CREATE DATABASE G09_DATA_VAULT1;`

Once this has been completed, the DBMS is ready for the scripts to be ran.

### Preparing your python environment to run the code <a name="instructions2"></a>

This project was developed on Python Version 3.8. While other versions may work, it is recomended to use this version to avoid any issues.

Python 3.8 is avaiable at: https://www.python.org/downloads/release/python-380/



##  Instructions for getting the project to run on your machines.

1. Open PostgreSQL shell, create a user called g09 with password g09, grant user permissions.

2. Create a database called v4_test.

3. Download Python scripts to your project file. Your directory needs to look like the below:

![Screenshot](https://raw.githubusercontent.com/MattBenyon/DataVault/main/Screenshot%202021-11-10%20135209.png)

4. Make sure that you have pip'd to your environment the following:

	- easygui
	- psycopg2
	- pandas
	- numpy
	- plotly
	- hashlib


4. Run main.py by either entering details into gui or by commenting out gui section and uncommenting variables below it

5. Let it run, it will take approx. 15 minutes, sorry.

6. Run D1_dashboard, press on the IP address and it will pop up

## To do:

1. Dataset 1 JSON strings are a little wrong so they need fixing
2. Dataset 2



