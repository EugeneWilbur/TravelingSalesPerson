from TravellingSalesPerson import *
import numpy as np

import matplotlib.pyplot as plt


try:
    import wx
except ImportError:
    print("The wxPython module is required to run this program")


#########################################################################################
# TO USE:                                                                               #
# All file input is just the name, no .tsp, etc. (e.g. 'a280')                          #
# Time is in seconds, and is the amount of time you would like to solve for             #
# Upload data: Uploads local file to db                                                 #
# Load data: Loads file from a db to be used locally                                    #
# Show data: shows a plot of all the points in a local file                             #
# Solve: solve a loaded file for the given time                                         #
# Display solution: displays the local solve                                            #
# Load solution: Loads a solution from the data base and displays it                    #
# Save solution: saves the last solution to the db.                                     #
#########################################################################################


GOAT = ""
dist = 0

class myGUI(wx.Frame):
    def __init__(self, *args, **kw):
        super(myGUI, self).__init__(*args, **kw, size=(900, 200))
        self.init()

    def init(self):
        pnl = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)
        progBox = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

        TimerName = wx.StaticText(pnl, label="Time: ")
        font = TimerName.GetFont()
        font.PointSize += 3
        TimerName.SetFont(font)

        fileName = wx.StaticText(pnl, label="File: ")
        font = fileName.GetFont()
        font.PointSize += 3
        fileName.SetFont(font)

        self.timerBox = wx.TextCtrl(pnl, style=wx.TE_PROCESS_ENTER, size=(100, 25))
        self.fileBox = wx.TextCtrl(pnl, style=wx.TE_PROCESS_ENTER, size=(100, 25))
        Upload = wx.Button(pnl, label="Upload Data")
        disCurSol = wx.Button(pnl, label="Display Solution")
        loadFrom = wx.Button(pnl, label="Load Data")
        solve = wx.Button(pnl, label="Solve")
        show = wx.Button(pnl, label="Show Data")
        fetch = wx.Button(pnl, label="Load Solution")
        save = wx.Button(pnl, label="Save Solution")

        self.Bind(wx.EVT_BUTTON, self.onButton, Upload)
        self.Bind(wx.EVT_BUTTON, self.onButton, fetch)
        self.Bind(wx.EVT_BUTTON, self.onButton, loadFrom)
        self.Bind(wx.EVT_BUTTON, self.onButton, solve)
        self.Bind(wx.EVT_BUTTON, self.onButton, show)
        self.Bind(wx.EVT_BUTTON, self.onButton, save)
        self.Bind(wx.EVT_BUTTON, self.onButton, disCurSol)

        progBox.Add(TimerName, 0)
        progBox.Add(self.timerBox, 0)
        progBox.AddSpacer(10)
        progBox.Add(fileName, 0)
        progBox.Add(self.fileBox, 0, 10)

        buttonSizer.Add(Upload, 0)
        buttonSizer.AddSpacer(10)
        buttonSizer.Add(loadFrom, 0)
        buttonSizer.AddSpacer(10)
        buttonSizer.Add(show, 0)
        buttonSizer.AddSpacer(10)
        buttonSizer.Add(solve, 0)
        buttonSizer.AddSpacer(10)
        buttonSizer.Add(disCurSol, 0)
        buttonSizer.AddSpacer(10)
        buttonSizer.Add(fetch, 0)
        buttonSizer.AddSpacer(10)
        buttonSizer.Add(save, 0)

        vbox.Add((0, 30))
        vbox.Add(progBox, proportion=1, flag=wx.ALIGN_CENTER)
        vbox.Add((0, 30))
        vbox.Add(buttonSizer, proportion=1, flag=wx.ALIGN_CENTER)
        vbox.Add((0, 30))

        pnl.SetSizer(vbox)
        #self.Centre()

        self.Show(True)

    def onButton(self, event):
        global GOAT
        global dist
        fn = self.fileBox.GetValue()
        fnTSP = fn + ".tsp"
        button = event.GetEventObject()
        toBeSolved = main(fn, "LoadForSolve", None)

        if button.GetLabel() == "Solve":
            solveTime = int(self.timerBox.GetValue())
            print("Solving...")
            GOAT, dist = solve(toBeSolved, solveTime)
            print("Solve Successful. ", dist)
        if button.GetLabel() == "Upload Data":
            main(fn, "ADD", fnTSP)
            print("Successfully added.")
        if button.GetLabel() == "Load Solution":
            nodes = main(fn, "SHOW", "")
            nodesOrder = main(fn, "FETCH", None)
            nodesOrder = nodesOrder[0].replace('[', '').replace(']', '').split(",")
            list1 = []
            list2 = []
            for i in nodesOrder:
                i = int(i)
                x, y = nodes[i]
                list1.append(x)
                list2.append(y)
            x = np.array(list1)
            y = np.array(list2)
            plt.plot(x, y)
            plt.show()
            print("Fetch Successful.")
        if button.GetLabel() == "Show Data":
            print("Displaying data.")
            nodes = main(fn, "SHOW", "")
            list1 = []
            list2 = []
            for (i, j) in nodes:
                list1.append(i)
                list2.append(j)
            plt.plot(list1, list2, "ob")
            plt.show()
        if button.GetLabel() == "Load Data":
            print("Loading from db.")
            main(fn, "LoadForSolve", None)
            print("Load successful.")
        if button.GetLabel() == "Save Solution":
            today = date.today()
            solveTime = int(self.timerBox.GetValue())
            print("Saving current solution.")
            format_str = """INSERT INTO Solution(Tour, TourLength, ProblemName, Author, date, Algorithm, RunningTime) VALUES ("{s}", "{d}", "{n}", "{a}", "{day}", "{Alg}", "{time}");"""
            sql_command = format_str.format(s=GOAT, d=dist, n=fn, a="5130828", day=today, Alg="Genetic", time=solveTime)
            main(fn, "SaveNewSolve", sql_command)
            print("Save successful.")
        if button.GetLabel() == "Display Solution":
            nodes = main(fn, "SHOW", "")
            list1 = []
            list2 = []
            try:
                for i in GOAT:
                    i = int(i)
                    x, y = nodes[i]
                    list1.append(x)
                    list2.append(y)
                x = np.array(list1)
                y = np.array(list2)
                plt.plot(x, y)
                plt.show()
            except UnboundLocalError:
                print("Please make a solve before trying to display local solved.")
        if button.GetLabel() == "Save Solution":
            main(fn, "SaveNewSolve", None)


if __name__ == "__main__":
    app = wx.App()
    frame = myGUI(None)
    app.MainLoop()
