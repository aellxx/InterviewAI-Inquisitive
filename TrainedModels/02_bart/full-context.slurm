#!/bin/bash
#
#SBATCH --job-name fc-inquisitive
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH -t 01:00:00
#
# Reserve GPUs
#SBATCH --gpus=1
#
# Reserve CPU cores
#SBATCH -c 2
#
# Need this for accessing scratch, according to https://portal.xsede.org/sdsc-expanse
#SBATCH --constraint="lustre"
#
# Reserve RAM
#SBATCH --mem=8G
#
#SBATCH --account=TG-ASC150024
#SBATCH -p gpu
#
# Debug:
# srun -p gpu-debug --gpus=1 --pty --account=TG-ASC150024  --nodes=1 --ntasks-per-node=4 --mem=4G -t 00:30:00 --wait=0 --export=ALL /bin/bash

source ~/.bashrc
conda activate torch_gpu
echo "Starting job"
date

export WANDB_PROJECT=inquisitive1

python ./run_summarization.py \
	--model_name_or_path facebook/bart-base \
	--output_dir ~/scratch/model/inquisitive-full \
	--overwrite_output_dir TRUE \
	--train_file ./data/train-full-context.json \
	--validation_file ./data/validation-full-context.json \
	--do_train TRUE \
	--do_eval TRUE \
	--logging_dir ./log \
	--report_to=wandb \
	--per_device_train_batch_size 8 \
	--per_device_eval_batch_size 8 \
	--num_train_epochs 15 \
	--push_to_hub \
	--hub_model_id kcarnold/inquisitive-full

echo "Done!"
date
