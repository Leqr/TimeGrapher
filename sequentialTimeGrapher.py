from watchSoundGetter import WatchSoundGetter
from watchSoundProcesser import WatchSoundProcesser
import tkinter as tk
import os


class TimeGrapher():
    def __init__(self):
        self.secRec = 5
        self.soundGetter = WatchSoundGetter(secRec = self.secRec)
        self.soundProcesser = WatchSoundProcesser()
        self.outFile = 'data.wav'

    def ON(self):
        #setup
        self.root = tk.Tk()
        self.root.geometry("325x250")
        self.root.title('TimeGrapher')
        frame = tk.Frame(self.root)
        frame.grid()
        # reassign close button
        self.root.protocol('WM_DELETE_WINDOW', self.OFF)

        #freq radiobutton
        self.refFreq = tk.IntVar()
        self.refFreq.set(28800)  # initializing the choice, i.e. 28800

        freqs = [
            ("36000 A/h",36000),
            ("28800 A/h",28800),
            ("25200 A/h",25200),
            ("21600 A/h",21600),
            ("19800 A/h",19800),
            ("18000 A/h",18000),
        ]

        def chooseFreq():
            try:
                self.soundProcesser.setRefFrequency(self.refFreq.get())
            except:
                pass
        j = 2
        for i in freqs:
            tk.Radiobutton(frame,
                  text=i[0],
                  padx = 20,
                  variable=self.refFreq,
                  command=chooseFreq,
                  value=i[1]).grid(row = j + 1,column = 3,sticky = tk.E,padx=50)
            j +=1


        #record button
        recordB = tk.Button(frame,text="1.Record",fg="red",command = self.record)
        recordB.grid(row = 0,column = 0,sticky = tk.W,padx=10,pady = 5)


        #analyze button
        analyseB = tk.Button(frame,text="2.Analyze",command=self.analyse)
        analyseB.grid(row = 1,column = 0,sticky = tk.W,padx=10,pady = 5)

        #plot button
        plotB = tk.Button(frame,text="3.Plot Wave Form",command = self.plotWaveForm)
        plotB.grid(row = 2,column = 0,sticky = tk.W,padx=10,pady = 5)

        #record time entry box
        timeEntry = tk.Entry(frame,width = 8)
        timeEntry.insert(0,str(self.secRec))
        timeEntry.grid(row = 0, column = 3,sticky = tk.E,padx=50)

        timeButton = tk.Button(frame,text="Set record time (s)",fg="blue",command= lambda: self.timeSet(timeEntry.get()))
        timeButton.grid(row = 1,column = 3,sticky = tk.E,padx=50)

        '''
        #toggle button
        def toggle():
            if t_btn.config('text')[-1] == 'True':
                t_btn.config(text='False')
            else:
                t_btn.config(text='True')
        t_btn = tk.Button(text="True", width=12, command=toggle)
        t_btn.pack(pady=5)
        '''


        #text info analysis
        self.analysisTitle = tk.Label(frame, text= 'Analysis Data :')
        self.analysisTitle.grid(row = 4,column = 0)

        self.timeText = tk.StringVar()
        self.timeLabel = tk.Label(frame, textvariable=self.timeText)
        self.timeLabel.grid(row = 5,column = 0)
        self.errorText = tk.StringVar()
        self.errorLabel = tk.Label(frame, textvariable=self.errorText)
        self.errorLabel.grid(row = 6,column = 0)


        self.root.mainloop()

    def timeSet(self,time):
        self.soundGetter.setRecTime(time)
        self.secRec = time

    def record(self):
        self.soundGetter.openSoundStream()
        self.soundGetter.record(self.outFile)

    def analyse(self):
        dat = self.soundProcesser.analysisGUI(self.outFile)
        self.latestDeviation = dat[0]
        self.beatError = dat[1]
        self.timeText.set("{:5.2f}".format(self.latestDeviation)+ ' s/day')
        self.errorText.set("{:5.2f}".format(self.beatError)+ ' ms')

    def plotWaveForm(self):
        self.soundProcesser.plotWaveFormGUI()

    def OFF(self):

        try:
            os.remove(self.outFile)
            self.soundGetter.closeSoundStream()
        except:
            pass

        self.root.destroy()


if __name__ == '__main__':
    tool = TimeGrapher()
    tool.ON()
