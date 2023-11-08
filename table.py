import tkinter 

root = tkinter.Tk()


param_grid = tkinter.Frame(root)
param_grid.pack()    

#column config
param_grid.columnconfigure(0,weight=1)
param_grid.columnconfigure(1,weight=1)
#row config 
param_grid.rowconfigure(0,weight=1)
param_grid.rowconfigure(1,weight=1)
param_grid.rowconfigure(2,weight=1)
param_grid.rowconfigure(3,weight=1)
param_grid.rowconfigure(4,weight=1)

param_lbl = ['speed','headway','flow','accuracy','density','roadbreadth']
param_value = [45,60,12,15,30,20]
f = [] 
for i in range(0,5):
    f.append(tkinter.Label(param_grid,height=2,relief=tkinter.RIDGE))
    f[i].columnconfigure(0,weight=1)
    f[i].rowconfigure(0,weight=1)
    f[i].grid(row=i,column=0,sticky = 'nsew')

l = [] 
for i in range(0,5):
    if i % 2 == 0:
        color = 'white'
        rel = tkinter.RAISED
    else:
        color = 'white'
        rel = tkinter.RAISED
    l.append(tkinter.Label(f[i],text=str(param_lbl[i]),bg=color,height=2))
    l[i].grid(row=i,column=0,sticky = 'nsew')

l2 = [] 
for i in range(0,5):
    if i % 2 == 0:
        color = 'white'
        rel = tkinter.RAISED
    else:
        color='white'
        rel = tkinter.RAISED

    l2.append(tkinter.Label(f[i],text=str(i),anchor='center',bg=color,height=2,width=4))
    l2[i].grid(row=i,column=1,sticky='nsew')



root.mainloop()