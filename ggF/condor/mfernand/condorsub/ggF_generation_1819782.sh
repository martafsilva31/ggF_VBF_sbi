#!/bin/bash

export SCRIPT=/project/atlas/users/mfernand/sbi_madminer_code/ggF/condor/mfernand/condorsub/ggF_generation_1819782.sh
export SCRIPTsub=/project/atlas/users/mfernand/sbi_madminer_code/ggF/condor/mfernand/condorsub/ggF_generation_1819782.sub
export enviromentvariablescript=/project/atlas/users/mfernand/sbi_madminer_code/ggF/condor/mfernand/condorsub/enviromentvariables_1819782.sh
export PATH=/project/atlas/users/mfernand/software/Miniforge3/bin:/bin:/user/mfernand/lhapdf/bin:/cvmfs/sft.cern.ch/lcg/external/texlive/2017/bin/x86_64-linux:/project/atlas/Users/mfernand/.vscode-server/cli/servers/Stable-ddc367ed5c8936efe395cffeec279b04ffd7db78/server/bin/remote-cli:/user/mfernand/bin:/user/mfernand/.local/bin:/data/atlas/users/mfernand/conda_pkgs/madsbi/bin:/project/atlas/Users/mfernand/software/Miniforge3/condabin:/bin:/user/mfernand/lhapdf/bin:/cvmfs/sft.cern.ch/lcg/external/texlive/2017/bin/x86_64-linux:/user/mfernand/bin:/user/mfernand/.local/bin:/cvmfs/sft.cern.ch/lcg/external/texlive/2017/bin/x86_64-linux:/usr/share/Modules/bin:/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/user/mfernand/.vscode-server/extensions/ms-python.debugpy-2025.4.1-linux-x64/bundled/scripts/noConfigScripts:/user/mfernand/.vscode-server/data/User/globalStorage/github.copilot-chat/debugCommand
cd /project/atlas/users/mfernand/sbi_madminer_code/ggF
source /project/atlas/users/mfernand/sbi_madminer_code/ggF/condor/mfernand/condorsub/enviromentvariables_1819782.sh

python3 /project/atlas/users/mfernand/sbi_madminer_code/ggF/2a_gen_signal.py --do_pythia --reweight

