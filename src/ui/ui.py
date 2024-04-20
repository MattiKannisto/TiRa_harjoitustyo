from tkinter import *
from tkinter.messagebox import showinfo
from collections import namedtuple
from inspect import signature

from services import algorithms

def start_ui():
    """Starts GUI
    """

    root = Tk()
    root.resizable(width=False, height=False)
    root.title("Scientific Calculator")
    UserInterface(root)
    root.mainloop()

class UserInterface():
    """GUI for a scientific calculator.
    """

    def __init__(self, root):
        """A constructor for the GUI
        """

        self._root = root
        self._ui_font = "Arial, 15"
        self._vars = {}
        self._input_history = []
        self._current_input = 0
        self._calculator = algorithms.Calculator()

        def move_to_history() -> None:
            """Moves the input given by the user to the history area
            """

            if input := self._input_area.cget("text"):
                for i in range(len(self._history_area)-1):
                    self._history_area[i].config(text=self._history_area[i+1].cget('text'))
                self._history_area[-1].config(text=input)

        def save_result_to_variable() -> None:
            """Saves the result calculated by _calculator to variables' dictionary if the input
            has content and the result exists
            """

            if self._input_area.cget("text") and self._calculator.result:
                next_var_key = chr(ord('A')+len(self._calculator.variables))
                self._calculator.variables[next_var_key] = self._calculator.result
                self._vars_menu["menu"].add_command(label=next_var_key, command=lambda: combine([add_to_input], next_var_key))
                add_to_input(" → " + next_var_key)
        
        def add_to_input(text: str) -> None:
            """Appends text to the input

            Args:
                text (str): text to be appended to the input
            """

            self._input_area.config(text=self._input_area.cget("text") + text)

        def back_space() -> None:
            """Removes the last character from the input
            """

            self._input_area.config(text=self._input_area.cget("text")[:-1])

        def erase() -> None:
            """Sets the input to an empty string
            """

            self._input_area.config(text="")

        def calculate() -> None:
            """If input exists, asks _calculator to calculate the result and sets it in the input
            to be later moved to the history area
            """

            if input := self._input_area.cget("text"):
                precision = int(self._precision_menu.cget("text"))
                result = self._calculator.calculate(input, precision)
                self._input_area.config(text=result)

        def to_input_history() -> None:
            """If input exists, moves it to the input history and sets its index the current input
            """

            if input := self._input_area.cget("text"):
                self._input_history.append(input)
                self._current_input = len(self._input_history)

        def previous_input(event: Event) -> None:
            """Allows the user to autofill input area with previous input in input history

            Args:
                event (Event): unused argument that is given to the function by default
            """

            if self._current_input-1 >= 0 and self._input_history:
                self._current_input -= 1
                self._input_area.config(text=self._input_history[self._current_input])

        def next_input(event: Event) -> None:
            """Allows the user to autofill input area with next input in input history

            Args:
                event (Event): unused argument that is given to the function by default
            """

            if self._current_input <= len(self._input_history):
                if self._current_input < len(self._input_history)-1:
                    self._current_input += 1
                    self._input_area.config(text=self._input_history[self._current_input])
                elif self._current_input == len(self._input_history)-1:
                    self._current_input += 1
                    erase()
        
        def combine(functions: list, arguments):
            """Calls all functions in the function list. If the function takes arguments, they are
            given to the function when it is being called

            Args:
                functions (list): a list of functions
                arguments (): arguments for the functions that take parameters
            """

            for function in functions:
                if len(signature(function).parameters) > 0:
                    function(arguments)
                else:
                    function()

        def bind_left_mouse_click_to_input_addition(button, arguments, functions: list):
            """Binds the functions with their arguments to the left mouse button

            Args:
                button: button to which the functions will be bound
                arguments: arguments for the functions
                functions (list): functions to be bound to the button
            """

            button.bind('<Button-1>', lambda x:combine(functions, arguments))

        def key_controls(event: Event):
            """Handles keyboard events by mapping them to correct functions

            Args:
                event (Event): keyboard event
            """

            for button_row in self._button_layout:
                for button in button_row:
                    if button.keyboard_name == event.keysym:
                        combine(button.functions, button.name)
            # Add alphabets
            if len(event.keysym) == 1 and event.keysym.isalpha():
                combine([add_to_input], event.keysym)

        def popup_text(widget: Widget):
            """Creates a popup window showing the widget text

            Args:
                widget (Widget): the widget which text will be the message in the popup window
            """

            showinfo(message=widget.cget("text"))

        # Frame for buttons of the calculator
        self._button_frame = Frame(self._root)
        self._button_frame.grid(row=0,column=0)
        
        # The input given by the user will be shown in this label
        self._input_area = Button(self._button_frame, text="", font=self._ui_font, background="white", anchor="e", justify="left", width=10, activebackground="white", command=lambda: popup_text(self._input_area))
        self._input_area.grid(row=10, column=0, columnspan=10, sticky="EW")

        # The previous inputs and their results will be added to the lowest of these labels. When new input is given, label texts move
        # up in the history area and the topmost label text disappears
        self._history_area = []
        for i in range(10):
            self._history_area.append(Button(self._button_frame, font=self._ui_font, text="", background="white", anchor="e", justify="left", borderwidth=0, activebackground="white", width=10, command=lambda: popup_text(self._history_area[i])))
            self._history_area[-1].grid(row=i, column=0, columnspan=10, sticky="EW")

        Key = namedtuple('Key', ['name', 'keyboard_name', 'functions']) # Key means calculator button here
        # This layout shows how the buttons are arranged in the calculator. Each button (i.e. key) has a name which is show in the button,
        # keyboard key name (which is used to map keyboard strikes to correct buttons) and a functions that will be called when the button
        # is pressed
        self._button_layout = [[Key('sin', '', [add_to_input]),          Key('cos', '', [add_to_input]),          Key('tan', '', [add_to_input]),          Key('max', '', [add_to_input]),          Key('min', '', [add_to_input])],
                               [Key('7', '7', [add_to_input]),           Key('8', '8', [add_to_input]),           Key('9', '9', [add_to_input]),           Key('+', 'plus', [add_to_input]),        Key('ln', '', [add_to_input])],
                               [Key('4', '4', [add_to_input]),           Key('5', '5', [add_to_input]),           Key('6', '6', [add_to_input]),           Key('-', 'minus', [add_to_input]),       Key('pi', '', [add_to_input])],
                               [Key('1', '1', [add_to_input]),           Key('2', '2', [add_to_input]),           Key('3', '3', [add_to_input]),           Key('*', 'asterisk', [add_to_input]),    Key('sqrt', '', [add_to_input]),     Key(',', 'comma', [add_to_input])],
                               [Key('(', 'parenleft', [add_to_input]),   Key('0', '0', [add_to_input]),           Key(')', 'parenright', [add_to_input]),  Key('/', 'slash', [add_to_input]),       Key('^', '', [add_to_input]),        Key('=', 'Return', [to_input_history, calculate, move_to_history, erase])],
                               [Key('C', 'BackSpace', [back_space]),     Key('AC', 'Delete', [erase]),            Key('.', 'period', [add_to_input]),      Key('log', '', [add_to_input]),          Key('e', '', [add_to_input]),        Key('→X', 'Right', [to_input_history, calculate, save_result_to_variable, move_to_history, erase])]]
        # This adds the buttons to the GUI and binds them to their functions        
        starting_row = 11
        for button_row in self._button_layout:
            for button in button_row:
                new_button = Button(self._button_frame, text=str(button.name), font=self._ui_font, height=2, width=4)
                new_button.grid(row=self._button_layout.index(button_row)+starting_row, column=button_row.index(button))
                bind_left_mouse_click_to_input_addition(new_button, button.name, button.functions)

        # Label and menu for setting the precision (i.e. how many decimals the results should have)
        self._precision_label = Label(self._button_frame, text="Precision:", font=self._ui_font)
        self._precision_label.grid(row=11, column=5, sticky="S")
        self._precision_menu = OptionMenu(self._button_frame, IntVar(), *list(range(0,11)))
        self._precision_menu.grid(row=12, column=5, sticky="N")

        # Label and menu for selecting variables to which results have been stored
        self._vars_label = Label(self._button_frame, text="Variables:", font=self._ui_font)
        self._vars_label.grid(row=12, column=5, sticky="S")
        self._vars_menu = OptionMenu(self._button_frame, StringVar(), *[""])
        self._vars_menu.grid(row=13, column=5, sticky="N")

        root.bind("<Key>", key_controls) # Binds any keyboard keys to the function handling them
        root.bind("<Up>", lambda x: combine([previous_input], None)) # For selecting previous input in input history
        root.bind("<Down>", lambda x: combine([next_input], None)) # For selecting next input in input history
