

# fight-churn

<a name="top"/>

This is code for the book "***Fighting Churn With Data: Science and strategy for keeping your customers***"; the book serves as a detailed guide to the code.  You can get more information at:

- https://www.manning.com/books/fighting-churn-with-data, the publisher (Manning Publications)'s page for the book
- http://www.fightchurnwithdata.com, the author's blog site
- https://www.twitch.tv/carl24k_datascience, the author's live stream

This page contains the most up to date setup instructions, as well as information about some extra code that is mentioned in the book.

*WARNING TO PYPI USERS: None of the links or images in this document work on the pypi.org website! 
[To 
use the links in this README view it on github](https://github.com/carl24k/fight-churn/tree/20210605_packaging#fight-churn).*

**Quick Start Setup Instructions**  

Section 1 covers installing the pre-requisite software.

[0 Getting Started](#start)  
[1 Prerequisites](#prereq)  
[1.1 Python 3](#python)  
[1.2 Postgres](#postgres)  
[1.2.1 Database Setup](#createdb)  

Section 2 provides the fastest way to get started with the code, from a command line

[[2 Quickstart With Python Package](#package)  
[2.1 Create a virtual environment](#virtual)  
[2.2 Install the fightchurn package](#fightchurn)  
[2.3 Create a directory for output](#output)  
[2.4 Start the Python virtual environment](#startvirtual)  
[2.5 Import the run_churn_listing_module](#import)  
[2.6 Set the churn environment variables](#envvar)  
[2.7 Run the data simulation](#simulate)  
[2.8 Run code listings](#run)  

**Advanced Setup Instructions**  

 The following are  the "advanced" setup for people who are already accustomed to running Python in either a Jupyter Notebook or an Integrated Development Enivornment (IDE).

- [Jupyter Notebook Setup](readme_files/notebook.md)
- [Developers IDE Setup](readme_files/ide.md). ***Author's recommendation: If you are really going to use this code for anything it is recommended you take the time to do the IDE setup - this allow you to step through the code with a debugger, which is a great way to learn about it. Not to mention, if you are going to modify the code this is really required.***

There are also some extra code parts, which are partially documented on this page..

- [Extras](readme_files/extras.md)

*WARNING TO PYPI USERS: None of the links or images in this document work on the pypi.org website! 
[To 
use the links in this README view it on github](https://github.com/carl24k/fight-churn/tree/20210605_packaging#fight-churn).*


---
<a name="start"/>

## 0 Getting Started

Note from the author: These are basic startup/setup instructions that I think should work for most people using either shell Python, Jupyter Notebook, or an IDE, on either Mac or Windows.  I also want to apologize in advance because I am neither an expert in PostgreSQL nor an expert in Python, but I am about to give a lot of advice on how to setup and use these technologies - if you find I am not doing things the best way, or just not how you would have done it, please be patient.  Same goes for the rudimentary state of some of the code - I'm doing the best I can with the time I've got.  If you want to make things better please help help out! :)

Before you can load data or run the code you have to do some setup on your system. If you never have 
done this before it may seem like a lot of work, and it kind of is, but this amount of setup is routine
when you begin to work with a new technology.  If already know how to do this sort of thing feel free
to ignore my instructions, which are primarily written for beginners to use GUI tools to get up and
running.


---
---

<a name="prereq"/>

### 1 Prerequisites


Required:
* 12 Gb free disk space for the simulation data
* Python 3 and the required packages (requirements.txt)
* PostgreSQL

Recommended:
* PgAdmin - for PostgreSQL database setup
* PyCharm (Community Edition)   OR  Jupyter Notebooks - for running Python programs

---
<a name="pyton"/>

#### 1.1 Python 3

If you need help installing Python 3, you can refer to this page for Mac:
* https://docs.python-guide.org/starting/install3/osx/

Another good alternative for Mac is using Homebrew:

* To install homebrew see: https://brew.sh/
* For information on installing Python 3.9: https://formulae.brew.sh/formula/python@3.9

For Windows there are resources here:

* https://www.python.org/downloads/windows/

(If you are on linux I'm going to assume you know how to install your own python...)

##### Note about Python and Package versions

Nearly all of the code for Fighitng Churn With Data should run with any Python 3.x version and all common package versions.

The only packages used that have version dependencies are the `xgoost` and and `shap` packages introduced in the later listings of chapter 9. These packages contain recent updates and  may only be compatible with versions of Python later than 3.9, at the time of this writing. *Note `xgboost` has other installation issues on Windows and Mac platforms, as described below in the section "Installing Virtual Environment and Requirements"*.

Please create an issue in the repository if you find any other instances of package or version incompatibilities.

---

<a name="postgres"/>

#### 1.2 PostgreSQL

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
---

<a name="package"/>

## 2 Quickstart With Python Package


---

<a name="virtual"/>

### 2.1 Create a virtual environment

First, you should make a new virtual environment in which to install the Fight Churn code...

```shell
python3 -m venv <python_environment_name>
```

Use whatever you like for `<python_environment_name>` ; if you don't normally make python environments, call it "py_env". That command doesn't have any output. 

Next, your need to activate your environment:

```
~ user$ source churn_env/bin/activate
(py_env) ~ user$ 
```



<a name="fightchurn"/>

### 2.2 Install the fightchurn package

```shell
pip install fightchurn
```

This will lead to a lot of outputs, starting with something like this:

```shell
(py_env) MacBook-Yo:~ carl$ pip install fightchurn
Collecting fightchurn
  Using cached fightchurn-0.3.5-py3-none-any.whl (99 kB)
Collecting docutils==0.17.1
  Using cached docutils-0.17.1-py2.py3-none-any.whl (575 kB)
...
```

Your output probably will not say "Using cached..." unless you have already installed this before, so don't worry if yours looks a bit different than whats shown above. Regardless, after several minutes (depending on your system and internet connection) you should see this:

```shell
Successfully installed Pillow-8.1.2 Pygments-2.9.0 SQLAlchemy-1.4.3 bleach-3.3.0 build-0.4.0 certifi-2020.12.5 chardet-4.0.0 cloudpickle-1.6.0 colorama-0.4.4 cycler-0.10.0 docutils-0.17.1 fightchurn-0.3.5 greenlet-1.0.0 idna-2.10 importlib-metadata-4.5.0 joblib-1.0.1 keyring-23.0.1 kiwisolver-1.3.1 llvmlite-0.36.0 matplotlib-3.4.0 numba-0.53.1 numpy-1.20.2 packaging-20.9 pandas-1.2.3 patsy-0.5.1 pep517-0.10.0 pkginfo-1.7.0 postgres-3.0.0 psycopg2-binary-2.8.6 psycopg2-pool-1.1 pyparsing-2.4.7 python-dateutil-2.8.1 pytz-2021.1 readme-renderer-29.0 requests-2.25.1 requests-toolbelt-0.9.1 rfc3986-1.5.0 scikit-learn-0.24.1 scipy-1.6.2 shap-0.39.0 six-1.15.0 slicer-0.0.7 statsmodels-0.12.2 threadpoolctl-2.1.0 toml-0.10.2 tqdm-4.59.0 twine-3.4.1 urllib3-1.26.4 webencodings-0.5.1 xgboost-1.3.3 zipp-3.4.1
```

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

<a name="output"/>

### 2.3 Create a directory for output

You should make a local folder to store your output. On linux that would look as follows:

```shell
mkdir my_churn_output_folder
```

Naturally you can make your folder using the GUI if you are on Mac or Windows

<a name="startvirtual"/>

### 2.4 Start the Python virtual environment

Next you should start your Python environment, and enter a python shell:

```shell
source churn_env/bin/activate
python
```

You should see something like the following...

```shell
(py_env) :~ user$ python
Python 3.9.6 (default, Jun 29 2021, 05:25:02) 
[Clang 12.0.5 (clang-1205.0.22.9)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```



---

<a name="import"/>

### 2.5 Import the run_churn_listing_module

Next, you will import the `fightchurn` package that you will use to run everything:

```python
from fightchurn import run_churn_listing
```

That has no output, but it might take a few moments

<a name="envvar"/>

### 2.6  Set the churn environment variables

Now you need to set a few enviroment variables. These are:

1. The database name : 'churn' in the example below
2. The username for the database 
3. The password for the database
4. A local folder where  outputs can be written....


```python
run_churn_listing.set_churn_environment('churn','user','password','/path/to/my_churn_output_folder')
```

This will print out a confirmation line as follows:

```
Setting Environment Variables user=carl for db=churn
```

---

<a name="simulate"/>

### 2.7 Run the data simulation

Next, you need to write some data to the database in order to run the code against - no data is provided with the code distribution. Use the following command:


```python
run_churn_listing.run_standard_simulation(init_customers=10000)
```

The example is for a standard simulation of 10,000 customers. If you want to speed things up you can run it for 1000 customers and things will still work okay - the results will just be a bit more noisy and random.

You will see output as follows...

```shell
Creating schema socialnet7 (if not exists)...
Creating table event (if not exists)
Creating table subscription (if not exists)
Creating table event_type (if not exists)
Creating table metric (if not exists)
Creating table metric_name (if not exists)
Creating table active_period (if not exists)
Creating table observation (if not exists)
Creating table active_week (if not exists)
Creating table account (if not exists)

Creating 2000 initial customers for month of 2020-01-01
Simulated customer 0/2000: 2 subscriptions & 100 events
Simulated customer 100/2000: 448 subscriptions & 154,047 events
Simulated customer 200/2000: 872 subscriptions & 282,882 events
Simulated customer 300/2000: 1,324 subscriptions & 426,866 events
Simulated customer 400/2000: 1,767 subscriptions & 557,543 events
...
```

This will continue for a while - maybe 15-30 minutes if you ran the full 10,000 customer simulation.

<a name="run"/>

### 2.8 Run code listings

Now you are ready to run some code from the book! To do that you use the `run_listing` function that you previously imported. For examle, the following is chapter 2, listing 2:


```python
run_churn_listing.run_listing(2,2)
```

You should see output like this:

```
Running chapter 2 listing 2 churn_rate on schema socialnet7
SQL:
----------
set search_path = 'socialnet7'; with 
date_range as ( 
	select  '2020-03-01'::date as start_date, '2020-04-01'::date as end_date
), 
start_accounts as  
(
	select distinct account_id        
	from subscription s inner join date_range d on
		s.start_date <= d.start_date   
		and (s.end_date > d.start_date or s.end_date is null)
),
...

----------
RESULT:
Record(churn_rate=0.0570875665215288, retention_rate=0.942912433478471, n_start=2067, n_churn=118)
```

Explaining what you ares seeing there is beyond the scope of this README, thats what the book is about! But if you have gotten this far, then you have completed all the setup and you are ready to follow along with the book (or videos, however you are learning the code...)

***Advanced Setup Instructions***  

 The following are  the "advanced" setup for people who are already accustomed to running Python in either a Jupyter Notebook or an Integrated Development Enivornment (IDE)

- [Jupyter Notebook Setup](readme_files/notebook.md)
- [Developers IDE Setup](readme_files/ide.md)

## Authors

* **Carl Gold** [carl24k](https://github.com/carl24k)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details




[(top)](#top)  
