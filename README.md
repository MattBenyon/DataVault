# DataVault
Version from 10/11/2021 @ 13:50

##  Instructions for getting the project to run on your machines 

1. Open PostgreSQL shell, create a user called g09 with password g09, grant user permissions

2. Create a database called v4_test

3. Download python scripts to your project file. Your directory needs to look like the below:

![Screenshot](https://raw.githubusercontent.com/MattBenyon/DataVault/main/Screenshot%202021-11-04%20112951.png)

4. Make sure that you have pip'd to your environment the following:

	- easygui
	- psycopg2
	- pandas
	- numpy
	- plotly
	- hashlib


4. Run main.py by either entering details into gui or by commenting out gui section and uncommenting variables
	below it

5. Let it run, it will take approx. 15 minutes sorry

6. Once that has completed, you can run GeneratePlot_D1.py and you should be able to generate plots for a specific
   patient, the treatment (eg Visual stimulus, motor stimulus) and the type of data (eg oxy, deoxy)

