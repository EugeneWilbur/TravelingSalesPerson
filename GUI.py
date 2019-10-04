from TravellingSalesPerson import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas


try:
    import wx
except ImportError:
    print("The wxPython module is required to run this program")


class myGUI(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(600, 500))
        self.parent = parent
        self.pnl = wx.Panel(self)
        fileBox = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(75, 25))

        fileName = wx.StaticText(self.pnl, label="File: ")
        font = fileName.GetFont()
        font.PointSize += 3
        fileName.SetFont(font)



        #self.fig = plt.figure()
        #plt.plot([(2, 2), (3, 3)])
        # self.axes = self.fig.add_subplot(111)
       #self.canvas = FigureCanvas(self, -1, self.fig)
        # self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        # self.sizer.Add(self.canvas, 1, wx.BOTTOM)
        # self.SetSizerAndFit(self.sizer)

        add = wx.Button(self, label="Add")
        self.Bind(wx.EVT_BUTTON, self.onButton, add)
        fetch = wx.Button(self, label="Fetch")
        self.Bind(wx.EVT_BUTTON, self.onButton, fetch)
        solve = wx.Button(self, label="Solve")
        self.Bind(wx.EVT_BUTTON, self.onButton, solve)
        show = wx.Button(self, label="Show")
        self.Bind(wx.EVT_BUTTON, self.onButton, show)


        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        #buttonSizer = wx.GridSizer(4, 2, 0)
        #buttonSizer.Add(self.canvas)

        buttonSizer.Add(fileName, 0)
        ###buttonSizer.Add(10, 0, 0)
        buttonSizer.Add(fileBox, 0)
        buttonSizer.Add(add, 0)
        buttonSizer.Add(solve, 0)
        buttonSizer.Add(fetch, 0)
        buttonSizer.Add(show, 0)

        self.SetSizer(buttonSizer)
        #sizer.Add(buttonSizer, proportion=1)

        #self.SetSizerAndFit(sizer)

        self.Show(True)

    def onButton(self, event):
        fn = self.fileBox.GetValue()
        fnTSP = fn + ".tsp"
        button = event.GetEventObject()
        if button.GetLabel() == "Add":
            main(fn, "ADD", fnTSP)
            print("Successfully added.")
        elif button.GetLabel() == "Fetch":
            nodes = main(fn, "SHOW", "")
            nodesOrder = main(fn, "FETCH", "")
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
        elif button.GetLabel() == "Solve":
            print("Solving...")
            main(fn, "SOLVE", "120")
            print("Solve Successful.")

        elif button.GetLabel() == "Show":
            print("Displaying data.")
            nodes = main(fn, "SHOW", "")
            list1 = []
            list2 = []
            for (i, j) in nodes:
                list1.append(i)
                list2.append(j)
            plt.plot(list1, list2, "ob")
            plt.show()

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)


if __name__ == "__main__":
    app = wx.App()
    frame = myGUI(None, -1, "TSP Solver")
    app.MainLoop()
