<a name="pycharm"/>

#### 1.2.2 Pycharm Setup

After you have cloned this repository

1. launch PyCharm and go to the menu *File* / *New Project*
1. In the file section window, select the folder for the repo.  Leave it set to "Create New Virtual environment for this project"
1. Click **Create**
1. It should say "The directory ... is not empty.  Would you like to create a project from existing sources?"  Click Yes

![Name the database](pycharm0_existing_sources.png)

---

##### 1.2.2.1 Setup Python Project in Pycharm

You should create a Python "virtual environment" for the project (I won't try to go into details here,
but this allows you to install the packages used for the repo without interfering with anything else
on your system).  

In PyCharm, select from the menus: 

- Mac:  *Pycharm*  / *Preferences...*  and go to the area for *Project*
- Windows:   *File*  / *Settings...*  and go to the area for *Project*

![PyCharm Project Preferences](pycharm1_project_preferences.png)

If you click on the gear wheel to the right of where it says <No Interpreter> you have the option to add
a new one...

![PyCharm Add Intepreter](pycharm2_add_interpreter.png)

It will look something like this:

![PyCharm Interpreter Setting](pycharm3_interpreter_settings.png)

And after you click **Okay** it will take several seconds to create the virtual environment, and
then it should look like this:

![PyCharm After Create](pycharm4_after_create.png)

You will add more packages in a minute, but first finish with the project setup by going to the
*Project Structure* section of the preferences:


![PyCharm Project Structure](pycharm5_project_structure.png)

Select each folder that contains python source code, and click on the button *Sources*
(with the blue folder next to it):

![PyCharm Select One Source Folder](pycharm6_source_select.png)

You should select the following folders:

* data-generation/py
* listings/py
  * listings/chap3
  * listings/chap5
  * listings/chap6
  * listings/chap7
  * listings/chap8
  * listings/chap9
  * listings/chap10

When you are done your project preferences should look like this:

![PyCharm Source Folders Selected](pycharm7_sources_selected.png)

---

##### 1.2.2.2 Installing Python Package Requirements in Pycharm

Now that you have created a Python project you can easily install the
required packages.  

1. Start by opening the Python file *data-generation/py/churndb.py* . At this point you are not going to use it, but PyCharm might not do the requirements for you if you don't have a Python file open. (Thats actually a weird PyCharm gotcha.) At this point it should give you a bunch of message about Installing requirements at the top. 
2. Now, go ahead and opena the file *requirements.txt* in the root project folder - these are the packages you will install.
3. ![PyCharm Requirements](pycharm8_requirements.png)
4. Notice that at the top it says: *Install requirements* - click on that and the click
   **Install** in the dialog that comes up. Note that you have to be connected to the internet for
   this to work, and it will take several minutes for all the packages to be downloaded 
   and installed.


---

##### 1.2.2.3 Creating Run Configurations and Setting Database Environment Variables

A lot of the python code depends on access to the database you created for the churn data.
You will set environment variables that will hold your database and login information, so that
it does not have to be hard coded.  The easiset way to do this in PyCharm is to
set environment variables when you create a Run Configuration for the executables.

Here is one example of creating a run configuration for one of the programs: If you have not created any Run Configurations yet, you start with menu options `Run > Edit Configurations` as shown in pic below:


![PyCharm Add Config](pycharm9_add_config.png)

In the Run/Debug Configuration dialog click the **+**  then **Python** to make a new python script configuration.


![PyCharm Python Config](pycharm10_new_python_config.png)

You will get an empty configuration, and the first thing to do is click on the Folder icon in the 
script path text box and pick the script path.  The first script everyone will need to run is 
*data-generation/py/churndb.py*, which creates a schema for an analysis.  After selecting this script, your
configuration should look like this, with both the script path and the working directory set to 
wherever the script is on your system:

![PyCharm Script Path](pycharm11_script_path.png)

The next step is to add the environment variables, by clicking on the *Browse* button at the end
of the environment variables text box:

![PyCharm Add Config](pycharm12_browse_environ.png)

That button launches a dialog to add the environment variables.  You need to add three:

1.  CHURN_DB  : the name of the database for your churn analysis schemas (step 1.2.1 above)
1.  CHURN_DB_USER : the user name to login to the database
1.  CHURN_DB_PASS : the password to login to the database

After setting these, your environment variable dialog should look something like this:

![PyCharm Add Config](pycharm13_environ_vars.png)

Select **OK** and save all the configuration changes.  I'll say more about running this script in the 
next section on Data Loading / Creation.

------

##### 1.2.2.4 Duplicating Run Configurations

For creating additional Run configurations, note that PyCharm allows you to duplicate 
and modify an existing configuration.  So when you want to make another script with the same environment
variables open the Configuration Dialog, now by clicking on the run configuration drop down then selecting 
**Edit Configuration**


![PyCharm Add Config](pycharm14_edit_config.png)

Now choose to duplicate your existing Run configuration:

![PyCharm Add Config](pycharm15_copy_config.png)

This will make another configuration the same as the existing one - you can rename it and reset the 
path to a different script, keeping the environment variables you already setup.

- Duplicating run configurations saves you the trouble of re-entering the environment variables

One last thing: After creating the Run Configuration you actually run a script in PyCharm
using menu configurations `Run > Run 'churndb'` as shown in pic below:

![PyCharm Run Script](pycharm16_run_script.png)


---

---


