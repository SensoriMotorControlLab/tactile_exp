

# imports we will probably need...
from psychopy import visual, event

import numpy as np

import random, os, sys


def runExperiment(ID=NULL):

    # every function, except this one, will get a cfg dictionary as input
    # it will change it, and then also return it as output

    # here we set it up:

    cfg = {}

    # there will be 2 parts of this cfg dictionary:
    # 1. a part that is a more or less "plain text" dictionary,
    #    with objects that can be stored in a JSON
    #    this wwill be called "state"
    # 2. a part that has binary objects that can not be stored in a JSON
    #    most notably the psychopy window, and stimulus objects
    #    this will be called "bin"

    # after every trial, we store the state, and we also do this in case of exceptions
    # eventually, we'll write a function that can restart the experiment where it 
    # crashed, if that should ever happen, and for this we use the last 'state' that was saved

    cfg['state'] = {}
    cfg['bin']   = {}

    # everything else we do will live in a try / except / else / finally block:

    try:

        cfg = prepare(cfg, ID)

        cfg = runAll(cfg)

    except:

        # something went wrong, save the state part of the cfg:

        cfg = saveState(cfg)

        # close the psychopy environment (if still possible)

        try:

            cfg = closeEnvironment(cfg)

        except:

            # print the exception?

    else:

        # experiment finished, do final steps:

        # we combine all trial data into a full description
        cfg = combineData(cfg)

        # and maybe generate a summary with one line per trial?
        cfg = createSummary(cfg)

        # still also need to close the environment:
        cfg = closeEnvironment(cfg)

    # we don't need a "finally" block... I think



def prepare(cfg, ID):

    cfg = setupParticipant(cfg, ID)

    cfg = setupEnvironment(cfg)

    cfg = setupTasks(cfg)

    return(cfg)



def setupParticipant(cfg, ID):

    # check if participant directory already exists

    # if not, create

    # if it does exist, check if there is a state.json file

    # if there is, check if it finished the experiment, or not
    # (this means we should probably store that the state)

    # if it's not finished, set a toggle for setupTasks, to restore the tasks from the json

    # the environment will still need to be created, because it's not store in the json


    # the other thing that depends on the participant ID is the state of the random-number generator
    # we know the initial state of the random number generator, because we set it with a seed depending on the participant ID

    # what we would not know is the state of the random number generator after it has done stuff, so..
    # if there is an `rngstate` in the state.json, we can `random.setstate(cfg['state']['rngstate'])`
    # and have that right where we left it, so that the experiment will continue exactly as if it hadn't crashed

    # if it's not there, we set it as best as we can

    return(cfg)


def setupEnvironment(cfg):


    # here we do a few things, that each deserve their own function as well
    # all of this will end up in the cfg['bin']

    cfg = setupPsychopyWindow(cfg)

    cfg = setupTabletTracker(cfg)

    cfg = setupStimuli(cfg)


    return(cfg)

def setupPsychopyWindow(cfg):

    # this should be a psychopy window object that has the units as centimeters

    cfg['bin']['win'] = NULL

    return(cfg)


def setupTabletTracker(cfg):

    # create a custom getpos function
    # using the mouse.getPos thing internally
    # but transform to centimeters on the tablet
    # and add a timestamp, so we can store the stylus position with the time it was polled
    # for the most accurate estimates of speed, acceleration etc possible
    # make them system timestamps in UNIX time (seconds since jan 1st 1980)
    # so that we also know exactly when the participant did the task

    def trackerPos():
        
        # code
        # more code

        return([X,Y,T])

    cfg['bin']['pos'] = trackerPos

    return(cfg)


def setupStimuli(cfg):

    # this creates the stimulu we'll use, for now there are at least 4:

    # 1. a cursor (circle)
    # 2. a start postition (circle)
    # 3. a target position (circle)
    # 4. an empty text box for on-screen instructions

    # these are all psychopy stim objects, associated with the window we created


    return(cfg)