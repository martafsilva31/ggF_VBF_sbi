
"""
gen_signal.py

Generates ggF signal events 

- sample contains weights for different benchmarks (from MG reweighting)

Can also generate events at the BSM benchmarks to populate regions of phase space not well populated by the SM sample
- smaller number than for SM point, 1/5 for each BSM benchmark
- reweighted to other benchmarks (inc. SM point)

Marta Silva (LIP/IST/CERN-ATLAS), 02/04/2024
"""


from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import os
import argparse 
import yaml
import math
from madminer.core import MadMiner
from madminer.lhe import LHEReader

# MadMiner output
logging.basicConfig(
    format='%(asctime)-5.5s %(name)-20.20s %(levelname)-7.7s %(message)s',
    datefmt='%H:%M',
    level=logging.DEBUG #INFO 
)

# Output of all other modules (e.g. matplotlib)
for key in logging.Logger.manager.loggerDict:
    if "madminer" not in key:
        logging.getLogger(key).setLevel(logging.WARNING)

def gen_signal(main_dir, setup_file, do_pythia, pythia_card, generate_BSM, mg_dir, cards_folder_name):

    # Load morphing setup file
    miner = MadMiner()
    miner.load(f'{main_dir}/{setup_file}.h5')
    lhe = LHEReader(f'{main_dir}/{setup_file}.h5')

    param_card_template_file=f'{cards_folder_name}/param_card_massless.dat'

    # LIP specifics
    init_command="export LD_LIBRARY_PATH=/project/atlas/users/mfernand/software/MG5_aMC_v3_5_1/HEPTools/pythia8/lib:$LD_LIBRARY_PATH"

    #SM samples with MG (re)weights of BSM benchmarks
    miner.run(
        mg_directory=mg_dir,
        log_directory=f'{main_dir}/logs/ggF_smeftsim_SM',
        mg_process_directory=f'{main_dir}/signal_samples/ggF_smeftsim_SM',
        proc_card_file=f'{cards_folder_name}/proc_card_signal.dat',
        param_card_template_file=param_card_template_file,
        pythia8_card_file=pythia_card if do_pythia else None,
        sample_benchmark ='sm',
        is_background = not args.reweight,
        run_card_file=f'{cards_folder_name}/run_card_signal_large.dat',
        initial_command=init_command if init_command != '' else None,
    )

    if generate_BSM:

        miner.run(
            mg_directory=mg_dir,
            log_directory=f'{main_dir}/logs/ggF_smeftsim_pos_chwtil',
            mg_process_directory=f'{main_dir}/signal_samples/ggF_smeftsim_pos_chgtil',
            proc_card_file=f'{cards_folder_name}/proc_card_signal.dat',
            param_card_template_file=param_card_template_file,
            pythia8_card_file=pythia_card if do_pythia else None,
            sample_benchmark='pos_chgtil',
            is_background = not args.reweight,
            run_card_file=f'{cards_folder_name}/run_card_signal_small.dat',
            initial_command=init_command if init_command != '' else None
        )



        miner.run(
            mg_directory=mg_dir,
            log_directory=f'{main_dir}/logs/ggF_smeftsim_neg_chwtil',
            mg_process_directory=f'{main_dir}/signal_samples/ggF_smeftsim_neg_chgtil',
            proc_card_file=f'{cards_folder_name}/proc_card_signal.dat',
            param_card_template_file=param_card_template_file,
            pythia8_card_file=pythia_card if do_pythia else None,
            sample_benchmark='neg_chgtil',
            is_background = not args.reweight,
            run_card_file=f'{cards_folder_name}/run_card_signal_small.dat',
            initial_command=init_command if init_command != '' else None
        )


    os.remove('/tmp/generate.mg5')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generates WH signal events WH(->l v b b~), divided by W decay channel and charge.',
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--config_file', help='Path to the YAML configuration file', default='config_1D_cHGtil.yaml')

    parser.add_argument('--do_pythia',help='whether or not to run Pythia after Madgraph',action='store_true',default=False)

    parser.add_argument('--generate_BSM',help='Generate additional events at the BSM benchmarks',action='store_true',default=False)

    parser.add_argument('--reweight',help='if running reweighting alongside generation (doesnt work on multi-core mode)',action='store_true',default=False)


    args=parser.parse_args()

    # Read configuration parameters from the YAML file
    with open(args.config_file, 'r') as config_file:
        config = yaml.safe_load(config_file)

        main_dir = config['main_dir']
        setup_file = config['setup_file']
        pythia_card = config['pythia_card']
        mg_dir = config['mg_dir']
        cards_folder_name = config['cards_folder_name']

    # Generate signal
    gen_signal(main_dir, setup_file, args.do_pythia, pythia_card, args.generate_BSM, mg_dir, cards_folder_name)
