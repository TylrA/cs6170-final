import os
from Part1 import Subpart1


def subpart2(crit_or_ripser):
    cwd = os.getcwd()
    parent = os.path.join(cwd, os.path.join(os.path.dirname(__file__)))

    Subpart1.display_mds(parent, parent + "/../Data/WassersteinDistances/", "wasserstein_distances", crit_or_ripser, "Wasserstein")
    Subpart1.display_tsne(parent, parent + "/../Data/WassersteinDistances/", "wasserstein_distances", crit_or_ripser, "Wasserstein")
