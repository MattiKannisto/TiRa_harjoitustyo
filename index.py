from tkinter import *
from ui import UserInterface

def main():
    root = Tk()
    root.title("Scientific Calculator")
    UserInterface(root)
    root.mainloop()

if __name__ == '__main__':
    main()