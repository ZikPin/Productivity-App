import customtkinter as ctk
from settings import *
from panels import *


class Window(ctk.CTkFrame):
    def __init__(self, parent, name):
        super().__init__(master=parent, fg_color=DARK_BLUE)

        self.window_name = name

    def start(self):
        print(self.window_name)
        self.place(relwidth=0.75, relheight=1, relx=0.25, rely=0, anchor="nw")

    def forget(self):
        self.place_forget()


class Timer(Window):
    def __init__(self, parent):
        super().__init__(parent=parent, name="timer")
        self.columnconfigure((0, 1, 2), weight=1, uniform="a")
        self.rowconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform="a")

        # data
        self.total_time_float = ctk.DoubleVar(value=0.0)

        StopWatchPanel(self, 0, 0, self.total_time_float, 1, 2)
        TotalTimePanel(self, 0, 4, self.total_time_float, 1, 2)
        Panel(parent=self, x=0, y=2, x_span=1, y_span=2)
        PomodoroPanel(self, 1, 0, 2, 3)
        Panel(parent=self, x=1, y=3, x_span=2, y_span=3)


class ToDo(Window):
    def __init__(self, parent):
        super().__init__(parent=parent, name="to do")


class Projects(Window):
    def __init__(self, parent):
        super().__init__(parent=parent, name="projects")


class HabitTracker(Window):
    def __init__(self, parent):
        super().__init__(parent=parent, name="habit")
