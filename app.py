from tkinter import *
from tkinter import messagebox
from models.link import *

fillColor = 'white'
fillHoverColor = 'lightskyblue'
borderColor = 'dodgerblue'
borderWidth = 2
linkColor = '#0069c0'
linkWidth = 3
rectSize = 50

createMethod = None;
createMode = False;
linkMode = False;

toDrag = None
toCreate = None
toLink = []

linkInstances = []
links = {}

window = Tk()
window.pack_propagate (0)
window.title ('Modeling Tool Prototype')

frm_control = Frame(master=window, height=50, pady=15, padx=15)
frm_control.pack(fill=BOTH)

canvas = Canvas(master=window)

cnv_rect = Canvas(master=frm_control, height=20, width=20)
cnv_circle = Canvas(master=frm_control, height=20, width=20)

def onSelect(e):
    global createMethod
    condition = e.widget is cnv_rect
    cnv_rect.itemconfig(1, fill=('limegreen' if condition else 'white'))
    cnv_circle.itemconfig(1, fill=('white' if condition else 'limegreen'))
    createMethod = canvas.create_rectangle if e.widget is cnv_rect else canvas.create_oval

cnv_rect.pack (side=LEFT)
cnv_rect.create_rectangle(5, 5, 20, 20, fill='white', width=2, outline='black')

cnv_circle.pack (side=LEFT)
cnv_circle.create_oval(5, 5, 20, 20, fill='white', width=2, outline='black')

cnv_rect.bind ('<Button-1>', onSelect)
cnv_circle.bind ('<Button-1>', onSelect)

btn_create = Button(master=frm_control, text='Create Shape', padx=15, pady=5, relief=FLAT, bg='limegreen', fg='white')
btn_create.pack (side=LEFT, padx=15)

btn_link = Button(master=frm_control, text='Link 2 Shapes', padx=15, pady=5, relief=FLAT, bg='dodgerblue', fg='white')
btn_link.pack (side=LEFT)

btn_exit = Button(master=frm_control, text='Close', padx=12, pady=5, relief=FLAT, bg='tomato', fg='white', command=window.destroy)
btn_exit.pack(side=RIGHT)

canvas.configure(bg='white')
canvas.pack(fill=BOTH, expand=True)

def correctPosition (x, y):
    xc = x - rectSize/2
    yc = y - rectSize/2
    return (xc, yc)

def onCreateClick (e):
    global toCreate
    if createMode is True:
        # Correct Create Position
        x1, y1 = e.x, e.y
        # Create Rectangle
        toCreate = createMethod(
            (x1, y1),
            (x1, y1),
            fill=fillColor,
            outline=borderColor,
            width=borderWidth,
            activefill='lightskyblue'
        )
    elif linkMode is True:
        onLink(e)

def onCreateMove (e):
    if createMode is False: return
    if toCreate is not None:
        x0 = canvas.coords(toCreate)[0]
        y0 = canvas.coords(toCreate)[1]
        canvas.coords(toCreate, x0, y0, e.x, e.y)

def onRelease (e):
    global toCreate, toDrag
    toCreate = None
    toDrag = None

def onMarkToDrag (e):
    global toDrag
    x, y = correctPosition(e.x, e.y)
    toDrag = canvas.find_overlapping(x, y, x + rectSize/2, y + rectSize/2)
    if type(toDrag) is tuple:
        if len(toDrag) > 0: 
            toDrag = toDrag[-1]

def onDrag (e):
    global toDrag
    if toDrag is not None:
        if toDrag in linkInstances:
            toDrag = None
            return
        xOff, yOff = e.x, e.y
        xs = canvas.coords(toDrag)[0]
        ys = canvas.coords(toDrag)[1]
        xe = canvas.coords(toDrag)[2] + (xOff - xs)
        ye = canvas.coords(toDrag)[3] + (yOff - ys)
        canvas.coords(toDrag, xOff, yOff, xe, ye)
        if toDrag in links:
            for link in links[toDrag]:
                link.update_link()

def enableLinkMode(e):
    global linkMode, createMode
    linkMode = True
    createMode = False
    toLink.clear ()

def enableCreateMode(e):
    global createMode, createMethod
    if createMethod is None:
        createMethod = canvas.create_rectangle
        cnv_rect.itemconfig(1, fill='limegreen')
    createMode = True
    linkMode = False

def onLink(e):
    global linkMode, links

    x, y = correctPosition(e.x, e.y)
    targets = canvas.find_overlapping(x, y, x + rectSize/2, y + rectSize/2)

    if type(targets) is tuple:
        if len(targets) > 0:
            targets = targets[-1]

    if targets in linkInstances:
        return
    
    toLink.append (targets)

    if targets not in links:
        links[targets] = []
    
    if len(toLink) > 1:
        # Create link
        link = Link(toLink[0], toLink[1], canvas)
        # Draw link
        lineItem = link.draw_link(width=linkWidth, fill=linkColor)
        # Save the link
        linkInstances.append (lineItem)
        for item in toLink: links[item].append (link)
        # If link is drawn then disable linking mode
        linkMode = False
        toLink.clear()

btn_create.bind('<Button-1>', enableCreateMode)
btn_link.bind('<Button-1>', enableLinkMode)
canvas.bind('<Button-1>', onCreateClick)
canvas.bind('<B1-Motion>', onCreateMove)
canvas.bind('<ButtonRelease-1>', onRelease)
canvas.bind('<Button-2>', onLink)
canvas.bind('<Button-3>', onMarkToDrag)
canvas.bind('<B3-Motion>', onDrag)
canvas.bind('<ButtonRelease-3>', onRelease)

# Centering the window

window_width = 800
window_height = 600
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

xOff = int((screen_width - window_width) / 2)
yOff = int((screen_height - window_height) / 2) 

window.geometry(f'{window_width}x{window_height}+{xOff}+{yOff}');

link = Link(1, 2, canvas)

def onKeyPressed (e):
    if len(canvas.find_all()) > 1:
        points = []
        for port in link.get_linkable_ports().values():
            points.append (port)
        
        canvas.create_line (points, width=2, fill=borderColor)

window.bind('<Key>', onKeyPressed)
window.mainloop()