import customtkinter as ctk
from settings import *
from panels import *
import calendar
from datetime import datetime
import pickle


# the main app
class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=DARK_BLUE)
        self.title("Productivity App")
        self.geometry(f"{WIDTH}x{HEIGHT}+300+100")
        self.minsize(WIDTH, HEIGHT)
        ctk.set_appearance_mode("Dark")

        # data
        self.current_window = ctk.StringVar(value="to do")
        self.current_window.trace("w", self.change_window)

        # widgets
        self.menu = Menu(self, self.current_window)
        self.timer_window = Timer(self)
        self.to_do_window = ToDo(self)
        self.projects_window = Projects(self)
        self.habit_tracker_window = HabitTracker(self)

        self.change_window()
        self.mainloop()

    def change_window(self, *args):
        match self.current_window.get():
            case "timer":
                self.to_do_window.forget()
                self.habit_tracker_window.forget()
                self.projects_window.forget()
                self.timer_window.start()
            case "to do":
                self.timer_window.forget()
                self.habit_tracker_window.forget()
                self.projects_window.forget()
                self.to_do_window.start()
            case "projects":
                self.to_do_window.forget()
                self.habit_tracker_window.forget()
                self.timer_window.forget()
                self.projects_window.start()
            case "habit":
                self.to_do_window.forget()
                self.timer_window.forget()
                self.projects_window.forget()
                self.habit_tracker_window.start()


# the menu
class Menu(ctk.CTkFrame):
    def __init__(self, parent, window_string):
        super().__init__(master=parent, fg_color=BLACK, corner_radius=0)

        # variables
        self.font = ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZE_MAIN, weight="bold")
        self.window_string = window_string

        # menu buttons
        self.timer_button = self.create_menu_button("Timer", False)
        self.to_do_button = self.create_menu_button("To Do", True)
        self.projects_button = self.create_menu_button("Projects", False)
        self.habit_tracker_button = self.create_menu_button("Habit Tracker", False)

        # adding commands to change the window
        self.buttons = [self.timer_button, self.to_do_button, self.projects_button, self.habit_tracker_button]

        self.timer_button.configure(command=lambda: self.window_changed(self.timer_button, "timer"))
        self.to_do_button.configure(command=lambda: self.window_changed(self.to_do_button, "to do"))
        self.projects_button.configure(command=lambda: self.window_changed(self.projects_button, "projects"))
        self.habit_tracker_button.configure(command=lambda: self.window_changed(self.habit_tracker_button, "habit"))

        # placing buttons
        for button in self.buttons:
            button.pack(fill="x", padx=20, pady=10, ipady=5)

        self.place(relwidth=0.25, relheight=1, relx=0, rely=0, anchor="nw")

    def create_menu_button(self, title, toggled=False):
        button = ctk.CTkButton(master=self, text=title,
                               corner_radius=10, font=self.font,
                               hover_color=DARK_BLUE)
        if toggled:
            button.configure(fg_color=DARK_BLUE)
        else:
            button.configure(fg_color=BLACK)

        return button

    def window_changed(self, button, window_name):
        self.window_string.set(window_name)

        for i in self.buttons:
            if i is button:
                i.configure(fg_color=DARK_BLUE)
            else:
                i.configure(fg_color=BLACK)


# head class for all windows
class Window(ctk.CTkFrame):
    def __init__(self, parent, name):
        super().__init__(master=parent, fg_color=DARK_BLUE)

        self.window_name = name

    def start(self):
        print(self.window_name)
        self.place(relwidth=0.75, relheight=1, relx=0.25, rely=0, anchor="nw")

    def forget(self):
        self.place_forget()


# a window to measure time spent on studying and working
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


# a window to create to do lists and etc
class ToDo(Window):
    def __init__(self, parent):
        super().__init__(parent=parent, name="to do")

        # contains all the lists
        self.lists = ...

        # main frame to store all lists
        self.list_frame_main = ctk.CTkScrollableFrame(self, fg_color="transparent",
                                                      scrollbar_button_color=OTHER_BLUES["middle"],
                                                      scrollbar_button_hover_color=OTHER_BLUES["dark"])

        self.list_frame_main.columnconfigure((0, 1, 2), weight=1, uniform="c")
        self.list_frame_main.rowconfigure(0, weight=1, uniform="c")

        # columns
        self.columns = []

        # placing all the frames
        for column in range(3):
            frame = ctk.CTkFrame(self.list_frame_main, fg_color="transparent")
            self.columns.append(frame)
            frame.grid(row=0, column=column, sticky="new")
        self.list_frame_main.pack(expand=True, fill="both")

        # button to add lists
        ctk.CTkButton(self, text="+", corner_radius=20, text_color=WHITE, fg_color=OTHER_BLUES["middle"],
                      font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN + 10, "bold"),
                      hover_color=OTHER_BLUES["dark"], width=50, height=50,
                      command=self.add_list).place(relx=0.95, rely=0.97, anchor="se")

        self.lists = self.load_lists()

    # a helper function to find the smallest column to pack a list to
    def find_smallest_frame(self):
        smallest_height = float("inf")
        smallest_frame = None

        for frame in self.columns:
            if frame.winfo_height() < smallest_height:
                smallest_frame = frame
                smallest_height = frame.winfo_height()

        return smallest_frame

    # creating the list
    def add_list(self):
        smallest_frame = self.find_smallest_frame()
        todo_list = ListPanel(smallest_frame, self, {})
        todo_list.edit()

    # saving the list (or updating the existing list)
    def save_list(self, the_list: ListPanel):
        self.lists[the_list.id] = {"title": the_list.title_string.get(),
                                   "tasks": the_list.tasks}

        with open("storing data/list_data_set.pickle", "wb") as file:
            pickle.dump(self.lists, file)

    # deleting the list
    def delete_list(self, the_list: ListPanel):
        del self.lists[the_list.id]

        with open("storing data/list_data_set.pickle", "wb") as file:
            pickle.dump(self.lists, file)

    # loading the existing lists
    def load_lists(self):
        print("Loading Lists...")

        with open("storing data/list_data_set.pickle", "rb") as file:
            lists = pickle.load(file)

        for ID, the_list_data in lists.items():
            smallest_frame = self.find_smallest_frame()
            the_list = ListPanel(smallest_frame, self, the_list_data["tasks"], the_list_data["title"], ID)
            the_list.load_the_list()

        return lists


# a window to keep track of projects
class Projects(Window):
    def __init__(self, parent):
        super().__init__(parent=parent, name="projects")


# a window to track habits
class HabitTracker(Window):
    def __init__(self, parent):
        super().__init__(parent=parent, name="habit")


if __name__ == '__main__':
    App()
