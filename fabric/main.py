from modules.audio import SpeakerVolume, MicVolume, AudioOutputSwitch
from modules.popup import TogglePopUpVisibility
from modules.nowplaying import NowPlaying
from modules.overrides import OverriddenDateTime, OverriddenWorkspaces
from modules.power import Power

from __init__ import *

class barbar(WaylandWindow):
    def __init__(self):
        super().__init__(
            layer="top",
            anchor="left top right",
            exclusivity="auto",
            visible=False,
            monitor=0
        )

        self.media = Box(
            children=[
                NowPlaying(),
                AudioOutputSwitch(),
                MicVolume(),
                SpeakerVolume(),
                Power()
            ])
        self.centerbox = CenterBox()
        self.centerbox.add_start(OverriddenWorkspaces())
        self.centerbox.add_start(TogglePopUpVisibility())
        self.centerbox.add_center(OverriddenDateTime())
        self.centerbox.add_end(self.media)

        self.add(self.centerbox)
        self.show_all()


if __name__ == "__main__":
    bar = Application(barbar(), open_inspector=False)
    bar.set_stylesheet_from_file(file_path=get_relative_path("style.css"))
    bar.run() 


