import typing
from tkinter import *

class UserInterface():
    """A class for the graphical user interface of a scientific calculator.
    """


    def __init__(self, root):
        self._root = root
        self._variables = {}
        self._variable_keys = StringVar()
        self._input = StringVar()
        self._history = StringVar()
        self._button_layout = [['(',')','C','AC'],
                               ['7','8','9','+'],
                               ['4','5','6','-'],
                               ['1','2','3','*'],
                               [None,'0',None,'/'],
                               [None,None,'=', '=X']]

        def update_input_area() -> None:
            self._input_area.config(text=self._input.get())

        def add_to_input(event: Event) -> None:
            input = event.widget.cget('text')
            if input == "C":
                self._input.set(self._input.get()[:-1])
            elif input == "AC":
                self._input.set("")
            elif input == "=" or input == '=X':
                if self._input.get():
                    if input == "=X":
                        self._variables[chr(ord('A')+len(self._variables))] = len(self._variables)
                        self._variable_keys.set(self._variables.keys())
                        print(self._variables)
                    for i in range(len(self._history_area)-1):
                        self._history_area[i].config(text=self._history_area[i+1].cget('text'))
                    self._history_area[-1].config(text=self._input.get())
                    self._input.set("")
            else:
                self._input.set(self._input.get() + input)
       
            update_input_area()

        self._button_frame = Frame(self._root)
        self._button_frame.grid(row=0,column=0)

        self._history_area = []
        for i in range(10):
            self._history_area.append(Label(self._button_frame, text=""))
            self._history_area[-1].grid(row=i, column=0, columnspan=5)

        self._input_area = Label(self._button_frame, text=self._input.get())
        self._input_area.grid(row=10, column=0, columnspan=10)

        def bind_right_mouse_click_to_input_addition(button):
            button.bind('<Button-1>', add_to_input)

        starting_row = 11
        for button_row in self._button_layout:
            for button in button_row:
                if button:
                    new_button = Button(self._button_frame, text=str(button))
                    new_button.grid(row=self._button_layout.index(button_row)+starting_row, column=button_row.index(button))
                    bind_right_mouse_click_to_input_addition(new_button)

        self._variables_menu = OptionMenu(self._root, variable=self._input, value=self._variable_keys.get(), *self._variable_keys.get(), command=add_to_input)
        self._variables_menu.grid(row=11, column=5)