# 1 Prerequisites

[0 Getting Started](#start)  
[1 Prerequisites](#prereq)  
[1.1 Python 3](#python)  
[1.2 Postgres](#postgres)  
[1.2.1 Database Setup](#createdb)  

Required:

* 12 Gb free disk space for the simulation data
* Python 3 and the required packages (requirements.txt)
* PostgreSQL

Recommended:

* PgAdmin - for PostgreSQL database setup

Optional:

* PyCharm (Community Edition)   OR  Jupyter Notebooks - for running Python programs

---

<a name="python"/>

## 1.1 Python 3

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

## 1.2 PostgreSQL

To install PostgreSQL for Mac following these instructions:

* https://postgresapp.com/downloads.html

To install PostgreSQL for Windows, use :

* https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

(That page has a different Mac installer if you don't like Postgresapp.)

For both Mac and Win, I also recommend installing installing pgAdmin to make it easier to import and export
data, and run adhoc queries. (Recent versions of PostgreSQL on Windows have PgAdmin installed already!)  Follow the instructions  here:

* https://www.pgadmin.org/download/

For Mac you should make sure Posgres is running - here's what it looks like if you installed with
PostgresApp on a Mac:

![Postgres Running on Mac](./postico.png)

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

![Connect to Server in PgAdmin](./pgadmin_connect.png)

A dialog will open. Assuming you are working on a PostgreSQL database installed on your own computer then  
in the first tab (*General*) name your connection `localhost`, and on the second tab (*Connection*) enter the
address `127.0.0.1` (which is the IP address to connect to a database locally.) You should also enter your
user name and password.  So your dialog should look like the one below - then hit *Save*.

![Connect to Server in PgAdmin](./pgadmin_connect_details.png)


Next you need to create a new database to hold all of the churn data schemas you create.
You will probably create multiple schemas as you work on the examples in the book and/or your own
data so this will help keep these organized.  An easy way to create a database is in PgAdmin - right click
on the *Databases* node under *localhost* in the tree:

![Create Database in PgAdmin](./pgadmin_createdb1.png)

And enter the name of the new database (I used churn, but you can use whatever you want - just make the
appropriate settings in your environment variable, section 1.2.2.3 below):

![Name the database](./pgadmin_createdb2.png)


---

---

