import customtkinter as ctk
from settings import *
import time

# To Do
# 3) connect to total time
# change timer in stop watch panel


# head-panel responsible for designs
class Panel(ctk.CTkFrame):
    def __init__(self, parent, x, y, name=None, x_span=1, y_span=1):
        super().__init__(master=parent, fg_color=VIOLET, corner_radius=20)

        if name:
            ctk.CTkLabel(self, text=name, font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN + 3, "bold")).\
                place(relx=0.07, rely=0.02)

        self.grid(column=x, row=y, rowspan=y_span, columnspan=x_span, sticky="nsew", padx=10, pady=10)


# panel for stopwatch
class StopWatchPanel(Panel):
    def __init__(self, parent, x, y, total_time, x_span=1, y_span=1):
        super().__init__(parent=parent, x=x, y=y, name="Timer", x_span=x_span, y_span=y_span)

        # data
        self.total_time_global = total_time
        self.time_float = 0.0
        self.total_time_float = 0.0
        self.total_time_string = ctk.StringVar(value="0:0:0.0")
        self.started_bool = True

        # widgets
        ctk.CTkLabel(self, textvariable=self.total_time_string, font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN + 20)).\
            place(relx=0.5, rely=0.5, anchor="center")

        self.button = ctk.CTkButton(self, text="START", fg_color=OTHER_BLUES["middle"],
                                    corner_radius=10, font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN - 2, "bold"),
                                    command=self.button_clicked)
        self.button.place(relx=0.5, rely=0.85, anchor="center")

    def button_clicked(self):
        self.time_float = round(time.perf_counter(), 3)

        if self.started_bool:
            self.button.configure(text="STOP")
        else:
            self.button.configure(text="START")
            self.total_time_global.set(self.total_time_global.get() + self.total_time_float)

        self.started_bool = not self.started_bool
        self.timer()

    def timer(self):
        if not self.started_bool:
            self.total_time_float = round(time.perf_counter() - self.time_float, 1)
            time_string = ":".join(map(str, seconds_to_time(self.total_time_float)))
            self.total_time_string.set(time_string)
            self.after(100, self.timer)


# panel for total time elapsed in one day
class TotalTimePanel(Panel):
    def __init__(self, parent, x, y, total_time, x_span=1, y_span=1):
        super().__init__(parent=parent, x=x, y=y, name="Total", x_span=x_span, y_span=y_span)

        self.total_time = total_time
        self.total_time.trace("w", self.change_label)

        self.label = ctk.CTkLabel(self, text="0 hours\n0 minutes\n0 seconds", justify="left",
                                  font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN + 10))
        self.label.place(relx=0.08, rely=0.55, anchor="w")

    def change_label(self, *args):
        time_formatted = seconds_to_time(self.total_time.get())
        time_string = f"{time_formatted[0]} hours\n{time_formatted[1]} minutes\n{time_formatted[2]} seconds"
        self.label.configure(text=time_string)


# panel for pomodoro
class PomodoroPanel(Panel):
    def __init__(self, parent, x, y, total_time, x_span=1, y_span=1):
        super().__init__(parent=parent, x=x, y=y, name="Pomodoro", x_span=x_span, y_span=y_span)

        # data
        self.minutes = {
            "work": ctk.IntVar(value=5),
            "pause": ctk.IntVar(value=1),
            "long pause": ctk.IntVar(value=1)
        }
        self.modes = ["work", "pause", "work", "pause", "work", "pause", "work", "long pause"]
        self.current_mode = 0
        self.timer = self.minutes[self.modes[self.current_mode]].get() * 60
        self.activated_frame_label = ctk.StringVar(value="0:0:0")
        self.activated_title_label = ctk.StringVar(value=self.modes[self.current_mode].upper())
        self.mode_frame_color = {
            "work": PINKS["dark"],
            "pause": PINKS["light"],
            "long pause": PINKS["light"]
        }
        self.mode_button_color = {
            "work": PINKS["light"],
            "pause": PINKS["dark"],
            "long pause": PINKS["dark"]
        }
        self.paused = True
        self.total_time = total_time

        # later useful widgets
        self.stop_button = None
        self.skip_button = None

        # frames
        self.start_frame = self.starting_frame()
        self.activated = self.activated_frame()

        self.place_frame(self.start_frame)

    def starting_frame(self):
        # main frame
        frame = ctk.CTkFrame(self, fg_color=VIOLET)

        # create frames for minutes
        self.create_choosing_frame("Work", self.minutes["work"], frame).place(relx=0, rely=0, anchor="nw", relwidth=1)
        self.create_choosing_frame("Pause", self.minutes["pause"], frame).place(relx=0, rely=0.25,
                                                                                anchor="nw", relwidth=1)
        self.create_choosing_frame("Long Pause", self.minutes["long pause"], frame).place(relx=0, rely=0.5,
                                                                                          anchor="nw", relwidth=1)

        ctk.CTkButton(frame, text="START",
                      fg_color=OTHER_BLUES["middle"],
                      corner_radius=10,
                      font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN - 2, "bold"),
                      command=self.start).place(relx=0.5, rely=1, anchor="s", relwidth=0.6)

        return frame

    def create_choosing_frame(self, title, minutes, main_frame):
        # little widgets for choosing minutes for work and pause
        frame = ctk.CTkFrame(main_frame, fg_color=VIOLET)

        ctk.CTkLabel(frame, text=f"{title}: ",
                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN + 5)).pack(side="left")
        ctk.CTkLabel(frame, textvariable=minutes,
                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN + 5)).pack(side="left")
        ctk.CTkButton(frame, text="-", width=30, command=lambda: self.add_remove_minutes(title, -1),
                      font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN + 5),
                      fg_color=OTHER_BLUES["middle"]).pack(side="right", padx=10)
        ctk.CTkButton(frame, text="+", width=30, command=lambda: self.add_remove_minutes(title, 1),
                      font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN + 5),
                      fg_color=OTHER_BLUES["middle"]).pack(side="right", padx=10)

        return frame

    def add_remove_minutes(self, title, amount):
        self.minutes[title.lower()].set(max(0, self.minutes[title.lower()].get() + amount))
        self.timer = self.minutes[self.modes[self.current_mode]].get() * 60
        print(title, self.minutes[title.lower()].get())

    def activated_frame(self):
        main_frame = ctk.CTkFrame(master=self)
        main_frame.configure(fg_color=self.mode_frame_color[self.modes[self.current_mode]])
        ctk.CTkLabel(main_frame, textvariable=self.activated_title_label,
                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN+10)).\
            place(relx=0.5, rely=0.1, anchor="center")

        ctk.CTkLabel(main_frame, textvariable=self.activated_frame_label,
                     font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN + 60)). \
            place(relx=0.5, rely=0.5, anchor="center")

        # buttons
        self.session_buttons(main_frame, "END SESSION", "red", 0, 1, 0.4, "sw", self.end_session)
        self.stop_button = self.session_buttons(main_frame, "STOP",
                                                self.mode_button_color[self.modes[self.current_mode]],
                                                0.57, 1, 0.3, "s", self.stop_session)
        self.skip_button = self.session_buttons(main_frame, "SKIP",
                                                self.mode_button_color[self.modes[self.current_mode]],
                                                1, 1, 0.26, "se", self.skip_session)

        return main_frame

    def start(self):
        self.start_frame.place_forget()
        self.configure(fg_color=PINKS["dark"])
        self.place_frame(self.activated)
        self.paused = False
        self.timer_func()

    def place_frame(self, frame):
        # placing the starting and activated frames
        frame.place(relx=0.05, rely=0.2, anchor="nw", relheight=0.75, relwidth=0.9)

    def session_buttons(self, main_frame, title, color, relx, rely, relwidth, anchor, command):
        button = ctk.CTkButton(master=main_frame, text=title,
                               fg_color=color, corner_radius=10,
                               font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN - 2, "bold"),
                               command=command)

        button.place(relx=relx, rely=rely, anchor=anchor, relwidth=relwidth)
        return button

    def timer_func(self):
        # a recursive timer for pomodoro
        if not self.paused:
            self.timer -= 1
            if self.modes[self.current_mode] == "work":
                self.total_time.set(self.total_time.get()+1)
            if self.timer >= 0:
                self.activated_frame_label.set(":".join(map(str, seconds_to_time(self.timer))))
                self.after(1000, self.timer_func)
            else:
                self.current_mode = (self.current_mode + 1) % len(self.modes)
                self.timer = self.minutes[self.modes[self.current_mode]].get() * 60
                self.activated_title_label.set(self.modes[self.current_mode].upper())
                self.configure(fg_color=self.mode_frame_color[self.modes[self.current_mode]])
                self.activated.configure(fg_color=self.mode_frame_color[self.modes[self.current_mode]])
                self.stop_button.configure(fg_color=self.mode_button_color[self.modes[self.current_mode]])
                self.skip_button.configure(fg_color=self.mode_button_color[self.modes[self.current_mode]])
                self.timer_func()

    def end_session(self):
        self.current_mode = 0
        self.activated.place_forget()
        self.place_frame(self.start_frame)
        self.timer = self.minutes[self.modes[self.current_mode]].get() * 60
        self.activated_frame_label.set(value="0:0:0")
        self.paused = True
        self.activated_title_label.set(value=self.modes[self.current_mode].upper())
        self.configure(fg_color=VIOLET)

    def stop_session(self):
        self.paused = not self.paused
        if not self.paused:
            self.stop_button.configure(text="STOP")
            self.timer_func()
        else:
            self.stop_button.configure(text="START")

    def skip_session(self):
        self.current_mode = (self.current_mode + 1) % len(self.modes)
        self.timer = self.minutes[self.modes[self.current_mode]].get() * 60
        self.activated_title_label.set(value=self.modes[self.current_mode].upper())
        self.activated_frame_label.set(value=":".join(map(str, seconds_to_time(self.timer))))
        self.activated.place_forget()
        self.activated = self.activated_frame()
        self.place_frame(self.activated)
        self.configure(fg_color=self.mode_frame_color[self.modes[self.current_mode]])


# helper function to convert total seconds into hours, minutes and seconds
def seconds_to_time(seconds):
    hours = seconds // 3600
    seconds -= hours * 3600
    minutes = seconds // 60
    seconds -= minutes * 60
    return int(hours), int(minutes), round(seconds, 1)
