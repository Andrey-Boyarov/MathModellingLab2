import random
from tkinter import *
# import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from random import randrange
import matplotlib
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

window = Tk()
window.geometry('950x400')
cell_height = 20  # not under control
cell_width = 8

# Global variables
g_impact = []
g_number_of_species = []
g_increase = []
g_results = []
g_year = 0
total_text = StringVar()
time_text = StringVar()


def number_window():
    new_window = Toplevel(window)
    new_window.title("Set number of populations")
    new_window.geometry("150x60")
    txt = Entry(new_window, width=10)
    txt.place(x=10, y=10)
    txt.insert(0, '2')

    def further():
        number = int(txt.get())
        new_window.destroy()
        param_window(number)

    btn_ok = Button(new_window, text="Ok", command=further)
    btn_ok.place(x=100, y=10)


def paint_first_table(current_window, number: int, x: int, y: int):
    number_of_species = []
    increase = []
    for row in range(number):
        number_row = Entry(current_window, width=cell_width)
        number_row.place(x=x, y=y + row * cell_height)
        number_row.insert(0, "100")
        number_of_species.append(number_row)

        increase_row = Entry(current_window, width=cell_width)
        increase_row.place(x=x + cell_width * 7, y=y + row * cell_height)
        increase_row.insert(0, "-0.1")
        increase.append(increase_row)

    return number_of_species, increase


def paint_second_table(current_window, number: int, x: int, y: int):
    impact = []
    for column in range(number):
        column_array = []
        for row in range(number):
            entry = Entry(current_window, width=cell_width)
            entry.place(x=x + cell_width * 7 * column, y=y + row * cell_height)
            if row == column:
                entry.insert(0, '0')
            if row > column:
                entry.insert(0, '0.0001')
            if row < column:
                entry.insert(0, '-0.0001')
            column_array.append(entry)
        impact.append(column_array)
    return impact


def place_labels_for_tables(current_window, x1, y1, x2, y2):
    lbl1 = Label(current_window, text='Count and increase')
    lbl1.place(x=x1, y=y1)
    lbl2 = Label(current_window, text='Impact values')
    lbl2.place(x=x2, y=y2)


def param_window(number: int):
    new_window = Toplevel(window)
    new_window.title("Set params")
    new_window.geometry("400x300")
    number_of_species, increase = paint_first_table(new_window, number, 10, 65)
    impact = paint_second_table(new_window, number, 10 + 2 * 7 * cell_width + 40, 65)
    place_labels_for_tables(new_window, 10, 40, 10 + 2 * 7 * cell_width + 40, 40)

    def save():
        global g_impact
        for i in range(len(impact)):
            arr = []
            for j in range(len(impact[i])):
                arr.append(float(impact[i][j].get()))
            g_impact.append(arr)

        global g_increase
        g_increase = [float(i.get()) for i in increase]
        global g_number_of_species
        g_number_of_species = [float(i.get()) for i in number_of_species]
        new_window.destroy()

    btn_save = Button(new_window, text="Save", command=save)
    btn_save.place(x=10, y=10)


# This function is called periodically from FuncAnimation


def get_value():
    global g_results
    g_results = []
    dN = []
    for j in range(len(g_number_of_species)):
        dNj = 0
        for k in range(len(g_number_of_species)):
            dNj = dNj + g_impact[j][k] * g_number_of_species[j] * g_number_of_species[k]
        dN.append(dNj)
    for j in range(len(g_number_of_species)):
        a = g_number_of_species[j]
        if a < 2:
            g_number_of_species[j] = 0
        else:
            g_number_of_species[j] = a + dN[j] + g_increase[j]


def start():

    btn_start.place_forget()
    btn_start_alternative.place_forget()
    fig = plt.figure(figsize=(6, 3))
    fig_canvas = FigureCanvasTkAgg(fig, window)
    x = [0]
    y = []
    for i in range(len(g_number_of_species)):
        y.append([g_number_of_species[i]])

    lns = []

    for b in range(len(y)):
        ln, = plt.plot(x, y[b], '-')
        lns.append(ln)

    def update(frame):
        global i
        get_value()
        x.append(x[-1] + 1)
        print('тараканы1 = ', g_number_of_species[0])
        print('тараканы2 = ', g_number_of_species[1])
        for b in range(len(y)):
            y[b].append(g_number_of_species[b])

        for b in range(len(lns)):
            lns[b].set_data(x, y[b])

        fig.gca().relim()
        fig.gca().autoscale_view()

        total_text.set(sum(g_number_of_species))
        time_text.set(i)
        i += 1

    plt_widget = fig_canvas.get_tk_widget()
    plt_widget.place(x=10, y=50)
    animation = FuncAnimation(fig, update, interval=1)

    def stop():
        plt_widget.destroy()
        btn_stop.destroy()
        btn_start.place(x=110, y=10)
        btn_start_alternative.place(x=160, y=10)
    btn_stop = Button(window, text="Stop", command=stop)
    btn_stop.place(x=110, y=10)
    animation.save()



def start_alternative():
    btn_start.place_forget()
    btn_start_alternative.place_forget()
    fig = plt.figure(figsize=(6, 3))
    fig_canvas = FigureCanvasTkAgg(fig, window)
    x = [g_number_of_species[0]]
    y = [g_number_of_species[1]]

    ln, = plt.plot(x, y, '-')

    def update(frame):
        global i
        get_value()
        print('тараканы1 = ', g_number_of_species[0])
        print('тараканы2 = ', g_number_of_species[1])
        x.append(g_number_of_species[0])
        y.append(g_number_of_species[1])

        ln.set_data(x, y)

        fig.gca().relim()
        fig.gca().autoscale_view()

        total_text.set(sum(g_number_of_species))
        time_text.set(i)
        i += 1

    plt_widget = fig_canvas.get_tk_widget()
    plt_widget.place(x=10, y=50)
    animation = FuncAnimation(fig, update, interval=1)

    def stop():
        plt_widget.destroy()
        btn_stop.destroy()
        btn_start.place(x=110, y=10)
        btn_start_alternative.place(x=160, y=10)
    btn_stop = Button(window, text="Stop", command=stop)
    btn_stop.place(x=110, y=10)
    animation.save()



if __name__ == "__main__":
    i = 0

    btn_params = Button(window, text='Set params', command=number_window)
    btn_params.place(x=10, y=10)

    btn_start = Button(window, text='Start', command=start)
    btn_start.place(x=110, y=10)

    btn_start_alternative = Button(window, text='Start alternative', command=start_alternative)
    btn_start_alternative.place(x=160, y=10)

    total_label = Label(window, text="Species in total")
    total_label.place(x=700, y=300)
    total = Entry(window, state="readonly", textvariable=total_text)
    total.place(x=800, y=300)

    time_label = Label(window, text="Time")
    time_label.place(x=700, y=350)
    time = Entry(window, state="readonly", textvariable=time_text)
    time.place(x=800, y=350)

    window.mainloop()
