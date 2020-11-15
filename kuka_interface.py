import tkinter as tk

def widgets(window,command:list):

# here we start the gui window
# change the background's colors
    
    window.config(bg="black")
    window.title("JASS")
# the button to export the info (not yet implemented)
    export_ = tk.Button(
    master=window,
    bg="orange",
    text="execute\ncommand",
    width=17
    )

    email_n = tk.Text(
    master=window,
    bg="black",
    fg='white',
    height=2,
    width=16
    )

# button for start all the robot 

    on = tk.Button(
    master=window,
    bg="lime",
    text="turn on",
    command=command[0],
    width=17
    )

# button to turn off all the robot's system
    shout = tk.Button(
    master=window,
    bg="red",
    text="turn off",
    command=command[1],
    width=17
    )
    
# button to start the emergency system
    emergency = tk.Button(
    master=window,
    bg="red",
    text="emergency\nalarm",
    width=17
    )
# the label for the gui 
    info = tk.Label(
    master=window,
    bg='black',
    fg='white',
    text='JASS gui 0.1'
    )
# then just gather all widgets on the window 
    on.grid(row=1,column=0)
    shout.grid(row=1,column=1)
    email_n.grid(row=2,column=1)
    export_.grid(row=2,column=0)
    emergency.grid(row=3,column=0)
    info.grid(row=3,column=1)

    window.mainloop()
