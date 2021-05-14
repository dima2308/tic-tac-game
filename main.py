import os
import sys
import random
import tkinter as tk
from tkinter import messagebox


class TicTac:

    _window = tk.Tk()
    WIDTH = 3
    first = None
    counter = 0
    winner = False
    type_game = None

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
        self.sm = 'x' if TicTac.first else 'o'
        self.b = tk.Label(text=self.sm, fg="black", font='Arial 14')
        self.b.grid(row=3, column=1)

        for i in range(TicTac.WIDTH):
            for j in range(TicTac.WIDTH):
                btn = self.buttons[i][j]
                btn.grid(row=i, column=j)

    def print_symbol(self, btn, symbol, color):
        btn.config(text=symbol, disabledforeground=color)

    def get_empty_btn(self, line, btn):
        if btn.active:
            return btn
        else:
            return self.get_empty_btn(random.choice(self.buttons), random.choice(line))

    def set_active_state(self, btn):
        btn.active = False
        btn.config(state='disabled')

    def move(self, btn, sm, color, player_flag):
        self.print_symbol(btn, sm, color)
        btn.symbol = sm
        self.check_winner(sm)
        TicTac.first = player_flag

    def set_symbol(self):
        self.sm = 'x' if self.sm == 'o' else 'o'

    def click(self, clicked_btn):
        if TicTac.type_game == 'no':
            """ Игра друг с другом """
            if clicked_btn.active:
                if TicTac.first:
                    self.move(clicked_btn, 'x', 'blue', False)
                    self.b.config(text='o')
                else:
                    self.move(clicked_btn, 'o', 'red', True)
                    self.b.config(text='x')
                TicTac.counter += 1

            self.set_active_state(clicked_btn)

        else:
            """ Игра с компьютером """
            if clicked_btn.active:
                self.move(clicked_btn, self.sm, 'blue', True)
                self.set_symbol()

            self.set_active_state(clicked_btn)

            if TicTac.counter != 8 and not TicTac.winner:
                line = random.choice(self.buttons)
                btn = random.choice(line)
                empty_btn = self.get_empty_btn(line, btn)
                self.move(empty_btn, self.sm, 'red', False)
                self.set_active_state(empty_btn)
                self.set_symbol()

            TicTac.counter += 2

    def check_line(self, btn1, btn2, btn3, sm):
        if btn1.symbol == sm and btn2.symbol == sm and btn3.symbol == sm:
            btn1.config(background='orange')
            btn2.config(background='orange')
            btn3.config(background='orange')
            TicTac.winner = True
            self.disable_buttons()

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
            if TicTac.choose_option():
                TicTac.restart()

        if TicTac.counter == 8 and not TicTac.winner:
            self.show_message('Ничья!')
            if TicTac.choose_option():
                TicTac.restart()

    def disable_buttons(self):
        for i in range(TicTac.WIDTH):
            for j in range(TicTac.WIDTH):
                self.buttons[i][j].config(state='disabled')

    def start(self):
        TicTac.type_game = messagebox.askquestion(
            "Выбор противника", "Игра с компьютером?")
        TicTac.first = messagebox.askyesno(
            "Выбор символа", "Крестики начинают?")
        self._create_field()
        TicTac._window.title('Крестики-нолики')
        TicTac._window.resizable(0, 0)
        TicTac._window.mainloop()

    @staticmethod
    def show_message(text):
        messagebox.showinfo(title='Игра окончена', message=text)

    @staticmethod
    def choose_option():
        return messagebox.askyesno("Выбор действия", "Заново?")

    @staticmethod
    def restart():
        python = sys.executable
        os.execl(python, python, * sys.argv)


class MyButton(tk.Button):

    def __init__(self, master, *args, **kwargs):
        super(MyButton, self).__init__(master, width=5,
                                       height=2, font='Calibri 25 bold', *args, **kwargs)
        self.active = True
        self.symbol = None

    def __repr__(self):
        return f'MyButton: x={self.active} y={self.symbol}'


game = TicTac()
game.start()
