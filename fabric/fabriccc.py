from stuff.audio import SpeakerVolume, MicVolume, AudioOutputSwitch
from stuff.cache import Cache
from stuff.hardwareinfo import HardwareUsage, HardwareTemps
from stuff.network import Network
from stuff.nowplaying import NowPlaying
from stuff.power import Power

import fabric
from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.date_time import DateTime
from fabric.widgets.wayland import Window
#from fabric.widgets.window import Window

from fabric.utils import (
    get_relative_path,
    set_stylesheet_from_file
    )

from fabric.hyprland.widgets import WorkspaceButton, Workspaces


class barbar(Window):
    def __init__(self):
        super().__init__(
            layer="top",
            anchor="left top right",
            #open_inspector=True,
            visible=False,
            all_visible=False,
        )

        self.centerbox = CenterBox()
        self.media_box = Box(
            children=[
                Power(),
                Network(),
                Cache(),
                MicVolume(),
                SpeakerVolume(),
                AudioOutputSwitch()
            ]
        )
        self.workspaces = Workspaces(
            buttons_list=[WorkspaceButton(style="padding: 0px 6px") for _ in range(10)]
        )
        self.centerbox.add_start(self.workspaces)

        self.centerbox.add_center(CenterBox(style="min-width:166px", end_children=HardwareUsage()))
        self.centerbox.add_center(DateTime(["%H:%M", "%A | %m.%d.%Y"]))
        self.centerbox.add_center(CenterBox(style="min-width:166px", start_children=HardwareTemps()))

        self.centerbox.add_end(NowPlaying())
        self.centerbox.add_end(self.media_box)

        self.add(self.centerbox)
        self.show_all()


if __name__ == "__main__":
    bar = barbar()
    set_stylesheet_from_file(get_relative_path("style.css"))
    fabric.start()
