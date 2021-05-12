import tkinter as tk
from tkinter import messagebox


class TicTac:

    _window = tk.Tk()
    WIDTH = 3
    first = True
    counter = 0
    winner = False

    def __init__(self):
        self.buttons = []
        for i in range(TicTac.WIDTH):
            t = []
            for j in range(TicTac.WIDTH):
                btn = MyButton(TicTac._window)
                btn.config(command=lambda button=btn: self.click(button))
                t.append(btn)
            self.buttons.append(t)

    def _create_field(self):
        for i in range(TicTac.WIDTH):
            for j in range(TicTac.WIDTH):
                btn = self.buttons[i][j]
                btn.grid(row=i, column=j)

    def print_symbol(self, btn, symbol, color):
        btn.config(text=symbol, disabledforeground=color)

    def click(self, clicked_btn):
        if clicked_btn.active:
            if TicTac.first:
                self.print_symbol(clicked_btn, 'x', 'blue')
                clicked_btn.symbol = 'x'
                self.check_winner('x')
                TicTac.first = False
            else:
                self.print_symbol(clicked_btn, 'o', 'red')
                clicked_btn.symbol = 'o'
                self.check_winner('o')
                TicTac.first = True
            TicTac.counter += 1

        clicked_btn.active = False
        clicked_btn.config(state='disabled')

    def check_line(self, btn1, btn2, btn3, sm):
        if btn1.symbol == sm and btn2.symbol == sm and btn3.symbol == sm:
            btn1.config(background='orange')
            btn2.config(background='orange')
            btn3.config(background='orange')
            TicTac.winner = True
            self.disable_buttons()

    @staticmethod
    def show_message(text):
        messagebox.showinfo(title='Игра окончена', message=text)

    def check_winner(self, sm):
        for n in range(3):
            self.check_line(
                self.buttons[n][0], self.buttons[n][1], self.buttons[n][2], sm)
            self.check_line(
                self.buttons[0][n], self.buttons[1][n], self.buttons[2][n], sm)
        self.check_line(self.buttons[0][0],
                        self.buttons[1][1], self.buttons[2][2], sm)
        self.check_line(self.buttons[2][0],
                        self.buttons[1][1], self.buttons[0][2], sm)

        if TicTac.winner:
            if sm == 'x':
                self.show_message('Крестики победили!')
            else:
                self.show_message('Нолики победили!')

        if TicTac.counter == 8 and not TicTac.winner:
            self.show_message('Ничья!')

    def disable_buttons(self):
        for i in range(TicTac.WIDTH):
            for j in range(TicTac.WIDTH):
                self.buttons[i][j].config(state='disabled')

    def start(self):
        self._create_field()
        TicTac._window.title('Крестики-нолики')
        TicTac._window.resizable(0, 0)
        TicTac._window.mainloop()


class MyButton(tk.Button):

    def __init__(self, master, *args, **kwargs):
        super(MyButton, self).__init__(master, width=5,
                                       height=2, font='Calibri 25 bold', *args, **kwargs)
        self.active = True
        self.symbol = None

    def __repr__(self):
        return f'MyButton: x={self.x} y={self.y}'


game = TicTac()
game.start()
