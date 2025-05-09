from __future__ import absolute_import, division, print_function, unicode_literals

import logging

from madminer.delphes import DelphesReader
import argparse as ap
import os
import yaml
import numpy as np

# MadMiner output
logging.basicConfig(
    format='%(asctime)-5.5s %(name)-20.20s %(levelname)-7.7s %(message)s',
    datefmt='%H:%M',
    level=logging.DEBUG
)

# Output of all other modules (e.g. matplotlib)
for key in logging.Logger.manager.loggerDict:
    if "madminer" not in key:
        logging.getLogger(key).setLevel(logging.WARNING)

def process_events(event_path, setup_file_path, is_background_process=False, k_factor=1.0, do_delphes=True, delphes_card='', benchmark='sm'):

    observable_names = [
        'l1_px', 'l1_py', 'l1_pz', 'l1_e',
        'l2_px', 'l2_py', 'l2_pz', 'l2_e',
        'pt_l1', 'eta_l1', 'phi_l1',
        'pt_l2', 'eta_l2', 'phi_l2',
        'dR_ll','dphi_ll',
        'm_ll',
        'met',
        'mt_tot',
        'pt_tot',
        'j1_px', 'j1_py', 'j1_pz', 'j1_e',
        'j2_px', 'j2_py', 'j2_pz', 'j2_e',
        'pt_j1', 'eta_j1', 'phi_j1',
        'pt_j2', 'eta_j2', 'phi_j2',
        'm_jj',
        'deta_jj',
        'dR_jj',
        'dphi_jj' ]

    list_of_observables = [
        'l[0].px', 'l[0].py', 'l[0].pz', 'l[0].e',
        'l[1].px', 'l[1].py', 'l[1].pz', 'l[1].e',
        'l[0].pt', 'l[0].eta', 'l[0].phi',
        'l[1].pt', 'l[1].eta', 'l[1].phi',
        'l[0].deltaR(l[1])','l[0].deltaphi(l[1])',
        '(l[0] + l[1]).m',
        'met.pt',
        '(l[0] + l[1] + met).mt',
        '(l[0] + l[1] + met).pt',
        'j[0].px', 'j[0].py', 'j[0].pz', 'j[0].e',
        'j[1].px', 'j[1].py', 'j[1].pz', 'j[1].e',
        'j[0].pt', 'j[0].eta', 'j[0].phi',
        'j[1].pt', 'j[1].eta', 'j[1].phi',
        '(j[0] + j[1]).m',
        'j[0].deltaeta(j[1])',
        'j[0].deltaR(j[1])',
        'j[0].deltaphi(j[1]) * (-1. + 2.*float(j[0].eta > j[1].eta))'
    ]
    
    reader=DelphesReader(setup_file_path)
    
    logging.info(f'event_path: {event_path}, is_background: {is_background_process}')

    reader.add_sample(hepmc_filename=f'{event_path}/tag_1_pythia8_events.hepmc.gz',
                    sampled_from_benchmark=benchmark,
                    is_background=is_background_process,
                    lhe_filename=f'{event_path}/unweighted_events.lhe.gz',
                    delphes_filename=None if do_delphes else f'{event_path}/tag_1_pythia8_events_delphes.root',
                    k_factor=k_factor,
                    weights='lhe')

    if do_delphes:
        if os.path.exists(event_path+'/tag_1_pythia8_events_delphes.root'):
            logging.warning(f'Delphes file in {event_path} already exists !')
        reader.run_delphes('/cvmfs/sw.el7/gcc63/madgraph/3.3.1/b01/Delphes/', delphes_card, initial_command='module load gcc63/madgraph/3.3.1; source /cvmfs/sw.el7/gcc63/madgraph/3.3.1/b01/Delphes/DelphesEnv.sh', log_file=event_path+'/do_delphes.log')

    if os.path.exists(event_path+'/analysed_events.h5'):
        logging.warning(f'analysed (.h5) file in {event_path} already exists !')

    # Adding observables
    for i, name in enumerate(observable_names):
        reader.add_observable( name, list_of_observables[i], required=True )

    reader.analyse_delphes_samples(delete_delphes_files=True)

    reader.save(f'{event_path}/analysed_events.h5')


    

if __name__ == '__main__':

    parser = ap.ArgumentParser(description='Detector-level analysis of signal and background events (with Delphes). Includes the computation of the pZ of the neutrino and several angular observables',formatter_class=ap.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('--config_file', help='Path to the YAML configuration file', default='config_1D_cHGtil.yaml')

    parser.add_argument('--sample_dir',help='folder where the individual sample is', required=True)

    parser.add_argument('--do_delphes',help='run Delphes before analysis code', default=False, action="store_true")
   
    parser.add_argument('--benchmark',help='benchmark from which the sample is originally generated')
   
    args=parser.parse_args()



    # Read configuration parameters from the YAML file
    with open(args.config_file, 'r') as config_file:
        config = yaml.safe_load(config_file)

        main_dir = config['main_dir']
        setup_file = config['setup_file']
        mg_dir = config['mg_dir']
        cards_folder_name = config['cards_folder_name']
        delphes_card = config['delphes_card']

    if 'background' in args.sample_dir:
        process_events(f'{args.sample_dir}',f'{main_dir}/setup_1D_cHGtil.h5',is_background_process=True,k_factor=1.0,do_delphes=args.do_delphes, delphes_card=delphes_card, benchmark = args.benchmark)
    else:
        process_events(f'{args.sample_dir}',f'{main_dir}/setup_1D_cHGtil.h5',is_background_process=False,k_factor=1.0,do_delphes=args.do_delphes, delphes_card=delphes_card, benchmark = args.benchmark)
