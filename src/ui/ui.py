import typing
import math
from tkinter import *
from services import algorithms, validation, math_functions

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
        # Unicode code point integers of all allowed characters of the input. These are used in identification
        # of different elements in the input for validation purposes
        self._operators_ints = algorithms.string_to_unicode_code_point_integers('+-*/^')
        self._dot_int = ord('.')
        self._space_int = ord(' ')
        self._left_bracket_int = ord('(')       
        self._right_bracket_int = ord(')')
        self._var_ints = range(ord('A'),ord('Z')+1)
        self._operator_char_ints = range(ord('a'),ord('z')+1)
        self._number_ints = range(ord('0'),ord('9')+1)
        # Dictionary for identifying function names from the input's lowercase alphabets
        self._function_names = {ord('s'): {ord('i'): {ord('n'): "sin"}, ord('q'): {ord('r'): {ord('t'): "sqrt"}}},
                               ord('m'): {ord('a'): {ord('x'): "max"}, ord('i'): {('n'): "min"}},
                               ord('l'): {ord('n'): "ln", ord('o'): {ord('g'): "log"}},
                               ord('c'): {ord('o'): {ord('s'): "cos"}},
                               ord('p'): {ord('i'): "pi"},
                               ord('e'): "e"}
        # Variables used by the GUI
        self._operations = {'+': math_functions.add, '-': math_functions.subtract, '*': math_functions.multiply,
                            '/': math_functions.divide, '^': math_functions.raise_to_exponent, 'sin': math.sin,
                            'cos': math.cos, 'tan': math.tan, 'max': max, 'min': min, 'ln': math.log, 'log': math.log10,
                            'pi': math.pi, 'sqrt': math.sqrt}
        self._operands_no = {'+': 2, '-': 2, '*': 2, '/': 2, '^': 2, 'sin': 1, 'cos': 1, 'tan': 1, 'max': 2, 'min': 2,
                             'ln': 1, 'log': 1, 'pi': 0, 'sqrt': 1}
        self._root = root
        self._ui_font = "Arial, 15"
        self._variables = {}
        self._input = StringVar()
        self._history = StringVar()
        self._button_layout = [['sin','cos','tan','max','min'],
                               ['7','8','9','+','ln'],
                               ['4','5','6','-','pi'],
                               ['1','2','3','*','sqrt', 'space'],
                               ['(','0',')','/','^','='],
                               ['C','AC','.','log','e', '→X']]

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
            elif button_pressed == "=" or button_pressed == '→X':
                if input := self._input.get():
                    move_old_history_upwards()
                    # Convert input strings characters into a list of unicode point integer list to simplify validation
                    chars_as_ints = algorithms.string_to_unicode_code_point_integers(input)
                    if validation.unassigned_variables(chars_as_ints, self._var_ints, range(ord('A'),ord('A')+len(self._variables.keys()))):
                        move_to_history("Unassigned variables used!")
                    elif validation.improper_operator_use(chars_as_ints, self._operators_ints):
                        move_to_history("Invalid use of operators!")
                    else:
                        input_list = algorithms.input_int_list_to_input_element_list(input=chars_as_ints, alphabets=self._operator_char_ints,
                                                                                     variables=self._var_ints, numbers=self._number_ints,
                                                                                     single_chars=[self._left_bracket_int,
                                                                                                   self._right_bracket_int, self._space_int],
                                                                                     dot=self._dot_int, operators=self._operators_ints,
                                                                                     space=self._space_int)
                        if validation.element_in_list(input_list=input_list, element=[self._dot_int]):
                            move_to_history("Invalid use of dot!")
                        # elif validation.improper_function_use(input_list=input_list, alphabets=self._operator_char_ints,
                        #                                       left_bracket=self._left_bracket_int, right_bracket=self._right_bracket_int,
                        #                                       numbers=self._number_ints, dot=self._dot_int):
                        #     move_to_history("Invalide use of functions!")
                        else:
                            input_list_in_postfix_notation = algorithms.shunting_yard(validated_input=input_list, alphabets=self._operator_char_ints,
                                                                                      numbers=self._number_ints, left_bracket=self._left_bracket_int,
                                                                                      right_bracket=self._right_bracket_int,
                                                                                      used_operators=self._operators_ints,
                                                                                      variables=self._variables)
                            if not input_list_in_postfix_notation:
                                move_to_history("Mismatched parentheses!")
                            else:
                                decimal_places = algorithms.get_min_number_of_decimal_places(input_list, self._dot_int)
                                input_in_postfix = algorithms.unicode_code_point_integers_to_values(input_list=input_list_in_postfix_notation,
                                                                                                    numbers=self._number_ints,
                                                                                                    variable_chars=self._var_ints,
                                                                                                    variables=self._variables)
                                result = algorithms.evaluate_input_in_postfix_notation(input_in_postfix, self._operations, self._operands_no)
                                if decimal_places == 0:
                                    result_with_correct_precision = int(result)
                                else:
                                    result_with_correct_precision = round(result, decimal_places)
                                input += " = " + str(result_with_correct_precision)
                                if button_pressed == '→X':
                                    save_result_to_variable(result_with_correct_precision)
                                    input += " → " + chr(ord('A')-1+len(self._variables.keys()))
                                move_to_history(input)
            else:
                if button_pressed == "space":
                    button_pressed = " "
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
                    'parenright': ')', 'period': '.', 'space': " "}
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

            if len(key) == 1 and (ord(key) in self._operator_char_ints or ord(key) in self._var_ints):
                self._input.set(self._input.get() + key)
                update_input_area()

        root.bind("<Key>", key_controls)
