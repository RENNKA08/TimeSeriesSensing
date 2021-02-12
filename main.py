import tkinter as tk

from tss.Application import Application

def main():
    root = tk.Tk()

    application = Application(root)
    application.mainloop()


if __name__ == '__main__':
    main()
