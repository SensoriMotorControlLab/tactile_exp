import os, shutil

def collectSummaryFiles():
    

    # make the DIRECTORIES?

    # these are the conditions we are running:
    conditions = [  'aiming20',
                    'aiming30',
                    'aiming40',
                    'aiming50',
                    'aiming60'  ]

    for condition in conditions:
        # print('\n%s scan...'%(condition.upper()))

        cdir = 'data/%s/'%(condition)
        cdirlist = os.listdir(cdir)
        # all content, need to select only the directories in there:
        pdirs = []
        for entry in cdirlist:
            if os.path.isdir(os.path.join(cdir, entry)):
                pdirs += [entry]


        for folder in pdirs:
            filename = 'data/%s/%s/SUMMARY_%s_%s.csv'%(condition, folder, condition, folder)
            # print(filename)

            if not(os.path.isfile(filename)):
                # could move the folder elsewhere?
                continue

            shutil.copyfile(filename, '/home/explicit/Desktop/Summary Files/SUMMARY_%s_%s.csv'%(condition, folder))

    shutil.make_archive('/home/explicit/Desktop/Summary_Files', 'zip', '/home/explicit/Desktop/Summary Files/')

                
