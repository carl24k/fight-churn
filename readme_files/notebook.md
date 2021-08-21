<a name="notebook"/>

#### 1.2.3 Jupyter Notebook Setup

These instructions assume you already have Jupyter Notebooks installed. If you don't then you can consider the resources at https://jupyter.org/install. 

##### 1.2.3.1 Installing Packages Under Jupyter

1. launch a Jupyter  notebook from the project root directory. It should look like the view shown below : 

   ![note1_start](note1_start.png)

1. Start a new notebook from here (new button on the upper right...)

   ![note2_new](note2_new.png)

1. To install the required packages, run `pip install -r requirements.txt`

   ![note3_pip](note3_pip.png)

##### 1.2.3.2 Opening the Notebook & Setting the environment variables

1. Change the current directory to `data-generation/py`

2. ![note4_listdir](note4_datagen.png)

3. Open the Notbook `churn_db_sim.ipnyb`

4. In the second cell, change the environment variables to match the database, username and password that you have created...

   ![note5_environ](note5_environ.png)

5. Run the first two cells to set the environment variables. You will need to re-run these cells every time you re-open the notebook, and the similar notebook that you use to run the listings.

6. The first program to run, which will create the required database tables, is in the next cell of the notebook - this is explained in more detail below in section 1.3.1.

------

------

