from tkinter import *
from collections import namedtuple
from inspect import signature

from services import algorithms, validation

def start_ui():
    """Starts the GUI
    """

    root = Tk()
    root.resizable(width=False, height=False)
    root.title("Scientific Calculator")
    UserInterface(root)
    root.mainloop()

class UserInterface():
    """Graphical user interface for a scientific calculator.
    """

    def __init__(self, root):
        """A constructor for the GUI
        """

        self._root = root
        self._ui_font = "Arial, 15"
        self._variables = {}
        self._input = StringVar()
        Key = namedtuple('Key', ['name', 'keyboard_name', 'functions'])
        self._calculator = algorithms.Calculator()
        self._validator = validation.Validator()

        def move_to_history():
            for i in range(len(self._history_area)-1):
                self._history_area[i].config(text=self._history_area[i+1].cget('text'))
            self._history_area[-1].config(text=self._input.get())
            self._input.set("")

        def update_input_area():
            self._input_area.config(text=self._input.get())

        def save_result_to_variable():
            next_var = chr(ord('A')+len(self._variables))
            self._variables[next_var] = self._calculator.result
            self._variables_menu["menu"].add_command(label=next_var, command=lambda: combine([add_to_input, update_input_area], next_var))
            self._input.set(self._input.get() + " → " + next_var)
        
        def add_to_input(text):
            self._input.set(self._input.get() + text)

        def back_space():
            self._input.set(self._input.get()[:-1])

        def erase():
            self._input.set("")

        def calculate():
            if self._input.get():
                self._calculator.set_input(self._input.get(), self._variables, int(self._precision_menu.cget("text")))
                self._validator.set_input(self._calculator.input_elements, self._variables)
                if self._validator.unassigned_variables():
                    self._input.set("Unassigned variables used!")
                elif self._validator.improper_operator_use():
                    self._input.set("Invalid use of operators!")
                elif self._validator.lone_dot_found():
                    self._input.set("Invalid use of dot!")
                elif self._validator.improper_function_use():
                    self._input.set("Invalid use of functions!")
                elif self._validator.missing_function_argument():
                    self._input.set("Missing function argument!")
                elif not self._calculator.input_elements_in_postfix:
                    self._input.set("Mismatched parentheses!")
                else:
                    self._calculator.evaluate_input_in_postfix_notation()
                    self._input.set(self._input.get() + " = " + str(self._calculator.result))

        self._button_frame = Frame(self._root)
        self._button_frame.grid(row=0,column=0)
        self._button_frame.pack_propagate(0)
        self._input_area = Label(self._button_frame, text=self._input.get(), font=self._ui_font, background="white", anchor="w", justify="left")
        self._input_area.grid(row=10, column=0, columnspan=10, sticky="EW")
        self._history_area = []
        
        for i in range(10):
            self._history_area.append(Label(self._button_frame, font=self._ui_font, text="", background="white", anchor="w", justify="left"))
            self._history_area[-1].grid(row=i, column=0, columnspan=10, sticky="EW")
        
        self._button_layout = [[Key('sin', '', [add_to_input, update_input_area]),          Key('cos', '', [add_to_input, update_input_area]),          Key('tan', '', [add_to_input, update_input_area]),          Key('max', '', [add_to_input, update_input_area]),          Key('min', '', [add_to_input, update_input_area])],
                               [Key('7', '7', [add_to_input, update_input_area]),           Key('8', '8', [add_to_input, update_input_area]),           Key('9', '9', [add_to_input, update_input_area]),           Key('+', 'plus', [add_to_input, update_input_area]),        Key('ln', '', [add_to_input, update_input_area])],
                               [Key('4', '4', [add_to_input, update_input_area]),           Key('5', '5', [add_to_input, update_input_area]),           Key('6', '6', [add_to_input, update_input_area]),           Key('-', 'minus', [add_to_input, update_input_area]),       Key('pi', '', [add_to_input, update_input_area])],
                               [Key('1', '1', [add_to_input, update_input_area]),           Key('2', '2', [add_to_input, update_input_area]),           Key('3', '3', [add_to_input, update_input_area]),           Key('*', 'asterisk', [add_to_input, update_input_area]),    Key('sqrt', '', [add_to_input, update_input_area]),     Key(',', 'comma', [add_to_input, update_input_area])],
                               [Key('(', 'parenleft', [add_to_input, update_input_area]),   Key('0', '0', [add_to_input, update_input_area]),           Key(')', 'parenright', [add_to_input, update_input_area]),  Key('/', 'slash', [add_to_input, update_input_area]),       Key('^', '', [add_to_input, update_input_area]),        Key('=', 'Return', [calculate, move_to_history, update_input_area])],
                               [Key('C', 'BackSpace', [back_space, update_input_area]),     Key('AC', '', [erase, update_input_area]),                  Key('.', 'period', [add_to_input, update_input_area]),      Key('log', '', [add_to_input, update_input_area]),          Key('e', '', [add_to_input, update_input_area]),        Key('→X', '', [calculate, save_result_to_variable, move_to_history, update_input_area])]]
        
        def combine(functions, arguments):
            for function in functions:
                if len(signature(function).parameters) > 0:
                    function(arguments)
                else:
                    function()

        def bind_right_mouse_click_to_input_addition(new_button, arguments, functions):
            new_button.bind('<Button-1>', lambda x:combine(functions, arguments))

        starting_row = 11
        for button_row in self._button_layout:
            for button in button_row:
                new_button = Button(self._button_frame, text=str(button.name), font=self._ui_font, height=2, width=4)
                new_button.grid(row=self._button_layout.index(button_row)+starting_row, column=button_row.index(button))
                bind_right_mouse_click_to_input_addition(new_button, button.name, button.functions)
                
        self._precision_label = Label(self._button_frame, text="Precision:", font=self._ui_font)
        self._precision_label.grid(row=11, column=5, sticky="S")
        self._precision_menu = OptionMenu(self._button_frame, IntVar(), *list(range(0,11)))
        self._precision_menu.grid(row=12, column=5, sticky="N")

        self._var_label = Label(self._button_frame, text="Variables:", font=self._ui_font)
        self._var_label.grid(row=12, column=5, sticky="S")
        self._variables_menu = OptionMenu(self._button_frame, StringVar(), *[""])
        self._variables_menu.grid(row=13, column=5, sticky="N")

        def key_controls(event):
            for button_row in self._button_layout:
                for button in button_row:
                    if button.keyboard_name == event.keysym:
                        combine(button.functions, button.name)
            if len(event.keysym) == 1 and event.keysym.isalpha():
                combine([add_to_input, update_input_area], event.keysym)

        root.bind("<Key>", key_controls)
