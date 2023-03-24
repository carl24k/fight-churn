#!/usr/bin/env bash
# COPY: listing params (& rename paths in conf)
# EDIT schema below

# run_churn_listing.py

SCHEMA=crm1
PYTHONUNBUFFERED=1
CHURN_DB=churn
CHURN_DB_USER=carl
CHURN_DB_PASS=churn


CHURN_ROOT=Documents/churn/
CHURN_OUT_DIR=/Users/carl/Documents/churn/fight-churn-output

PYTHONPATH="${PYTHONPATH}:$HOME/$CHURN_ROOT/fight-churn/fightchurn/listings/chap3:"\
"$HOME/$CHURN_ROOT/fight-churn/fightchurn/listings/chap5:"\
"$HOME/$CHURN_ROOT/fight-churn/fightchurn/listings/chap6:"\
"$HOME/$CHURN_ROOT/fight-churn/fightchurn/listings/chap7:"\
"$HOME/$CHURN_ROOT/fight-churn/fightchurn/listings/chap8:"\
"$HOME/$CHURN_ROOT/fight-churn/fightchurn/listings/chap9:"\
"$HOME/$CHURN_ROOT/fight-churn/fightchurn/listings/chap10:"\
"$HOME/$CHURN_ROOT/fight-churn/fightchurn:"\
"$HOME/$CHURN_ROOT/fight-churn"


export PYTHONPATH
export PYTHONUNBUFFERED
export CHURN_DB
export CHURN_DB_USER
export CHURN_DB_PASS
export CHURN_OUT_DIR

cd $HOME/$CHURN_ROOT/fight-churn/fightchurn/

cd $HOME/$CHURN_ROOT/fight-churn/fightchurn/datagen/
../../venv/bin/python churndb.py $SCHEMA
../../venv/bin/python churnsim.py --model $SCHEMA  --n_parallel 5 --init_customers 10000 --start_date 2023-01-01 --end_date 2023-06-01  --growth_rate 0.04  --complex True
cd $HOME/$CHURN_ROOT/fight-churn/fightchurn/

# churn rate
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 2 --listing 1 2 4 5

# simple counts
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 1 2



# Account tenure metric, MRR, Total, Users Quantity
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 13 17 18 19
# MRR, Tenure, Total names
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 4 --version 1 2 3 4

# Scaled metrics
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 7
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 8
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 8 --version 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 --insert --n_parallel 6

# active users
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 9  --insert

# ratios
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 1 --version 1 2  --insert

# Metric & Event QA
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 8 11

# Calculate active periods and observation dates
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 4 --listing 1 2 4

# Extract the data
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 4 --listing 9

# Stats and scores
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 5 --listing 2 3


# Correlation analysis
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 6 --listing 2 4 3 5

# Cohorts
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 5 --listing 1 --version 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 30 31 32 33 34 35

# XGB Fit
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 9 --listing 6

# SHAP
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 9 --listing 8
