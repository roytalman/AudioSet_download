# AudioSet_download
Written by Roy Talman 16/8/2021

Python script do download audioset audio and labels

Instructions:
1.  Navigate to AudioSet web and download "audioset_train_strong.tsv" and "mid_to_display_name.tsv" to the project folder 
2. Select classes name you would like to download from "mid_to_display_name.tsv", if you would like to download all files classes you can comment line 79 "if" state
3. On terminal, cd to the folder of the project and run  "Down_save_strong_label.py" with desired classes as argument 1-N, for exmple:

     python3  Down_save_strong_label.py Cough Sneeze Whistle

to down load recordings with Cough,Sneeze and Whistle

4. Output of code - 
      - Ten seconds  ./Audio_Segment_hard/ <Original Name> .mp3 : audio data with sample rate selected in code
      - Dictionary of the noises in record ./Audio_Segment_hard_labels/ <Original Name> .mp3.pickle : Dictionary with all noises in audio segment (notice that each recordings has a few noises type, some of them are not the ones you list for, but each recording has at least one noise type that is in your input list) each noise values are the onset and offset of noise, if noise appears more then ones, the length of value will be 2*k  number off appearence, and will list all onset and offset pairs.


