

# imports we will probably need...
from psychopy import visual, event, monitors

import numpy as np

import random, os, sys, time, json

import pandas as pd


def runExperiment(ID=NULL):

    # every function, except this one, will get a cfg dictionary as input
    # it will change it, and then also return it as output

    # here we set it up:

    cfg = {}

    # there will be 2 parts of this cfg dictionary:
    # 1. a part that is a more or less "plain text" dictionary,
    #    with objects that can be stored in a JSON
    #    this will be called "state"
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

        cfg = runTasks(cfg)

    except:

        # something went wrong, save the state part of the cfg:

        cfg = saveState(cfg)

        # close the psychopy environment (if still possible)

    else:

        # experiment finished, do final steps:

        # we combine all trial data into a full description
        cfg = combineData(cfg)

        # and maybe generate a summary with one line per trial?
        cfg = createSummary(cfg)

    finally:

        # still also need to close the environment:
        cfg = closeEnvironment(cfg)



def prepare(cfg, ID):

    cfg = setupParticipant(cfg, ID)

    cfg = setupEnvironment(cfg)

    cfg = setupTasks(cfg)

    cfg = saveState(cfg)

    return(cfg)



def setupParticipant(cfg, ID):

    if ID == NULL:
        print("participant ID not defined")
        raise Exception("participant ID not defined")

    dataFolder = "data/%s/"%(ID)


    if os.path.isdir("data"):
        if os.path.isdir(dataFolder):
            # participant folder exists
            cfg["state"]["crashRecovery"] = False
            if os.path.isfile("%sstate.json"%(dataFolder)):
                cfg["state"]["crashRecovery"] = True
        else:
            os.makedirs(dataFolder, exist_ok = True)
    cfg["state"]["dataFolder"] = dataFolder

    random.seed(ID)  

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
    myMonitor = monitors.Monitor(name='temp',
                                 distance=100,
                                 width=52.7)
    myMonitor.setSizePix([1920,1080])

    cfg["bin"]['win'] = visual.Window( size=[1920,1080], 
                                fullscr=True, 
                                units='cm', 
                                waitBlanking=False, 
                                #viewScale=[1,-1], 
                                color=[-1,-1,-1], 
                                screen=0, 
                                monitor=myMonitor)

    #   "size_px"         : [1920, 1080], 
    #   "size_cm"         : [52.7, 29.6],
    #   "viewscale"       : [1,-1],

    # for testing on non-mirrored setup:
    #cfg['win'] = visual.Window(fullscr=True, units='pix', waitBlanking=True, viewScale=[1,1], color=[-1,-1,-1])

    # set up the workspace as a function of the size of the window:
    # winSize = cfg['win'].size

    # we want 8 cm reaches
    # if we apply the viewscale correctly, that should be possible
    # leaving 3.375/2 cm free on top and bottom
    # the monitor on the tablet setup is 1920 pixels wide,
    # and that should span 31 cm on the tablet surface

    # cfg['xPPC'] = 1920/52.7
    # cfg['yPPC'] = 1080/29.6

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
        
            # set up 'mouse' object to track reaches:
        class myMouse:

            # TABLET:
            # "size_px"    : [1920, 1080],
            # "size_cm"    : [31.1, 21.6],
            # "mapping"    : 'relative',     <-   this is not true right now

            # MONITOR:
            #   "size_px"         : [1920, 1080], 
            #   "size_cm"         : [52.7, 29.6],
            #   "viewscale"       : [1,-1],

            def __init__(self,cfg):
                # we use a psychopy mouse object
                self.psyMouse = event.Mouse(visible = False, newPos = None, win = cfg['bin']['win'])
                self.xfactor = 52.7/31.1
                self.yfactor = 29.6/21.6

            def getPos(self):
                # but in addition to the position, we also return the time the position was asked for
                [X,Y] = self.psyMouse.getPos()
                st = time.time()
                X = X / self.xfactor # scale to centimeters ?
                Y = Y / self.yfactor # scale to centimeters ?

                return [X,Y,st]

    cfg['bin']["tracker"] = myMouse(cfg)

    return(cfg)


def setupStimuli(cfg):

    # this creates the stimulu we'll use, for now there are at least 4:

    # 1. a cursor (circle)
    cfg['bin']['cursor'] = visual.Circle(  win=cfg['bin']['win'], 
                                    radius=0.25, 
                                    lineWidth=0, 
                                    lineColorSpace='rgb', 
                                    lineColor=None, 
                                    fillColorSpace='rgb', 
                                    fillColor='#990000'     )
    # 2. a start postition (circle)
    cfg['bin']['start'] = visual.Circle(  win=cfg['bin']['win'], 
                                    radius=1 
                                    lineWidth=2, 
                                    lineColorSpace='rgb', 
                                    lineColor='#999999', 
                                    fillColorSpace='rgb', 
                                    fillColor=None          )
    # 3. a target position (circle)
    cfg['bin']['target'] = visual.Circle(  win=cfg['bin']['win'], 
                                    radius=1 
                                    lineWidth=2, 
                                    lineColorSpace='rgb', 
                                    lineColor='#999999', 
                                    fillColorSpace='rgb', 
                                    fillColor=None          )
    # 4. an empty text box for on-screen instructions
    cfg['bin']['instruction'] = visual.TextStim(win=cfg['bin']['win'], text='hello world', pos=[0,0], colorSpace='rgb', color='#999999')


    # these are all psychopy stim objects, associated with the window we created


    return(cfg)

def runTrial(cfg):
    # read in trial info from cfg
    # current trial number (variable)
    # look up condition (in condition order list)
    # defintion of conditions
    # columns = start position, end position, target size, tactile stim
    # run while loop
    # store data with trial number in folder
    # independent variables plus participant dependent variables (movement time)




    return(cfg)

def foldout(values, names):
    # http://code.activestate.com/recipes/496807-list-of-all-combination-from-multiple-lists/



    r=[[]]
    for x in values:
        r = [ i + [y] for y in x for i in r ]

    # return(pd.DataFrame(r))

    df = pd.DataFrame(r)
    df.columns = names
    return(df.to_dict())

def setupTasks(cfg):

    # master list of all conditions, positon, size, tactile stim
    conditions = foldout(values = [[1, 0.5], 
                                    [False, 1/3, 2/3], 
                                    [(-10, 5), (-10, -5), (10, 5), (10, -5)]]
                         names = ["targetSize", "tactileStim", "targetPos"])
    cfg["state"]["conditions"] = conditions

    # create a randomized list of trials unique to each participant ID

    Nconditions = len(conditions[list(conditions.keys())[0]])
    CondIdxOne = list(range(int(Nconditions/2)))
    CondIdxTwo = list(range(int(Nconditions/2, Nconditions)))
    if random.sample([True, False],1):
        CondIdxOne, CondIdxTwo = CondIdxTwo, CondIdxOne

    # two pseudo-randomized blocks

    trialOrder = []

    for blockNo in range(2):
        random.shuffle(CondIdxOne)
        random.shuffle(CondIdxTwo)
        for Idx in range(len(CondIdxOne)):
            
            trialOrder.append(CondIdxOne[Idx])
            trialOrder.append(CondIdxTwo[Idx])
    cfg["state"]["trialOrder"] = trialOrder

    return(cfg)

def saveState(cfg):

    # generate a file name, open a stream, and save state as JSON into the stream

    filename = '%s/state.json'%(cfg["state"]["dataFolder"])

    with open( file=filename,
               mode='w') as fp:
        json.dump(cfg["state"], fp, indent=2)

    return(cfg)