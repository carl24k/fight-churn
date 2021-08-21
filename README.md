# fight-churn

<a name="top"/>

This is code for the book "***Fighting Churn With Data: Science and strategy for keeping your customers***"; the book serves as a detailed guide to the code.  You can get more information at:

- https://www.manning.com/books/fighting-churn-with-data, the publisher (Manning Publications)'s page for the book
- http://www.fightchurnwithdata.com, the author's blog site
- https://www.twitch.tv/carl24k_datascience, the author's live stream

This page contains the most up to date setup instructions, as well as information about some extra code that is mentioned in the book.

**Setup Instructions**  
[1 Getting Started](#start)  
[1.1 Prerequisites](#prereq)    
[1.2 Development Environment Setup](#devenv)      
[1.2.1 Database Setup](#createdb)      
[1.2.3 Jupyter Notebook Setup](#notebook)      
[1.2.4 Command Line Setup](#command)      
[1.3 Data Creation / Loading](#data)  
[2 Running Book Code Listings](#examples)  
[2.1 Running a Listing](#runlist)  
[2.2 Configuring How Listings are Run](#conflist)  

[Developers IDE Setup](readme_files/idea.md)

[Extras](readme_files/extras.md)


---
<a name="start"/>

## 1 Getting Started

Note from the author: These are basic startup/setup instructions that I think should work for most people using either shell Python, Jupyter Notebook, or an IDE, on either Mac or Windows.  I also want to apologize in advance because I am neither an expert in PostgreSQL nor an expert in Python, but I am about to give a lot of advice on how to setup and use these technologies - if you find I am not doing things the best way, or just not how you would have done it, please be patient.  Same goes for the rudimentary state of some of the code - I'm doing the best I can with the time I've got.  If you want to make things better please help help out! :)


---
---

<a name="prereq"/>

### 1.1 Prerequisites


Required:
* 12 Gb free disk space for the simulation data
* Python 3 and the required packages (requirements.txt)
* PostgreSQL

Recommended:
* PgAdmin - for PostgreSQL database setup
* PyCharm (Community Edition)   OR  Jupyter Notebooks - for running Python programs
  * If you have never used Python before (or used Python and never used Jupyter) then start with the PyCharm because it is an all GUI set up process. Jupyter instructions are provided below for those who are already familiar with it.

---
#### 1.1.1 Python 3
If you need help installing Python 3, you can refer to this page for Mac:
* https://docs.python-guide.org/starting/install3/osx/

For Windows there are resources here:
* https://www.python.org/downloads/windows/

(If you are on linux I'm going to assume you know how to install your own python...)

##### Note about Python and Package versions

Nearly all of the code for Fighitng Churn With Data should run with any Python 3.x version and all common package versions.

The only packages used that have version dependencies are the `xgoost` and and `shap` packages introduced in the later listings of chapter 9. These packages contain recent updates and  may only be compatible with versions of Python later than 3.9, at the time of this writing. *Note `xgboost` has other installation issues on Windows and Mac platforms, as described below in the section "Installing Virtual Environment and Requirements"*.

Please create an issue in the repository if you find any other instances of package or version incompatibilities.

##### Python IDE

I also recommend installing an Integrated Development Environment like PyCharm. PyCharm 
**Community Edition** was used by the author to write and run
all the code for the book, so this README will include how to setup PyCharm (this is especially useful if you 
are new to Python, since an IDE can take care of some of the setup for you...)

* https://www.jetbrains.com/pycharm/download

---
#### 1.1.2 PostgreSQL
To install PostgreSQL for Mac following these instructions:

* https://postgresapp.com/downloads.html

To install PostgreSQL for Windows, use :

* https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

(That page has a different Mac installer if you don't like Postgresapp.)

For both Mac and Win, I also recommend installing installing pgAdmin to make it easier to import and export
data, and run adhoc queries.  Follow the instructions  here:

* https://www.pgadmin.org/download/

For Mac you should make sure Posgres is running - here's what it looks like if you installed with
PostgresApp on a Mac:

![Postgres Running on Mac](./readme_files/postico.png)

For Windows, I have not yet figured out how to make sure Postgres is running, but I also have not yet had a
problem with it not running (please notify me if you have something to contribute on either subject.)

---
---

<a name="devenv"/>

### 1.2 Development Environment Setup

Before you can load data or run the code you have to do some setup on your system. If you never have 
done this before it may seem like a lot of work, and it kind of is, but this amount of setup is routine
when you begin to work with a new technology.  If already know how to do this sort of thing feel free
to ignore my instructions, which are primarily written for beginners to use GUI tools to get up and
running.

---
<a name="createdb"/>

#### 1.2.1 Creating a Database

The first thing you might need to do is connect to your local server (when I do this on Mac this is necessary;
on Windows, the connection to the localhost server was already present by default.)
If you don't already see `localhost` under the Servers tree in Pgadmin,  control (right)
clicking on the root of the Servers tree and selecting *Create*

![Connect to Server in PgAdmin](./readme_files/pgadmin_connect.png)

A dialog will open. Assuming you are working on a PostgreSQL database installed on your own computer then  
in the first tab (*General*) name your connection `localhost`, and on the second tab (*Connection*) enter the
address `127.0.0.1` (which is the IP address to connect to a database locally.) You should also enter your
user name and password.  So your dialog should look like the one below - then hit *Save*.

![Connect to Server in PgAdmin](./readme_files/pgadmin_connect_details.png)


Next you need to create a new database to hold all of the churn data schemas you create.
You will probably create multiple schemas as you work on the examples in the book and/or your own
data so this will help keep these organized.  An easy way to create a database is in PgAdmin - right click
on the *Databases* node under *localhost* in the tree:

![Create Database in PgAdmin](./readme_files/pgadmin_createdb1.png)

And enter the name of the new database (I used churn, but you can use whatever you want - just make the
appropriate settings in your environment variable, section 1.2.2.3 below):

![Name the database](./readme_files/pgadmin_createdb2.png)


---
<a name="notebook"/>

#### 1.2.3 Jupyter Notebook Setup

These instructions assume you already have Jupyter Notebooks installed. If you don't then you can consider the resources at https://jupyter.org/install. 

##### 1.2.3.1 Installing Packages Under Jupyter

1. launch a Jupyter  notebook from the project root directory. It should look like the view shown below : 

   ![note1_start](./readme_files/note1_start.png)
1. Start a new notebook from here (new button on the upper right...)

   ![note2_new](./readme_files/note2_new.png)
1. To install the required packages, run `pip install -r requirements.txt`

   ![note3_pip](./readme_files/note3_pip.png)

##### 1.2.3.2 Opening the Notebook & Setting the environment variables

1. Change the current directory to `data-generation/py`

2. ![note4_listdir](./readme_files/note4_datagen.png)

3. Open the Notbook `churn_db_sim.ipnyb`

4. In the second cell, change the environment variables to match the database, username and password that you have created...

   ![note5_environ](./readme_files/note5_environ.png)
   
5. Run the first two cells to set the environment variables. You will need to re-run these cells every time you re-open the notebook, and the similar notebook that you use to run the listings.

6. The first program to run, which will create the required database tables, is in the next cell of the notebook - this is explained in more detail below in section 1.3.1.

------

------



<a name="command"/>

#### 1.2.4 Running From the Command Line

If you are not using PyCharm of course you can run all this code from a terminal shell. You will need
to manually setup a Python virtual environment with the required packages, and  set a few environment variables.

---

##### 1.2.4.1 Installing Virtual Environment and Requirements

In either Windows or Mac/Linux you should setup a virtual environment following the 
instructions at pythong.org:

https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

Then change to the repository folder ```fight-churn``` and install the requirements with:

```
pip install -r requirements.txt
```

The command for installing requirements is further documented on the same page at python.org.

**NOTE:** The precise version of packages required may vary on different systems and in the future.
What is in the requirements is mostly non-specific but you may need to tailor it to your system.

__**Windows XG-Boost Warning:**__ At the time of this writing there have been problems reported 
 installing the xgboost package on  Windows: https://discuss.xgboost.ai/t/pip-install-xgboost-isnt-working-on-windows-x64/57.
If you are unable to install xgboost with pip, then you can try to install using the instructions
  outlined in that link. Alternatively, you can remove that requirement - note that you can
still run all the code in the book except for the 2nd half of chapter 9 without xgboost.

__**Mac XG-Boost Warning:**__ At the time of this writing there have been problems reported 
 installing the xgboost package on recent versions of  Mac OS: https://stackoverflow.com/questions/61971851/getting-this-simple-problem-while-importing-xgboost-on-jupyter-notebook
If you are unable to install xgboost with pip, try performing the Lib OMP installation described above first. Alternatively, you can remove the xgboost requirement - note that you can
still run all the code in the book except for the 2nd half of chapter 9 without xgboost.

---

##### 1.2.4.2 Mac/Linux Command Line Environment Variables
The environment variables are specific to these programs and contain information need to access the
databse. You should add a few lines like this in your `.bash_profile` or `.bashrc` file on Mac/Linux 
(or whatever is appropriate for the shell you use, but I will show this for bash because it seems to be the most common...)

```
export CHURN_DB=your_db
export CHURN_DB_USER=your_user
export CHURN_DB_PASS=your_password
```

Make sure to open a new terminal or source the `.bashrc` script after making the changes.  You will also
need to add the code folders you want to run from the project to your `PYTHONPATH` environement variable;
note that because the code (particularly the examples) add code from packages defined in other directories
you really need to add these paths (it is not sufficient to simply run the script from the directory it is in.)

The rest of the README is written for people using PyCharm, but you can always run the same commands
illustrated from the terminal...

---


##### 1.2.4.3 Windows Command Line Environment Variables
If you are using Windows, you will need to setup the enviornment variables in the Advanced System Preferences.
To make a long story short, you will need to end up with settings looking like this screenshot, but with 
the correct database, username and password for your setup:

![Windows Environment Variables](./readme_files/win_envvar.png)

The rest of the README is written for people using PyCharm, but you can always run the same commands
illustrated from the terminal...

---
---

<a name="data"/>

### 1.3 Data Loading / Creation

To run any of the code in the book you need to get some data loaded into your database.
There are two types of data you need:

1. Subscriptions (or the equivalent) for purchase of the product
1. Customer Behavior Events using the product

For more detailed information about what the data has to look like you can see these on-line
resources:
* [Subscription Data (and Churn Calculation)](http://fightchurnwithdata.com/how-to-calculate-churn-with-sql/)
* [Event Data (and Metric Calculation)](http://fightchurnwithdata.com/user-metrics-101/)

 Or, see Chapter 2 (for Subscriptions) and Chapter 3 (for Events) in the book. 
 For setup purposes (the focuse here) there are two options for getting this kind of data:

1. You already have data of your own - this is the option for anyone who already works on an online product or service
1. You can generate a simulated data set from a random model - this is the option for most students or people doing this for training purposes 

Note that unfortunately there is no publicly available *real* data at this time. Subscription and
customer data like this tends to be very sensitive information for the companies that hold it
and so far there are no offers of data that can be made publicly available. (**If you have
such data that you would be willing to make publicly available please contact the author.**)

---
#### 1.3.1 Schema Creation

Regardless of where you get your data from, you need to create the database schema and tables that it
to hold it.  There is a python script in the folder *data-generation* for this.  If you have been
following the instructions above then you have already made a Run Configuration for the script in
PyCharm, or prepared the Jupyter notebook `churn_db_sim.ipnyb`.  There's just one more thing to do: name the schema that you will create.

1. Open the file *data-generation/py/churndb.py*
1. Edit the schema name in the file to the name you want
    1. If you are loading your own data, name it whatever you want
    1. If you are generating simulated data, leave it set to the name **socialnet7** which is the default model for simulation
1. Run the script using PyCharm or a Jupyter Notebook, as described above.

If everything works as planned you should see something like the following output:

```
/Users/user_name/fight-churn-master/venv/bin/python /Users/user_name/fight-churn-master/data-generation/py/churndb.py
Creating schema test (if not exists)...
Creating table event (if not exists)
Creating table subscription (if not exists)
Creating table event_type (if not exists)
Creating table metric (if not exists)
Creating table metric_name (if not exists)
Creating table active_period (if not exists)
Creating table observation (if not exists)

Process finished with exit code 0
```


A new schema and tables were created in your PostgreSQL database, which you can confirm by looking
in PgAdmin:

![PgAdmin Churn Schema Tables](./readme_files/pgadmin_create_schema.png)

If you made it this far then congratulations!  You just ran your first bit of the fight-churn code.

---
#### 1.3.2 Generating Simulated Data

If you don't have your own data to analyze then you should use the simulator program to create a 
realistic (enough) simulation of subscription, churn and event data for you to run the book code examples on.
Code for generating artificial data to run the code is in the directory `data-generation`.  In
the near future there will be a blog post explaining how the simulation works, and the instructions
here are limited to simply running the simulation.

*  For *PyCharm*, follow the instructions in section 1.2.2.4 and duplicate and modify the run configuration for `data-generation/churndb.py` (which you ran above) to make a *new* run configuration  for the script `data-generation/churnsim.py` (which you are about to run.)  
*  For *JupyterNotebooks* you should have already run the first 3 cells of the notebook `churn_db_sim.ipynb`. The simulation command is in the 4th cell of the notebook: `run churnsim.py`

If this is your first time following these instructions, just run it.  You should start to see output like this:

```
/Users/user_name/fight-churn-master/venv/bin/python /Users/user_name/fight-churn-master/data-generation/py/churnsim.py
Matrix is not positive semi-definite: Multiplying by transpose

Creating 10000 initial customers for 2019-01-01 start date
Simulated customer 0: 5 subscription, 10243 events @ 2019-05-21 06:00:01.611085
Simulated customer 1: 5 subscription, 10076 events @ 2019-05-21 06:00:01.805228
Simulated customer 2: 5 subscription, 11501 events @ 2019-05-21 06:00:02.034017
Simulated customer 3: 5 subscription, 11643 events @ 2019-05-21 06:00:02.250260
Simulated customer 4: 5 subscription, 9869 events @ 2019-05-21 06:00:02.433102
...

```

There will be more like this and the whole process will take from around 10-30 minutes depending on the speed of your
system (**so this may be a good time to go for a coffee break, lunch, nap, etc.**.) Please pardon the delay,
 but the program is simulating the subscriptions, behavior and churn of more than 10,000 customers over 6 months time. The results of the simulation are  all inserted into the  database tables `subscription` and `event`. (There is no data for churns yet : you will derive that as part of the  analysis process described in the book chapters 2 and 4.)  You can (and should) confirm the results of the data  simulation by querying the database directly, and you don't have to wait for the simulation to complete (so this is  actually a good next step to take while you are waiting...)

```
churn=# select count(*) from socialnet7.subscription;
 count 
-------
  52048
(1 row)

churn=# select count(*) from socialnet7.event;
  count  
---------
 34198616
(1 row)

churn=# 

```

Those are examples of what the numbers will look like when the simulation is over; yours won't look exactly like that,
 because its a random simulation and the results are different every time.  But it should be a similar overall number.
 If you check the count midway through it will be less of course.
(If you don't know how to launch a SQL prompt on your launch the PostgreSQL app and double click on
the database.  Mine doesn't actually launch the terminal directly, but it points in the right direction....)


![Mac PostgreSQL terminal launch](./readme_files/mac_launch_psql_terminal.png)


Great!  Now you have the data you need to run the code and learn the techniques in the book.

---
#### 1.3.3 Loading Your Own Data (If you have it)

If you have your own data that you want to analyze then you need to load it into the `subscription` and 
`event` tables of the churn analysis schema. I will outline the basic steps here, but I'm going to assume
that if you work in an organization that has its own churn data to analyze then either you know how to
export and import the data already (probably better than I could tell you), or you can get support from
someone else in your oganization.  That said, for those of you have your own data but don't have a better
 resource to turn to for how to load it, the process you will follow is:

* Export the data from your equivalent of a `subscription` table. If you use Zuora to track your subscriptions, this
is actually the `rate_plan_charge` object.  If you use Salesforce, this is may be the `Opportunity` table (where the
opportunity was won.)   Each subscription record must have an account identifier, a start date 
and a price, quoted in Monthly Recurring Revenue (MRR).  Terminated (churned) subscriptions must have the end date.  
If you have other fields in the churn analysis subscription table (product name, units and quantity, billing frequency) 
then you can export these as well, or else export a NULL in those positions (which will make the import simpler.)
Follow the order in the churn analysis subscription table:
    1. id : integer
    1. account_id : integer
    1. product : text
    1. start_date : date
    1. end_date : date
    1. mrr : double
    1. quantity : double
    1. units : text
    1. bill_period_months : integer

* Export the data from your equivalent of an `event` table, and from whatever table names the event types (assuming
  there is a code name table separate from the event table.  Every event must have an account identifier, a timestamp,
  and a type.  The required fields for the events are:
    1. id : integer
    1. event_time : timestamp
    1. event_type_id : integer
* You can and should also export whatever additional data fields you have for your events that you think
are important (amounts viewed or consumed, prices, content categories, etc.) Start by updating the the event table
schema in `data-generation/schema/create_event.sql` and recreate the table including your fields (You will have to 
drop the existing table that you created in step 1.3.1.)

If you know how to import and export PostgreSQL data using the command line then have it.  Personally I did 
it with the PgAdmin Import/Export GUI, which you launch by command clicking (right clicking) with your mouse on the
listing for the table you want to import into:


![Mac PostgreSQL terminal launch](./readme_files/mac_launch_psql_terminal.png)

[(top)](#top)  

---
---
---

<a name="examples"/>

## 2 Running the Code from the Book Listings

You can run the book listings with the python script `listings/py/run_churn_listing.py`.

* This script reads SQL and Python source code, and either
binds variables (for SQL) or passes parameters (for Python) and executes the code.  
* The code (listings from the book) are in the folders `chapN` under the listings directory.
* Exactly what listings to run and what parametes are used are set in JSON files in the directory `listings/conf`.

So you can use this utility as you go through the book - if you want to actually run the code
from any listing on your local database, this is the easiest way to do it.

[(top)](#top)  

---

<a name="runlist"/>

### 2.1 Running a Listing

* For *PyCharm*, start by making a Run Configuration for the script `listings/py/run_churn_listing.py`, 
  following the instructions in Section 1.2.2.4 (duplicate and modify one of your old configurations.)

* For a *Jupyter Notebook*  change to the folder `listings/py` and use the notebook  `run_churn_listing.ipnyb`. Set the environment variables in the 2nd cell, as described above sin  Section 1.2.3.2. The comand to run a listing is in the 3rd cell.

The script is preset to run the first code listing, listing 2.1 from chapter 2, for the
simulated data set `socialnet7`.  If you have created a simulated dataset named `socialnet7` as described
in section 1.3.2 you can run your configuration as is and you should see a result like this:

```
/Users/user_name/fight-churn/venv/bin/python /Users/user_name/fight-churn/listings/py/run_churn_listing.py

Running chap2 listing listing_2_1_net_retention
SQL:
----------
set search_path = 'socialnet7'; with 
date_range as (    
	select  '2019-03-01'::date as start_date, '2019-04-01'::date as end_date
), 
start_accounts as    
(
	select  account_id, sum (mrr) as total_mrr    
	from subscription s inner join date_range d on
		s.start_date <= d.start_date    
		and (s.end_date > d.start_date or s.end_date is null)
	group by account_id    
),
end_accounts as    
(
	select account_id, sum(mrr) as total_mrr      
	from subscription s inner join date_range d on
		s.start_date <= d.end_date    
		and (s.end_date > d.end_date or s.end_date is null)
	group by account_id    
), 
retained_accounts as     
(
	select s.account_id, sum(e.total_mrr) as total_mrr     
	from start_accounts s 
	inner join end_accounts e on s.account_id=e.account_id  
	group by s.account_id    
),
start_mrr as (    
	select sum (start_accounts.total_mrr) as start_mrr from start_accounts
), 
retain_mrr as (    
	select sum(retained_accounts.total_mrr) as retain_mrr 
from retained_accounts
)
select 
	retain_mrr /start_mrr as net_mrr_retention_rate,    
	1.0 - retain_mrr /start_mrr as net_mrr_churn_rate,    
	start_mrr,    
	retain_mrr
from start_mrr, retain_mrr

----------
RESULT:
Record(net_mrr_retention_rate=0.96039603960396, net_mrr_churn_rate=0.0396039603960396, start_mrr=1008.99, retain_mrr=969.030000000001)

Process finished with exit code 0
```

The first line shows you what chapter and listing are being run.  Next it shows the SQL being run (this is a SQL
listing).  The final line prints out the result - the net retention rate, calculated with the SQL.  Because the data
was randomly simulated your result on the last line won't be exactly the same as that one, but it should be similar.

One way you  can change what the script will run for by simply editing the constants in the "main" portion 
**at the bottom of the file**.  Note these variables:

* `schema` : the name of the churn data schema to run on
* `chapter` : the chapter to run a listing from
* `listing` : the number of the listing to run

The most common thing you will do is run a different listing on the same schema and chapter, so you would edit this line:

`--listing=1`

to whatever listing you want. So for example, to run listing 2.2 you can change the variable to:

`--listing=2`

Alternatively, the script accepts command line parameters.  To run this way, provide the following three parameters 
(all required) and it will use those instead of the hard coded constants:

1. The first command line parameter is the schema
1. The second command line parameter is the chapter number
1. The third command line parameter is the listing number 

**Note:**
If you want to run listings from the command line, you also need to setup your Python virtual environment
and add the listing code paths to your PYTHONPATH (meaning, set them up the old fashioned way - not using PyCharm.)  
Command line setup is not covered in this README at this time (but if you want to add such instructions please contribute!)

You can also set command line arguments in PyCharm, in the Run Configurations setup dialog. (But IMHO changing the command 
line arguments in the configuration dialog is more tedious than simply editing them script for this type of use...)

To see what listings are available to run, peruse the code in the chapter folders below `listing`.  But note that your
schema must be *configured* to run each listing, as described in the next  section.  The `socialnet7` (default) schema
has entries created for it already, but if you want to run the code on your own data you will need to enter your own 
configuration.

[(top)](#top)  

---

<a name="conflist"/>

### 2.2 Configuring How Listings Run

Your schema must be *configured* to run each listing.  The `socialnet7` (default) schema
has entries created for it already, but if you want to run the code on your own data you will need to enter your own 
configuration. Also if you want to change how the listings are run on `socialnet7` this section will explain how to do it.

The configuration files are all in folder `listings/conf` and each schema has a configuration file that must have a name
that is `<schema_name>_listings.json`.  So the configuration for the `socialnet7` data set is in the file `socialnet7_listings.json`.
The configuration his a JSON with the following structure:

1. The top level are keys for the chapters, "chap2", "chap3", etc.
1. The next level is a set of objects representing each listing in the chapter
    * The key for each object is the listing name, beginning with "listing_<chapter>_<number>"
    * The values for each object are parameters that apply to running that listing.  
      There are a few possible types of parameters.
        1. Variables which are substituted in SQL, or passed as values to python functions
        1. Control parameters (described more below)
1. There is a special object of chapter default parameters in each chapter, with the key `params`. The defaults for the 
chapter will automatically be applied to every listing -  parameters specified in each listing are override the
defaults.

As mentioned, there are two special control parameters which are are *not* parameters of the listing:
1. `type` : must be either `sql` or `python` and controls how the listing is executed
1. `mode` : controls how the result of the program is handled:
    * `mode=run` : A SQL expected to return no results (like an insert)
    * `mode=one` : A SQL expected to return one result, print it
    * `mode=top` : A SQL expected to return many results, print the first 5 lines
    * `mode=save`: A SQL expected to return many results, save the result in a csv file

Below is an example of the beginning of the listing configuration for the `socialnet7` simulated data set:

```
	"chap2" : {
		"params" : {
			"%from_yyyy-mm-dd": "2019-03-01",
			"%to_yyyy-mm-dd": "2019-04-01",
			"mode" : "one",
			"type" : "sql"
		},
		"listing_2_1_net_retention" : {
		},
		"listing_2_2_churn_rate" : {
		},
		...
```

The following summarizes the configuration:
*  `listing_2_1_net_retention` and `listing_2_2_churn_rate` are enabled
* Both listing will run with the parameters shown in the `params` section: 
    * The strings for start and from date and to date in the queries will be set as shown
    * The listings are SQL
    * The listings will print one result

(More to come on running Python listings when Chapter 5 is released...) 

[(top)](#top)  

---
---






---
---



---
---

## Authors

* **Carl Gold** [carl24k](https://github.com/carl24k)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details




[(top)](#top)  
