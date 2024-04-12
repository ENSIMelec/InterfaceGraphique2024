from tkinter import *

window=Tk()
window.title("Maps")
window.geometry("1000x667")



width=1000
height=667
image=PhotoImage(file="vinyle_table_2024_FINAL_V1.png")

canvas=Canvas(window, width=width, height=height)
canvas.create_image(width/2,height/2,image=image)
canvas.pack(expand=YES)
window.mainloop()


vinyle_table_2024_FINAL_V1

Stratégie N°1 Bleu

Stratégie N°1 Jaune

STRATEGIE