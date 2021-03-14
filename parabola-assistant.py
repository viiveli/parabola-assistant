from tkinter import Tk, Canvas, Entry, Button, Label, Frame, BOTTOM, BOTH, TOP, SUNKEN, W, X
from numpy import arange
from numpy.linalg import solve
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

class GUI:
    def __init__(self, master):
        self.master = master
        master.geometry('800x600')
        master.title('Parabola-assistant')

        self.graph_frame = Frame()
        self.graph_frame.pack(side=TOP, fill=BOTH, expand=1)

        self.canvas = Canvas(self.graph_frame)
        self.canvas.pack(fill=BOTH, expand=1)

        self.entry_frame = Frame()
        self.entry_frame.pack()

        self.x1y1_label = Label(self.entry_frame, text='x1, y1')
        self.x1y1_label.grid(row=0, column=0, padx=5, pady=5)
        self.x1y1_entry = Entry(self.entry_frame, fg='red')
        self.x1y1_entry.insert(0, '-1, -1')
        self.x1y1_entry.grid(row=0, column=1, padx=5, pady=5)

        self.x2y2_label = Label(self.entry_frame, text='x2, y2')
        self.x2y2_label.grid(row=1, column=0, padx=5, pady=5)
        self.x2y2_entry = Entry(self.entry_frame, fg='green')
        self.x2y2_entry.insert(0, '0, 1')
        self.x2y2_entry.grid(row=1, column=1, padx=5, pady=5)

        self.x3y3_label = Label(self.entry_frame, text='x3, y3')
        self.x3y3_label.grid(row=2, column=0, padx=5, pady=5)
        self.x3y3_entry = Entry(self.entry_frame, fg='blue')
        self.x3y3_entry.insert(0, '1, -1')
        self.x3y3_entry.grid(row=2, column=1, padx=5, pady=5)

        self.calculate_button = Button(self.entry_frame, text='Calculate', command=calculate)
        self.calculate_button.grid(row=1, column=2, padx=5, pady=5)

        self.statusbar = Label(self.master, bd=1, relief=SUNKEN, anchor=W)
        self.statusbar.pack(side=BOTTOM, fill=X)

    def clear_reinit_graph(self):
        self.canvas.destroy()

        self.canvas = Canvas(self.graph_frame)
        self.canvas.pack(fill=BOTH, expand=1)

def calculate():
    try:
        main_gui.clear_reinit_graph()

        # Get thre three known points
        x1,y1 = [float(main_gui.x1y1_entry.get().split(',')[0]), float(main_gui.x1y1_entry.get().split(',')[1].strip())]
        x2,y2 = [float(main_gui.x2y2_entry.get().split(',')[0]), float(main_gui.x2y2_entry.get().split(',')[1].strip())]
        x3,y3 = [float(main_gui.x3y3_entry.get().split(',')[0]), float(main_gui.x3y3_entry.get().split(',')[1].strip())]

        # Init matrices from known points
        M1 = [[x1**2, x1, 1], [x2**2, x2, 1], [x3**2, x3, 1]]
        M2 = [[y1], [y2], [y3]]

        # Solve the equation
        a, b, c, = solve(M1, M2)[0][0], solve(M1, M2)[1][0], solve(M1, M2)[2][0]

        main_gui.statusbar.configure(text=f'Equation: {round(a, 3)}x^2 + {round(b, 3)}x + {round(c, 3)}'.replace('+ -', '- '))

        # Define x range for which to calc parabola
        x_pos=arange(min(x1, x2, x3), max(x1, x2, x3), max(x1, x2, x3)/10)
        y_pos=[]

        # Calculate y values 
        for x in x_pos:
            y_pos.append((a*(x**2))+(b*x)+c)

        fig = Figure(figsize=(5, 4), dpi=100)
        plot = fig.add_subplot(111)
        
        plot.plot(x_pos, y_pos, linestyle='-.', color='black') # parabola line
        plot.scatter(x_pos, y_pos, color='gray') # parabola points
        plot.scatter(x1,y1,color='r',marker="D",s=50) # 1st known xy
        plot.scatter(x2,y2,color='g',marker="D",s=50) # 2nd known xy
        plot.scatter(x3,y3,color='b',marker="D",s=50) # 3rd known xy
        plot.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.8)
        plot.minorticks_on()
        plot.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)

        canvas = FigureCanvasTkAgg(fig, master=main_gui.canvas)  # A tk.DrawingArea.

        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, main_gui.canvas)
        toolbar.update()
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
        
    except:
        main_gui.statusbar.configure(text='Error')

root = Tk()
main_gui = GUI(root)

calculate()

root.mainloop()
