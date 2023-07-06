import customtkinter as ctk
from settings import *
from panels import *
import calendar
from datetime import datetime
import pickle


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
        self.date_now = str(datetime.now())
        self.today_date = self.format_date_time()
        self.current_month = calendar.monthcalendar(self.today_date[2], self.today_date[1])
        self.time_is_running = ctk.BooleanVar(value=False)

        self.time_data = {self.today_date: self.total_time_float.get()}

        with open("storing data/timer_data_set.pickle", "rb") as time_data_set:
            file = pickle.load(time_data_set)
            self.time_data = file
            if self.time_data.get(self.today_date) is None:
                self.time_data[self.today_date] = self.total_time_float.get()

        self.total_time_float.trace("w", self.update_data)

        # panels for timers
        StopWatchPanel(self, self.total_time_float, self.time_is_running, 0, 0,  1, 2)
        PomodoroPanel(self, 1, 0, self.total_time_float, self.time_is_running, 2, 3)

        # more statistical panels
        self.panel_today_total = TotalTimePanel(self, self.today_date, self.time_data, 0, 4, 1, 2)
        self.panel_stats_monthly = MonthlyStatsPanel(self, 0, 2, self.today_date,
                                                     self.total_time_float, self.time_data, 1, 2)
        self.panel_stats_weekly = WeeklyStatsPanel(self, self.today_date, self.time_data,
                                                   1, 3, 2, 3)

    def format_date_time(self):
        calendar_date, time = self.date_now.split()
        year, month, day = map(int, calendar_date.split("-"))

        return day, month, year

    def update_data(self, *args):
        if self.time_is_running.get():
            self.time_data[self.today_date] = round(self.time_data[self.today_date] + 0.1, 1)
        else:
            self.time_data[self.today_date] = round(self.time_data[self.today_date] + 1, 1)
        with open("storing data/timer_data_set.pickle", "wb") as time_data_set:
            pickle.dump(self.time_data, time_data_set)

        self.panel_today_total.update_label()
        self.panel_stats_monthly.update_labels()
        self.panel_stats_weekly.draw_stats()


class ToDo(Window):
    def __init__(self, parent):
        super().__init__(parent=parent, name="to do")


class Projects(Window):
    def __init__(self, parent):
        super().__init__(parent=parent, name="projects")


class HabitTracker(Window):
    def __init__(self, parent):
        super().__init__(parent=parent, name="habit")
