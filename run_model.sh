#!/usr/bin/env bash
# COPY: listing params
# EDIT model in:

# run_churn_listing.py

SCHEMA=soc_net_sim_2
PYTHONUNBUFFERED=1
CHURN_DB=churn
CHURN_DB_USER=cgold
CHURN_DB_PASS=churn

CHURN_ROOT=/projects/ChurnBook

PYTHONPATH="${PYTHONPATH}:$HOME$CHURN_ROOT/fight-churn/listings/chap5:"\
"$HOME$CHURN_ROOT/fight-churn/listings/chap6:"\
"$HOME$CHURN_ROOT/fight-churn/listings/chap8:"\
"$HOME$CHURN_ROOT/fight-churn/listings/chap7"

export PYTHONPATH
export PYTHONUNBUFFERED
export CHURN_DB
export CHURN_DB_USER
export CHURN_DB_PASS

cd $HOME$CHURN_ROOT/fight-churn/listings/py/

cd $HOME$CHURN_ROOT/fight-churn/data-generation/py
../../venv/bin/python churndb.py $SCHEMA
../../venv/bin/python churnsim.py $SCHEMA

cd $HOME$CHURN_ROOT/fight-churn/listings/py/

# standard metric names
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 4 --version 1 2 3 4 5 6 7 8 11

# standard metric
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 3 --version 1 2 3 4 5 6 7 8

# Account tenure metric
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 11

# 1st ratio & total
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 1 3 --insert

# 2nd ratio
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 1 --version 2 --insert

# Change metrics
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 4 6 --insert

# Scaled metrics
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 8 --version 1 2 --insert

# Calculate active periods and observation dates
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 4 --listing 1 2 4

# Extract the data
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 2

# Stats
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 5 --listing 2

# Scores
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 5

# Grouping
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 6 --listing 4 3 5

# Regression
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 8 --listing 2

# Prediction
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 8 --listing 3 4 5

# Current Stats
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 5 --listing 2 --version 3


# Cohorts
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 5 --listing 1 --version 1 2 3 4 5 6 7 8 10
