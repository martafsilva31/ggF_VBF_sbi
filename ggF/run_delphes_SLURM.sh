#!/bin/bash
#SBATCH -p lipq
#SBATCH -n 4
#SBATCH --mem=16G
# INPUT = 3_run_delphes_analysis.py

module load gcc63/madgraph/3.3.1
source /cvmfs/sw.el7/gcc63/madgraph/3.3.1/b01/Delphes/DelphesEnv.sh
module load python/3.9.12

python3 3_run_delphes_analysis.py --sample_dir /lstore/titan/martafsilva/master_thesis/bachelor_projects/ggF_output/signal_samples/ggF_smeftsim_neg_chgtil/Events/run_01 --do_delphes --benchmark neg_chgtil > /lstore/titan/martafsilva/master_thesis/bachelor_projects/ggF_output/output_logs/delphes_analysis_signal_neg_chgtil.txt 2>&1