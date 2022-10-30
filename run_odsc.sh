#!/usr/bin/env bash
# COPY: listing params (& rename paths in conf)
# EDIT schema below

# run_churn_listing.py

SCHEMA=biznet2
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
../../venv/bin/python churnsim.py $SCHEMA
cd $HOME/$CHURN_ROOT/fight-churn/fightchurn/

# churn rate
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 2 --listing 1 2 4 5

# simple counts
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 1 2



# Account tenure metric
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 13
# MRR metric
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 14


# Scaled metrics
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 7
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 8
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 8 --version 1 2 3 4 5 6 7 8 --insert

## ratios
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 1  --insert

# Calculate active periods and observation dates
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 4 --listing 1 2 4

# Extract the data
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 4 --listing 5

# Stats
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 5 --listing 2

# XGB Fit
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 9 --listing 6

# SHAP
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 9 --listing 8

# MRR Cohorts
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 5 --listing 1
