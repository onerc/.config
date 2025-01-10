from __init__ import *


class Network(Button):
    def __init__(self):
        
        self.label = Label(h_expand=True, name="revealerLabel")
        
        self.stack = Stack(transition_type="slide-up-down")
        for icon in ["network-wired-acquiring", "network-wired", "network-wired-disconnected"]:
            self.stack.add_named(Image(icon_name=f"{icon}-symbolic", icon_size=icon_size, name="icon"), name=icon)

        super().__init__(
            child=Box(
                children=[
                    self.stack,
                    self.label
                ]
            )
        )
        psutil_fabricator.connect("changed", self.update_label_and_icon)

    # todo bandwidth usage
    # maybe todo interface speed

    def update_label_and_icon(self, fabricator, value):
        self.label.set_label(value["ip_address"] if value["is_network_up"] else "N/A")
        self.stack.set_visible_child_name("network-wired" if value["is_network_up"] else "network-wired-disconnected")
