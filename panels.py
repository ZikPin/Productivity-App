import customtkinter as ctk
import tkinter as tk
from settings import *
import calendar

# Thoughts for later
# - to make gallery view for "to-do lists", make 3 frames in "to do"
#   window and pack each list to column with the least height


# head-panel responsible for designs
class Panel(ctk.CTkFrame):
    def __init__(self, parent, x, y, name=None, x_span=1, y_span=1):

        super().__init__(master=parent, fg_color=VIOLET, corner_radius=20)

        if name:
            ctk.CTkLabel(self, text=name, font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_PANEL_TITLE, "bold")).\
                place(relx=0.07, rely=0.02)

        self.grid(column=x, row=y, rowspan=y_span, columnspan=x_span, sticky="nsew", padx=10, pady=10)


# panel for stopwatch
class StopWatchPanel(Panel):
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

        self.button = ctk.CTkButton(self, text="START", fg_color=OTHER_BLUES["middle"], hover_color=OTHER_BLUES["dark"],
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
class TotalTimePanel(Panel):
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
class PomodoroPanel(Panel):
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
            "work": {"frame": PINKS["dark"], "button": PINKS["light"]},
            "pause": {"frame": PINKS["light"], "button": PINKS["dark"]},
            "long pause": {"frame": PINKS["light"], "button": PINKS["dark"]}
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
        frame = ctk.CTkFrame(self, fg_color=VIOLET)

        # create frames for minutes
        self.create_choosing_frame("Work", self.minutes["work"], frame).place(relx=0, rely=0, anchor="nw", relwidth=1)
        self.create_choosing_frame("Pause", self.minutes["pause"], frame).place(relx=0, rely=0.25,
                                                                                anchor="nw", relwidth=1)
        self.create_choosing_frame("Long Pause", self.minutes["long pause"], frame).place(relx=0, rely=0.5,
                                                                                          anchor="nw", relwidth=1)

        ctk.CTkButton(frame, text="START",
                      fg_color=OTHER_BLUES["middle"], hover_color=OTHER_BLUES["dark"],
                      corner_radius=10,
                      font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_BUTTONS, "bold"),
                      command=self.start).place(relx=0.5, rely=1, anchor="s", relwidth=0.6)

        return frame

    def create_choosing_frame(self, title, minutes, main_frame):
        # little widgets for choosing minutes for work and pause
        frame = ctk.CTkFrame(main_frame, fg_color=VIOLET)

        ctk.CTkLabel(frame, text=f"{title}: ",
                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_POMODORO_CHOOSING_MINUTES)).pack(side="left")
        ctk.CTkLabel(frame, textvariable=minutes,
                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_POMODORO_CHOOSING_MINUTES)).pack(side="left")
        ctk.CTkButton(frame, text="-", width=30, command=lambda: self.add_remove_minutes(title, -1),
                      font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_BUTTONS), hover_color=OTHER_BLUES["dark"],
                      fg_color=OTHER_BLUES["middle"]).pack(side="right", padx=10)
        ctk.CTkButton(frame, text="+", width=30, command=lambda: self.add_remove_minutes(title, 1),
                      font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_BUTTONS), hover_color=OTHER_BLUES["dark"],
                      fg_color=OTHER_BLUES["middle"]).pack(side="right", padx=10)

        return frame

    def add_remove_minutes(self, title, amount):
        self.minutes[title.lower()].set(max(0, self.minutes[title.lower()].get() + amount))
        self.timer = self.minutes[self.modes[self.current_mode_index]].get() * 60

    def create_activated_frame(self):
        main_frame = ctk.CTkFrame(master=self, fg_color=self.mode_color[self.modes[self.current_mode_index]]["frame"])

        # title label
        ctk.CTkLabel(main_frame, textvariable=self.activated_title_label,
                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_POMODORO_SESSION_TITLE)).\
            place(relx=0.5, rely=0.1, anchor="center")

        # timer label
        ctk.CTkLabel(main_frame, textvariable=self.activated_frame_label,
                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_POMODORO_SESSION_TIMER)).\
            place(relx=0.5, rely=0.5, anchor="center")

        # session buttons
        ctk.CTkButton(master=main_frame, text="END SESSION", fg_color="red", corner_radius=10, hover_color=BLACK,
                      font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_BUTTONS, "bold"),
                      command=self.end_session).place(relx=0, rely=1, anchor="sw", relwidth=0.4)

        self.stop_button = ctk.CTkButton(master=main_frame, text="STOP",
                                         fg_color=self.mode_color[self.modes[self.current_mode_index]]["button"],
                                         corner_radius=10, hover_color=OTHER_BLUES["dark"],
                                         font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_BUTTONS, "bold"),
                                         command=self.stop_session)

        self.skip_button = ctk.CTkButton(master=main_frame, text="SKIP",
                                         fg_color=self.mode_color[self.modes[self.current_mode_index]]["button"],
                                         corner_radius=10, hover_color=OTHER_BLUES["dark"],
                                         font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_BUTTONS, "bold"),
                                         command=self.next_session)

        self.stop_button.place(relx=0.57, rely=1, anchor="s", relwidth=0.3)
        self.skip_button.place(relx=1, rely=1, anchor="se", relwidth=0.26)

        return main_frame

    def start(self):
        # starting the timer
        self.start_frame.place_forget()
        self.configure(fg_color=PINKS["dark"])
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
        self.configure(fg_color=self.mode_color[self.modes[self.current_mode_index]]["frame"])

    def end_session(self):
        self.paused = True
        self.temp_name(0, "0:0:0")
        self.start_frame.place(relx=0.05, rely=0.2, anchor="nw", relheight=0.75, relwidth=0.9)
        self.configure(fg_color=VIOLET)

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


class MonthlyStatsPanel(Panel):
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
                    self.labels_by_date[(i, self.month, self.year)].configure(fg_color=OTHER_BLUES["light"])
                elif abs(time - self.average) <= difference:
                    self.labels_by_date[(i, self.month, self.year)].configure(fg_color=OTHER_BLUES["middle"])
                else:
                    self.labels_by_date[(i, self.month, self.year)].configure(fg_color=OTHER_BLUES["dark"])

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


class WeeklyStatsPanel(Panel):
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

        self.main_canvas = tk.Canvas(self, background=VIOLET, bd=0, highlightthickness=0, relief="ridge")

        # finding the week and setting up the header frame
        self.find_current_week()
        self.set_up_header_frame()

        self.main_canvas.pack(expand=True, fill="both", side="top", padx=15, pady=5)
        self.main_canvas.bind("<Configure>", lambda event: self.draw_stats())

    def set_up_header_frame(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent", height=30)

        ctk.CTkButton(header_frame, text="<", width=25, fg_color="transparent", hover_color=OTHER_BLUES["dark"],
                      font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_CALENDAR, "bold"),
                      command=lambda: self.change_week("left")).pack(side="left")
        ctk.CTkLabel(header_frame, textvariable=self.week_label,
                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN, "bold"),
                     fg_color="transparent").pack(side="left", fill="both", expand=True)
        ctk.CTkButton(header_frame, text=">", width=25, fg_color="transparent", hover_color=OTHER_BLUES["dark"],
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
                                     capstyle="round", width=3, fill=WHITE)
        self.main_canvas.create_line(canvas_width * 0.85, 0, canvas_width * 0.85, canvas_height * 0.7,
                                     capstyle="round", width=3, fill=WHITE)

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
                                     capstyle="round", fill=WHITE, width=30)

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
                                     text=day_text, fill=VIOLET,
                                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN - 3, "bold"))

        self.main_canvas.create_text(graph_x_offset + day_width * day_index + day_offset,
                                     graph_y_offset + graph_height + 40,
                                     text=self.week_days[day_index], fill=WHITE,
                                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN-3, "bold"))

    def draw_stat_indicator(self, x2, y, title):
        self.main_canvas.create_line(0, y, x2, y,
                                     dash=20, fill=WHITE, capstyle="round", width=3)
        self.main_canvas.create_text(x2+5, y, anchor="w",
                                     text=title, fill=WHITE, font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN-3, "bold"))

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


# helper function to convert total seconds into hours, minutes and seconds
def seconds_to_time(seconds):
    hours = seconds // 3600
    seconds -= hours * 3600
    minutes = seconds // 60
    seconds -= minutes * 60
    return int(hours), int(minutes), round(seconds, 1)
