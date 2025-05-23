class DefaultApplication:
    icon = None

    def __init__(self, parent):
        parent.new_window(self)

    def update(self, parent, event):
        for i in parent.get_windows(self):
            parent.requestedUpdates.append(i)
        if len(parent.get_windows(self)) == 0:
            parent.quit_application(self)