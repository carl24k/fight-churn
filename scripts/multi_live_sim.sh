#!/usr/bin/env bash

CONF=socialnet7
CHURN_ROOT="Documents/churn"
CHURN_OUT_DIR="s3://gold-churn"

PYTHONPATH="$PYTHONPATH:$HOME/$CHURN_ROOT/fight-churn/fightchurn:"\
"$HOME/$CHURN_ROOT/fight-churn/fightchurn/churnsim:"\
"$HOME/$CHURN_ROOT/fight-churn"

echo "$CHURN_ROOT"
echo "$CHURN_OUT_DIR"
echo "$PYTHONPATH"

export CHURN_ROOT
export CHURN_OUT_DIR
export PYTHONPATH

cd "$HOME/$CHURN_ROOT/fight-churn/fightchurn/churnsim/" || exit 1
python churnsim.py --config-name=$CONF live_sim=parquet
python churnsim.py --config-name=$CONF live_sim=parquet
python churnsim.py --config-name=$CONF live_sim=parquet
python churnsim.py --config-name=$CONF live_sim=parquet
python churnsim.py --config-name=$CONF live_sim=parquet
python churnsim.py --config-name=$CONF live_sim=parquet
python churnsim.py --config-name=$CONF live_sim=parquet
