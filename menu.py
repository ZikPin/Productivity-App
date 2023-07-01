import customtkinter as ctk
from settings import *


class Menu(ctk.CTkFrame):
    def __init__(self, parent, window_string):
        super().__init__(master=parent, fg_color=BLACK, corner_radius=0)

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
