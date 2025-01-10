from __init__ import *

dirty_fabricator = Fabricator(poll_from="grep Dirty: /proc/meminfo", interval=1000)


class Cache(Button):
    def __init__(self):

        self.label = Label(h_expand=True, name="cacheLabel")
        self.image = Image(icon_name="drive-removable-media-symbolic", icon_size=icon_size, name="icon")

        super().__init__(
            child=Box(
                children=[
                    self.image,
                    self.label,
                ]
            )
        )

        dirty_fabricator.connect("changed", self.update_label)

    def update_label(self, fabricator, value):
        self.label.set_label(convert_kb_to_gb(int(value.split()[1])))
        return True
        
