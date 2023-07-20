import customtkinter as ctk
from settings import *
from panels import *
import calendar
from datetime import datetime
import pickle


# the main app
class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=COLORS["blue_dark_"])
        self.title("Productivity App")
        self.geometry(f"{WIDTH}x{HEIGHT}+300+100")
        self.minsize(WIDTH, HEIGHT)
        ctk.set_appearance_mode("Dark")

        # data
        self.current_window = ctk.StringVar(value="timer")
        self.current_window.trace("w", self.change_window)

        # widgets
        self.menu = Menu(self, self.current_window)
        self.windows = {"timer": Timer(self), "to do": ToDo(self),
                        "projects": Projects(self), "habits": HabitTracker(self)}

        self.change_window()
        self.mainloop()

    def change_window(self, *args):
        for name, window in self.windows.items():
            if self.current_window.get() == name:
                window.start()
            else:
                window.forget()


# the menu
class Menu(ctk.CTkFrame):
    def __init__(self, parent, window_string):
        super().__init__(master=parent, fg_color=COLORS["black"], corner_radius=0)

        # variables
        self.font = ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZE_MAIN, weight="bold")
        self.window_string = window_string

        # menu buttons
        self.timer_button = self.create_menu_button("Timer", True)
        self.to_do_button = self.create_menu_button("To Do", False)
        self.projects_button = self.create_menu_button("Projects", False)
        self.habit_tracker_button = self.create_menu_button("Habit Tracker", False)

        # adding commands to change the window
        self.buttons = [self.timer_button, self.to_do_button, self.projects_button, self.habit_tracker_button]

        self.timer_button.configure(command=lambda: self.window_changed(self.timer_button, "timer"))
        self.to_do_button.configure(command=lambda: self.window_changed(self.to_do_button, "to do"))
        self.projects_button.configure(command=lambda: self.window_changed(self.projects_button, "projects"))
        self.habit_tracker_button.configure(command=lambda: self.window_changed(self.habit_tracker_button, "habits"))

        # placing buttons
        for button in self.buttons:
            button.pack(fill="x", padx=20, pady=10, ipady=5)

        self.place(relwidth=0.25, relheight=1, relx=0, rely=0, anchor="nw")

    def create_menu_button(self, title, toggled=False):
        button = ctk.CTkButton(master=self, text=title,
                               corner_radius=10, font=self.font,
                               hover_color=COLORS["blue_dark_"])
        if toggled:
            button.configure(fg_color=COLORS["blue_dark_"])
        else:
            button.configure(fg_color=COLORS["black"])

        return button

    def window_changed(self, button, window_name):
        self.window_string.set(window_name)

        for i in self.buttons:
            if i is button:
                i.configure(fg_color=COLORS["blue_dark_"])
            else:
                i.configure(fg_color=COLORS["black"])


# head class for all windows
class Window(ctk.CTkFrame):
    def __init__(self, parent, name):
        super().__init__(master=parent, fg_color=COLORS["blue_dark_"])

        self.window_name = name

    def start(self):
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
                                                      scrollbar_button_color=COLORS["blue_middle"],
                                                      scrollbar_button_hover_color=COLORS["blue_dark"])

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
        ctk.CTkButton(self, text="+", corner_radius=20, text_color=COLORS["white"], **BUTTON_COLORS["blue_middle"],
                      font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN + 10, "bold"), width=50, height=50,
                      command=self.add_list).place(relx=0.95, rely=0.97, anchor="se")

        self.data_manager: DataManager = DataManager("storing data/list_data_set.pickle", self.lists)
        self.lists = self.data_manager.load()
        self.load_lists()

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
        todo_list = ListPanel(smallest_frame, data_manager=self.data_manager, tasks={})
        todo_list.edit()

    # loading the existing lists
    def load_lists(self):
        for ID, the_list_data in self.lists.items():
            smallest_frame = self.find_smallest_frame()
            the_list = ListPanel(smallest_frame, data_manager=self.data_manager, id_=ID, **the_list_data)
            the_list.load_the_list()


# a window to keep track of projects
class Projects(Window):
    def __init__(self, parent):
        super().__init__(parent=parent, name="projects")

        # data
        self.project_data, self.tabs = {}, {}
        self.project_current = None
        self.tabs_frame = None

        self.setup_header_frame()

        self.data_manager = DataManager("storing data/projects_data_set.pickle", self.project_data)
        self.project_data = self.data_manager.load()
        self.load_projects()

    def setup_header_frame(self):
        tab_x = ctk.IntVar(value=10)

        tabs_main_frame = ctk.CTkFrame(self, fg_color=COLORS["violet"], corner_radius=20, height=60)
        tabs_main_frame.pack(fill="x", padx=10, pady=10)

        self.tabs_frame = ctk.CTkFrame(tabs_main_frame, fg_color="transparent")
        self.tabs_frame.place(x=10, y=12, anchor="nw")

        ctk.CTkButton(self.tabs_frame, text="+", **BUTTON_COLORS["blue_middle"], width=30, command=self.create_tab). \
            pack(side="right", fill="y", expand=True, padx=5)

        ScrollBar(tabs_main_frame, self.tabs_frame, tab_x)

    def add_tabs(self, tab_title, tab_id):
        tab_button = ctk.CTkButton(self.tabs_frame, text=tab_title, **BUTTON_COLORS["blue_middle"], width=30,
                                   command=lambda: self.open_tab(tab_id))
        tab_button.pack(side="left", fill="y", expand=True, padx=5)

        self.tabs[tab_id] = tab_button
        if self.project_data.get(tab_id) is None:
            self.project_data[tab_id] = {"name": tab_title,
                                         "lists": {}}
            self.data_manager.save(self.project_data)

    def create_tab(self):
        if self.project_current is not None:
            self.project_current.pack_forget()
        self.project_current = NewProject(self, self.add_tabs)

    def open_tab(self, id_):
        if self.project_current is not None:
            if not isinstance(self.project_current, NewProject):
                self.project_data[self.project_current.id_]["lists"] = self.project_current.lists
                self.data_manager.save(self.project_data)
            self.project_current.pack_forget()
        self.project_current = ProjectPanel(self, self.data_manager, id_, **self.project_data[id_])

    def load_projects(self):
        for ID, value in self.project_data.items():
            self.add_tabs(value["name"], ID)

    def delete_project(self, tab: ProjectPanel):
        self.project_current = self.data_manager.delete(tab.id_, (self.project_current, self.tabs[tab.id_]), None)[0]


# a window to track habits
class HabitTracker(Window):
    def __init__(self, parent):
        super().__init__(parent=parent, name="habit")

        # data
        self.habits = ...

        self.habit_frame = ctk.CTkScrollableFrame(self, fg_color="transparent",
                                                  scrollbar_button_color=COLORS["blue_middle"],
                                                  scrollbar_button_hover_color=COLORS["blue_dark"])

        ctk.CTkButton(self, text="+", corner_radius=20, text_color=COLORS["white"], **BUTTON_COLORS["blue_middle"],
                      font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN + 10, "bold"), width=50, height=50,
                      command=self.add_habit).place(relx=0.95, rely=0.97, anchor="se")

        self.habit_frame.pack(expand=True, fill="both")

        self.data_manager = DataManager("storing data/habits_data_set.pickle", self.habits)
        self.habits = self.data_manager.load()
        self.load()

    def add_habit(self):
        HabitPanel(self.habit_frame, self.data_manager, {}).edit()

    def load(self):
        for id_, habit in self.habits.items():
            HabitPanel(self.habit_frame, self.data_manager, id_=id_, **habit).load()


if __name__ == '__main__':
    App()
