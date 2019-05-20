# fight-churn

This is code for the (forthcoming) book "Fighting Churn With Data: The
Subscribed Institute Guide to Data Driven Customer Engagement".  See
http://www.fightchurnwithdata.com for more information.


## 1 Getting Started

These are basic startup/setup instructions that I think should work for most people using a recent Mac.
I apologize that so far I have not had a chance to provide more detailed setup instructions for Windows,
but I will do so ASAP (and I would welcome contributions in this area.)   I also want to apologize in advance
because I am neither an expert in PostgreSQL nor an expert in Python, but I am about to give a lot
of advice on how to setup and use these technologies - if you find I am not doing things the best
way, or just not how you would have done it, all I can say is: (1) I'm doing the best I can; (2) This worked for me; and 
(3) I welcome your contributions! :)

### 1.1 Prerequisites

* Python 3 and the required packages (requirements.txt)
* PostgreSQL

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

#### 1.1.2 PostgreSQL
To install PostgreSQL for Mac following these instructions:

* https://postgresapp.com/downloads.html

I also recommend installing installing pgAdmin to make it easier to import and export 
data, and run adhoc queries.  Follow the instructions  here:

* https://www.pgadmin.org/download/

Make sure Posgres is running - here's what it looks like if you installed with PostgresApp on a Mac:

![Postgres Running on Mac](/readme_files/postico.png)

### 1.2 Development Environment Setup

Before you can load data or run the code you have to do some setup on your system. If you never have 
done this before it may seem like a lot of work, and it kind of is, but this amount of setup is routine
when you begin to work with a new technology.  If already know how to do this sort of thing feel free
to igonre my instructions, which are primarily written for beginners to use GUI tools to get up and
running.

#### 1.2.1 Creating a Database

You might want to create a new database to hold all of the churn data schemas you create. 
You will probably create multiple schemas as you work on the exmaples in the book and/or your own
data so this will help keep these organized.  An easy way to create a database is in PgAdmin - right click
on the *Databases* node under *localhost* in the tree:

![Create Database in PgAdmin](/readme_files/pgadmin_createdb1.png)

And enter the name of the new database:

![Name the database](/readme_files/pgadmin_createdb2.png)


#### 1.2.3 Create a PyCharm Project

After you have cloned this repository

1. launch PyCharm and go to the menu *File* / *New Project*
1. In the file section window, select the folder for the repo.  Leave it set to "Create New Virtual environment for htis project"
1. Click **Create**
1. It should say "The directory ... is not empty.  Would you like to create a project from existing sources?"  Click Yes

![Name the database](/readme_files/pycharm0_existing_sources.png)

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


#### 1.2.5 Installing Python Requirements

Now that you have created a Python project you can easily install the
required packages.  Start by opening the file requirements.txt in the root
project folder

#### 1.2.6 Creating Run Configurations and Setting Database Environment Variables

A lot of the python code depends on access to the database you created for the churn data.
You will set environment variables that will hold your database and login information, so that
it does not have to be hard coded.  The easiset way to do this in PyCharm is to
set environment variables when you create a Run Configuration for the executables.

Here is one example of creating a run configuration for one of the programs - 

![PyCharm Requirements](/readme_files/pycharm8_requirements.png)


For creating additiona configurations, note thatn PyCharm allows you to duplicate 
and modify each configuration.)


#### 1.2.7 Create Directories for Result Data



### 1.3 Data Loading / Creation

Code for generating artificial data to run the code is in the directory data-generation.  Details to come...


#### 1.3.1 Schema Creation

You will need to create a schema with the tables in the schema folder - 

#### 1.3.2 Loading Your Own Data (If you have it)

If you have your own data that you want to analyze... For details on the subscription data see
the blog posts on http://www.fightchurnwithdata.com for more information:

* [Subscription Data (and Churn Calculation)](http://fightchurnwithdata.com/how-to-calculate-churn-with-sql/)
* [Event Data (and Metric Calculation)](http://fightchurnwithdata.com/user-metrics-101/)

#### 1.3.3 Generating Random Data



## 2 Running the Code from Book Examples

You can run the book examples with the project under _examples_.  

```
python churn_example.py
```

Currently everything is hard coded.  If you want to run just one example or
chapter you can uncomment the variables *one_chapter* and/or *one_example*.
Command line parameters coming soon...


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

## Authors

* **Carl Gold** [carl24k](https://github.com/carl24k)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Coming soon
