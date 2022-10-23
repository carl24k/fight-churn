sudo apt-get install g++
sudo apt-get install python3-venv
sudo apt-get install postgresql-client  
python3 -m venv venv
pip install fightchurn
mkdir churn_output

# ADD VM ADDRESS TO DATBASE Connections
#   "Connections" tab 
#   -> "ADD NETWORK" button
#   -> "SAVE" button

# Use quotes around this command
psql "dbname=postgres user=postgres hostaddr=34.168.158.126"

# In PSQL
create database churn;
\q

# Back on the shell
source venv/bin/activate
# In Python
import fightchurn
from fightchurn import run_churn_listing
run_churn_listing.set_churn_environment('churn','postgres','churn','/home/carl/churn_output','34.168.158.126')
run_churn_listing.run_standard_simulation()


# If events were generated for 2020, and you want to simulate 2022...
'''update socialnet7.event
set event_time = date_add(event_time, INTERVAL 27 month)
where 1=1;'''


# Airflow Update Parallism to 2
# In Airflow
# Check Admin -> Configuration in Airflow UI
# In Composer
# Click Tab "AIRFLOW CONFIGURATION OVERRIDES"
# Add override key="parallelsim" value=2
# Check Admin -> Configuration in Airflow UI
# ALSO try min_file_process_interval - set to lower value like 5
