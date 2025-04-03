"""
Madminer parameter and morphing setup code for a WH signal.

Includes only the CP-odd operator (oHGtil), with morphing done up to 2nd order (SM + SM-EFT interference term + EFT^2 term).

WARNING: events should ALWAYS be generated with proc cards which have at least the same order in the ME^2 as in the morphing (best: same order) - see gen_signal.py and gen_background.py

Marta Silva (LIP/IST/CERN-ATLAS), 08/02/2024


"""

import os
import logging
import argparse 
import yaml
from madminer import MadMiner
from madminer.plotting import plot_1d_morphing_basis

# MadMiner output
logging.basicConfig(
    format='%(asctime)-5.5s %(name)-20.20s %(levelname)-7.7s %(message)s',
    datefmt='%H:%M',
    level=logging.INFO
)

# Output of all other modules (e.g. matplotlib)
for key in logging.Logger.manager.loggerDict:
    if "madminer" not in key:
        logging.getLogger(key).setLevel(logging.WARNING)


def setup_madminer(main_dir,plot_dir):
    """
    Sets up the MadMiner instance for WH signal, with only the CP-odd operator (oHWtil), and morphing up to 2nd order.
    """

    # Instance of MadMiner core class
    miner = MadMiner()

    miner.add_parameter(
        lha_block='smeftcpv',
        lha_id=3,
        parameter_name='cHGtil',
        morphing_max_power=2, # interference + squared terms
        parameter_range=(-3,3),
        param_card_transform='1.0*theta' # mandatory to avoid a crash due to a bug
    )

    miner.add_benchmark({'cHGtil':0.00},'sm')
    miner.add_benchmark({'cHGtil':2.868},'pos_chgtil')
    miner.add_benchmark({'cHGtil':-2.972},'neg_chgtil')

    # Morphing - automatic optimization to avoid large weights
    miner.set_morphing(max_overall_power=2,include_existing_benchmarks=True,n_trials = 1000, n_test_thetas=1000)

    miner.save(f'{main_dir}/setup_1D_cHGtil.h5')

    morphing_basis=plot_1d_morphing_basis(miner.morpher,xlabel=r'$\tilde{c_{HG}}$',xrange=(-3,3))
    morphing_basis.savefig(f'{plot_dir}/morphing_basis_1D_cHGtil.pdf')

    return miner
    
 
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Creates MadMiner parameter and morphing setup file for a WH signal, with only the CP-odd operator (oHGtil), \
                               morphing up to second order (SM + SM-EFT interference + EFT^2 term).',
                               formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--config_file', help='Path to the YAML configuration file', default='config_1D_cHGtil.yaml')
    args = parser.parse_args()

    # Read main_dir and plot_dir from the YAML configuration file
    with open(args.config_file, 'r') as config_file:
        config = yaml.safe_load(config_file)
        main_dir = config['main_dir']
        plot_dir = config['plot_dir']

    # MadMiner setup function
    setup_madminer(main_dir, plot_dir)