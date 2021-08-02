#!/usr/bin/env bash
# COPY: listing params (& rename paths in conf)
# EDIT schema below

# run_churn_listing.py

SCHEMA=socialnet7
PYTHONUNBUFFERED=1
CHURN_DB=churn
CHURN_DB_USER=user
CHURN_DB_PASS=pass

CHURN_ROOT=path_from_home_to_code
CHURN_OUT_DIR=path_to_output_dir

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
../../venv/bin/python churnsim.py $SCHEMA
cd $HOME/$CHURN_ROOT/fight-churn/fightchurn/

# churn rate
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 2 --listing 1 2 3 4 5

# simple counts
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 1 2

# event QA
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 9 --version 1 2 3 4 5 6 7 8
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 10 --version 1 2 3 4 5 6 7 8

# standard metric names
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 4 --version 1 2 3 4 5 6 7 8 11

# Account tenure metric
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 13

# standard metric
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 3
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 3 --version 2 3 4 5 6 7 8

# metric QA
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 6 --version 1 2 3 4 5 6 7 8
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 7 --version 1 2 3 4 5 6 7 8

# Metric coverage test
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 8 11

# total metric
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 3 --insert

# Change metrics
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 4 6 --insert

# Scaled metrics
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 7 --insert
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 8 --version 1 2 --insert

## ratios
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 1 --version 1 2 3 4 5 6 7 --insert

# Calculate active periods and observation dates
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 4 --listing 1 2 4

# Extract the data
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 4 --listing 5

# Stats
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 5 --listing 2

# Scores data set 1
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 5 --listing 3

# Pair scatter plots
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 6 -listing 1 --version 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16

# Grouping data set 1
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 6 --listing 2 4 3 5

# Dataset2 Extract & Processing
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 8 --listing 0 1

# Regression
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 8 --listing 2

# Prediction
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 8 --listing 3 4 5 6

# Current Stats
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 5 --listing 2 --version 7 8 9

# Accuracy code test
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 9 --listing 1 2 3

# Levels of C param
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 9 --listing 4 --version 1 2 3

# Cross validation
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 9 --listing 5
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 9 --listing 5 --version 1
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 9 --listing 6
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 9 --listing 6 --version 1

# Forecast xgb
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 9 --listing 7


# Categorical data extract
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 10 --listing 1

# Categorical plots
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 10 --listing 2 --version 1 2

# Categorical plot with group
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 10 --listing 3


# Dummy variables
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 10 --listing 4

# Re-prepare the non-dummy part of categorical data
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 8 --listing 1 --version 3

# Merge dummies & groupscores
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 10 --listing 5
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 6 --listing 2 --version 3


#  Categorical cross valid / regression
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 9 --listing 5 --version 2 3
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 9 --listing 4 --version 4 5
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 9 --listing 6 --version 2

# Current Categorical data
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 10 --listing 6

# Current categorical data prep (call 4 and 5)
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 10 --listing 7

# Categorical current forecast
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 8 --listing 5 --version 2
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 9 --listing 7 --version 2

# Cohorts (after all metrics generated)
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 5 --listing 1 --version 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17
