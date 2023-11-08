import tkinter as tk 

class Parameters():
    def __init__(self,app,label_list,width=1,height=1):
        self.params = {}
        self.total_rows = len(label_list)
        self.total_columns = 2
        self.app = app 
        self.font = ('Arial',10)
        for index,l in enumerate(label_list):
            id_lbl = tk.Label(self.app,font=('Arial',10,'bold'),text=str(l),fg='black',bg='snow',relief=tk.SUNKEN,width=25)
            value_lbl = tk.Label(self.app,fg='black',bg='gainsboro',font=self.font,relief=tk.SUNKEN,width=25)
           
            id_lbl.grid(column=0,row=index,sticky=tk.NSEW,ipadx=5,ipady=10)
            value_lbl.grid(column=1,row=index,sticky=tk.NSEW)
            self.params[l] = (id_lbl,value_lbl)
            
        
    def update(self,id,val):        
        self.params[id][1].configure(text=str(val))