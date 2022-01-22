#!/usr/bin/python -tt
# Project: python
# Filename: test_ntg.py
# claudia
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "12/6/21"
__copyright__ = "Copyright (c) 2018 Claudia"
__license__ = "Python"

import argparse
from N2G import yed_diagram
from N2G import drawio_diagram

def some_function():
    pass


def main():

    diagram = yed_diagram()
    diagram.add_node('R1', top_label='Core', bottom_label='ASR1004')
    diagram.add_node('R2', top_label='Edge', bottom_label='MX240')
    diagram.add_link('R1', 'R2', label='DF', src_label='Gi0/1', trgt_label='ge-0/1/2')
    diagram.layout(algo="kk")
    diagram.dump_file(filename="Sample_graph.graphml", folder="./Output/")

    diagram = drawio_diagram()
    diagram.add_diagram("Page-1")
    diagram.add_node(id="R1")
    diagram.add_node(id="R2")
    diagram.add_link("R1", "R2", label="DF")
    diagram.layout(algo="kk")
    diagram.dump_file(filename="Sample_graph.drawio", folder="./Output/")


# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python test_ntg.py' ")

    # parser.add_argument('all', help='Execute all exercises in week 4 assignment')
    parser.add_argument('-a', '--all', help='Execute all exercises in week 4 assignment', action='store_true',
                        default=False)
    arguments = parser.parse_args()
    main()
