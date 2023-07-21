from dataclasses import dataclass
import datetime
import pickle
import customtkinter as ctk
import tkinter as tk
from settings import *
import calendar
from uuid import uuid4
import os


class DataManager:
    def __init__(self, file_path, main_var):
        self.file_path = file_path
        self.main_var = main_var
        self.check_file_path()

    def check_file_path(self):
        if "storing data" not in os.listdir():
            os.makedirs("storing data")
        file_name = self.file_path.split("/")[1]
        if file_name not in os.listdir("storing data/"):
            with open(f"storing data/{file_name}", "wb") as file:
                pickle.dump({}, file)

    def load(self):
        with open(self.file_path, "rb") as file:
            self.main_var = pickle.load(file)

        return self.main_var

    def save(self, value):
        with open(self.file_path, "wb") as file:
            pickle.dump(value, file)

        self.main_var = value

    def save_one_obj(self, id_, value):
        self.main_var[id_] = value
        self.save(self.main_var)

    def delete(self, obj_id, objs_to_pack: tuple, *optional_return):
        if self.main_var.get(obj_id) is not None:
            del self.main_var[obj_id]

        for obj in objs_to_pack:
            obj.pack_forget()

        self.save(self.main_var)

        if len(optional_return) != 0:
            return optional_return


class ScrollBar(ctk.CTkSlider):
    def __init__(self, parent, frame, frame_pos, orientation="horizontal"):
        super().__init__(parent, button_corner_radius=10, variable=frame_pos, from_=10, orientation=orientation,
                         progress_color=COLORS["blue_middle"], fg_color=COLORS["blue_middle"], to=600,
                         button_color=COLORS["blue_dark"], button_hover_color=COLORS["blue_dark"], button_length=30)

        # data
        self.parent = parent
        self.frame = frame
        self.frame_pos = frame_pos

        self.place(rely=0.98, relx=0.5, anchor="s", relwidth=0.95)

        self.bind("<Configure>", self.change_scroll_bar)
        self.frame.bind("<Configure>", self.change_scroll_bar)
        self.frame_pos.trace("w", self.change_tab_x)

    def change_scroll_bar(self, event):
        if self.frame.winfo_width() <= self.parent.winfo_width():
            self.configure(from_=10, to=11)
        else:
            self.configure(from_=10, to=self.frame.winfo_width() - self.parent.winfo_width() + 30)

    def change_tab_x(self, *args):
        self.frame.place(x=-self.frame_pos.get() + 20, y=12)


# head-panel responsible for panels in timer window
class TimerPanel(ctk.CTkFrame):
    def __init__(self, parent, x, y, name=None, x_span=1, y_span=1):

        super().__init__(master=parent, fg_color=COLORS["violet"], corner_radius=20)

        if name:
            ctk.CTkLabel(self, text=name, font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_PANEL_TITLE, "bold")).\
                place(relx=0.07, rely=0.02)

        self.grid(column=x, row=y, rowspan=y_span, columnspan=x_span, sticky="nsew", padx=10, pady=10)


@dataclass
class CreatablePanels(ctk.CTkFrame):
    def __init__(self, parent, name, data_manager: DataManager, id_=None, color="violet"):
        super().__init__(master=parent, fg_color=COLORS[color], corner_radius=20)

        # data
        self.name = ctk.StringVar(value=name)
        self.data_manager = data_manager
        if id_ is None:
            self.id_ = uuid4()
        else:
            self.id_ = id_
        self.color = color


# panel for stopwatch
class StopWatchPanel(TimerPanel):
    def __init__(self, parent, total_time, time_running, x, y, x_span=1, y_span=1):
        super().__init__(parent=parent, x=x, y=y, name="Timer", x_span=x_span, y_span=y_span)

        # data
        self.time_total = total_time
        self.time_current = 0.0
        self.time_total_string = ctk.StringVar(value="0:0:0.0")
        self.time_running_bool = time_running

        # widgets
        ctk.CTkLabel(self, textvariable=self.time_total_string, font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_TIMER)).\
            place(relx=0.5, rely=0.5, anchor="center")

        self.button = ctk.CTkButton(self, text="START", **BUTTON_COLORS["blue_middle"],
                                    corner_radius=10, font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_BUTTONS, "bold"),
                                    command=self.button_clicked)

        self.button.place(relx=0.5, rely=0.85, anchor="center")

    def button_clicked(self):
        button_text = {False: "STOP", True: "START"}
        self.button.configure(text=button_text[self.time_running_bool.get()])
        self.time_running_bool.set(not self.time_running_bool.get())
        self.time_current = 0.0
        self.timer()

    # adding seconds to the current time
    def timer(self):
        if self.time_running_bool.get():
            self.time_current += 0.1
            self.time_total.set(self.time_total.get() + 0.1)
            time_string = ":".join(map(str, seconds_to_time(self.time_current)))
            self.time_total_string.set(time_string)
            self.after(100, self.timer)


# panel for total time elapsed in one day
class TotalTimePanel(TimerPanel):
    def __init__(self, parent, today_date, time_data, x, y, x_span=1, y_span=1):
        super().__init__(parent=parent, x=x, y=y, name="Total", x_span=x_span, y_span=y_span)

        # data
        self.time_data = time_data
        self.today_date = today_date

        # widgets
        self.label = ctk.CTkLabel(self, text="0 hours\n0 minutes\n0 seconds", justify="left",
                                  font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_TOTAL_TIME))
        self.label.place(relx=0.08, rely=0.55, anchor="w")

        self.update_label()

    def update_label(self, *args):
        time_formatted = seconds_to_time(self.time_data[self.today_date])
        time_string = f"{time_formatted[0]} hours\n{time_formatted[1]} minutes\n{time_formatted[2]} seconds"
        self.label.configure(text=time_string)


# panel for pomodoro
class PomodoroPanel(TimerPanel):
    def __init__(self, parent, x, y, total_time, time_running, x_span=1, y_span=1):
        super().__init__(parent=parent, x=x, y=y, name="Pomodoro", x_span=x_span, y_span=y_span)

        # data
        self.minutes = {
            "work": ctk.IntVar(value=5),
            "pause": ctk.IntVar(value=1),
            "long pause": ctk.IntVar(value=1)
        }
        self.modes = ["work", "pause", "work", "pause", "work", "pause", "work", "long pause"]
        self.current_mode_index = 0
        self.timer = self.minutes[self.modes[self.current_mode_index]].get() * 60
        self.activated_frame_label = ctk.StringVar(value="0:0:0")
        self.activated_title_label = ctk.StringVar(value=self.modes[self.current_mode_index].upper())
        self.mode_color = {
            "work": "pink_dark",
            "pause": "pink_light",
            "long pause": "pink_light"
        }
        self.paused = True
        self.time_total = total_time
        self.time_running = time_running

        # later useful widgets
        self.stop_button = None
        self.skip_button = None
        self.activated_frame = None

        # frames
        self.start_frame = self.create_starting_frame()

        self.start_frame.place(relx=0.05, rely=0.2, anchor="nw", relheight=0.75, relwidth=0.9)

    def create_starting_frame(self):
        # main frame
        frame = ctk.CTkFrame(self, fg_color=COLORS["violet"])

        # create frames for minutes
        self.create_choosing_frame("Work", self.minutes["work"], frame).place(relx=0, rely=0, anchor="nw", relwidth=1)
        self.create_choosing_frame("Pause", self.minutes["pause"], frame).place(relx=0, rely=0.25,
                                                                                anchor="nw", relwidth=1)
        self.create_choosing_frame("Long Pause", self.minutes["long pause"], frame).place(relx=0, rely=0.5,
                                                                                          anchor="nw", relwidth=1)

        ctk.CTkButton(frame, text="START",
                      **BUTTON_COLORS["blue_middle"],
                      corner_radius=10,
                      font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_BUTTONS, "bold"),
                      command=self.start).place(relx=0.5, rely=1, anchor="s", relwidth=0.6)

        return frame

    def create_choosing_frame(self, title, minutes, main_frame):
        # little widgets for choosing minutes for work and pause
        frame = ctk.CTkFrame(main_frame, fg_color=COLORS["violet"])

        ctk.CTkLabel(frame, text=f"{title}: ",
                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_POMODORO_CHOOSING_MINUTES)).pack(side="left")
        ctk.CTkLabel(frame, textvariable=minutes,
                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_POMODORO_CHOOSING_MINUTES)).pack(side="left")
        ctk.CTkButton(frame, text="-", width=30, command=lambda: self.add_remove_minutes(title, -1),
                      font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_BUTTONS), **BUTTON_COLORS["blue_middle"]).\
            pack(side="right", padx=10)
        ctk.CTkButton(frame, text="+", width=30, command=lambda: self.add_remove_minutes(title, 1),
                      font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_BUTTONS), **BUTTON_COLORS["blue_middle"]).\
            pack(side="right", padx=10)

        return frame

    def add_remove_minutes(self, title, amount):
        self.minutes[title.lower()].set(max(0, self.minutes[title.lower()].get() + amount))
        self.timer = self.minutes[self.modes[self.current_mode_index]].get() * 60

    def create_activated_frame(self):
        main_frame = ctk.CTkFrame(master=self,
                                  fg_color=COLORS[self.mode_color[self.modes[self.current_mode_index]]])

        # title label
        ctk.CTkLabel(main_frame, textvariable=self.activated_title_label,
                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_POMODORO_SESSION_TITLE)).\
            place(relx=0.5, rely=0.1, anchor="center")

        # timer label
        ctk.CTkLabel(main_frame, textvariable=self.activated_frame_label,
                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_POMODORO_SESSION_TIMER)).\
            place(relx=0.5, rely=0.5, anchor="center")

        # session buttons
        ctk.CTkButton(master=main_frame, text="END SESSION", **BUTTON_COLORS["delete"], corner_radius=10,
                      font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_BUTTONS, "bold"),
                      command=self.end_session).place(relx=0, rely=1, anchor="sw", relwidth=0.4)

        self.stop_button = ctk.CTkButton(master=main_frame, text="STOP", corner_radius=10,
                                         **BUTTON_COLORS[self.mode_color[self.modes[self.current_mode_index]]+"_inverse"],
                                         font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_BUTTONS, "bold"),
                                         command=self.stop_session)

        self.skip_button = ctk.CTkButton(master=main_frame, text="SKIP", corner_radius=10,
                                         **BUTTON_COLORS[self.mode_color[self.modes[self.current_mode_index]]+"_inverse"],
                                         font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_BUTTONS, "bold"),
                                         command=self.next_session)

        self.stop_button.place(relx=0.57, rely=1, anchor="s", relwidth=0.3)
        self.skip_button.place(relx=1, rely=1, anchor="se", relwidth=0.26)

        return main_frame

    def start(self):
        # starting the timer
        self.start_frame.place_forget()
        self.configure(fg_color=COLORS[self.mode_color[self.modes[self.current_mode_index]]])
        self.activated_frame = self.create_activated_frame()
        self.activated_frame.place(relx=0.05, rely=0.2, anchor="nw", relheight=0.75, relwidth=0.9)
        self.paused = False
        self.timer_func()

    def timer_func(self):
        # a recursive timer for pomodoro
        if not self.paused:
            self.timer -= 1
            if self.modes[self.current_mode_index] == "work" and not self.time_running.get():
                self.time_total.set(self.time_total.get() + 1)

            if self.timer >= 0:
                self.activated_frame_label.set(":".join(map(str, seconds_to_time(self.timer))))
                self.after(1000, self.timer_func)
            else:
                self.next_session()
                self.timer_func()

    def next_session(self):
        self.temp_name((self.current_mode_index + 1) % len(self.modes), ":".join(map(str, seconds_to_time(self.timer))))
        self.activated_frame = self.create_activated_frame()
        self.activated_frame.place(relx=0.05, rely=0.2, anchor="nw", relheight=0.75, relwidth=0.9)
        self.configure(fg_color=COLORS[self.mode_color[self.modes[self.current_mode_index]]])

    def end_session(self):
        self.paused = True
        self.temp_name(0, "0:0:0")
        self.start_frame.place(relx=0.05, rely=0.2, anchor="nw", relheight=0.75, relwidth=0.9)
        self.configure(fg_color=COLORS["violet"])

    def temp_name(self, current_mode_index, activated_frame_timer):
        # created to eliminate dupes in end_session and next_session
        # stops updates the current_mode_index and timer and updates the activated frame_vars
        self.current_mode_index = current_mode_index
        self.timer = self.minutes[self.modes[self.current_mode_index]].get() * 60
        self.activated_frame_label.set(value=activated_frame_timer)
        self.activated_title_label.set(value=self.modes[self.current_mode_index].upper())
        self.activated_frame.place_forget()

    def stop_session(self):
        self.paused = not self.paused
        if not self.paused:
            self.stop_button.configure(text="STOP")
            self.timer_func()
        else:
            self.stop_button.configure(text="START")


class MonthlyStatsPanel(TimerPanel):
    def __init__(self, parent, x, y, date, total_time, time_data, x_span, y_span):
        super().__init__(parent=parent, x=x, y=y, x_span=x_span, y_span=y_span)

        # data
        self.day, self.month, self.year = date
        self.labels_by_date = dict()
        self.month_label = ctk.StringVar(value=calendar.month_name[self.month])
        self.year_label = ctk.IntVar(value=self.year)
        self.time_total = total_time
        self.time_data = time_data
        self.average = 0

        # creating header and calendar frames
        self.setup_header_frame()
        self.create_calendar_frame()

    def setup_header_frame(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)

        ctk.CTkButton(header_frame, text="<", width=25, fg_color="transparent",
                      font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN - 5, "bold", ),
                      command=lambda: self.change_month(-1)).pack(side="left")
        ctk.CTkLabel(header_frame, textvariable=self.month_label, font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN, "bold"),
                     fg_color="transparent").pack(side="left", fill="both", expand=True)
        ctk.CTkLabel(header_frame, textvariable=self.year_label, font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN, "bold"),
                     fg_color="transparent").pack(side="left", fill="both")
        ctk.CTkButton(header_frame, text=">", width=25, fg_color="transparent",
                      font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN - 5, "bold"),
                      command=lambda: self.change_month(1)).pack(side="right")

        header_frame.place(relx=0.5, rely=0.05, anchor="n", relheight=0.20, relwidth=0.95)

    def create_calendar_frame(self):
        # "updating" frames
        calendar_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        current_month = calendar.monthcalendar(self.year, self.month)

        # grid
        calendar_frame.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform="b")
        rows = tuple([i for i in range(len(current_month))])
        calendar_frame.rowconfigure(rows, weight=1, uniform="b")

        # labels for days
        for row in range(len(current_month)):
            for column in range(7):
                if current_month[row][column] != 0:
                    label = ctk.CTkLabel(calendar_frame, text=str(current_month[row][column]), corner_radius=5,
                                         fg_color="transparent", font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_CALENDAR))

                    self.labels_by_date[(current_month[row][column], self.month, self.year)] = label

                    label.grid(row=row, column=column, sticky="nsew", padx=1)

        self.update_labels()

        calendar_frame.place(relx=0.5, rely=0.95, anchor="s", relheight=0.70, relwidth=0.9)

    def update_labels(self, *args):
        self.average = self.find_average()
        difference = self.average * 0.1

        for i in range(1, self.day + 1):
            time = self.time_data.get((i, self.month, self.year))
            if time != 0.0 and time is not None:
                if time < self.average - difference:
                    self.labels_by_date[(i, self.month, self.year)].configure(fg_color=COLORS["blue_light"])
                elif abs(time - self.average) <= difference:
                    self.labels_by_date[(i, self.month, self.year)].configure(fg_color=COLORS["blue_middle"])
                else:
                    self.labels_by_date[(i, self.month, self.year)].configure(fg_color=COLORS["blue_dark"])

    def change_month(self, amount):
        self.month += amount
        if self.month < 1:
            self.year -= 1
            self.month = 12
            self.day = 1
        elif self.month > 12:
            self.year += 1
            self.month = 1
            self.day = 1

        self.month_label.set(calendar.month_name[self.month])
        self.year_label.set(self.year)

        self.create_calendar_frame()

    def find_average(self):
        s = 0
        counter = 0
        for i in range(1, self.day+1):
            day_time = self.time_data.get((i, self.month, self.year))
            if day_time is not None:
                s += day_time
                counter += 1
        if s == 0:
            return 0.1
        avg = s / counter
        return avg


class WeeklyStatsPanel(TimerPanel):
    def __init__(self, parent, today_date, time_data, x, y, x_span, y_span):
        super().__init__(parent=parent, x=x, y=y, x_span=x_span, y_span=y_span)

        # data
        self.day_date, self.month_date, self.year_date = today_date
        self.time_data = time_data
        self.week = None
        self.day_stats = []
        self.weekly_max = 0
        self.weekly_avg = 0
        self.week_label = ctk.StringVar()
        self.week_days = ["M", "T", "W", "T", "F", "S", "S"]

        self.main_canvas = tk.Canvas(self, background=COLORS["violet"], bd=0, highlightthickness=0, relief="ridge")

        # finding the week and setting up the header frame
        self.find_current_week()
        self.set_up_header_frame()

        self.main_canvas.pack(expand=True, fill="both", side="top", padx=15, pady=5)
        self.main_canvas.bind("<Configure>", lambda event: self.draw_stats())

    def set_up_header_frame(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent", height=30)

        ctk.CTkButton(header_frame, text="<", width=25, fg_color="transparent", hover_color=COLORS["blue_dark"],
                      font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_CALENDAR, "bold"),
                      command=lambda: self.change_week("left")).pack(side="left")
        ctk.CTkLabel(header_frame, textvariable=self.week_label,
                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN, "bold"),
                     fg_color="transparent").pack(side="left", fill="both", expand=True)
        ctk.CTkButton(header_frame, text=">", width=25, fg_color="transparent", hover_color=COLORS["blue_dark"],
                      font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_CALENDAR, "bold"),
                      command=lambda: self.change_week("right")).pack(side="right")

        header_frame.pack(fill="x", side="top", padx=15, pady=5)

    def find_current_week(self):
        current_month = calendar.monthcalendar(self.year_date, self.month_date)

        for week in current_month:
            if self.day_date in week:
                self.week = week
                self.correct_week()
                break

    def correct_week(self):
        if self.week[0] == 0:
            previous_month = self.month_date - 1
            previous_year = self.year_date
            if previous_month == 0:
                previous_year -= 1
                previous_month = 12
            for day in range(7):
                if self.week[day] == 0:
                    self.week[day] = calendar.monthcalendar(previous_year, previous_month)[-1][day]
        elif self.week[-1] == 0:
            next_month = self.month_date + 1
            next_year = self.year_date
            if next_month == 13:
                next_year += 1
                next_month = 1
            for day in range(7):
                if self.week[day] == 0:
                    self.week[day] = calendar.monthcalendar(next_year, next_month)[0][day]

        self.update_date()
        self.week_average()
        self.draw_stats()

    def update_date(self):
        # changing the day_date to the last day of week to ease computations
        if self.week[0] > self.week[-1] and self.day_date > 15:
            self.month_date += 1
            if self.month_date == 13:
                self.month_date = 1
                self.year_date += 1

        self.day_date = self.week[-1]

        self.week_label.set(f"{self.week[0]} - {self.week[-1]} {calendar.month_name[self.month_date]} {self.year_date}")

    def week_average(self):
        self.day_stats = []
        month, year = self.month_date, self.year_date

        for i in range(7):
            day = self.week[i]
            if day > self.week[-1]:
                month -= 1
                if month < 1:
                    month = 12
                    year -= 1
            time_from_data = self.time_data.get((day, month, year))
            if time_from_data is not None:
                self.day_stats.append(time_from_data)
            else:
                self.day_stats.append(0)

        self.weekly_max = max(max(self.day_stats), 0.1)
        self.weekly_avg = max(sum(self.day_stats)/7, 0.1)

    def draw_stats(self):
        # updating canvas and canvas info
        self.main_canvas.delete("all")
        canvas_height = self.main_canvas.winfo_height()
        canvas_width = self.main_canvas.winfo_width()

        # drawing graph lines
        self.main_canvas.create_line(0, canvas_height * 0.7, canvas_width * 0.85, canvas_height * 0.7,
                                     capstyle="round", width=3, fill=COLORS["white"])
        self.main_canvas.create_line(canvas_width * 0.85, 0, canvas_width * 0.85, canvas_height * 0.7,
                                     capstyle="round", width=3, fill=COLORS["white"])

        for i in range(7):
            self.draw_stat_day(0, canvas_height * 0.2, canvas_width * 0.85, canvas_height * 0.4, i)

        # drawing indicator lines
        self.draw_stat_indicator(canvas_width * 0.85, canvas_height * 0.2 - 15, "max")
        avg_height = (canvas_height * 0.2 + 15) * (1 + 1 / self.weekly_avg)
        self.draw_stat_indicator(canvas_width * 0.85, avg_height, "avg")

    def draw_stat_day(self, graph_x_offset, graph_y_offset, graph_width, graph_height, day_index):
        day_width = graph_width//7
        day_offset = day_width*0.5
        day_stat_height = self.day_stats[day_index] / self.weekly_max * graph_height

        self.main_canvas.create_line(graph_x_offset + day_width * day_index + day_offset,
                                     graph_y_offset + graph_height,
                                     graph_x_offset + day_width * day_index + day_offset,
                                     graph_y_offset + graph_height - day_stat_height,
                                     capstyle="round", fill=COLORS["white"], width=30)

        if self.day_stats[day_index] == 0:
            day_text = "0s"
        else:
            day_text = seconds_to_time(self.day_stats[day_index])
            for i in (0, 1, 2):
                if day_text[i] != 0:
                    if i == 0:
                        day_text = f"{int(day_text[i])}h"
                    elif i == 1:
                        day_text = f"{int(day_text[i])}m"
                    elif i == 2:
                        day_text = f"{int(day_text[i])}s"
                    break

        self.main_canvas.create_text(graph_x_offset + day_width * day_index + day_offset,
                                     graph_y_offset + graph_height,
                                     text=day_text, fill=COLORS["violet"],
                                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN - 3, "bold"))

        self.main_canvas.create_text(graph_x_offset + day_width * day_index + day_offset,
                                     graph_y_offset + graph_height + 40,
                                     text=self.week_days[day_index], fill=COLORS["white"],
                                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN-3, "bold"))

    def draw_stat_indicator(self, x2, y, title):
        self.main_canvas.create_line(0, y, x2, y,
                                     dash=20, fill=COLORS["white"], capstyle="round", width=3)
        self.main_canvas.create_text(x2+5, y, anchor="w", text=title, fill=COLORS["white"],
                                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN-3, "bold"))

    def change_week(self, direction):
        if direction == "left":
            self.day_date -= 7
            if self.day_date < 1:
                self.month_date -= 1
                if self.month_date < 1:
                    self.year_date -= 1
                    self.month_date = 12
            if self.day_date < 0:
                self.day_date = calendar.monthcalendar(self.year_date, self.month_date)[-2][0]
            elif self.day_date == 0:
                self.day_date = calendar.monthcalendar(self.year_date, self.month_date)[-1][0]
            self.find_current_week()
        elif direction == "right":
            self.day_date += 7
            if self.day_date > max(calendar.monthcalendar(self.year_date, self.month_date)[-1]):
                self.month_date += 1
                if self.month_date > 12:
                    self.year_date += 1
                    self.month_date = 1
                self.day_date = calendar.monthcalendar(self.year_date, self.month_date)[0][-1]
            self.find_current_week()


class ListPanel(CreatablePanels):
    def __init__(self, parent: ctk.CTkFrame, data_manager: DataManager, tasks: dict, name: str = "To do list",
                 id_=None):
        super().__init__(parent, name, data_manager, id_)

        # data
        self.tasks = tasks

        # main frames
        self.edit_frame = self.setup_edit_frame()
        self.main_frame = self.setup_main_frame()

        # packing the list
        self.pack(padx=5, pady=5, side="top", fill="x")

    def setup_edit_frame(self):
        edit_frame = ctk.CTkFrame(self, fg_color="transparent")
        font = ctk.CTkFont(FONT_FAMILY, FONT_SIZE_TODO, "bold")

        # setting the title
        ctk.CTkLabel(edit_frame, text="Name of the list:", font=font, anchor="w").pack(fill="x")
        ctk.CTkEntry(edit_frame, textvariable=self.name, border_width=0, fg_color=COLORS["blue_dark"],
                     font=font).pack(fill="x")

        # adding the tasks
        ctk.CTkLabel(edit_frame, text="Add some tasks:",
                     font=font, anchor="w").pack(fill="x")
        task_entry = ctk.CTkEntry(edit_frame, font=font, fg_color=COLORS["blue_dark"], border_width=0)
        task_entry.pack(fill="x")

        # adding tasks if they exist
        task_frame = self.add_tasks(edit_frame)

        # done and edit buttons
        ctk.CTkButton(edit_frame, text="DONE", **BUTTON_COLORS["blue_middle"],
                      width=50, command=self.done).pack(side="left", pady=10)
        ctk.CTkButton(edit_frame, text="ADD TASK", **BUTTON_COLORS["blue_middle"],
                      width=50, command=lambda: self.create_task(task_entry, task_frame)).pack(side="right", pady=10)

        task_entry.bind("<Key-Return>", lambda event: self.create_task(task_entry, task_frame))
        return edit_frame

    def setup_main_frame(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")

        # title
        ctk.CTkLabel(main_frame, textvariable=self.name, font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN, "bold"),
                     text_color=COLORS["white"], anchor="w").pack()

        # adding tasks
        self.add_tasks(main_frame)

        # buttons
        ctk.CTkButton(main_frame, text="EDIT", **BUTTON_COLORS["blue_middle"],
                      width=50, command=self.edit).pack(side="left", pady=10)
        ctk.CTkButton(main_frame, text="DELETE LIST", **BUTTON_COLORS["delete"],
                      width=50, command=self.delete).pack(side="right", pady=10)
        return main_frame

    # editing the list
    def edit(self):
        self.main_frame.pack_forget()
        self.edit_frame = self.setup_edit_frame()
        self.edit_frame.pack(expand=True, fill="both", padx=10, pady=10)

    # after editing to save the list
    def done(self):
        self.load_the_list()
        self.save()

    # loading the list
    def load_the_list(self):
        self.edit_frame.pack_forget()
        self.main_frame = self.setup_main_frame()
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

    # loading the tasks
    def add_tasks(self, frame):
        task_frame = ctk.CTkFrame(frame, fg_color="transparent", height=0)

        for task, value in self.tasks.items():
            ListWork(self, task_frame, task, self.tasks)

        task_frame.pack(expand=True, fill="both")
        return task_frame

    # creating new tasks
    def create_task(self, entry: ctk.CTkEntry, frame: ctk.CTkFrame):
        task = entry.get()
        self.tasks[task] = {"value": False,
                            "type": "main"}

        ListWork(self, frame, task, self.tasks)

        # emptying the entry
        entry.delete(0, "end")

    # deleting the list
    def delete(self):
        self.data_manager.delete(self.id_, (self,))

    def save(self):
        self.data_manager.save_one_obj(self.id_, {"name": self.name.get(), "tasks": self.tasks})


class ListWork(ctk.CTkFrame):
    def __init__(self, main_list: ListPanel, parent: ctk.CTkFrame, name: str, tasks: dict):
        super().__init__(master=parent, fg_color="transparent")

        # data
        self.tasks = tasks
        self.task = name
        self.task_label = ctk.StringVar()
        self.parent = parent
        self.value = ctk.BooleanVar(value=tasks[name]["value"])
        self.main_list = main_list

        # the widgets
        self.drag = self.init_widgets()

        self.events()
        self.pack(fill="both")

    # initialising the widgets and returning label to drag
    def init_widgets(self) -> ctk.CTkLabel:
        label = ctk.CTkLabel(self, text="::  ", font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN + 1, "bold"),
                             text_color=COLORS["white"])
        label.pack(side="left")
        ctk.CTkCheckBox(self, textvariable=self.task_label, font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN - 3),
                        variable=self.value, **BUTTON_COLORS["blue_dark"],
                        border_width=2, border_color=COLORS["white"]).pack(side="left", fill="x", pady=5)
        ctk.CTkButton(self, text="x", **BUTTON_COLORS["delete"], command=self.delete,
                      font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN - 3, "bold"), width=25).place(relx=1, rely=0.5,
                                                                                                 anchor="e")

        if self.tasks[self.task]["type"] == "sub":
            label.configure(text="     ::  ")

        return label

    def delete(self):
        del self.tasks[self.task]
        self.main_list.tasks = self.tasks
        self.update_list()
        self.pack_forget()

    def events(self):
        self.value.trace("w", self.save_value)
        self.bind("<Configure>", lambda event: self.format())
        self.drag.bind("<Enter>", lambda event: self.configure(fg_color=COLORS["blue_middle"]))
        self.drag.bind("<Leave>", lambda event: self.configure(fg_color=COLORS["violet"]))
        self.drag.bind("<B1-Motion>", self.change_place)

    # originally meant to change type and the placement of tasks but is only capable of changing the type
    def change_place(self, event):
        if event.x > 50:
            if self.tasks[self.task]["type"] == "main":
                self.tasks[self.task]["type"] = "sub"
                self.drag.configure(text="     ::  ")
                self.update_list()
        else:
            if self.tasks[self.task]["type"] == "sub":
                self.tasks[self.task]["type"] = "main"
                self.drag.configure(text="::  ")
                self.update_list()

    # formatting done for a little longer tasks
    def format(self):
        text = self.task.split()
        # formatting according to the type
        if self.tasks[self.task]["type"] == "main":
            max_line_length = self.parent.winfo_width() * 13 // 163 - 3
            line_length = 0
            for i in range(len(text)):
                line_length += len(text[i])
                if line_length > max_line_length:
                    text[i - 1] += "\n"
                    line_length = 0

        self.task_label.set(" ".join(text))

    def save_value(self, *args):
        self.main_list.tasks[self.task]["value"] = self.value.get()
        self.update_list()

    def update_list(self):
        self.main_list.save()


class HabitPanel(CreatablePanels):
    def __init__(self, parent, data_manager, track, id_=None, name="Habit Name",
                 description="Short description of the habit", color="violet"):
        super().__init__(parent, name, data_manager, id_, color)

        # data
        self.description = ctk.StringVar(value=description)
        self.date = format_date()
        self.date_display = self.date[:]
        self.content_frame = None
        self.main_canvas: tk.Canvas = ...
        self.habit_tracker = track.copy()

        self.edit_frame = self.setup_edit_frame()
        self.main_frame = self.setup_main_frame()
        self.pack(expand=True, fill="both", padx=5, pady=5)

    # setting up the edit frame
    def setup_edit_frame(self) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self, fg_color="transparent")

        # questions related to title, description and color
        ctk.CTkLabel(frame, text="Write your habit name:", anchor="w",
                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN, "bold")).pack(fill="x")
        ctk.CTkEntry(frame, textvariable=self.name, border_width=0, fg_color=COLORS_OPPOSITE[self.color],
                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN, "bold")).pack(fill="x", pady=5)

        ctk.CTkLabel(frame, text="Write a short description of your habit:", anchor="w",
                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN, "bold")).pack(fill="x")
        ctk.CTkEntry(frame, textvariable=self.description, border_width=0, fg_color=COLORS_OPPOSITE[self.color],
                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN, "bold")).pack(fill="x", pady=5)

        ctk.CTkLabel(frame, text="Pick a color for your habit:", anchor="w",
                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN, "bold")).pack(fill="x", pady=5)

        color_button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        available_colors = {"red": COLORS["red"], "pink_dark": COLORS["pink_dark"],
                            "green": COLORS["green"], "blue_dark": COLORS["blue_dark"], "violet": COLORS["violet"],
                            "coral": COLORS["coral"]}

        for color_name, color in available_colors.items():
            self.color_buttons(color_name, color, color_button_frame)

        color_button_frame.pack(fill="x")

        ctk.CTkButton(frame, text="DONE", **BUTTON_COLORS[self.color + "_inverse"], border_width=2, command=self.done,
                      border_color=COLORS["white"]).pack(side="left", pady=10, padx=20, fill="both", expand=True)
        ctk.CTkButton(frame, text="DELETE", **BUTTON_COLORS["delete"], border_color=COLORS["white"], border_width=2,
                      command=self.delete).\
            pack(side="right", pady=10, padx=20, fill="both", expand=True)

        return frame

    # setting up the main frame
    def setup_main_frame(self) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self, fg_color="transparent")

        # for the title and the short description
        self.setup_title_main_frame(frame)

        # frame to display the calendar and the stats
        self.setup_content_frame(frame)

        return frame

    # setting up frame responsible for displaying the month and the relevant stats
    def setup_content_frame(self, frame):
        self.content_frame = ctk.CTkFrame(frame, fg_color="transparent")

        helper_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        # frame to display calendars
        self.setup_monthly_calendar(helper_frame)
        # frame to display the stats
        self.setup_monthly_stat(helper_frame)
        helper_frame.pack(expand=True, fill="both", pady=10)

        ctk.CTkButton(self.content_frame, text="EDIT", **BUTTON_COLORS[self.color + "_inverse"], border_width=2, command=self.edit,
                      border_color=COLORS["white"]).pack(side="left", padx=20, fill="both", expand=True, pady=5)
        ctk.CTkButton(self.content_frame, text="DELETE", **BUTTON_COLORS["delete"], border_color=COLORS["white"], border_width=2,
                      command=self.delete). \
            pack(side="right", padx=20, fill="both", expand=True, pady=5)

        self.content_frame.pack(expand=True, fill="both")

    # setting up title frame for main frame
    def setup_title_main_frame(self, main_frame):
        frame = ctk.CTkFrame(main_frame, fg_color=COLORS_OPPOSITE[self.color], corner_radius=20)
        ctk.CTkLabel(frame, textvariable=self.name, anchor="s",
                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN + 15, "bold")).pack(side="left", fill="x", padx=13)
        ctk.CTkLabel(frame, text=" - ", anchor="s",
                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN - 2, "bold")).pack(side="left", fill="x")
        ctk.CTkLabel(frame, textvariable=self.description, anchor="sw",
                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN - 2, "bold")).pack(side="left", fill="x")
        frame.pack(side="top", fill="x", pady=5, ipady=5)

    # setting up calendar frame for main frame
    def setup_monthly_calendar(self, content_frame):
        month = calendar.monthcalendar(self.date_display[2], self.date_display[1])

        # main frame for calendar
        calendar_frame = ctk.CTkFrame(content_frame, fg_color=COLORS_OPPOSITE[self.color], corner_radius=20)

        # frame for title of calendar
        calendar_title_frame = ctk.CTkFrame(calendar_frame, fg_color=COLORS[self.color],
                                            corner_radius=20)

        ctk.CTkButton(calendar_title_frame, text="<", **BUTTON_COLORS[self.color], corner_radius=9,
                      command=lambda: self.change_month(-1)).place(relx=0.04, rely=0.5, anchor="w", relwidth=0.1,
                                                                   relheight=0.9)
        ctk.CTkLabel(calendar_title_frame, text=f"{calendar.month_name[self.date_display[1]]} {self.date_display[2]}",
                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_CALENDAR + 8, "bold")).place(relx=0.5, rely=0.5,
                                                                                          anchor="center")
        ctk.CTkButton(calendar_title_frame, text=">", **BUTTON_COLORS[self.color], corner_radius=9,
                      command=lambda: self.change_month(1)).place(relx=0.96, rely=0.5, anchor="e", relwidth=0.1,
                                                                  relheight=0.9)

        # setting up the month itself
        calendar_month_frame = ctk.CTkFrame(calendar_frame, fg_color="transparent")
        calendar_month_frame.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform="z")
        calendar_month_frame.rowconfigure(list((i for i in range(len(month)))), weight=1, uniform="z")

        for row in range(len(month)):
            for column in range(7):
                if month[row][column] != 0:
                    self.calendar_buttons(calendar_month_frame, month, row, column)

        calendar_title_frame.place(relx=0.5, rely=0.05, anchor="n", relwidth=0.93, relheight=0.14)
        calendar_month_frame.place(relx=0.5, rely=0.95, anchor="s", relwidth=0.93, relheight=0.75)
        calendar_frame.place(relx=0, rely=1, relwidth=0.48, anchor="sw")

    def change_month(self, amount: int):
        self.date_display = [self.date_display[0], self.date_display[1] + amount, self.date_display[2]]
        if self.date_display[1] < 1:
            self.date_display[2] -= 1
            self.date_display[1] = 12
            self.date_display[0] = 31
        elif self.date_display[1] > 12:
            self.date_display[2] += 1
            self.date_display[1] = 1
            self.date_display[0] = 1

        self.content_frame.pack_forget()
        print(self.habit_tracker)
        self.setup_content_frame(self.main_frame)

    # setting up monthly stats for main frame
    def setup_monthly_stat(self, content_frame):
        stats_frame = ctk.CTkFrame(content_frame, fg_color=COLORS_OPPOSITE[self.color], corner_radius=20)

        # canvas to draw stats
        self.main_canvas = tk.Canvas(stats_frame, background=COLORS_OPPOSITE[self.color], bd=0, highlightthickness=0,
                                     relief="ridge")
        self.main_canvas.pack(expand=True, fill="both", padx=7, pady=7)

        self.main_canvas.bind("<Configure>", lambda event: self.draw_stats(event.width, event.height))

        stats_frame.place(relx=1, rely=1, relwidth=0.48, relheight=1, anchor="se")

    def draw_stats(self, width, height):
        # drawing graph lines
        self.main_canvas.delete("all")
        self.main_canvas.create_line(width*0.01, height*0.1, width*0.01, height*0.9, fill=COLORS["white"], width=2)
        self.main_canvas.create_line(width * 0.01, height * 0.9, width * 0.99, height * 0.9, fill=COLORS["white"],
                                     width=2)

        month = calendar.monthcalendar(self.date_display[2], self.date_display[1])
        month_max = max(month[-1])
        gap = width // month_max
        s = 0
        coords = [(width*0.01, height*0.9)]
        for i in range(1, month_max+1):
            if self.date[1] == self.date_display[1] and i > self.date[0]:
                break
            if self.habit_tracker.get((i, self.date_display[1], self.date_display[2])) is not None:
                s += 1
            h = height * 0.8 * s/i
            coords.append((width*0.01 + gap*i - gap, height*0.9 - h))
        if self.date[1] == self.date_display[1] and i > self.date[0]:
            coords.append((width*0.01 + gap*self.date[0] - gap, height*0.9))
        else:
            coords.append((width*0.01 + gap*month_max - gap, height*0.9))

        self.main_canvas.create_polygon(coords, width=4, fill=COLORS[self.color], outline=COLORS["white"])

    # function that is responsible for changing color in edit mode
    def change_color(self, color):
        self.color = color
        self.edit_frame.pack_forget()
        self.configure(fg_color=COLORS[color])
        self.edit_frame = self.setup_edit_frame()
        self.edit_frame.pack(expand=True, fill="both", padx=15, pady=15)

    # helper function that helps to avoid the bug with buttons and functions
    def color_buttons(self, color_name, color, color_button_frame):
        button = ctk.CTkButton(color_button_frame, text="", width=50, height=50, **BUTTON_COLORS[color_name],
                               border_width=2, border_color=COLORS["white"], corner_radius=20,
                               command=lambda: self.change_color(color_name))
        button.pack(side="left", padx=5, expand=True)

    def calendar_buttons(self, calendar_month_frame, month, row, column):
        date = (month[row][column], self.date_display[1], self.date_display[2])
        state = "disabled"
        if self.date_display[2] == self.date[2] and self.date_display[1] <= self.date[1]:
            state = "normal"
            if self.date_display[1] == self.date[1] and month[row][column] > self.date[0]:
                state = "disabled"

        if self.habit_tracker.get(date) is None:
            button = ctk.CTkButton(calendar_month_frame, text=str(month[row][column]), text_color=COLORS["white"],
                                   fg_color=COLORS_OPPOSITE[self.color], hover_color=COLORS[self.color],
                                   corner_radius=10, width=0, font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_CALENDAR, "bold"),
                                   state=state, height=30)
        else:
            button = ctk.CTkButton(calendar_month_frame, text=str(month[row][column]), text_color=COLORS["white"],
                                   fg_color=COLORS[self.color], hover_color=COLORS[self.color],
                                   corner_radius=10, width=0, font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_CALENDAR, "bold"),
                                   state=state, height=30)

        button.configure(command=lambda: self.done_work(date, button))
        button.grid(row=row, column=column, sticky="nsew", pady=1, padx=2)

    # after editing
    def done(self):
        self.load()
        self.save()

    def load(self):
        self.edit_frame.pack_forget()
        self.main_frame = self.setup_main_frame()
        self.main_frame.pack(expand=True, fill="both", padx=15, pady=5)

    def edit(self):
        self.main_frame.pack_forget()
        self.edit_frame = self.setup_edit_frame()
        self.edit_frame.pack(expand=True, fill="both", padx=15, pady=15)

    def done_work(self, date, button):
        if self.habit_tracker.get(date) is None:
            self.habit_tracker[date] = True
            button.configure(fg_color=COLORS[self.color])
        else:
            del self.habit_tracker[date]
            button.configure(fg_color=COLORS_OPPOSITE[self.color])

        self.save()
        self.draw_stats(self.main_canvas.winfo_width(), self.main_canvas.winfo_height())

    def delete(self):
        self.data_manager.delete(self.id_, (self,))

    def save(self):
        values = {"name": self.name.get(), "description": self.description.get(),
                  "track": self.habit_tracker, "color": self.color}
        self.data_manager.save_one_obj(self.id_, values)


class NewProject(ctk.CTkFrame):
    def __init__(self, parent, func):
        super().__init__(master=parent, fg_color=COLORS["violet"], corner_radius=20)

        # data
        self.title = ""
        self.func = func
        self.id_ = uuid4()

        ctk.CTkLabel(self, text="Name your new Project", text_color=COLORS["white"],
                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_PANEL_TITLE, "bold")).pack(expand=True, anchor="s",
                                                                                        padx=10, pady=10)
        self.name_entry = ctk.CTkEntry(self, corner_radius=10, fg_color=COLORS["blue_dark"], border_width=0, height=50,
                                       font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_PANEL_TITLE - 5, "bold"),
                                       text_color=COLORS["white"], placeholder_text="New Project")
        self.name_entry.pack(anchor="n", padx=100, pady=10, fill="x")
        ctk.CTkButton(self, text="DONE", **BUTTON_COLORS["blue_middle"], command=self.done).pack(expand=True,
                                                                                                 anchor="n")
        self.name_entry.bind("<Key-Return>", lambda event: self.done())

        self.pack(expand=True, fill="both", padx=10, pady=10)

    # assigning new name
    def done(self):
        self.title = self.name_entry.get()
        self.name_entry.delete(0, "end")
        self.func(self.title, self.id_)
        self.pack_forget()


class ProjectPanel(CreatablePanels):
    def __init__(self, parent, data_manager, id_, name, lists):
        super().__init__(parent, name, data_manager, id_)

        # data
        self.parent = parent
        self.lists = lists
        self.todo_frame_x = ctk.IntVar(value=10)
        self.todo_frame = None

        # setting up title and content frame
        self.setup_title_frame()
        self.setup_content_frame()

        self.pack(expand=True, fill="both", padx=10, pady=10)

    def setup_title_frame(self):
        title_frame = ctk.CTkFrame(self, fg_color=COLORS["blue_middle"], corner_radius=15)
        ctk.CTkLabel(title_frame, text=self.name.get(), text_color=COLORS["white"],
                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_PANEL_TITLE, "bold")). \
            pack(side="left", padx=10, pady=10)
        ctk.CTkButton(title_frame, text="DELETE", **BUTTON_COLORS["delete"], width=40, corner_radius=7,
                      font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN),
                      command=lambda: self.parent.delete_project(self)).pack(side="right", padx=10, pady=10)
        ctk.CTkButton(title_frame, text="CLOSE", **BUTTON_COLORS["blue_dark"], width=40, corner_radius=7,
                      font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN), command=self.pack_forget).pack(side="right",
                                                                                                    padx=10, pady=10)
        title_frame.pack(fill="x", anchor="n", pady=7, padx=7)

    def setup_content_frame(self):
        content_frame = ctk.CTkFrame(self, fg_color=COLORS["blue_middle"], corner_radius=15)

        self.todo_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        self.todo_frame.place(x=0, y=12, relheight=0.85)

        ctk.CTkButton(content_frame, text="+", **BUTTON_COLORS["blue_dark"], corner_radius=15, width=50, height=50,
                      font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN+5), command=self.add_list).\
            place(relx=0.95, rely=0.93, anchor="se")

        content_frame.pack(expand=True, fill="both", pady=7, padx=7)

        # scrollbar
        ScrollBar(content_frame, self.todo_frame, self.todo_frame_x)

        self.load_lists()

    def add_list(self):
        list_ = ProjectList(self.todo_frame, self, self.data_manager, {})
        list_.edit()

    def save_list(self, list_: ListPanel):
        self.lists[list_.id_] = {"title": list_.name.get(), "tasks": list_.tasks}
        self.data_manager.save_one_obj(self.id_, {"name": self.name.get(), "lists": self.lists})

    def delete_list(self, list_):
        del self.lists[list_.id]
        self.data_manager.save_one_obj(self.id_, {"name": self.name.get(), "lists": self.lists})

    def load_lists(self):
        for ID, the_list_data in self.lists.items():
            the_list = ProjectList(self.todo_frame, self, self.data_manager, the_list_data["tasks"],
                                   the_list_data["title"], ID)
            the_list.load_the_list()


class ProjectList(ListPanel):
    def __init__(self, parent_frame, panel: ProjectPanel, data_manager, tasks, name="To do list", id_=None):
        super().__init__(parent=parent_frame, data_manager=data_manager, tasks=tasks, name=name, id_=id_)

        self.panel = panel

        self.pack(side="left", expand=True, fill="both", padx=10)

    def setup_main_frame(self):
        main_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", scrollbar_button_color=COLORS["white"],
                                            scrollbar_button_hover_color=COLORS["blue_dark"])

        # title
        ctk.CTkLabel(main_frame, textvariable=self.name, font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN, "bold"),
                     text_color=COLORS["white"], anchor="w").pack()

        # adding tasks
        self.add_tasks(main_frame)

        # buttons
        ctk.CTkButton(main_frame, text="EDIT", **BUTTON_COLORS["blue_middle"],
                      width=50, command=self.edit).pack(side="left", pady=10)
        ctk.CTkButton(main_frame, text="DELETE LIST", fg_color="red", hover_color=COLORS["black"],
                      width=50, command=self.delete).pack(side="right", pady=10)

        return main_frame

    def setup_edit_frame(self):
        edit_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", scrollbar_button_color=COLORS["white"],
                                            scrollbar_button_hover_color=COLORS["blue_dark"])
        font = ctk.CTkFont(FONT_FAMILY, FONT_SIZE_TODO, "bold")

        # setting the title
        ctk.CTkLabel(edit_frame, text="Name of the list:", font=font, anchor="w").pack(fill="x")
        ctk.CTkEntry(edit_frame, textvariable=self.name, border_width=0, fg_color=COLORS["blue_dark"],
                     font=font).pack(fill="x")

        # adding the tasks
        ctk.CTkLabel(edit_frame, text="Add some tasks:",
                     font=font, anchor="w").pack(fill="x")
        task_entry = ctk.CTkEntry(edit_frame, font=font, fg_color=COLORS["blue_dark"], border_width=0)
        task_entry.pack(fill="x")

        # adding tasks if they exist
        task_frame = self.add_tasks(edit_frame)

        # done and edit buttons
        ctk.CTkButton(edit_frame, text="DONE", **BUTTON_COLORS["blue_middle"],
                      width=50, command=self.done).pack(side="left", pady=10)
        ctk.CTkButton(edit_frame, text="ADD TASK", **BUTTON_COLORS["blue_middle"],
                      width=50, command=lambda: self.create_task(task_entry, task_frame)).pack(side="right", pady=10)

        task_entry.bind("<Key-Return>", lambda event: self.create_task(task_entry, task_frame))
        return edit_frame

    def save(self):
        self.panel.save_list(self)

    def delete(self):
        self.panel.delete_list(self)


# helper function to convert total seconds into hours, minutes and seconds
def seconds_to_time(seconds):
    hours = seconds // 3600
    seconds -= hours * 3600
    minutes = seconds // 60
    seconds -= minutes * 60
    return int(hours), int(minutes), round(seconds, 1)


def format_date():
    date, _ = str(datetime.datetime.now()).split()
    date = date.split("-")[::-1]
    date = list(map(int, date))
    return date
