# fight-churn

<a name="top"/>

This is code for the (forthcoming) book "Fighting Churn With Data: The
Subscribed Institute Guide to Data Driven Customer Engagement".  See
http://www.fightchurnwithdata.com for more information.

**Table of Contents**  
[1 Getting Started](#start)  
[1.1 Prerequisites](#prereq)    
[1.2 Development Environment Setup](#devenv)      
[1.3 Data Creation / Loading](#data)  
[2 Running Book Code Examples](#examples)  
[3 Metric Calculation Framework](#metrics)


---
<a name="start"/>

## 1 Getting Started

These are basic startup/setup instructions that I think should work for most people using a recent Mac.
I apologize that so far I have not had a chance to provide more detailed setup instructions for Windows,
but I will do so ASAP (and I would welcome contributions in this area.)   I also want to apologize in advance
because I am neither an expert in PostgreSQL nor an expert in Python, but I am about to give a lot
of advice on how to setup and use these technologies - if you find I am not doing things the best
way, or just not how you would have done it, please be patient.  Same goes for the rudimentary state
of some of the code - I'm doing the best I can with the time I've got.  If you want to make things
better please help help out! :)


---
---

<a name="prereq"/>

### 1.1 Prerequisites

* Python 3 and the required packages (requirements.txt)
* PostgreSQL

---
#### 1.1.1 Python 3
If you need help installing Python 3, you can refer to this page for Mac:
* https://docs.python-guide.org/starting/install3/osx/

For Windows there are resources here:
* https://www.python.org/downloads/windows/

(If you are on linux I'm going to assume you know how to install your own python...)

I also recommend installing an Integrated Development Environment like PyCharm. PyCharm 
**Community Edition** was used by the author to write and run
all the code for the book, so this README will include how to setup PyCharm (this is especially useful if you 
are new to Python, since an IDE can take care of some of the setup for you...)

* https://www.jetbrains.com/pycharm/download

---
#### 1.1.2 PostgreSQL
To install PostgreSQL for Mac following these instructions:

* https://postgresapp.com/downloads.html

I also recommend installing installing pgAdmin to make it easier to import and export 
data, and run adhoc queries.  Follow the instructions  here:

* https://www.pgadmin.org/download/

Make sure Posgres is running - here's what it looks like if you installed with PostgresApp on a Mac:

![Postgres Running on Mac](/readme_files/postico.png)

---
---

<a name="devenv"/>

### 1.2 Development Environment Setup

Before you can load data or run the code you have to do some setup on your system. If you never have 
done this before it may seem like a lot of work, and it kind of is, but this amount of setup is routine
when you begin to work with a new technology.  If already know how to do this sort of thing feel free
to igonre my instructions, which are primarily written for beginners to use GUI tools to get up and
running.

---
#### 1.2.1 Creating a Database

You might want to create a new database to hold all of the churn data schemas you create. 
You will probably create multiple schemas as you work on the exmaples in the book and/or your own
data so this will help keep these organized.  An easy way to create a database is in PgAdmin - right click
on the *Databases* node under *localhost* in the tree:

![Create Database in PgAdmin](/readme_files/pgadmin_createdb1.png)

And enter the name of the new database (I used churn, but you can use whatever you want - just make the
appropriate settings in your environment variable, section 1.2.6 below):

![Name the database](/readme_files/pgadmin_createdb2.png)


---
#### 1.2.3 Create a PyCharm Project

After you have cloned this repository

1. launch PyCharm and go to the menu *File* / *New Project*
1. In the file section window, select the folder for the repo.  Leave it set to "Create New Virtual environment for htis project"
1. Click **Create**
1. It should say "The directory ... is not empty.  Would you like to create a project from existing sources?"  Click Yes

![Name the database](/readme_files/pycharm0_existing_sources.png)

---
#### 1.2.4 Setup Python Project

You should create a Python "virtual environment" for the project (I won't try to go into details here,
but this allows you to install the packages used for the repo without interfering with anything else
on your system).  

In PyCharm, select from the menus:  *Pycharm*  / *Preferences...*  and go to the area for *Project*

![PyCharm Project Preferences](/readme_files/pycharm1_project_preferences.png)

If you click on the gear wheel to the right of where it says <No Interpreter> you have the option to add
a new one...

![PyCharm Add Intepreter](/readme_files/pycharm2_add_interpreter.png)

It will look something like this:

![PyCharm Interpreter Setting](/readme_files/pycharm3_interpreter_settings.png)

And after you click **Okay** it will take several seconds to create the virtual environment, and
then it should look like this:

![PyCharm After Create](/readme_files/pycharm4_after_create.png)

You will add more packages in a minute, but first finish with the project setup by going to the
*Project Structure* section of the preferences:


![PyCharm Project Structure](/readme_files/pycharm5_project_structure.png)

Select each folder that contains python source code, and click on the button *Sources*
(with the blue folder next to it):

![PyCharm Select One Source Folder](/readme_files/pycharm6_source_select.png)

You should select the following folders:
* churnalyze/py
* data-generation/py
* metric-framework/py
* examples/py
    * examples/chap5
    * examples/chap6
    * examples/chap7
    * examples/chap8
    * examples/chap9
    * examples/chap10
    * examples/chap11
    
When you are done your project preferences should look like this:

![PyCharm Source Folders Selected](/readme_files/pycharm7_sources_selected.png)

(At the time of creation of these instructions, later chapters have not been written.)

---
#### 1.2.5 Installing Python Package Requirements

Now that you have created a Python project you can easily install the
required packages.  Start by opening the file requirements.txt in the root
project folder

![PyCharm Requirements](/readme_files/pycharm8_requirements.png)

Notice that at the top it says: *Install requirements* - click on that and the click
**Install** in the dialog that comes up. Note that you have to be connected to the internet for
this to work, and it will take several minutes for all the packages to be downloaded 
and installed.


---
#### 1.2.6 Creating Run Configurations and Setting Database Environment Variables

A lot of the python code depends on access to the database you created for the churn data.
You will set environment variables that will hold your database and login information, so that
it does not have to be hard coded.  The easiset way to do this in PyCharm is to
set environment variables when you create a Run Configuration for the executables.

Here is one example of creating a run configuration for one of the programs: If you have not created
any Run Configurations yet, you start with the *Add Configuration* button...


![PyCharm Add Config](/readme_files/pycharm9_add_config.png)

In the Run/Debug Configuration dialog click the **+**  then **Python** to make a new python script configuration.


![PyCharm Python Config](/readme_files/pycharm10_new_python_config.png)

You will get an empty configuration, and the first thing to do is click on the Folder icon in the 
script path text box and pick the script path.  The first script everyone will need to run is 
*data-generation/py/churndb.py*, which creates a schema for an analysis.  After selecting this script, your
configuration should look like this, with both the script path and the working directory set to 
wherever the script is on your system:

![PyCharm Script Path](/readme_files/pycharm11_script_path.png)

The next step is to add the environment variables, by clicking on the *Browse* button at the end
of the environment variables text box:

![PyCharm Add Config](/readme_files/pycharm12_browse_environ.png)

That button launches a dialog to add the environment variables.  You need to add three:
1.  CHURN_DB  : the name of the database for your churn analysis schemas (step 1.2.1 above)
1.  CHURN_DB_USER : the user name to login to the database
1.  CHURN_DB_PASS : the password to login to the database

After setting these, your environment variable dialog should look something like this:

![PyCharm Add Config](/readme_files/pycharm13_environ_vars.png)

Select **OK** and save all the configuration changes.  I'll say more about running this script in the 
next section on Data Loading / Creation.

For creating additional Run configurations, note that PyCharm allows you to duplicate 
and modify an existing configuration.  So when you want to make another script with the same environment
variables open the Configuration Dialog, now by clicking on the run configuration drop down then selecting 
**Edit Configuration**


![PyCharm Add Config](/readme_files/pycharm14_edit_config.png)

Now choose to duplicate your existing Run configuration:

![PyCharm Add Config](/readme_files/pycharm15_copy_config.png)

This will make another configuration the same as the existing one - you can rename it and reset the 
path to a different script, keeping the environment variables you already setup.

One last thing: After creating the Run Configuration you actually run a script in PyCharm
using the little green arrow next to the Configuration drop down menu...

![PyCharm Run Script](/readme_files/pycharm16_run_script.png)

(The green bug next to the arrow runs it in debug mode...)

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

Note that unforatunately there is no publicly avaiable *real* data at this time. Subscription and
customer data like this tends to be very sensitive information for the companies that hold it
and so far there are no offers of data that can be made publicly available. (**If you have
such data that you would be willing to make publicly available please contact the author.**)

---
#### 1.3.1 Schema Creation

Regardless of where you get your data from, you need to create the database schema and tables that it
to hold it.  There is a python script in the folder *data-generation* for this.  If you have been
following the instructions above then you have already made a Run Configuration for the script in
PyCharm.  There's just one more thing to do: name the schema that you will create.

1. Open the file *data-generation/py/churndb.py*
1. Edit the schema name in the file to the name you want
    1. If you are loading your own data, name it whatever you want
    1. If you are generating simulated data, leave it set to the name **chunrsim2** which is the default model for simulation
1. Run the script using PyCharm, as described above

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

![PgAdmin Churn Schema Tables](/readme_files/pgadmin_create_schema.png)

If you made it this far then congratulations!  You just ran your first bit of the fight-churn code.

---
#### 1.3.2 Generating Simulated Data

If you don't have your own data to analyze then you should use the simulator program to create a 
realistic (enough) simulation of subscription, churn and event data for you to run the book code examples on.
Code for generating artificial data to run the code is in the directory `data-generation`.  In
the near future there will be a blog post explaining how the simulation works, and the instructions
here are limited to simply running the simulation.

* Create a run configuration for the script `data-generation/churnsim.py` following the instructions in
section 1.2.6.  

If this is your first time following these instructions, just run it.  You should start to see output like this:

```
/Users/user_name/fight-churn-master/venv/bin/python /Users/user_name/fight-churn-master/data-generation/py/churnsim.py
Matrix is not positive semi-definite: Multiplying by transpose

Creating 500 initial customers for 2019-01-01 start date
Simulated customer 0: 5 subscription, 10243 events @ 2019-05-21 06:00:01.611085
Simulated customer 1: 5 subscription, 10076 events @ 2019-05-21 06:00:01.805228
Simulated customer 2: 5 subscription, 11501 events @ 2019-05-21 06:00:02.034017
Simulated customer 3: 5 subscription, 11643 events @ 2019-05-21 06:00:02.250260
Simulated customer 4: 5 subscription, 9869 events @ 2019-05-21 06:00:02.433102
...

```

There will be more like this and the whole process will take a couple of minutes.  The program has simulated the
subscriptions, behavior and churn of a few hundred customers and inserted them into the database tables `subscription`
and `event`. (There is no data for churns yet : you will derive that as part of the analysis process described
in the book chapters 2 and 4.)  You can (and should) confirm the results of the data simulation by
 querying the database directly:

```
churn=# select count(*) from churnsim2.subscription;
 count 
-------
  2594
(1 row)

churn=# select count(*) from churnsim2.event;
  count  
---------
 5454701
(1 row)

churn=# 

```

Yours won't look exactly like that, because its a random simulation and the results are different every time.
But it should be a similar overall number.
(If you don't know how to launch a SQL prompt on your launch the PostgreSQL app and double click on
the database.  Mine doesn't actually launch the terminal directly, but it points in the right direction....)


![Mac PostgreSQL terminal launch](/readme_files/mac_launch_psql_terminal.png)


Nice work!  Now you have the data you need to learn the techniques in the book!

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


![Mac PostgreSQL terminal launch](/readme_files/mac_launch_psql_terminal.png)

[(top)](#top)  

---
---
---

<a name="examples"/>

## 2 Running the Code from Book Examples

You can run the book examples with the python script `examples/churn_example.py`.

* This script reads SQL and Python source code, and either
binds variables (for SQL) or passes parameters (for Python) and executes the code.  
* The code (listings from the book) are in the folders `chapN` under the examples directory.
* Exactly what examples to run and what parametes are used are set in JSON files in the directory `examples/conf`.

### 2.1 Running a Book Listing

Start by making a Run Configuration, following the instructions in Section 1.2.6.

The script is preset to run the first code example, listing 2.1 from chapter 2, for the
simulated data set `churnsim2`.  If you have created a simulated dataset named `churnsim2` as described
in section 1.3.2 you can run your configuration as is and you should see a result like this:


You modify what the script will run for by simply
changing the constants at the top of the file 
(a command line option system is on the to do list.)  Note these variables:

* `schema` : the name of the churn data schema to run on
* `one_chapter` : run only examples from this chapter, if specified.  Set to `None` for all chapters.
* `one_example` : run only the named example


### 2.2 Configuring listings to run

To see what examples are available to run you can peruse the 


[(top)](#top)  

---
---
---

<a name="metrics"/>


## 3 Calculating Metrics with the Framework

First you need to configure some metrics specifically for your event data in a
configuration file for your schema.  See the examples
_metric-example/conf/x_metrics.json_ where the "x" is replaced with your
schema name.  Then running _metrics.py_ in the metric-framework folder will 1)
truncate the metrics in the metric table and 2) insert new metrics defined by
whatever is in  the file _metric-example/conf/yourschema_metrics.json_.  

Currently everything is hard coded, so you *must* set the postgres connection string, the 
schema, and date range in the file.  

```
python metrics.py
```

If you want to run just one metric you can uncomment the variable
*one_metric*.   Note that when running one metric currently you need to take
care of deleting values yourself (if you find yourself running the same metric
again after changes.)

Command line parameters coming soon...


### Event QA

Details coming soon...


```
python event_qa.py
```

### Metric QA

Details coming soon...


```
python metric_qa.py
```
---
[(top)](#top)  

## Authors

* **Carl Gold** [carl24k](https://github.com/carl24k)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Coming soon
