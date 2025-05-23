from datetime import datetime


def time():
    hour = datetime.now().hour
    hour, suffix = (hour, "AM") if hour < 13 else (hour - 12, "PM")
    return f"{hour}:{datetime.now().minute:02d} {suffix}"

def date():
    return datetime.today().strftime("%Y/%m/%d")