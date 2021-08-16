#Written by Roy Talman 16/8/2021
# for more support contact roytalman@gmail.com

from __future__ import unicode_literals
import numpy as np
import pandas as pd
import os
import youtube_dl
from glob import glob
import librosa
import matplotlib.pyplot as plt
import pickle
import sys

CurrentFolder = os.getcwd()
# Finel relevant segment folder
Audio_segment_Folder = CurrentFolder + '/Audio_Segment_hard/'
# labels destination folder:
LabelDest = CurrentFolder + '/Audio_Segment_hard_labels/'
# name of desired classes
Classes = sys.argv[1:]
print("List of classes to download:")
print(sys.argv[1:])
# output data sample rate
Out_SR = 20000
# maximum recordings to down load
MaxRecNum = 100  # maximum number of records


if os.path.exists(Audio_segment_Folder) == 0:
    os.mkdir(Audio_segment_Folder)
if os.path.exists(LabelDest) == 0:
    os.mkdir(LabelDest)
if not os.path.exists(os.getcwd()+'/mid_to_display_name.csv'):
    tsv_file='mid_to_display_name.tsv'
    csv_table=pd.read_table(tsv_file,sep='\t')
    csv_table.to_csv('mid_to_display_name.csv',index=False)
    tsv_file='audioset_train_strong.tsv'
    csv_table=pd.read_table(tsv_file,sep='\t')
    csv_table.to_csv('audioset_train_strong.csv',index=False)


# read data csv
TrainSet = pd.read_csv('./audioset_train_strong.csv', error_bad_lines=False)

Names = list(TrainSet[list(TrainSet.columns)[0]])

# set youtube read settings
ydl_opts = {'forcetitl|e': True,
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            }
ColumnsList = list(TrainSet.columns)

# names of classes and their code-names dictionary:
Names = pd.read_csv('./mid_to_display_name.csv',header=None)
#p
DictClass = {}
DictClassInv = {}
for i,j in zip(Names[0],Names[1]):
    DictClass[i]= j
    DictClassInv[j] = i

OldRecName = ' '
ClassesColumnsList = list(TrainSet.columns)
TrainSetList = list(TrainSet)

Id_List = []
IndRec = 0

for recName in list(set(TrainSet[ColumnsList[0]])):

    RecIndex = [i for i, x in enumerate(TrainSet[ColumnsList[0]]) if x == recName]
    ClassMapKey = list(TrainSet[ColumnsList[3]][RecIndex])
    ClassNameRec = [DictClass[i] for i in list(ClassMapKey)]

    # dowbload only if one of the words in desired classes is in current rec
    if  len(set(ClassNameRec) & set(Classes))> 0 :

        recName1 = '_'.join(recName.split('_')[:-1])
        StartTime = int(recName.split('_')[-1]) / 1000
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        #try:
            ydl.download(['http://www.youtube.com/watch?v=' + recName1])
            Files = glob(CurrentFolder + '/*.mp3')
            y, sr = librosa.load(CurrentFolder + '/' + Files[0].split('/')[-1], sr=Out_SR)
            Y_seg = y[int(StartTime * sr):int((StartTime + 10) * sr)]
            librosa.output.write_wav(Audio_segment_Folder + Files[0].split('/')[-1], Y_seg, sr)
            os.remove(CurrentFolder + '/' + Files[0].split('/')[-1])
            Id_List.append(i)
            IndRec += 1

            # save label:
            DictOut = {}
            for i, className in enumerate(ClassNameRec):
                if className in DictOut.keys():
                    DictOut[className].append(TrainSet[ColumnsList[1]][RecIndex[i]])
                    DictOut[className].append(TrainSet[ColumnsList[2]][RecIndex[i]])
                else:
                    DictOut[className] = [TrainSet[ColumnsList[1]][RecIndex[i]], TrainSet[ColumnsList[2]][RecIndex[i]]]
            with open(LabelDest + Files[0].split('/')[-1] + '.pickle', 'wb') as handle:
                pickle.dump(DictOut, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print("Good recordings downloaded: {}".format(IndRec))
        #except:
        #    print('Bad File')

    OldRecName = recName
