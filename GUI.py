from TravellingSalesPerson import *
import numpy as np
import matplotlib.pyplot as plt


try:
    import wx
except ImportError:
    print("The wxPython module is required to run this program")


class myGUI(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)
        self. parent = parent
        self.pnl = wx.Panel(self)
        self.fileBox = wx.TextCtrl(self.pnl, style=wx.TE_PROCESS_ENTER, pos=(10, 50), size=(75, 25))

        self.st = wx.StaticText(self.pnl, label="TSP Solver", pos=(5, 5))
        font = self.st.GetFont()
        font.PointSize += 10
        self.st.SetFont(font)

        add = wx.Button(self.pnl, pos=(10, 100), label="Add")
        self.Bind(wx.EVT_BUTTON, self.onButton, add)
        fetch = wx.Button(self.pnl, pos=(105, 100), label="Fetch")
        self.Bind(wx.EVT_BUTTON, self.onButton, fetch)
        solve = wx.Button(self.pnl, pos=(200, 100), label="Solve")
        self.Bind(wx.EVT_BUTTON, self.onButton, solve)
        show = wx.Button(self.pnl, pos=(295, 100), label="Show")
        self.Bind(wx.EVT_BUTTON, self.onButton, show)

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


if __name__ == "__main__":
    app = wx.App()
    frame = myGUI(None, -1, "TSP Solver")
    app.MainLoop()
