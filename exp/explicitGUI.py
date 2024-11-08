#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import wx
import wx.adv # advanced GUI widgets

# we need our experiment:
import experiment

# we need to open webbrowsers to fill in the consent form:
import webbrowser as wb

# and we need to check stuff in the operating system:
import os

# this is to generate random participant IDs:
import secrets

# to check and pick which condition to do:
import numpy as np   # make arrays, and get math / trig functions
import pandas as pd  # check SUMMARY file for learners / non-learners
import random        # pick one at random in case of ties


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin: MyFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        self.Qualtrics = {'url':'',
                          'visited':False}

        self.SetSize((400, 250))
        self.text_participantID = wx.StaticText(self, wx.ID_ANY, "")

        self.hyperlink_qualtrics = wx.adv.HyperlinkCtrl(self, wx.ID_ANY, " ", " ", size=[400,20])
        self.button_runit = wx.Button(self, wx.ID_ANY, "run experiment")

        # we'll set the run button to be disabled for now:
        self.button_runit.Disable()

        # self.setParticipantID()
        self.setIDandTask()

        self.__set_properties()
        self.__do_layout()

        # and when certain things are clicked we run some functions...

        # when the run button is clicked, we need to run the experiment:
        self.Bind(wx.EVT_BUTTON, self.onRunExperiment, self.button_runit)

        # when people click the link to the consent form, we need to register this:
        self.Bind(wx.adv.EVT_HYPERLINK, self.onClickQualtrics, self.hyperlink_qualtrics)

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("clamp speed tasks runner (order test)")
        # end wxGlade

        # newURL = 'https://yorkufoh.ca1.qualtrics.com/jfe/form/SV_cZ7siSsepnvqtOS?id=%s'%(self.text_participantID.GetLabel())
        newURL = 'https://docs.google.com/forms/d/e/1FAIpQLSdZylS-xmd4rS0BdjeqWfAK2m7LfZvaRKMJZGGanh9aFRZ00A/viewform?usp=pp_url&entry.1851916630=%s'%(self.text_participantID.GetLabel())
        self.hyperlink_qualtrics.SetURL(newURL)
        self.hyperlink_qualtrics.SetLabel('questionnaire')


    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        grid_sizer_1 = wx.GridSizer(3, 2, 0, 0)
        label_1 = wx.StaticText(self, wx.ID_ANY, "participant ID (code):")
        grid_sizer_1.Add(label_1, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.text_participantID, 0, wx.ALIGN_CENTER, 0)

        label_2 = wx.StaticText(self, wx.ID_ANY, "pre questionnaire:")
        grid_sizer_1.Add(label_2, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.hyperlink_qualtrics, 0, wx.ALIGN_CENTER, 0)

        label_3 = wx.StaticText(self, wx.ID_ANY, "run experiment:")
        grid_sizer_1.Add(label_3, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.button_runit, 0, wx.ALIGN_CENTER, 0)

        self.SetSizer(grid_sizer_1)
        self.Layout()
        # end wxGlade

    def onRunExperiment(self, e):
        self.button_runit.Disable()
        print('\n\n' + self.task + '\n\n')

        # PyVMEC2.runExperiment(experiment=self.task, participant='%s'%(self.text_participantID.GetLabel()))
        experiment.runExp(ID='%s'%(self.text_participantID.GetLabel()), rotation=int(self.task[6:]))



    def onClickQualtrics(self, e):

        self.Qualtrics = {'url' : self.hyperlink_qualtrics.GetURL(),
                          'visited' : True}

        wb.open( url = self.hyperlink_qualtrics.GetURL(),
                 new = 1,
                 autoraise = True )
        
        self.button_runit.Enable()
        # self.testEnableRunButton()


    def setIDandTask(self):

        # these are the conditions we are running:
        conditions = [  'aiming20',
                        'aiming30',
                        'aiming40',
                        'aiming50',
                        'aiming60'  ]

        # we get the IDs for participants in each condition:
        existing = []
        learners = {}
        for condition in conditions:
            # pdirs = os.listdir('data/%s/'%(condition))

            cdir = 'data/%s/'%(condition)
            pdirs = next(os.walk(os.path.join(cdir,'.')))[1]

            print(pdirs)
            existing += pdirs # this is to decide on a new participant ID

            # provisional:
            # learners[condition] = pdirs

            # to decide on a condition, we need to have only the learners:
            # we got a list of participants, but we only care about the "learners"
            # lets find the learners, using their SUMMARY files

            condition_learners = []

            for folder in pdirs:
                filename = 'data/%s/%s/SUMMARY_%s_%s.csv'%(condition, folder, condition, folder)
                print(filename)
                summary = pd.read_csv(filename)

                # take the last 16 trials of the rotated phase:
                rotated = summary.loc[(summary['task_idx']==5),]
                rotend  = rotated.loc[(rotated['trial_idx']>4),]
                meandev = rotend['reachdeviation_deg'].median()
                rotation = list(rotend['rotation_deg'])[0]
                meandev = -1 * np.sign(rotation) * meandev
                if meandev > (np.abs(rotation)/2):
                    print('%s is a learner'%(folder))
                    condition_learners += [folder]
                else:
                    print('%s is NOT a learner'%(folder))

            learners[condition] = condition_learners

            # participants[condition] = participantfolders

        
        # in order to pick a _NEW_ participants ID, we need to know the...
        # names_in_use = sum([existing[k] for k in existing.keys()], []) # flatten the list... bit hacky

        new_name = ''+secrets.token_hex(3)
        
        while new_name in existing:
            new_name = ''+secrets.token_hex(3)
        
        self.text_participantID.SetLabel(new_name)

        # decide on which condition to assign the participant:
        # - get list of numbers of participants in each condition
        # condition_Ns = [len(participants[k]) for k in participants.keys()]

        condition_Ns = [len(learners[k]) for k in learners.keys()]

        # - get the lowest number of participants in any condition
        lowN = np.min(condition_Ns)

        # get all conditions with that number of participants
        indexes = [i for i, x in enumerate(condition_Ns) if x == lowN]

        # get condition names associated with the indexes:
        condition_names = np.array(conditions)[indexes]

        # shuffle them (no effect if there is only 1)
        random.shuffle(condition_names)
        # pick the first:
        selected_condition = condition_names[0]
        self.task = selected_condition

        


# end of class MyFrame

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class MyApp
if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
