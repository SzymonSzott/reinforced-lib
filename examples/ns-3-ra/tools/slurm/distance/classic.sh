#!/usr/bin/scl enable devtoolset-11 rh-python38 -- /bin/bash -l

NS3_DIR="${NS3_DIR:=$HOME/ns-3.38}"
TOOLS_DIR="${TOOLS_DIR:=$HOME/reinforced-lib/examples/ns-3-ra/tools}"

cd "$NS3_DIR"
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$NS3_DIR/build/lib
cd build/scratch

SEED_SHIFT=$1
MANAGER=$2
MANAGER_NAME=$3
N_WIFI=$4
DISTANCE=$5
SIM_TIME=$6
LOSS_MODEL=$7

SEED=$(( SEED_SHIFT + SLURM_ARRAY_TASK_ID ))

CSV_PATH="$TOOLS_DIR/outputs/distance_${MANAGER_NAME}_d${DISTANCE}_n${N_WIFI}_s${SEED}.csv"
WARMUP_TIME=$(( N_WIFI + 4))

./ns3.38-ra-sim-optimized --mobilityModel="Distance" --wifiManager="$MANAGER" --wifiManagerName="$MANAGER_NAME" --initialPosition="$DISTANCE" --nWifi="$N_WIFI" --simulationTime="$SIM_TIME" --warmupTime="$WARMUP_TIME" --logEvery="$SIM_TIME" --lossModel="$LOSS_MODEL" --RngRun="$SEED" --csvPath="$CSV_PATH"
