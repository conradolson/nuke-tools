"""
Two functions that match the layer being viewed in the viewer to a shuffle node
or visa-versa
"""

import nuke

#Create a shuffle node set to the layer currently being viewed
def shuffleFromViewer():
    #define function to create shuffle nodes, depeneding on Nuke version
    def createShuffleNode():
        try:
            shuffle = nuke.createNode('Shuffle2')
        except:
            shuffle = nuke.createNode('Shuffle')
        shuffle['in1'].setValue(viewed)
        shuffle['label'].setValue('[value in1]')

    #get the channels currently being viewed
    viewed = nuke.activeViewer().node()['channels'].value()

    if len(nuke.selectedNodes()) == 0:
        #if no nodes are seleced, create a shuffle
        createShuffleNode()
    elif len(nuke.selectedNodes()) == 1:
        #if a single shuffle node is selected set it to the selected layer
        if nuke.selectedNode().Class() == 'Shuffle2' or nuke.selectedNode().Class() == 'Shuffle2':
            nuke.selectedNode()['in1'].setValue(viewed)
        #if the selected node isn't a shuffle, create a shuffle bellow
        else:
            createShuffleNode()
    else:
        #if there are multiple nodes selected set any shuffle to match viewer
        count = 0
        for n in nuke.selectedNodes():
            if n.Class() == 'Shuffle2' or n.Class() == 'Shuffle2':
                n['in1'].setValue(viewed)
                count = count + 1
        #if there are no shuffles in the selection, make one
        if count == 0:
            createShuffleNode()

#Set the viewer layer to match the selected shuffle node
def viewerFromShuffle():
    try:
        #check if nodes are selected and if more than one, or not a shuffle
        #show error message
        if len(nuke.selectedNodes()) < 2:
            if nuke.selectedNode().Class() == 'Shuffle2' or nuke.selectedNode().Class() == 'Shuffle2':
                selected_layer = nuke.selectedNode()['in1'].value()
                nuke.activeViewer().node()['channels'].setValue(selected_layer)
        else:
            nuke.message('Please select a single shuffle node')
    except:
        nuke.message('Select a shuffle node')

# add to menu
nuke.menu('Nuke').addCommand("Utilities/Set Viewer From Shuffle", 'shuffleFromViewer.viewerFromShuffle()', 'ctrl+alt+shift+v')
nuke.menu('Nuke').addCommand("Utilities/Shuffle From Viewer", 'shuffleFromViewer.shuffleFromViewer()', 'ctrl+alt+shift+s')
