#!/bin/bash
#
# Reserve one GPU
#SBATCH --gres=gpu:1
#
# Reserve four CPU cores
#SBATCH -c 4
#
# Reserve 128GB RAM
#SBATCH --mem=128G
#
#SBATCH -p gpus
#
# Run the program
python ./run_summarization.py \
	--model_name_or_path facebook/bart-base \
	--output_dir ./model/inquisitive-questions \
	--overwrite_output_dir TRUE \
	--train_file ./data/transformers-train.json \
	--validation_file ./data/transformers-validation.json \
	--do_train TRUE \
	--do_eval TRUE \
	--logging_dir ./log \
	--per_device_train_batch_size 2 \
	--per_device_eval_batch_size 2 \
	--num_train_epochs 7
