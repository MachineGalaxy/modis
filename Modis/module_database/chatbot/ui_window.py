from ...tools import ui_window
from ...share import *

pagename = "chatbot"
pad_element = 2


class Page(ui_window.Page):
    def __init__(self, parent):
        """The module tab for chatbot

        Args:
            parent: tk or ttk obkect
        """

        super(Page, self).__init__(parent)

        # API call log
        apicalls = APICalls(self)

        apicalls.grid(
            column=0,
            row=0,
            padx=pad_element,
            pady=pad_element,
            sticky="W E N S"
        )

        # Configure stretch ratios
        self.rowconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Register dynamic elements globally
        from . import _constants
        _constants.pipe_api_mitsuku = apicalls.display


class APICalls(ui_window.Frame):
    def __init__(self, parent):
        """The tree showing all API calls made to Mitsuku

        Args:
            parent: tk or ttk object
        """

        super(APICalls, self).__init__(parent, "Mitsuku API calls")

        # API call history tree
        self.display = ttk.Treeview(
            self,
            columns=[
                "input",
                "output",
                "time"
            ],
            displaycolumns=[
                "input",
                "output",
                "time"
            ]
        )
        self.display.grid(
            column=0,
            row=0,
            padx=pad_element,
            pady=pad_element,
            sticky="W E N S"
        )
        self.display.column("input", width=100, anchor="w")
        self.display.heading("input", text="Input")
        self.display.column("output", width=100, anchor="w")
        self.display.heading("output", text="Output")
        self.display.column("time", width=120, anchor="center")
        self.display.heading("time", text="Time")

        # Configure stretch ratios
        self.rowconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
