# Sparkify Amozone s3 and redshift dwh ETL

## Details
A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. 
The analytics team is particularly interested in understanding what songs users are listening to. 
Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

---------------Your role is to create a database schema and ETL pipeline for this analysis-----------------------
### Data
- **Song datasets**: all json files are nested in subdirectories under */data/song_data*. A sample of this files is:

```{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}```

- **Log datasets**: all json files are nested in subdirectories under */data/log_data*. A sample of a single row of each files is:

```{"artist":"Slipknot","auth":"LoggedIn","firstName":"Aiden","gender":"M","itemInSession":0,"lastName":"Ramirez","length":192.57424,"level":"paid","location":"New York-Newark-Jersey City, NY-NJ-PA","method":"PUT","page":"NextSong","registration":1540283578796.0,"sessionId":19,"song":"Opium Of The People (Album Version)","status":200,"ts":1541639510796,"userAgent":"\"Mozilla\/5.0 (Windows NT 6.1) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"","userId":"20"}```

## Project structure
This project includes three script files, and one notebook:

1] create_table.py is where fact and dimension tables for the star schema in Redshift are created.
2] etl.py is where data gets loaded from S3 into staging tables on Redshift and then processed into the analytics tables on Redshift.
3] sql_queries.py where SQL statements are defined, which are then used by etl.py, create_table.py and analytics.py.
README.md is current file.

## Database schema design

# Staging Tables
    staging_events
    staging_songs
# Fact Table
    songplays 
# Dimension Tables
    users  
    songs 
    artists 
    time 
 
## Steps followed on this project

**- Create Table Schemas
-Design schemas for your fact and dimension tables
-Write a SQL CREATE statement for each of these tables in sql_queries.py
-Complete the logic in create_tables.py to connect to the database and create these tables
-Write SQL DROP statements to drop tables in the beginning of - create_tables.py if the tables already exist. This way, you can run create_tables.py whenever you want to reset your database and test your ETL pipeline.
-Launch a redshift cluster and create an IAM role that has read access to S3.
-Add redshift database and IAM role info to dwh.cfg.
-Test by running create_tables.py and checking the table schemas in your redshift database. You can use Query Editor in the AWS Redshift console for this.
-Build ETL Pipeline
-Implement the logic in etl.py to load data from S3 to staging tables on Redshift.
-Implement the logic in etl.py to load data from staging tables to analytics tables on Redshift.
-Test by running etl.py after running create_tables.py and running the analytic queries on your Redshift database to compare your results with the expected results.
-Delete your redshift cluster when finished.-**