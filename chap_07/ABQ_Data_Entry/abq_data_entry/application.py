"""The application/controller class for ABQ Data Entry"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from . import views as v
from . import models as m
from tkinter import messagebox


class Application(tk.Tk):
    """Application root window"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.withdraw()
        if not self._show_login():
            self.destroy()
            return
        self.deiconify()

        self.model = m.CSVModel()

        self.title("ABQ Data Entry Application")
        self.columnconfigure(0, weight=1)

        ttk.Label(
            self,
            text="ABQ Data Entry Application",
            font=("TkDefaultFont", 16)
        ).grid(row=0)

        self.recordform = v.DataRecordForm(self, self.model)
        self.recordform.grid(row=1, padx=10, sticky=(tk.W + tk.E))
        self.recordform.bind('<<SaveRecord>>', self._on_save)

        # status bar
        self.status = tk.StringVar()
        self.statusbar = ttk.Label(self, textvariable=self.status)
        self.statusbar.grid(sticky=(tk.W + tk.E), row=3, padx=10)

        self._records_saved = 0

    def _on_save(self, *_):
        """Handles file-save requests"""

        # Check for errors first

        errors = self.recordform.get_errors()
        if errors:
            self.status.set(
                "Cannot save, error in fields: {}"
                .format(', '.join(errors.keys()))
            )
            message = 'Cannot save record'
            detail = (
                "The following fields have erors: "
                "\n * {}".format(
                    '\n * '.join(errors.keys())
                )
            )
            messagebox.showerror(
                title='Error',
                message=message,
                detail=detail
            )
            return False

        data = self.recordform.get()
        self.model.save_record(data)
        self._records_saved += 1
        self.status.set(
            f"{self._records_saved} records saved this session"
        )
        self.recordform.reset()

    def _on_file_select(self, *_):
        """Handle the file->select action"""

        filename = filedialog.asksaveasfilename(
            title='Select the target file for saving records',
            defaultextension='.csv',
            filetypes=[('CSV', '*.csv *.CSV')]
        )

        if filename:
            self.model = m.CSVModel(filename=filename)

    @staticmethod
    def _simple_login(username, password):
        return username == 'abq' and password == 'Flowers'

    def _show_login(self):
        error = ''
        title = "Login to ABQ Data Entry"
        while True:
            login = v.LoginDialog(self, title, error)
            if not login.result:  # User canceled
                return False
            username, password = login.result
            if self._simple_login(username, password):
                return True
            error = 'Login Failed'  # Loop and redisplay
