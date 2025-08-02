#!/usr/bin/env bash
# COPY: listing params (& rename paths in conf)
# EDIT schema below

# run_churn_listing.py

SCHEMA=socialnet8
PYTHONUNBUFFERED=1
CHURN_DB=treat
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

# churn rate
/Users/carl/.pyenv/versions/3.9.18/envs/churn/bin/python run_churn_listing.py --schema $SCHEMA --chap 2 --listing 6 7

# standard metric names
/Users/carl/.pyenv/versions/3.9.18/envs/churn/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 4 --version 1 2 3 4 5 6 7 8 9 10

# Account tenure metric
/Users/carl/.pyenv/versions/3.9.18/envs/churn/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 13

# MRR metric
/Users/carl/.pyenv/versions/3.9.18/envs/churn/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 17

# standard metric
/Users/carl/.pyenv/versions/3.9.18/envs/churn/bin/python run_churn_listing.py --schema $SCHEMA --chap 3 --listing 3 --version 1 2 3 4 5 6 7 8 --n_parallel 8

# Ratios
/Users/carl/.pyenv/versions/3.9.18/envs/churn/bin/python run_churn_listing.py --schema $SCHEMA --chap 7 --listing 1 --version 1 2 --insert

# Calculate active periods and observation dates
/Users/carl/.pyenv/versions/3.9.18/envs/churn/bin/python run_churn_listing.py --schema $SCHEMA --chap 4 --listing 1 2 4

# Extract the data
/Users/carl/.pyenv/versions/3.9.18/envs/churn/bin/python run_churn_listing.py --schema $SCHEMA --chap 4 --listing 10

# Stats
/Users/carl/.pyenv/versions/3.9.18/envs/churn/bin/python run_churn_listing.py --schema $SCHEMA --chap 5 --listing 2

# Cross validation
/Users/carl/.pyenv/versions/3.9.18/envs/churn/bin/python run_churn_listing.py --schema $SCHEMA --chap 9 --listing 6

# XGB SHAP
/Users/carl/.pyenv/versions/3.9.18/envs/churn/bin/python run_churn_listing.py --schema $SCHEMA --chap 9 --listing 8

