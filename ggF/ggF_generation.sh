# Load Conda if not in PATH
#export PATH="/project/atlas/users/mfernand/software/Miniforge3/bin:$PATH"

# Activate conda environment
source /project/atlas/users/mfernand/venvs/madsbi/bin/activate


# Submit the job
#condorsubMC -J ggF_generation -q medium -n 4 -m 16000 \
python3 /project/atlas/users/mfernand/sbi_madminer_code/ggF/2a_gen_signal.py --do_pythia --reweight  > /data/atlas/users/mfernand/1D_cHGtil/output_logs/signal_generation.txt 2>&1