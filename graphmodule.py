from tkinter import *
from matplotlib.figure import Figure
from matplotlib import pyplot as pt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import time

class Graph():
    def __init__(self,window,width=2,height=2) -> None:
        self.canvas_created = False
        self.window = window
        self.canvas = None
        self.title='none'
        
        self.Figure = Figure(figsize = (width, height),
                dpi = 100) 
        self.sub_plot = self.Figure.add_subplot(frameon=False)    
        
    
    def set_title(self,title="none"):
        self.title = title
        self.sub_plot.set_title(title) 
        self.x_axis_label = title

    def set_background_color(self,color):
        self.sub_plot.set_facecolor(color)

    def set_x_axis_label(self,label):
        self.sub_plot.set_xlabel(label)             


    def set_y_axis_label(self,label):
        self.sub_plot.set_ylabel(label)

    def create_canvas(self):
        self.canvas = FigureCanvasTkAgg(self.Figure,
                                master = self.window)
        # canvas.draw()
        
        self.canvas_created = True
        
    def destroy_canvas(self):
        if self.canvas_created == True:
            self.canvas.get_tk_widget().destroy()
        else:
            return None

    def show_canvas(self):
        if self.canvas_created == True:
            self.canvas.draw()
            self.canvas.get_tk_widget().pack()

    
    def plot(self,y_list):
        if self.canvas_created != True:
            self.create_canvas()
            self.plot(y_list=y_list)
            self.show_canvas()
            # plot1 = self.Figure.add_subplot(111)    
            # plot1.plot(y_list)

        elif self.canvas_created == True:
            self.sub_plot.plot(y_list)

    def update_plot(self,y_list):
        if self.canvas_created == True:
            self.destroy_canvas()
            self.create_canvas()
            self.plot(y_list)
            self.show_canvas()
    



def play_array(arr):
    new_arr = [] 
    for i in arr:
        x = (i+1) * i
        new_arr.append(x)
    
    return new_arr




       
# val = [0.820,0.822,0.829,0.525,0.55,0.91,0.922,0.97,0.89]


# # # the main Tkinter window
# window = Tk()

# # setting the title
# window.title('Plotting in Tkinter')
# lbl = Label(window)
# lbl.pack()
# # dimensions of the main window
# window.geometry("500x500")



# g = Graph(window=lbl,width=5,height=10)
#g.set_title("Madhav")
# g.set_x_axis_label("time")
# g.set_y_axis_label("distance")
# g.plot(val)#

# window.mainloop()
