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

![Windows Environment Variables](/Users/carl/Documents/churn/fight-churn/readme_files/win_envvar.png)

Much of the other README pages here are written for people using PyCharm, but you can always run the same commands
illustrated from the terminal..

