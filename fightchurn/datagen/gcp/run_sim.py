import fightchurn
from fightchurn import run_churn_listing
run_churn_listing.set_churn_environment('churn','postgres','churn','/home/USER/churn_output','XX.XXX.XXX.XXX')
run_churn_listing.run_standard_simulation()
