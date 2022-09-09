# modules
from tkinter import *
from tkinter import font
import mysql.connector as ms
from tkinter import colorchooser
from tkinter import ttk
from idlelib.tooltip import Hovertip

# establish connection with databse
cn=ms.connect(host='localhost', user='root', passwd='abc123', database='project')
if cn.is_connected()==False:
    print('error connecting to databse')
cursor=cn.cursor()

# variable to access clipboard
global selected
selected = False

# functions

# create new file
def new(e):
    a= text.get(1.0, END)

    def newf(e):
        text.delete('1.0',END)
        root.title('tetor - new file')
        status.config(text='new file')

    def close(e):
        bl.destroy()

    # usual new file for blank file
    if a=='':
        newf()
        
    # popup for save if it has text
    else:
        bl=Tk()
        bl.title('tetor')
        c=Label(bl, text='do u wish to save changes ?')
        d=Button(bl, text='yes', command=saveas )
        e=Button(bl, text='no', command= lambda: [newf(False), close(False)] )
        c.pack()
        d.pack(side = LEFT, padx=20, pady=10)
        e.pack(side=RIGHT, padx=20, pady=10)


# open file
def openfile(e):
    boom = Tk()
    boom.title('search file')
    name=StringVar()

    #search execution
    def search():
        try:
            a=nentry.get()
        
            cursor.execute('select * from tetor where title = %s', (a,))
            data= cursor.fetchone()

            text.delete('1.0',END)
            text.insert(END, str(data[1]))
            name.set('')
            boom.destroy()
            #update tetor
            root.title(f'tetor - {a}')
            status.config(text=f'file_name: {a}')

        except TypeError:
            x=Label(boom, text='file not found!!!!!')
            x.grid( row=3)
            y=Label(boom, text='type name again')
            y.grid( row=4)
    
    #popup   
    nlabel= Label(boom, text='enter file name')
    nentry= ttk.Combobox(boom, width = 17, textvariable = name)
    cursor.execute('select title from tetor' )
    data= cursor.fetchall()
    nentry['values'] = data
    sub = Button(boom, text = 'search', command = search, )
    nlabel.grid (row=0 , column=0)
    nentry.grid (row=0, column =1)
    sub.grid(row=1, column =1)


# saveas in database
def saveas():
    boom = Tk()
    boom.title('save file')
    name=StringVar()

    # saveas execution
    def ok():
        try:
            a= nentry.get()
            b= text.get(1.0, END)
            cursor.execute("insert into tetor values (%s,%s)", (a,b))
            cn.commit()
            name.set('')
            boom.destroy()
            
            # confirmation
            bcd=Tk()
            c=Label(bcd, text='file has been saved')
            d=Button(bcd, text='OK', command=bcd.destroy)
            c.pack()
            d.pack()
       
        except :
            x=Label(boom, text='file already exists')
            x.grid( row=3)
            y=Label(boom, text='try with another name')
            y.grid( row=4)
             
    #popup   
    nlabel= Label(boom, text='enter file name')
    nentry= Entry(boom, textvariable = name)
    sub = Button(boom, text = 'save', command = ok, )
    nlabel.grid (row=0 , column=0)
    nentry.grid (row=0, column =1)
    sub.grid (row=1, column =1)
    

# save/update in database
def savef(e):
    x= text.get(1.0, END)

    # save for new file calls save as
    y=status['text']
    if 'file_name' not in y:
        saveas()

    # normal save function
    else:
        z=y[11:]
        cursor.execute("update tetor set summary = %s where title = %s", (x,z))
        cn.commit()

        #popup
        bcd=Tk()
        c=Label(bcd, text='file has been saved')
        d=Button(bcd, text='OK', command=bcd.destroy)
        c.pack()
        d.pack()


# cut
def cut(e):
    global selected
    # check if shortcut is used
    if e:
        selected = root.clipboard_get()
    
    else:
        if text.selection_get():
            #grab the text
            selected = text.selection_get()
            # delet the text
            text.delete('sel.first','sel.last')
            #clear clipboard n add
            root.clipboard_clear()
            root.clipboard_append(selected)

        
# copy
def copy(e):
    global selected
    # check if shortcut is used
    if e:
        selected = root.clipboard_get()
    
    if text.selection_get():
        #grab the text
        selected = text.selection_get()
        #clear clipboard n add
        root.clipboard_clear()
        root.clipboard_append(selected)


# paste
def paste(e):
    global selected
    # check if shortcut used
    if e:
        selected = root.clipboard_get()
    
    else:
        if selected:
            position = text.index(INSERT)
            text.insert(position, selected)


#bold
def bold():
  #create font
  bold_font = font.Font(text, text.cget('font'))
  bold_font.configure(weight = 'bold')

  #configure a tag
  text.tag_configure('bold', font = bold_font)

  #define current tags
  current_tags = text.tag_names('sel.first')

  # to see if tag has been set
  if 'bold' in current_tags:
    text.tag_remove('bold', 'sel.first', 'sel.last')
  else:
    text.tag_add('bold', 'sel.first', 'sel.last')

 
#italic
def italic():
  #create font
  italic_font = font.Font(text, text.cget('font'))
  italic_font.configure(slant = 'italic')

  #configure a tag
  text.tag_configure('italic', font = italic_font)

  #define current tags
  current_tags = text.tag_names('sel.first')

  # to see if tag has been set
  if 'italic' in current_tags:
    text.tag_remove('italic', 'sel.first', 'sel.last')
  else:
    text.tag_add('italic', 'sel.first', 'sel.last')


#underline
def underline():
  #create font
  underline_font = font.Font(text, text.cget('font'))
  underline_font.configure(underline = 1)

  #configure a tag
  text.tag_configure('underline', font = underline_font)

  #define current tags
  current_tags = text.tag_names('sel.first')

  # to see if tag has been set
  if 'underline' in current_tags:
    text.tag_remove('underline', 'sel.first', 'sel.last')
  else:
    text.tag_add('underline', 'sel.first', 'sel.last')


#overstrike
def overstrike():
  #create font
  overstrike_font = font.Font(text, text.cget('font'))
  overstrike_font.configure(overstrike = 1)

  #configure a tag
  text.tag_configure('overstrike', font = overstrike_font)

  #define current tags
  current_tags = text.tag_names('sel.first')

  # to see if tag has been set
  if 'overstrike' in current_tags:
    text.tag_remove('overstrike', 'sel.first', 'sel.last')
  else:
    text.tag_add('overstrike', 'sel.first', 'sel.last')

#change font stles
def configure():
    #popup
    boom = Tk()
    boom.title('configure tetor')
    name=StringVar()
    surname=StringVar()

    def shane():
        try:
            f = a1.get()
            g = a2.get()
            fontstyle.configure(family = f, size = g)
            boom.destroy()
        except:
            x=Label(boom, text='enter valid size (natural numbers only)')
            x.grid( row=3)
                     
    q1 = Label(boom, text='enter font name')
    a1 = ttk.Combobox(boom, width = 17, textvariable = name)
    a1['values'] = ('arial','calibri','cambria','courier new','futura','garamond','helvetica','verdana')
    a1.insert(0, fontstyle['family'])
    q2 = Label(boom, text='enter font size')
    a2 = Entry(boom, textvariable = surname)
    a2.insert(0, fontstyle['size'])
    sub = Button(boom, text = 'set changes', command = shane, )
    q1.grid (row=0 , column=0)
    a1.grid (row=0, column =1)
    q2.grid (row=1 , column=0)
    a2.grid (row=1, column =1)
    sub.grid (row=2, column =1)
        

#change selected text colour
def text_colour():
  #pick a colour
  my_colour= colorchooser.askcolor()[1]
  if my_colour:
      #create a font
      colour_font = font.Font(text, text.cget('font'))
      
      #configure a tag
      text.tag_configure('coloured', font=colour_font, foreground=my_colour)

      #define current tags
      current_tags = text.tag_names('sel.first')

      # to see if tag has been set
      if 'coloured' in current_tags:
        text.tag_remove('coloured', 'sel.first', 'sel.last')
      else:
        text.tag_add('coloured', 'sel.first', 'sel.last')


#change all text colour
def alltextcolour():
    my_colour= colorchooser.askcolor()[1]
    if my_colour:
        text.config(fg=my_colour)


#change bg colour
def bgcolour():
    my_colour= colorchooser.askcolor()[1]
    if my_colour:
        text.config(bg=my_colour)


def caps():
    global selected
    selected = text.selection_get()
    # delete the text
    text.delete('sel.first','sel.last')
    #program
    selected = selected.upper()
    position = text.index(INSERT)
    text.insert(position, selected)

    
def lows():
    global selected
    selected = text.selection_get()
    # delete the text
    text.delete('sel.first','sel.last')
    #program
    selected = selected.lower()
    position = text.index(INSERT)
    text.insert(position, selected)


# horizontal scrollbar
def unwrap():
    if var.get()==1:
        xscroll.pack(side=BOTTOM, fill=X)
        text.configure(wrap='none', xscrollcommand= xscroll.set, )
        xscroll.config(command=text.xview)
    else:
        text.configure(wrap=WORD, xscrollcommand=0, )
        xscroll.forget()


# master window
root=Tk()
root.title('tetor - untitled')
root.geometry('900x500')

#toolbar frame
toolbar_frame = Frame(root)
toolbar_frame.pack(fill= X)

#frame
frame = Frame(root)
frame.pack(fill = BOTH, pady=5 , padx=5)

#scrollbar
xscroll = Scrollbar(frame, orient='horizontal')
yscroll = Scrollbar(frame)
yscroll.pack(side=RIGHT, fill=Y)

#text widget
fontstyle = font.Font(family = 'courier new', size = 15)
text = Text(frame, font= fontstyle, selectbackground='yellow', selectforeground='black',
            undo=True, yscrollcommand=yscroll.set, ) 
text.pack(fill = BOTH)

#sync scrollbar with text
yscroll.config(command=text.yview)

# status bar
status = Label(root, text='start', anchor=W, font = ('arial',10))
status.place(relx=0.0, rely=1.0, anchor='sw')

# menu section
menuframe = Menu(root)
root.config(menu=menuframe)

#file menu
filemenu = Menu(menuframe, tearoff=False)
menuframe.add_cascade(label='file', menu=filemenu)

#submenus
filemenu.add_command(label='new', accelerator= 'Ctrl+n', command= lambda: new(False))
filemenu.add_command(label='open', accelerator= 'Ctrl+o', command= lambda: openfile(False))
filemenu.add_command(label='save', accelerator= 'Ctrl+s', command= lambda: savef(False))
filemenu.add_command(label='save as', command= saveas)
filemenu.add_separator()
filemenu.add_command(label='exit', command=root.destroy)

#edit menu
editmenu = Menu(menuframe, tearoff=False)
menuframe.add_cascade(label='edit', menu=editmenu)

#submenus
editmenu.add_command(label='cut', accelerator= 'Ctrl+x', command=lambda: cut(False))
editmenu.add_command(label='copy', accelerator= 'Ctrl+c', command= lambda: copy(False))
editmenu.add_command(label='paste', accelerator= 'Ctrl+v', command= lambda: paste(False))
editmenu.add_separator()
editmenu.add_command(label='undo', accelerator= 'Ctrl+z', command= text.edit_undo)
editmenu.add_command(label='redo', accelerator= 'Ctrl+y', command= text.edit_redo)

#format menu
formatmenu = Menu(menuframe, tearoff=False)
menuframe.add_cascade(label='format', menu=formatmenu)

#submenus
var=IntVar()
formatmenu.add_checkbutton(label='unwrap text', variable=var, onvalue=1, offvalue=0, command=unwrap)
formatmenu.add_separator()
formatmenu.add_command(label='configure', command= configure,)
formatmenu.add_separator()
formatmenu.add_command(label='bold', command= bold,)
formatmenu.add_command(label='italics', command= italic,)
formatmenu.add_command(label='underline', command= underline,)
formatmenu.add_command(label='overstrike', command= overstrike,)

#colour menu
colourmenu = Menu(menuframe, tearoff=False)
menuframe.add_cascade(label='colours', menu=colourmenu)

#submenus
colourmenu.add_command(label='selected text', command=text_colour)
colourmenu.add_command(label='all text', command= alltextcolour)
colourmenu.add_separator()
colourmenu.add_command(label='background', command= bgcolour)

#toolbar frame
i1 = PhotoImage(file= 'assets/bold.png')
i2 = PhotoImage(file= 'assets/italic.png')
i3 = PhotoImage(file= 'assets/underline.png')
i4 = PhotoImage(file= 'assets/overstrike.png')
i5 = PhotoImage(file= 'assets/undo.png')
i6 = PhotoImage(file= 'assets/redo.png')

# undo/redo buttons
undo = Button(toolbar_frame, image = i5, command = text.edit_undo)
undo.grid (row=0, column=0, padx=5 )
redo = Button(toolbar_frame, image = i6, command = text.edit_redo)
redo.grid (row=0, column=1, padx=5)

space= Label(toolbar_frame, text='        ').grid(row=0,column=2)

'''ff = ttk.Combobox(toolbar_frame, width = 15,)
ff['values'] = ('arial','calibri','cambria','courier new','futura','garamond','helvetica','verdana')
ff.insert(0, fontstyle['family'])
ff.grid (row=0, column=10, padx=5)
gg = ttk.Combobox(toolbar_frame,width = 5)
gg.insert(0, fontstyle['size'])
ff.grid (row=0, column=11, padx=5)
fontstyle.configure'''

space= Label(toolbar_frame, text='        ').grid(row=0,column=2)

bold = Button(toolbar_frame,image = i1, command = bold, )
bold.grid (row=0, column=3, padx=5)
ital = Button(toolbar_frame,image = i2, command = italic)
ital.grid (row=0, column=4, padx=5)
under = Button(toolbar_frame,image = i3, command = underline)
under.grid (row=0, column=5, padx=5)
over = Button(toolbar_frame,image = i4, command = overstrike)
over.grid (row=0, column=6, padx=5)

space= Label(toolbar_frame, text='        ').grid(row=0,column=7)

caps = Button(toolbar_frame, text = 'aA',font = 'consolas 11 bold' ,command = caps)
caps.grid (row=0, column=8, padx=5, ipady=0)
lows = Button(toolbar_frame, text = 'Aa',font = 'consolas 11 bold' , command = lows)
lows.grid (row=0, column=9, padx=5, ipady=0)

Hovertip(undo, 'Undo (Ctrl+Z)\nReverses the last action')
Hovertip(redo, 'Redo (Ctrl+Y)\nRepeats the last action')
Hovertip(bold, 'Bold\nChange selected text to heavier font')
Hovertip(ital, 'Italic\nChange selected text to italic font')
Hovertip(under, 'Underline\nDraw a line below selected text')
Hovertip(over, 'Overstrike\nDraw a line over selected text')
Hovertip(caps, 'Change selected text to upper case')
Hovertip(lows, 'Change selected text to lower case')

# event bindings
root.bind('<Control-Key-n>', new)
root.bind('<Control-Key-o>', openfile)
root.bind('<Control-Key-s>', savef)

root.bind('<Control-Key-x>', cut)
root.bind('<Control-Key-c>', copy)
root.bind('<Control-Key-v>', paste)

root.mainloop()