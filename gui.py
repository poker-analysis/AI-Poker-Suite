from Tkinter import * 

root = Tk()
photo = PhotoImage(file="./img/Ac.gif")
label = Label(root,image=photo)
label.photo = photo
label.pack()
root.mainloop()

