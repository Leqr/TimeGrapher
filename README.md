# TimeGrapher
## Basic mechanical watch accuracy and fault detection software

Use tkinter, pyaudio, numpy and scipy in order to perform a time domain analysis of the watch sound to give the accuracy in s/day and the beat error in ms.

For simplicity reason this program first records and then analyzes the audio file to extract the deviation per day and beat error. Keep in mind that the longer the record time is, the smaller the variance between different measurement will be.

Can be used with an headphone microphone in a really silent environment or with a piezoelectric contact microphone.

GUI can be lauched by running :
       
    python3 sequentialTimeGrapher.py        
