import os
import logging
import numpy as np
import matplotlib
from matplotlib import pyplot as plt


from madminer.core import MadMiner
from madminer.delphes import DelphesReader
from madminer.sampling import combine_and_shuffle
from madminer.plotting import plot_distributions

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

plots = plot_distributions(
    filename='/lstore/titan/martafsilva/master_thesis/bachelor_projects/ggF_output/background_samples/ttbar_background/Events/run_01/analysed_events.h5',
    parameter_points=['sm'],
    line_labels=['SM'],
    uncertainties='none',
    n_bins=20,
    n_cols=3,
    normalize=True,
)

plots.savefig("/lstore/titan/martafsilva/master_thesis/bachelor_projects/ggF_output/plots/ttbar_background_distributions.png")