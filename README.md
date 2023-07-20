# Productivity-App
This app has basic tools for productivity, like timers, to-do lists, and habit trackers.

## Key features:
- Stopwatch timer to check how long you have been focusing on the task
- Pomodoro timer with an option to change minutes for work, pause, and the long pause
- The stat panels show your total time during the day, week, and the month
- To-do lists with the possibility to move tasks a little right (as if it was part of the main task)
- Option to edit and delete created list
- Use the projects tab to group to-do lists, if you want a separate group of lists for different projects
- Habits with name, a short description and an option to choose a theme

## Screenshots:
Timer:

![image](https://github.com/ZikPin/Productivity-App/assets/65452275/f636b84c-697e-4ad1-a4df-1ebc7fc8907b)

To do list:

![image](https://github.com/ZikPin/Productivity-App/assets/65452275/7f16e6bd-8f3f-49e2-88a0-ab419c4f8dea)

Projects:

![image](https://github.com/ZikPin/Productivity-App/assets/65452275/1c5cd5b6-3fbb-4d60-ae4e-988318c4dead)

Habit tracker:

![image](https://github.com/ZikPin/Productivity-App/assets/65452275/1bc32f46-a306-4c5a-b360-2d3be230c20a)


## File structure:
- There are 3 main Python files that contain all the logic:
  - main.py where the app is run
  - panels.py where the logic for panels is created
  - settings.py for some constant values
- Besides, there is a "storing data" folder to store all the necessary data like lists, habits, projects, total time (done by pickle module)
- In the dist folder, there is the main folder that contains the exe file for the program (built with pyinstaller on Windows, so probably runs only on Windows :/ )

## Features to be added in the future:
- Custom colors in projects
- Settings tab
- Custom theme for the whole app
- Drag and drop tasks from one list to another at least in the projects tab
- Gallery like view for habit trackers and to-do lists
