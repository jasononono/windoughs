from datetime import datetime


def time():
    hour = datetime.now().hour
    hour, suffix = (hour, "AM") if hour < 13 else (hour - 12, "PM")
    return f"{hour}:{datetime.now().minute:02d} {suffix}"

def date():
    return datetime.today().strftime("%Y/%m/%d")

# COLOURS
BLUE1 = (5, 170, 255)
BLUE2 = (0, 120, 212)
HIGHLIGHT1 = (59, 86, 107)
HIGHLIGHT2 = (179, 215, 243)
GREY1 = (243, 243, 243)
GREY2 = (230, 230, 230)
GREY3 = (130, 130, 130)
GREY4 = (70, 70, 70)
TINTED_GREY1 = (112, 121, 146)
TINTED_GREY2 = (228, 239, 250)
RED = (203, 48, 36)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)