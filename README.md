# Group 9 Data Warehousing project
Version correct to 26/11/2021 15:39

# Table of contents
1. [Introduction](#introduction)
2. [Instructions](#instructions)
    1. [Creating a PostgreSQL user and database](#instructions1)
    2. [Preparing the Python environment](#instructions2)
    3. [Populating the database](#instructions3)
    4. [Running data marts](#instructions4)
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

Required packages for this project:

- easygui
- psycopg2
- pandas
- numpy
- plotly

Please use `pip install <package name>` in your Python environment.

Warning: do not run the code without completing this step, it will not work!

### Populating the database <a name="instructions3"></a>

Before running any scripts, please ensure that you have pasted the correct folders for dataset 1 and 2 so that they REPLACE the folders as seen in the image below

![Screenshot](https://raw.githubusercontent.com/MattBenyon/DataVault/main/Screenshot%202021-11-10%20135209.png)


To populate the database, the user must run `main.py`. This ussually takes around 20-40 minutes to run depending on computer performance.


### Running data marts <a name="instructions4"></a>





