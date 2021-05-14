#!/usr/bin/env python3
from os import path
import sys
sys.path.append(path.abspath('../PyDG'))

import ast
import fnmatch
import os

from codegra_plag import cdg, graph, pdg

def find_files(directory, pattern):
    """Find all files in a directory that comply to the specify pattern.
    """
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                if os.path.isfile(filename):
                    yield filename


def get_pdgs(f_name):
    """Get all PDGs in a directory ``d`` and maybe split them.

    :param d: The directory to search in.
    :returns: A ``Subgraph`` instance
    """
    try:
        with open(f_name, 'r') as f:
            tree = ast.parse(f.read())
    except Exception as e:
        print('Invalid syntax in', f, e)
    else:
        cur_pdg = pdg.create_pdg(tree)
        cur_pdg.remove_useless_nodes()
        dot_pdg = cur_pdg.to_dot()
        print(dot_pdg)


get_pdgs(sys.argv[1])