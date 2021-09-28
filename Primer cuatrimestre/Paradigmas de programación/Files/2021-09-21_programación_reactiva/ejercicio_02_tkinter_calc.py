from tkinter import *
from tkinter.ttk import Combobox


class App:
    def __init__(self):
        self.__display = '0'
        self.__num_1 = None
        self.__num_2 = None
        self.window = Tk()
        self.window.title = 'KalkuleiTor!'

        self.display = Label(text=self.__display, font=('Arial Bold', 36))
        self.display.grid(column=0, row=0, columnspan=4, sticky='e')

        self.button7 = Button(text='7', command=self.pressedNum(7), pady=15, padx=20)
        self.button7.grid(column=0, row=1)
        self.button8 = Button(text='8', command=self.pressedNum(8), pady=15, padx=20)
        self.button8.grid(column=1, row=1)
        self.button9 = Button(text='9', command=self.pressedNum(9), pady=15, padx=20)
        self.button9.grid(column=2, row=1)
        self.buttonPlus = Button(text='+', command=self.pressedButton('+'), pady=15, padx=20)
        self.buttonPlus.grid(column=3, row=1)

        self.button4 = Button(text='4', command=self.pressedNum(4), pady=15, padx=20)
        self.button4.grid(column=0, row=2)
        self.button5 = Button(text='5', command=self.pressedNum(5), pady=15, padx=20)
        self.button5.grid(column=1, row=2)
        self.button6 = Button(text='6', command=self.pressedNum(6), pady=15, padx=20)
        self.button6.grid(column=2, row=2)
        self.buttonSubstract = Button(text='-', command=self.pressedButton('-'), pady=15, padx=20)
        self.buttonSubstract.grid(column=3, row=2)

        self.button1 = Button(text='1', command=self.pressedNum(1), pady=15, padx=20)
        self.button1.grid(column=0, row=3)
        self.button2 = Button(text='2', command=self.pressedNum(2), pady=15, padx=20)
        self.button2.grid(column=1, row=3)
        self.button3 = Button(text='3', command=self.pressedNum(3), pady=15, padx=20)
        self.button3.grid(column=2, row=3)
        self.buttonTimes = Button(text='*', command=self.pressedButton('*'), pady=15, padx=20)
        self.buttonTimes.grid(column=3, row=3)

        self.button0 = Button(text='0', command=self.pressedNum(0), pady=15, padx=20)
        self.button0.grid(column=0, row=4)
        self.buttonDivide = Button(text='/', command=self.pressedButton, pady=15, padx=20)
        self.buttonDivide.grid(column=1, row=4)
        self.buttonExec = Button(text='=', command=self.pressedButton('='), pady=15, padx=46)
        self.buttonExec.grid(column=2, row=4, columnspan=2)

        self.window.mainloop()

    def _set_display(self, num: str):
        self.__display = num
        self.display.configure(text=self.__display)

    def _sum(self, a, b):
        return a + b

    def _sub(self, a, b):
        return a - b

    def _div(self, a, b):
        return a / b  # Lmao pls don't divide by 0 k thx

    def _mult(self, a, b):
        return a * b

    def _eq(self, a, b):
        return a

    def pressedButton(self, action: str):
        if self.__num_1 is None:
            return
        elif self.__num_2 is None:
            self.__num_2 = float(self.__num_1)
            self.__num_1 = None
            self._set_display('0')
            return

        self.__num_2 = {
            '+': self._sum,
            '-': self._sub,
            '/': self._div,
            '*': self._mult,
            '=': self._div
        }[action](self.__num_2, float(self.__num_1))
        self.__num_1 = None
        self._set_display(str(self.__num_2))

    def pressedNum(self, num: int):
        def action():
            tmp = str(num)
            if self.__num_1 is not None:
                tmp = self.__num_1 + tmp
            self._set_display(tmp)
            self.__num_1 = tmp
        return action

if __name__ == '__main__':
    App()
