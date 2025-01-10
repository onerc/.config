from modules.calendar_popup import CalendarPopUp
from __init__ import *

class OverriddenWorkspaces(Workspaces):
    def __init__(self):
        super().__init__(
            buttons_list=[WorkspaceButton(id=1)],
        )   
    def scroll_handler(self, _, event):
        pass

class OverriddenDateTime(DateTime):
    def __init__(self):
        self.calendar = CalendarPopUp()
        super().__init__(
            formatters=["%H:%M"],
        )

    def do_handle_press(self, _, event, *args):
        if event.button == 1:
            super().do_cycle_next()
            self.calendar.hide() if self.calendar.get_visible() else self.calendar.show()

    def do_handle_scroll(self, _, event, *args):
        pass
