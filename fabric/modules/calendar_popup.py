from __init__ import *

class CalendarPopUp(WaylandWindow):
    def __init__(self):
        self.current_time = datetime.now()
        self.shown_year = self.current_time.year
        self.shown_month = self.current_time.month

        self.calendar_label = Label(self.current_time.strftime("%A | %d.%m.%Y"))
        self.month_stack = Stack(
            transition_duration=transition_duration, 
            transition_type="slide-left-right",
            children=self.create_grid(self.current_time.year, self.current_time.month)
        )

        self.calendar_box = Box(
            orientation="v",
            children=[
                self.calendar_label,
                Box(
                   children=[Button(f"{i[:-1]}") for i in day_abbr]
                ),
                self.month_stack
            ]
        )

        super().__init__(
            anchor="top center",
            visible=False,
            child=Box(
                children=[
                    Button("<", on_clicked = lambda *args: self.cycle_handler("previous")),
                    self.calendar_box,
                    Button(">", on_clicked = lambda *args: self.cycle_handler("next")),
                ]
            )
        )

        
    def update_calendar(self, year_to_show, month_to_show, direction):
        self.calendar_label.set_label(f"Shown date: {year_to_show}/{month_to_show}")
    
        child = self.create_grid(year_to_show, month_to_show)
        stack_label = f"{year_to_show}/{month_to_show}"

        if not self.month_stack.get_child_by_name(stack_label):
            self.month_stack.add_named(child, name = stack_label)

            if direction == "previous":
                self.month_stack.child_set_property(child, "position", 0)

        self.month_stack.set_visible_child_name(stack_label)
    
        self.shown_month = month_to_show
        self.shown_year = year_to_show

    def cycle_handler(self, direction):
        match direction:
            case "previous":
                if self.shown_month == 1:
                    month_to_show = 12
                    year_to_show = self.shown_year - 1
                else:
                    month_to_show = self.shown_month - 1
                    year_to_show = self.shown_year
            case "next":
                if self.shown_month == 12:
                    month_to_show = 1
                    year_to_show = self.shown_year + 1
                else:
                    month_to_show = self.shown_month + 1
                    year_to_show = self.shown_year

        self.update_calendar(year_to_show, month_to_show, direction) # type: ignore

    def create_grid(self, year, month):
        month_grid = Gtk.Grid(visible=True)
        month = [i for i in Calendar().itermonthdays(year, month)]
        self.add_padding(month)
        month = [month[i:i+7] for i in range(0, len(month), 7)]
        column = 0
        row = 0
        for week in month:
            for day in week:
                if day:
                    label = Label(f"{day}")
                else:
                    label = Label("x")
                    label.set_sensitive(False)
                month_grid.attach(Button(child=label, h_expand=True), column, row, 1, 1)
                column+=1
            column=0
            row+=1
            

        return month_grid
        
    @staticmethod
    def add_padding(list_to_pad):
        while True:
            if len(list_to_pad) == 42:
                break
            list_to_pad.append(0)
