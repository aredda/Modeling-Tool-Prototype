from tkinter import * 

def moveV(coords: list, offset: int):
    return [(cTuple[0], cTuple[1] + offset) for cTuple in coords]

def moveH(coords: list, offset: int):
    return [(cTuple[0] + offset, cTuple[1]) for cTuple in coords]

fillColor = 'indigo'
charWidth = 100 
charHeight = 25
paintWeight = 10

window = Tk()
window.configure (width=800, height=600)
window.pack_propagate (0)

panel = Frame(master=window, pady=20, padx=20, height=100, bg='white')
panel.pack_propagate (0)
panel.pack (fill=BOTH)

lbl_weight = Label(master=panel, text='Paint Weight: ', bg='white')
lbl_weight.pack (side=LEFT)

scl_weight = Scale(master=panel, bg='white', orient='horizontal', from_=5, to=50)
scl_weight.pack (side=LEFT, fill=BOTH)

lbl_color = Label(master=panel, text='Paint Color: ', bg='white')
lbl_color.pack (side=LEFT)

ent_color = Entry(master=panel, bg='white')
ent_color.insert(0, "indigo")
ent_color.pack(side=LEFT)

canvas = Canvas(master=window)
canvas.pack (fill=BOTH, expand=True)

toDrag = None

def onMouseMoveDrag(event):
    print (canvas.coords (toDrag))

def onMouseClick(event):
    global toDrag
    toDrag = canvas.find_closest (event.x, event.y)
    print (toDrag)

def onDeleteItem(event):
    item = canvas.find_closest (event.x, event.y)
    canvas.delete (item)

def onCreateItem(event):
    x = event.x - paintWeight/2
    y = event.y - paintWeight/2
    
    item = canvas.create_oval([
        (x, y),
        (x + paintWeight, y + paintWeight)
    ], fill=fillColor, width=0)

    canvas.tag_bind(item, '<Button-2>', onMouseClick)

def onMouseMoveCreate(event):
    global paintWeight, fillColor
    paintWeight = scl_weight.get()
    fillColor = ent_color.get()
    onCreateItem(event)

def onMouseMoveDelete(event):
    onDeleteItem(event)

canvas.bind('<B2-Motion>', onMouseMoveDrag)
canvas.bind('<B1-Motion>', onMouseMoveCreate)
canvas.bind('<B3-Motion>', onMouseMoveDelete)

window.mainloop ()