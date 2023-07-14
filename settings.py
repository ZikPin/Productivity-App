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
BLACK = "#020317"
DARK_BLUE = "#020F43"
VIOLET = "#6345FB"
WHITE = "#CFEBFF"
OTHER_BLUES = {
    "dark": "#032680",
    "middle": "#1942AC",
    "light": "#1D6FFF",
}
PINKS = {
    "light": "#FF7BE1",
    "dark": "#FE3EF2",
}

COLORS = {"black": {"self": "#020317", "opposite": "#CFEBFF"},
          "white": {"self": "#CFEBFF", "opposite": "#020317"},
          "blue_dark_": {"self": "#020F43", "opposite": "#020F43"},
          "blue_dark": {"self": "#032680", "opposite": "#1942AC"},
          "blue_middle": {"self": "#1942AC", "opposite": "#032680"},
          "blue_light": {"self": "#1D6FFF", "opposite": "#032680"},
          "pink_dark": {"self": "#FE3EF2", "opposite": "#FF7BE1"},
          "pink_light": {"self": "#FF7BE1", "opposite": "#FE3EF2"},
          "violet": {"self": "#6345FB", "opposite": "#032680"}}

BUTTON_COLORS = {
    "delete": {"fg_color": "red",
               "hover_color": COLORS["black"]["self"]},
    "blue_middle": {"fg_color": COLORS["blue_middle"]["self"],
                    "hover_color": COLORS["blue_middle"]["opposite"]},
    "pink_light": {"fg_color": COLORS["pink_light"]["self"],
                   "hover_color": COLORS["pink_light"]["opposite"]},
    "pink_dark": {"fg_color": COLORS["pink_dark"]["self"],
                  "hover_color": COLORS["pink_dark"]["opposite"]},
    "blue_dark": {"fg_color": COLORS["blue_dark"]["self"],
                  "hover_color": COLORS["blue_dark"]["opposite"]},
    "black": {"fg_color": COLORS["black"]["self"],
              "hover_color": COLORS["black"]["opposite"]},
    "white": {"fg_color": COLORS["white"]["self"],
              "hover_color": COLORS["white"]["opposite"],
              "text_color": COLORS["white"]["self"]},
    "violet": {"fg_color": COLORS["violet"]["self"],
               "hover_color": COLORS["blue_middle"]["self"]},
    "blue_middle_inverse": {"fg_color": COLORS["blue_middle"]["opposite"],
                    "hover_color": COLORS["blue_middle"]["self"]},
    "pink_light_inverse": {"fg_color": COLORS["pink_light"]["opposite"],
                   "hover_color": COLORS["pink_light"]["self"]},
    "pink_dark_inverse": {"fg_color": COLORS["pink_dark"]["opposite"],
                  "hover_color": COLORS["pink_dark"]["self"]},
    "blue_dark_inverse": {"fg_color": COLORS["blue_dark"]["opposite"],
                  "hover_color": COLORS["blue_dark"]["self"]},
    "black_inverse": {"fg_color": COLORS["black"]["opposite"],
              "hover_color": COLORS["black"]["self"]},
    "white_inverse": {"fg_color": COLORS["white"]["opposite"],
              "hover_color": COLORS["white"]["self"],
              "text_color": COLORS["white"]["opposite"]},
    "violet_inverse": {"fg_color": COLORS["blue_middle"]["self"],
               "hover_color": COLORS["violet"]["self"]},
}
