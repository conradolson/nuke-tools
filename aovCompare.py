# --------------------------------------------------------------
#  aovCompare.py
#  Version: 1.0.2
#  Author: Conrad Olson
#
#  Last Modified by: Conrad Olson
#  Last Updated: Dec 9th, 2020
# --------------------------------------------------------------

import nuke
import os

# check to make sure 2 read nodes and only 2 read nodes are selected
def checkSelection(checkThis):
    if len(checkThis) != 2:
        return False
    else:
        for i in checkThis:
            if i.Class() != 'Read':
                return False
            else:
                return True

# compare the diffenece in AVOs between two read Nodes

def aovCompare():
    selection = nuke.selectedNodes()
    selection.sort()
    # run the checkSelection function to confirm that we have two read nodes selected
    if checkSelection(selection) is False:
        nuke.message('Select 2 read nodes')
    else:
        # get each node from the list
        node1 = selection[0]
        node2 = selection[1]
        # get a list of channels from each read node
        channels1 = node1.channels()
        channels2 = node2.channels()
        # get rid of individual channels and group into layers
        layers1 = list(set([c.split ('.')[0] for c in channels1]))
        layers2 = list(set([c.split ('.')[0] for c in channels2]))
        # get all the layers that are missing from one or the other
        # if the two read nodes match finish here
        if len(list(set(layers1) ^ set(layers2))) == 0:
            nuke.message("The selected read nodes have the same AOVs")
            return
        # start the message that will be displayed at the end of the function
        message = ''
        # get the layers that are in node1 but not in node2
        file1 = os.path.basename(node1['file'].value())
        file2 = os.path.basename(node2['file'].value())
        s = set(layers2)
        difference1 = [x for x in layers1 if x not in s]
        if len(difference1) != 0:
            message = message + file1
            message = message + ' has the following AOVs that are not in '
            message = message + file2
            message = message + ': \n \n'
            message = message + ', '.join(difference1)
        # get the layers that are in node2 but are not in node1
        s = set(layers1)
        difference2 = [x for x in layers2 if x not in s]
        if len(difference2) != 0:
            message = message + '\n \n -------- \n \n'
            message = message + file2
            message = message + ' has the follwong AOVs that are not in '
            message = message + file1
            message = message +': \n \n'
            message = message + ', '.join(difference2)
        nuke.message(message)
        print message
        print '\n'


# add to Utilities menu
nuke.menu('Nuke').addCommand("Utilities/Compare AOVs", 'aovCompare.aovCompare()',)
