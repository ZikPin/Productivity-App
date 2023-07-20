# Dimensions
WIDTH = 800
HEIGHT = WIDTH * 500 // 800

# Font
FONT_FAMILY = "Arial"
FONT_SIZE_MAIN = 16
FONT_SIZE_PANEL_TITLE = FONT_SIZE_MAIN + 3
FONT_SIZE_TIMER = FONT_SIZE_MAIN + 20
FONT_SIZE_BUTTONS = FONT_SIZE_MAIN - 2
FONT_SIZE_TOTAL_TIME = FONT_SIZE_MAIN + 10
FONT_SIZE_POMODORO_CHOOSING_MINUTES = FONT_SIZE_MAIN + 5
FONT_SIZE_POMODORO_SESSION_TITLE = FONT_SIZE_MAIN + 10
FONT_SIZE_POMODORO_SESSION_TIMER = FONT_SIZE_MAIN + 60
FONT_SIZE_CALENDAR = FONT_SIZE_MAIN - 5
FONT_SIZE_TODO = FONT_SIZE_MAIN - 3

# Colors

COLORS = {"black": "#020317",
          "white": "#CFEBFF",
          "blue_dark_": "#020F43",
          "blue_dark": "#032680",
          "blue_middle": "#1942AC",
          "blue_light": "#1D6FFF",
          "pink_dark": "#FE3EF2",
          "pink_light": "#FF7BE1",
          "violet": "#6345FB",
          "coral": "#FF7761",
          "green": "#227A36",
          "red": "#F25CA2",
          "orange": "#F27405"}

COLORS_OPPOSITE = {"black": "#CFEBFF",
                   "white": "#020317",
                   "blue_dark_": "#020F43",
                   "blue_dark": "#1942AC",
                   "blue_middle": "#032680",
                   "blue_light": "#032680",
                   "pink_dark": "#FF7BE1",
                   "pink_light": "#FE3EF2",
                   "violet": "#032680",
                   "coral": "#FF5330",
                   "green": "#46B346",
                   "red": "#D9043D",
                   "orange": "#F24405"}

BUTTON_COLORS = {
    "delete": {"fg_color": "red",
               "hover_color": COLORS["black"]},
    "blue_middle": {"fg_color": COLORS["blue_middle"],
                    "hover_color": COLORS_OPPOSITE["blue_middle"]},
    "pink_light": {"fg_color": COLORS["pink_light"],
                   "hover_color": COLORS_OPPOSITE["pink_light"]},
    "pink_dark": {"fg_color": COLORS["pink_dark"],
                  "hover_color": COLORS_OPPOSITE["pink_dark"]},
    "blue_dark": {"fg_color": COLORS["blue_dark"],
                  "hover_color": COLORS_OPPOSITE["blue_dark"]},
    "black": {"fg_color": COLORS["black"],
              "hover_color": COLORS_OPPOSITE["black"]},
    "white": {"fg_color": COLORS["white"],
              "hover_color": COLORS_OPPOSITE["white"],
              "text_color": COLORS["white"]},
    "violet": {"fg_color": COLORS["violet"],
               "hover_color": COLORS["blue_middle"]},
    "coral": {"fg_color": COLORS["coral"],
              "hover_color": COLORS_OPPOSITE["coral"]},
    "coral_inverse": {"fg_color": COLORS_OPPOSITE["coral"],
                      "hover_color": COLORS["coral"]},
    "red": {"fg_color": COLORS["red"],
            "hover_color": COLORS_OPPOSITE["red"]},
    "red_inverse": {"fg_color": COLORS_OPPOSITE["red"],
                    "hover_color": COLORS["red"]},
    "green": {"fg_color": COLORS["green"],
              "hover_color": COLORS_OPPOSITE["green"]},
    "green_inverse": {"fg_color": COLORS_OPPOSITE["green"],
                      "hover_color": COLORS["green"]},
    "blue_middle_inverse": {"fg_color": COLORS_OPPOSITE["blue_middle"],
                            "hover_color": COLORS["blue_middle"]},
    "pink_light_inverse": {"fg_color": COLORS_OPPOSITE["pink_light"],
                           "hover_color": COLORS["pink_light"]},
    "pink_dark_inverse": {"fg_color": COLORS_OPPOSITE["pink_dark"],
                          "hover_color": COLORS["pink_dark"]},
    "blue_dark_inverse": {"fg_color": COLORS_OPPOSITE["blue_dark"],
                          "hover_color": COLORS["blue_dark"]},
    "black_inverse": {"fg_color": COLORS_OPPOSITE["black"],
                      "hover_color": COLORS["black"]},
    "white_inverse": {"fg_color": COLORS_OPPOSITE["white"],
                      "hover_color": COLORS["white"],
                      "text_color": COLORS_OPPOSITE["white"]},
    "violet_inverse": {"fg_color": COLORS["blue_middle"],
                       "hover_color": COLORS["violet"]},
}
