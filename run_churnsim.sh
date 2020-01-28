#!/usr/bin/env bash
# COPY: listing params (& rename paths in conf)
# EDIT schema below

# run_churn_listing.py

SCHEMA=socialnet7
PYTHONUNBUFFERED=1
CHURN_DB=churn
CHURN_DB_USER=cgold
CHURN_DB_PASS=churn

CHURN_ROOT=/projects/ChurnBook

PYTHONPATH="${PYTHONPATH}:$HOME$CHURN_ROOT/fight-churn/listings/chap5:"\
"$HOME$CHURN_ROOT/fight-churn/listings/chap6:"\
"$HOME$CHURN_ROOT/fight-churn/listings/chap7:"\
"$HOME$CHURN_ROOT/fight-churn/listings/chap8:"\
"$HOME$CHURN_ROOT/fight-churn/listings/chap9:"\
"$HOME$CHURN_ROOT/fight-churn/listings/chap10"

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

# Account tenure metric
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 11

# standard metric
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 3 --version 1 2 3 4 5 6 7 8

# Metric coverage test
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 7

# total metric
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 3 --insert

# Change metrics
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 4 6 --insert

# Scaled metrics
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 8 --version 1 2 --insert

## ratios
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 1 --version 1 2 3 4 5 6 7 --insert

# Calculate active periods and observation dates
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 4 --listing 1 2 4

# Extract the data
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 4 --listing 5

# Stats
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 5 --listing 2

# Scores data set 1
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 5 --listing 3

# Grouping data set 1
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 6 --listing 4 3 5

# Dataset2 Extract & Processing
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 2
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 8 --listing 1

# Regression
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 8 --listing 2

# Prediction
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 8 --listing 3 4 5

# Current Stats
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 5 --listing 2 --version 7 8 9


# Levels of C param
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 9 --listing 4 --version 1 2 3

# Cross validation
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 9 --listing 5
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 9 --listing 5 --version 1
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 9 --listing 6
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 9 --listing 6 --version 1

# Forecast xgb
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 9 --listing 7

# Categorical data extract
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 10 --listing 1

# Categorical plots
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 10 --listing 2 --version 1 2

# Categorical plot with group
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 10 --listing 3

# Categorical data prep (call 4 and 5)
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 10 --listing 6

# Categorical scores
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 5 --version 2

# Categorical cross valid / regression
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 9 --listing 5 --version 2
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 9 --listing 6 --version 2
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 9 --listing 4 --version 4


# Current Categorical data
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 10 --listing 7
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 10 --listing 8

# Categorical current foecast
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 8 --listing 5 --version 2
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 9 --listing 7 --version 2

# Cohorts (after all metrics generated)
../../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 5 --listing 1 --version 1 2 3 4 5 6 7 8 10 11 12 13 14 15 16 17
