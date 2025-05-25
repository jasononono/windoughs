# Non-functional application template

class Application:
    icon = None

    def __init__(self, parent):
        pass

    def update(self, parent, event):
        for i in parent.get_windows(self): # Check for existing windows this application created and update
            parent.requestedUpdates.append(i)
        if len(parent.get_windows(self)) == 0: # Quit this application if no windows exist
            parent.quit_application(self)
            return True
        return False