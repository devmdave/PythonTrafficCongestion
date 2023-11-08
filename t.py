import tkinter as tk
import parameters
import trial

class App():
    def __init__(self):
        self.gui = tk.Tk()
        self.screen_dimensions = (self.gui.winfo_screenwidth(),self.gui.winfo_screenheight()) 
        self.gui_width =int(self.screen_dimensions[0]-100)
        self.gui_height = int(self.screen_dimensions[1]-100)
        self.gui.geometry(f'{self.gui_width}x{self.gui_height}')
        self.gui.wm_title('Traffic Flow Prediction')
        self.gui.attributes('-fullscreen', True)
        #configuring row and column size
        self.gui.columnconfigure(0, weight=1,uniform='a')
        self.gui.columnconfigure(1, weight=1,uniform='a')
        self.gui.columnconfigure(2, weight=1 ,uniform='a')
        self.gui.rowconfigure(0, weight=1)
        self.gui.rowconfigure(1, weight=1)

        self.cam_frame = tk.LabelFrame(self.gui,relief=tk.RIDGE,text='Video')
        self.cam_frame2 = tk.LabelFrame(self.gui,relief=tk.RIDGE,text='Predicted Frames')
        self.param_frame = tk.LabelFrame(self.gui,relief=tk.RIDGE,text='Model YOLO v8')
        self.param_frame2 = tk.LabelFrame(self.gui,relief=tk.RIDGE,text='Parameters')
        self.log_frame = tk.LabelFrame(self.gui,relief=tk.RIDGE,text='(Developer Option)--Logging',bg='gainsboro')
        self.functions_frame = tk.LabelFrame(self.gui,relief=tk.RIDGE,text='Functions',bg='gainsboro')

        self.cam_frame.grid(row=0,column=0,sticky='nsw',padx=10,pady=10,ipadx=10,ipady=10)
        self.cam_frame2.grid(row=1,column=0,sticky='nsw',padx=10,pady=10,ipadx=10,ipady=10)
        self.param_frame.grid(row=0,column=1,rowspan=1,sticky='nsew',padx=10,pady=10,ipadx=10,ipady=10)
        self.param_frame2.grid(row=0,column=2,rowspan=1,sticky='nsew',padx=10,pady=10,ipadx=10,ipady=10)
        self.log_frame.grid(row=1,column=1,rowspan=1,sticky='nsew',padx=10,pady=10,ipadx=10,ipady=10)
        self.functions_frame.grid(row=1,column=2,rowspan=1,sticky='nsew',padx=10,pady=10,ipadx=10,ipady=10)

##      functions here 
        self.restart_btn = tk.Button(self.functions_frame,relief=tk.RAISED,text='Restart',height=4,width=20,bg='red')
        self.stop_btn = tk.Button(self.functions_frame,relief=tk.RAISED,text='Stop',height=4,width=20,bg='red')
        self.save_to_txt = tk.Button(self.functions_frame,relief=tk.RAISED,text='Save Predictions',height=4,width=20,bg='green')
        self.change_model= tk.Button(self.functions_frame,relief=tk.RAISED,text='Change Prediction Model',height=4,width=20,bg='green')
        self.change_video = tk.Button(self.functions_frame,relief=tk.RAISED,text='Change Video Path',height=4,width=20,bg='yellow')
        self.toggle_fs = tk.Button(self.functions_frame,relief=tk.RAISED,text='Exit FullScreen',height=4,width=20,bg='yellow')
        # change_video = tk.Button(self.functions_frame,relief=tk.RIDGE,text='Change Video Path')
        # change_video = tk.Button(self.functions_frame,relief=tk.RIDGE,text='Change Video Path')
        # change_video = tk.Button(self.functions_frame,relief=tk.RIDGE,text='Change Video Path')


        self.restart_btn.grid(column=0,row=0,sticky='nsew',padx=20,pady=10,ipadx=10,ipady=10)
        self.stop_btn.grid(column=1,row=0,sticky='nsew',padx=10,pady=10,ipadx=10,ipady=10)
        self.save_to_txt.grid(column=0,row=1,sticky='nsew',padx=20,pady=10,ipadx=10,ipady=10)
        self.change_model.grid(column=1,row=1,sticky='nsew',padx=10,pady=10,ipadx=10,ipady=10)
        self.change_video.grid(column=0,row=2,sticky='nsew',padx=20,pady=10,ipadx=10,ipady=10)
        self.toggle_fs.grid(column=1,row=2,sticky='nsew',padx=10,pady=10,ipadx=10,ipady=10)
        

       
        self.cam_box = tk.Label(self.cam_frame) 
        self.cam_box2 = tk.Label(self.cam_frame2) 
        # self.t = trial.Table(self.params_frame)
        self.gui.update()
        self.data = ['speed','density','vehicles','flow','headway','accuracy','TrafficFlow(per hour)','Density(per hour)']
        self.data2 = ['Confidence(Model Yolo V8)','ModelVersion','Predictions(per frame)','Model-Name','ModelType','VehiclesGoingUp','VehiclesGoingDown']
        self.logdata = ['ProcessLogging','CPUusage','RAMusage','FrameBehavior'] 
        self.pgrid = parameters.Parameters(self.param_frame,self.data)        
        self.pgrid2 = parameters.Parameters(self.param_frame2,self.data2)        
        self.loggrid = parameters.Parameters(self.log_frame,self.logdata)        
        self.cam_box.pack(fill='both')   
        self.cam_box2.pack(fill='both')   
        
                

        

    def LoopFunctions(self,*argv):
        for i in argv:
            self.lbl_camera_fr.after(1000,i)
        
    def mainloop(self):
        self.gui.mainloop()
