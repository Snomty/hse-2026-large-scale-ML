#!/bin/bash
cd ~/lsml_hw_2
export PYTHONPATH="${PYTHONPATH}:${PWD}"

source /data/shared_ml/dminakov/.venv/bin/activate
mkdir -p task1_single_gpu/logs

MODEL="EleutherAI/pythia-160m"
DATASET="wikitext"
DATASET_SUBSET="wikitext-103-v1"

GLOBAL_BATCH_SIZE_TOKENS=131072  
SEQ_LEN=512
BATCH_SIZE=32
GRAD_ACCUM=$(((GLOBAL_BATCH_SIZE_TOKENS / SEQ_LEN) / BATCH_SIZE))

SEED=42      
NUM_EPOCHS=1
LOG_FREQ=80
LR=3e-4

FREE_GPU=$(nvidia-smi --query-gpu=index,memory.used --format=csv,nounits,noheader | \
           sort -t, -k2 -n | head -1 | cut -d, -f1)
echo "Using GPU: $FREE_GPU"


echo "=== 1/3 FP32 ==="
CUDA_VISIBLE_DEVICES=$FREE_GPU python scripts/train_single.py \
    -m $MODEL \
    -d $DATASET \
    --dataset-subset $DATASET_SUBSET \
    -e fp32 \
    -b $BATCH_SIZE -s $SEQ_LEN \
    --grad-accum-steps $GRAD_ACCUM \
    --num-epochs $NUM_EPOCHS \
    --lr $LR \
    --log-freq $LOG_FREQ\
    --seed $SEED \
    --fp32 \
    2>&1 | tee task1_single_gpu/logs/fp32.log


echo "=== 2/3 BF16 ==="
CUDA_VISIBLE_DEVICES=$FREE_GPU python scripts/train_single.py \
    -m $MODEL \
    -d $DATASET \
    --dataset-subset $DATASET_SUBSET \
    -e bf16 \
    -b $BATCH_SIZE -s $SEQ_LEN \
    --grad-accum-steps $GRAD_ACCUM \
    --num-epochs $NUM_EPOCHS \
    --lr $LR \
    --log-freq $LOG_FREQ\
    --seed $SEED \
    2>&1 | tee task1_single_gpu/logs/bf16.log


echo "=== 3/3 BF16 + Checkpointing ==="
CUDA_VISIBLE_DEVICES=$FREE_GPU python scripts/train_single.py \
    -m $MODEL \
    -d $DATASET \
    --dataset-subset $DATASET_SUBSET \
    -e bf16_ckpt \
    -b $BATCH_SIZE -s $SEQ_LEN \
    --grad-accum-steps $GRAD_ACCUM \
    --num-epochs $NUM_EPOCHS \
    --lr $LR \
    --log-freq $LOG_FREQ\
    --seed $SEED \
    --checkpointing \
    2>&1 | tee task1_single_gpu/logs/bf16_ckpt.log

echo "Done!"
