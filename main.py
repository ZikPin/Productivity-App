import customtkinter as ctk
from settings import *
from menu import Menu
from tkinter import font
from windows import *


class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=DARK_BLUE)
        self.title("Productivity App")
        self.geometry(f"{WIDTH}x{HEIGHT}+300+100")
        self.minsize(WIDTH, HEIGHT)
        ctk.set_appearance_mode("Dark")

        # data
        self.current_window = ctk.StringVar(value="timer")
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


if __name__ == '__main__':
    App()
