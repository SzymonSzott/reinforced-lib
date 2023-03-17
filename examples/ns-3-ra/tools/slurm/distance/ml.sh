#!/usr/bin/scl enable devtoolset-11 rh-python38 -- /bin/bash -l

RLIB_DIR="${RLIB_DIR:=$HOME/reinforced-lib/examples/ns-3-ra}"
TOOLS_DIR="${TOOLS_DIR:=$HOME/reinforced-lib/examples/ns-3-ra/tools}"
NS3_DIR="${NS3_DIR:=$HOME/ns-3.38}"

cd "$RLIB_DIR"

SEED_SHIFT=$1
MANAGER=$2
MANAGER_NAME=$3
N_WIFI=$4
DISTANCE=$5
SIM_TIME=$6
LOSS_MODEL=$7
MEMPOOL_SHIFT=$8

SEED=$(( SEED_SHIFT + SLURM_ARRAY_TASK_ID ))
MEMPOOL_KEY=$(( MEMPOOL_SHIFT + SLURM_ARRAY_TASK_ID ))

CSV_PATH="$TOOLS_DIR/outputs/distance_${MANAGER_NAME}_d${DISTANCE}_n${N_WIFI}_s${SEED}.csv"
WARMUP_TIME=$(( N_WIFI + 4))

python3 main.py --mobilityModel="Distance" --agent="$MANAGER" --ns3Path="$NS3_DIR" --wifiManagerName="$MANAGER_NAME" --initialPosition="$DISTANCE" --nWifi="$N_WIFI" --simulationTime="$SIM_TIME" --warmupTime="$WARMUP_TIME" --logEvery="$SIM_TIME" --lossModel="$LOSS_MODEL" --seed="$SEED" --csvPath="$CSV_PATH" --mempoolKey="$MEMPOOL_KEY"
