import typing
from tkinter import *
from algorithms import algorithms, validation

def start_ui():
    root = Tk()
    root.resizable(width=False, height=False)
    root.title("Scientific Calculator")
    UserInterface(root)
    root.mainloop()


class UserInterface():
    """A class for the graphical user interface of a scientific calculator.
    """

    def __init__(self, root):
        self._operators_ints = algorithms.string_to_unicode_code_point_integers('+-*/^')
        self._dot_int = ord('.')
        self._space_int = ord(' ')
        self._left_bracket_int = ord('(')       
        self._right_bracket_int = ord(')')
        self._var_ints = range(ord('A'),ord('Z')+1)
        self._operator_char_ints = range(ord('a'),ord('z')+1)
        self._number_ints = range(ord('0'),ord('9')+1)
        self._function_names = {ord('s'): {ord('i'): {ord('n'): "sin"}, ord('q'): {ord('r'): {ord('t'): "sqrt"}}},
                               ord('m'): {ord('a'): {ord('x'): "max"}, ord('i'): {('n'): "min"}},
                               ord('l'): {ord('n'): "ln", ord('o'): {ord('g'): "log"}},
                               ord('c'): {ord('o'): {ord('s'): "cos"}},
                               ord('p'): {ord('i'): "pi"},
                               ord('e'): "e"}

        self._root = root
        self._ui_font = "Arial, 15"
        self._variables = {}
        self._input = StringVar()
        self._history = StringVar()
        self._button_layout = [['sin','cos','tan','max','min'],
                               ['7','8','9','+','ln'],
                               ['4','5','6','-','pi'],
                               ['1','2','3','*','sqrt'],
                               ['(','0',')','/','^','='],
                               ['C','AC','.','log','e', '→X']]

        def move_to_history(current_input):
            self._history_area[-1].config(text=current_input)
            self._input.set("")

        def update_input_area() -> None:
            self._input_area.config(text=self._input.get())

        def move_old_history_upwards():
            for i in range(len(self._history_area)-1):
                self._history_area[i].config(text=self._history_area[i+1].cget('text'))

        def save_result_to_variable():
            next_var = chr(ord('A')+len(self._variables))
            self._variables[next_var] = len(self._variables)
            self._variables_menu["menu"].add_command(label=next_var, command=lambda: append_to_input(next_var))

        def add_to_input(event: Event) -> None:
            button_pressed = event.widget.cget('text')
            if button_pressed == "C":
                self._input.set(self._input.get()[:-1])
            elif button_pressed == "AC":
                self._input.set("")
            elif button_pressed == "=" or button_pressed == '→X':
                if input := self._input.get():
                    move_old_history_upwards()
                    chars_as_ints = algorithms.string_to_unicode_code_point_integers(input)
                    if validation.incorrect_brackets(chars_as_ints):
                        move_to_history("Invalid use of brackets!")
                    elif validation.unassigned_variables(chars_as_ints, self._var_ints, range(ord('A'),ord('A')+len(self._variables.keys())+1)):
                        move_to_history("Unassigned variables used!")
                    elif validation.improper_operator_use(chars_as_ints, self._operators_ints):
                        move_to_history("Invalid use of operators!")
                    else:
                        input_list = algorithms.input_int_list_to_input_element_list(input=chars_as_ints, alphabets=self._operator_char_ints,
                                                                                     variables=self._var_ints, numbers=self._number_ints,
                                                                                     left_bracket=self._left_bracket_int, right_bracket=self._right_bracket_int,
                                                                                     dot=self._dot_int, operators=self._operators_ints, space=self._space_int)
                        input += " = [result]"
                        if button_pressed == '→X':
                            save_result_to_variable()
                            input += " = " + list(self._variables.keys())[-1]
                        move_to_history(input)
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
                    new_button = Button(self._button_frame, text=str(button), font=self._ui_font, height=5, width=10)
                    new_button.grid(row=self._button_layout.index(button_row)+starting_row, column=button_row.index(button))
                    bind_right_mouse_click_to_input_addition(new_button)

        def append_to_input(menu_var):
            self._input.set(self._input.get() + menu_var)
            update_input_area()

        self._var_label = Label(self._button_frame, text="Variables:", font=self._ui_font)
        self._var_label.grid(row=11, column=5, sticky="S")

        menu_var = StringVar()
        self._variables_menu = OptionMenu(self._button_frame, menu_var, *[""])
        self._variables_menu.grid(row=12, column=5, sticky="N")