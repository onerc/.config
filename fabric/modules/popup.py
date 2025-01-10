from __init__ import *
from modules.owm_weather import WeatherGrid
from modules.hardwareinfo import HardwareUsage, HardwareTemps
from modules.network import Network
from modules.cache import Cache

class PopUpStack(Box):
    def __init__(self):
        self.stack = Stack(transition_duration=transition_duration, transition_type="slide-left-right")
        self.stack.add_titled(
            Box(
                children=[
                    WeatherGrid()
                ]
            ), 
            name="weather", 
            title="Weather"
        ),

        self.stack.add_titled(
            Box(
                orientation="v",
                children=[
                    HardwareTemps(),
                    HardwareUsage(),
                    Cache(),
                    Network()
                ]
            ), 
            name="stats",
            title="Stats"
        )

        self.stack_switcher = Gtk.StackSwitcher(visible=True)
        self.stack_switcher.set_stack(self.stack)
        
        [button.set_hexpand(True) for button in self.stack_switcher.get_children()]
            
        super().__init__(
            orientation="v",
            children=[
                self.stack_switcher,
                self.stack
            ]
        )
        

class PopUp(WaylandWindow):
    def __init__(self):
        super().__init__(
            anchor="top right",
            visible=False,
            child=PopUpStack(), 
        )
        # self.connect("leave-notify-event", lambda *args: self.hide())

        
class TogglePopUpVisibility(Button):
    def __init__(self):
        self.pop_up = PopUp()        
        self.icon = Image(icon_name="window-unpin")
        super().__init__(
            on_clicked = self.on_clicked,
            child=self.icon,
        )
    def on_clicked(self, *args):
        if self.pop_up.get_visible():
            self.pop_up.hide()  
            self.icon.set_from_icon_name("window-unpin")
        else:
            self.pop_up.show()
            self.icon.set_from_icon_name("window-pin")
