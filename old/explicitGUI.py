#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import wx
import wx.adv # advanced GUI widgets

# we need our experiment:
import experiment_v2
import tact_exp
import familiarization

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

        self.count_counts = wx.StaticText(self, wx.ID_ANY, "")

        self.text_participantID = wx.StaticText(self, wx.ID_ANY, "")

        self.hyperlink_qualtrics = wx.adv.HyperlinkCtrl(self, wx.ID_ANY, " ", " ", size=[400,20])
        
        self.button_runfam = wx.Button(self, wx.ID_ANY, "familiarization")
        self.button_runit = wx.Button(self, wx.ID_ANY, "run experiment")

        # we'll set the run button to be disabled for now:
        self.button_runfam.Disable()
        self.button_runit.Disable()

        # self.setParticipantID()
        self.setIDandTask()

        self.__set_properties()
        self.__do_layout()

        # and when certain things are clicked we run some functions...

        # when the run button is clicked, we need to run the experiment:
        self.Bind(wx.EVT_BUTTON, self.onRunFamiliarization, self.button_runfam)
        self.Bind(wx.EVT_BUTTON, self.onRunExperiment, self.button_runit)

        # when people click the link to the consent form, we need to register this:
        self.Bind(wx.adv.EVT_HYPERLINK, self.onClickQualtrics, self.hyperlink_qualtrics)

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("explicit timecourse runner")
        # end wxGlade

        # newURL = 'https://yorkufoh.ca1.qualtrics.com/jfe/form/SV_cZ7siSsepnvqtOS?id=%s'%(self.text_participantID.GetLabel())
        newURL = 'https://docs.google.com/forms/d/e/1FAIpQLSdZylS-xmd4rS0BdjeqWfAK2m7LfZvaRKMJZGGanh9aFRZ00A/viewform?usp=pp_url&entry.1851916630=PID%s'%(self.text_participantID.GetLabel())
        self.hyperlink_qualtrics.SetURL(newURL)
        self.hyperlink_qualtrics.SetLabel('questionnaire')


    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        grid_sizer_1 = wx.GridSizer(5, 2, 0, 0)

        count_label = wx.StaticText(self, wx.ID_ANY, "counts:")
        grid_sizer_1.Add(count_label, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.count_counts, 0, wx.ALIGN_CENTER, 0)

        label_1 = wx.StaticText(self, wx.ID_ANY, "participant ID (code):")
        grid_sizer_1.Add(label_1, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.text_participantID, 0, wx.ALIGN_CENTER, 0)

        label_2 = wx.StaticText(self, wx.ID_ANY, "pre questionnaire:")
        grid_sizer_1.Add(label_2, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.hyperlink_qualtrics, 0, wx.ALIGN_CENTER, 0)

        label_4 = wx.StaticText(self, wx.ID_ANY, "familiarization:")
        grid_sizer_1.Add(label_4, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.button_runfam, 0, wx.ALIGN_CENTER, 0)


        label_3 = wx.StaticText(self, wx.ID_ANY, "run experiment:")
        grid_sizer_1.Add(label_3, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.button_runit, 0, wx.ALIGN_CENTER, 0)

        self.SetSizer(grid_sizer_1)
        self.Layout()
        # end wxGlade

    def onRunFamiliarization(self, e):
        self.button_runit.Enable()
        print('[familiarization]')

        # PyVMEC2.runExperiment(experiment=self.task, participant='%s'%(self.text_participantID.GetLabel()))
        familiarization.runExp(ID='%s'%(self.text_participantID.GetLabel()))


    def onRunExperiment(self, e):
        self.button_runit.Disable()
        print('\n' + self.task + '\n')

        # PyVMEC2.runExperiment(experiment=self.task, participant='%s'%(self.text_participantID.GetLabel()))
        experiment_v2.runExp(ID='%s'%(self.text_participantID.GetLabel()), rotation=int(self.task[6:]))



    def onClickQualtrics(self, e):

        self.Qualtrics = {'url' : self.hyperlink_qualtrics.GetURL(),
                          'visited' : True}

        wb.open( url = self.hyperlink_qualtrics.GetURL(),
                 new = 1,
                 autoraise = True )
        
        self.button_runfam.Enable()
        # self.testEnableRunButton()


    def setIDandTask(self):

        # these are the conditions we are running:
        conditions = [  
                        'aiming20',
                        'aiming30',
                        'aiming40',
                        'aiming50',
                        'aiming60'  ]

        # we get the IDs for participants in each condition:
        existing = []
        learners = {}
        for condition in conditions:
            # pdirs = os.listdir('data/%s/'%(condition))

            print('\n%s scan...'%(condition.upper()))

            cdir = 'data/%s/'%(condition)
            cdirlist = os.listdir(cdir)
            # all content, need to select only the directories in there:
            pdirs = []
            for entry in cdirlist:
                if os.path.isdir(os.path.join(cdir, entry)):
                    pdirs += [entry]

            # cdir = os.path.join(cdir, '.')
            # print(cdir)
            # cdirgen = os.walk(cdir)
            # print(cdirgen)
            # cdircontent = next(cdirgen)
            # print(cdircontent)
            # pdirs = cdircontent[1]
            # print(pdirs)
            # pdirs = next(os.walk(os.path.join(cdir,'.')))[1]

            # print(pdirs)
            # we collect ALL existing participant IDs in one dictionary
            # to decide on a new ID that doesn't yet exist
            existing += pdirs

            # to decide on a condition, we need to have only the learners:
            # we got a list of participants, lets find the learners, using their SUMMARY files
            # the criterion is that they should be countering for at leats 50% of the rotation
            # at the end of the 120 trial rotated phase (corrected for baseline performance)

            condition_learners = []
            non_learners = []

            for folder in pdirs:
                filename = 'data/%s/%s/SUMMARY_%s_%s.csv'%(condition, folder, condition, folder)
                # print(filename)

                if not(os.path.isfile(filename)):
                    non_learners += [folder]
                    continue

                summary = pd.read_csv(filename)
                
                # calculate baseline:
                aligned = summary.loc[((summary['task_idx'] == 2) & (summary['trial_idx'] > 16)) | ((summary['task_idx'] == 4) & (summary['trial_idx'] > 4)) | (summary['task_idx'] == 6) | (summary['task_idx'] == 8) | (summary['task_idx'] == 10),]
                baseline = aligned['reachdeviation_deg'].median()

                # take the last 16 trials of the rotated phase, and apply baseline:
                rotated = summary.loc[(summary['task_idx']==12) & (summary['trial_idx']>104),]
                meandev = rotated['reachdeviation_deg'].median() - baseline
                
                # need to know the rotation to decide cutoff and direction of test:
                rotation = list(rotated['rotation_deg'])[0]
                # normalize mean reach deviation to (ideally) go positive regardless of direction of rotation:
                meandev = -1 * np.sign(rotation) * meandev
                
                # print(rotation)
                # print(meandev)

                # compared reach deviation to criterion:
                if meandev > (np.abs(rotation)/2):
                    # print('%s is a learner'%(folder))
                    condition_learners += [folder]
                else:
                    print('%s is NOT a learner'%(folder))
                    non_learners += [folder]

            print('   learners:')
            print(condition_learners)
            print('   non-learners:')
            print(non_learners)

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

        learners_counts = ' / '.join(str(l) for l in condition_Ns)
        self.count_counts.SetLabel(learners_counts)

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
