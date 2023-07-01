import customtkinter as ctk
from settings import *
import time


# head-panel responsible for designs
class Panel(ctk.CTkFrame):
    def __init__(self, parent, x, y, name=None, x_span=1, y_span=1):
        super().__init__(master=parent, fg_color=VIOLET, corner_radius=20)

        if name:
            ctk.CTkLabel(self, text=name, font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN + 3, "bold")).place(relx=0.07, rely=0.02)

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
        ctk.CTkLabel(self, textvariable=self.total_time_string, font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN + 20)).place(relx=0.5, rely=0.5, anchor="center")

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

        self.label = ctk.CTkLabel(self, text="0 hours\n0 minutes\n0 seconds", justify="left", font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN + 10))
        self.label.place(relx=0.08, rely=0.55, anchor="w")

    def change_label(self, *args):
        time_formatted = seconds_to_time(self.total_time.get())
        time_string = f"{time_formatted[0]} hours\n{time_formatted[1]} minutes\n{time_formatted[2]} seconds"
        self.label.configure(text=time_string)


# panel for pomodoro
class PomodoroPanel(Panel):
    def __init__(self, parent, x, y, x_span=1, y_span=1):
        super().__init__(parent=parent, x=x, y=y, name="Pomodoro", x_span=x_span, y_span=y_span)

        # data
        self.work_minutes = ctk.IntVar(value=0)
        self.pause_minutes = ctk.IntVar(value=0)
        self.long_pause_minutes = ctk.IntVar(value=0)

        # frames
        self.start_frame = ctk.CTkFrame(self, fg_color="black")
        self.work_frame = ctk.CTkFrame(self, fg_color=PINKS["dark"])
        self.pause_frame = ctk.CTkFrame(self, fg_color=PINKS["light"])
        self.long_pause_frame = ctk.CTkFrame(self, fg_color="red")

        self.starting_frame()

    def starting_frame(self):
        # create widgets
        work_label = ctk.CTkLabel(self.start_frame, text="Work: 45 minutes",
                                  font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN))

        pause_label = ctk.CTkLabel(self.start_frame, text="Pause: 5 minutes",
                                   font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN))

        long_pause_label = ctk.CTkLabel(self.start_frame, text="Long pause: 10 minutes",
                                        font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN))

        start_button = ctk.CTkButton(self.start_frame, text="START", fg_color=OTHER_BLUES["middle"],
                                     corner_radius=10, font=ctk.CTkFont(FONT_FAMILY, FONT_SIZE_MAIN - 2, "bold"))

        # placing widgets
        work_label.place(relx=0, rely=0, anchor="nw")
        pause_label.place(relx=0, rely=0.2, anchor="nw")
        long_pause_label.place(relx=0, rely=0.4, anchor="nw")
        start_button.place(relx=0.5, rely=1, anchor="s", relwidth=0.6)

        # placing frame
        self.start_frame.place(relx=0.05, rely=0.2, anchor="nw", relheight=0.8, relwidth=0.9)


# helper function to convert total seconds into hours, minutes and seconds
def seconds_to_time(seconds):
    hours = seconds // 3600
    seconds -= hours * 3600
    minutes = seconds // 60
    seconds -= minutes * 60
    return int(hours), int(minutes), round(seconds, 1)
