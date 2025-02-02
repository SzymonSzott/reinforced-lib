#!/usr/bin/scl enable devtoolset-11 rh-python38 -- /bin/bash -l

NS3_DIR="${NS3_DIR:=$HOME/ns-3.37}"
RLIB_DIR="${RLIB_DIR:=$HOME/reinforced-lib/examples/ns-3-ccod}"

cd "$RLIB_DIR"

AGENT="DDPG"
AGENT_TYPE="continuous"

SCENARIO="convergence"
N_WIFI=55

NUM_REPS=14
SEED=200
MEMPOOL_KEY=1234

for (( i = 1; i <= NUM_REPS; i += 1)); do
  if [[ $i -gt 1 ]]; then
    LOAD_PATH="$RLIB_DIR/checkpoints/${AGENT}_${SCENARIO}_${N_WIFI}_run_$(( i - 1 )).pkl.lz4"
  fi
  SAVE_PATH="$RLIB_DIR/checkpoints/${AGENT}_${SCENARIO}_${N_WIFI}_run_${i}.pkl.lz4"

  echo "Training ${AGENT} ${SCENARIO} ${N_WIFI} simulation [${i}/${NUM_REPS}]"
  python3 main.py --ns3Path="$NS3_DIR" --agent="$AGENT" --agentType="$AGENT_TYPE" --nWifi="$N_WIFI" --scenario="$SCENARIO" --pythonSeed="$SEED" --seed="$SEED" --loadPath="$LOAD_PATH" --savePath="$SAVE_PATH" --mempoolKey="$MEMPOOL_KEY"

  SEED=$(( SEED + 1 ))
done
