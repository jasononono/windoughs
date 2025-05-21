from datetime import datetime as d

def time():
    hour = d.now().hour
    hour, suffix = (hour, "AM") if hour < 13 else (hour - 12, "PM")
    return f"{hour}:{d.now().minute} {suffix}"

def date():
    return d.today().strftime("%Y/%m/%d")