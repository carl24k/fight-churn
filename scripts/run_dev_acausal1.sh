#!/usr/bin/env bash
# COPY: listing params (& rename paths in conf)
# EDIT schema below

# run_churn_listing.py

SCHEMA=crm5
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

cd $HOME/$CHURN_ROOT/fight-churn/fightchurn/churnsim/
../../venv/bin/python churndb.py $SCHEMA
../../venv/bin/python churnsim.py --config-name=$SCHEMA n_parallel=5 force=True acausal_churn=0.005
cd $HOME/$CHURN_ROOT/fight-churn/fightchurn/

# churn rate
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 2 --listing 6 7 8

# Account tenure metric, MRR, Total, Users Quantity, Discount
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 13 17 19 20 21
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 18 --version 1 2

# MRR, Discount, Tenure, bill period, Total names
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 4 --version 1 2 3 4 5 6 7

# Scaled metrics
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 7
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 8
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 8 --version 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19  21 23 24 25 26 --insert --n_parallel 6

# active users
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 9  --insert

# totals
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 3 --version 1 2 3 4 5 --insert

# ratios
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 1 --version 1 2 3  5 6 7 8 9 10 11 12 13 --insert

# Calculate active periods and observation dates
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 4 --listing 1 2 4

# Extract the data
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 4 --listing 9

# XGB Fit
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 9 --listing 6
../venv/bin/python run_churn_listing.py --schema $SCHEMA --chap 9 --listing 8

mv $CHURN_OUT_DIR/$SCHEMA $CHURN_OUT_DIR/$SCHEMA-$(date +'%Y%m%d%H%M')
