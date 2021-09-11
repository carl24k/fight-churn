# 2 Quick Start Command Line Setup

[2.0 Open a Terminal Session](#terminal)  
[2.1 Create a virtual environment](#virtual)  
[2.2 Install the fightchurn package](#fightchurn)  
[2.3 Create a directory for output](#output)  
[2.4 Start the Python virtual environment](#startvirtual)  
[2.5 Import the run_churn_listing_module](#import)  
[2.6 Set the churn environment variables](#envvar)  
[2.7 Run the data simulation](#simulate)  
[2.8 Run code listings](#run)  


---

<a name="terminal"/>

### 2.0 Open a Terminal Session

Start by opening a terminal session.

* [Instructions for Windows](https://www.lifewire.com/how-to-open-command-prompt-2618089)
* [Instructions for Mac](https://support.apple.com/guide/terminal/open-or-quit-terminal-apd5265185d-f365-44cb-8b09-71a064a42125/mac)

<a name="virtual"/>

### 2.1 Create a virtual environment

First, you should make a new virtual environment in which to install the Fight Churn code...

```shell
python3 -m venv <python_environment_name>
```

Use whatever you like for `<python_environment_name>` ; if you don't normally make python environments, call it "py_venv". That command doesn't have any output. 

Next, your need to activate your environment. 

#### 2.1.1 Active environment on Mac/Linux

On Mac or Linux you source the `activate` script in the bin folder:

```
~ user$ source py_venv/bin/activate
```

The prompt will change and you will see:

```
(py_venv) ~ user$ 
```

#### 2.1.2 Active environment on Windows

On Windows you activate the environment by running the `activate` script as follows:

```
C:\Users\Owner\desktop> py_env\Scripts\activate
```

The prompt will change and you will see:

```
(py_env)C:\Users\Owner\desktop\>
```

<a name="fightchurn"/>

### 2.2 Install the fightchurn package

```shell
pip install fightchurn
```

This will lead to a lot of outputs, starting with something like this:

```shell
(py_venv) ~ user$ pip install fightchurn
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
source py_venv/bin/activate
python
```

(The command above is assuming you named your virtual environment `py_env`). You should see something like the following...

```shell
(py_venv) :~ user$ python
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

This will print out a confirmation line like this:

```
Setting Environment Variables user=your_user_name for db=churn, output path =`/path/to/my_churn_output_folder`
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

#### 2.8.1 Running one listing

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


#### 2.8.2 Running multiple listings

In some parts of the book you might want to run more than one listing at once. To do this, 
pass as a list for the listing argument. For example, to run all four chapter 2 churn 
calculation listings try:


```python
run_churn_listing.run_listing(2,[1,2,3,4])
```


#### 2.8.3 Running listing versions

Later in the book, some of the listings have multiple versions with different arguments. The 
`run_listing` function also takes a version argument. For example, to run a query and plot the 
results of the events per day for the first event created by the simulation, try the following:


```python
run_churn_listing.run_listing(chapter=3,listing=[9,10],version=1)
```

That command should save a plot like this to your output directory:

![like_per_day](./like_per_day.png)

You can also run multiple versions at once:


```python
run_churn_listing.run_listing(chapter=3,listing=[9,10],version=[2,3])
```

For more information about what the code listings do, see the book Fighting Churn With Data.