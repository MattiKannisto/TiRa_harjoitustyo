import typing
from tkinter import *
from services import algorithms, validation

def start_ui():
    root = Tk()
    root.resizable(width=False, height=False)
    root.title("Scientific Calculator")
    UserInterface(root)
    root.mainloop()

class UserInterface():
    """Graphical user interface for a scientific calculator.
    """

    def __init__(self, root):
        self._calculator = algorithms.Calculator()
        self._validator = validation.Validator()
        # Variables used by the GUI
        self._root = root
        self._ui_font = "Arial, 15"
        self._variables = {}
        self._input = StringVar()
        self._button_layout = [['sin', 'cos', 'tan', 'max', 'min'],
                               ['7',   '8',   '9',   '+',   'ln'],
                               ['4',   '5',   '6',   '-',   'pi'],
                               ['1',   '2',   '3',   '*',   'sqrt', ','],
                               ['(',   '0',   ')',   '/',   '^',    '='],
                               ['C',   'AC',  '.',   'log', 'e',    '→X']]

        def append_to_input(menu_var):
            self._input.set(self._input.get() + menu_var)
            update_input_area()

        def move_to_history(current_input):
            self._history_area[-1].config(text=current_input)
            self._input.set("")

        def update_input_area() -> None:
            self._input_area.config(text=self._input.get())

        def move_old_history_upwards():
            for i in range(len(self._history_area)-1):
                self._history_area[i].config(text=self._history_area[i+1].cget('text'))

        def save_result_to_variable(result):
            next_var = chr(ord('A')+len(self._variables))
            self._variables[next_var] = result
            self._variables_menu["menu"].add_command(label=next_var, command=lambda: append_to_input(next_var))

        def add_to_input(*event: Event) -> None:
            if not event:
                button_pressed = "="
            else:
                button_pressed = event[0].widget.cget('text')
            if button_pressed == "C":
                self._input.set(self._input.get()[:-1])
            elif button_pressed == "AC":
                self._input.set("")
            elif self._input.get() and (button_pressed == "=" or button_pressed == '→X'):
                move_old_history_upwards()
                self._calculator.set_input(self._input.get(), self._variables)
                if self._validator.unassigned_variables(self._calculator.input_ints, self._variables):
                    move_to_history("Unassigned variables used!")
                elif self._validator.improper_operator_use(self._calculator.input_ints):
                    move_to_history("Invalid use of operators!")
                elif self._validator.lone_dot_found(input_list=self._calculator.input_elements):
                    move_to_history("Invalid use of dot!")
                elif self._validator.improper_function_use(input_list=self._calculator.input_elements):
                    move_to_history("Invalide use of functions!")
                elif not self._calculator.input_elements_in_postfix:
                    move_to_history("Mismatched parentheses!")
                else:
                    self._calculator.calculate_result()
                    self._calculator.input_chars += " = " + str(self._calculator.result)
                    if button_pressed == '→X':
                        save_result_to_variable(self._calculator.result)
                        self._calculator.input_chars += " → " + chr(ord('A')-1+len(self._variables.keys()))
                    move_to_history(self._calculator.input_chars)
            else:
                self._input.set(self._input.get() + button_pressed)
            update_input_area()

        self._button_frame = Frame(self._root)
        self._button_frame.grid(row=0,column=0)
        self._button_frame.pack_propagate(0)

        self._history_area = []
        for i in range(10):
            self._history_area.append(Label(self._button_frame, font=self._ui_font, text="", background="white", anchor="w", justify="left"))
            self._history_area[-1].grid(row=i, column=0, columnspan=10, sticky="EW")

        self._input_area = Label(self._button_frame, text=self._input.get(), font=self._ui_font, background="white", anchor="w", justify="left")
        self._input_area.grid(row=10, column=0, columnspan=10, sticky="EW")

        def bind_right_mouse_click_to_input_addition(button):
            button.bind('<Button-1>', add_to_input)

        starting_row = 11
        for button_row in self._button_layout:
            for button in button_row:
                if button:
                    new_button = Button(self._button_frame, text=str(button), font=self._ui_font, height=2, width=4)
                    new_button.grid(row=self._button_layout.index(button_row)+starting_row, column=button_row.index(button))
                    bind_right_mouse_click_to_input_addition(new_button)

        self._var_label = Label(self._button_frame, text="Variables:", font=self._ui_font)
        self._var_label.grid(row=11, column=5, sticky="S")

        menu_var = StringVar()
        self._variables_menu = OptionMenu(self._button_frame, menu_var, *[""])
        self._variables_menu.grid(row=12, column=5, sticky="N")

        def key_controls(event):
            operator_keys = {'plus': '+', 'minus': '-', 'asterisk': '*', 'slash': '/', 'parenleft': '(',
                    'parenright': ')', 'period': '.', 'comma': ","}
            key = event.keysym
            if key == "BackSpace":
                self._input.set(self._input.get()[:-1])
                update_input_area()
            elif key == 'Return':
                add_to_input()
            if operator_keys.get(key):
                key = operator_keys.get(key)
            if key == " ":
                self._input.set(self._input.get() + key)
                update_input_area()
            for row in self._button_layout:
                for button in row:
                    if len(key) == 1 and button == key:
                        self._input.set(self._input.get() + key)
                        update_input_area()

            if len(key) == 1 and (ord(key) in range(ord('a'),ord('z')+1) or ord(key) in range(ord('A'),ord('Z')+1)):
                self._input.set(self._input.get() + key)
                update_input_area()

        root.bind("<Key>", key_controls)
