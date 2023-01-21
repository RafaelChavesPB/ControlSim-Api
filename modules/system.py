from io import BytesIO
from urllib import parse
from base64 import b64encode
import control as co
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from .pid import *

matplotlib.use("Agg")

class System:
    def __init__(self, num: list, den: list, feedback: bool = False, gain: float = 1) -> None:
        self.__gs = gain*co.tf(num, den)
        self.__comp = co.tf(1, 1)
        self.__pid = co.tf(1, 1)
        self.__feedback = feedback
        self.__kgain = 1
        self.__update_system()

    def __update_system(self) -> None:
        self.__open_loop = self.__kgain*self.__gs*self.__comp*self.__pid
        self.__closed_loop = co.feedback(self.__open_loop)
        self.__system = self.__closed_loop if self.__feedback else self.__open_loop

    def conf_gs(self, num: list, den: list, gain: float = 1) -> None:
        self.__gs = gain*co.tf(num, den)
        self.__update_system()

    def conf_kgain(self, k: float):
        self.__kgain = k
        self.__update_system()

    def open_loop(self):
        self.__feedback = False
        self.__update_system()

    def close_loop(self):
        self.__feedback = True
        self.__update_system()

    def conf_pid(self, kp: float, ki: float,  kd: float) -> None:
        if kp or ki or kd:
            self.pid = co.tf([0], [1])
            self.pid += co.tf(float(kp), [1]
                              ) if kp and kp != '0' else co.tf([0], [1])
            self.pid += co.tf((float(ki)), [1, 0]
                              ) if ki and ki != '0' else co.tf([0], [1])
            self.pid += co.tf([float(kd), 0], [1]
                              ) if kd and kd != '0' else co.tf([0], [1])
        self.__update_system()

    def conf_comp(self, num: list, den: list, gain: float = 1) -> None:
        self.__comp = gain*co.tf(num, den)
        self.__update_system()

    def poles(self) -> tuple:
        return list(map(str, np.round(self.__system.poles(), 3)))

    def zeros(self) -> tuple:
        return list(map(str, np.round(self.__system.zeros(), 3)))

    def plot_decorator(generate_plot):
        def wrapper(self, *args, **kwargs):
            plt.clf()
            plt.figure(figsize=(6, 4), dpi=100)
            #####################
            generate_plot(self, *args, **kwargs)
            #####################
            if 'title' in kwargs:
                plt.title(kwargs['title'])
            fig = plt.gcf()
            buf = BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            word = b64encode(buf.read())
            url = parse.quote(word)
            plt.close()
            return url
        return wrapper

    @plot_decorator
    def step_response(self, *args, **kwargs):
        step = kwargs.get('step', 1)
        x, y = co.step_response(self.__system)
        plt.plot(x, y, label="Saida")
        plt.plot(x, [step]*len(x), label="Entrada")
        plt.ylabel('Amplitude')
        plt.xlabel('Tempo(s)')
        plt.legend()
        plt.grid()

    @plot_decorator
    def pzmap(self, *args, **kwargs):
        if len(self.__system.poles()):
            plt.scatter(np.real(self.__system.poles()), np.imag(
                self.__system.poles()), marker='x', s=75, facecolors='#1f77b4')
        if len(self.__system.zeros()):
            plt.scatter(np.real(self.__system.zeros()), np.imag(self.__system.zeros(
            )), marker='o', s=75, facecolors='#1f77b4', edgecolors='#1f77b4')
        plt.grid()
        plt.axhline(y=0, color='gray')
        plt.xlabel('Real')
        plt.axvline(x=0, color='gray')
        plt.ylabel('Imaginary')

    @plot_decorator
    def rlocus(self):
        co.root_locus(self.__open_loop, plot=True, grid=True)

    def tf(self) -> co.TransferFunction:
        return self.__system

    def gs(self) -> co.TransferFunction:
        return self.__gs

    def comp(self) -> co.TransferFunction:
        return self.__comp

    def pidcomp(self) -> co.TransferFunction:
        return self.__pid

    def open_loop_system(self) -> co.TransferFunction:
        return self.__open_loop

    def closed_loop_system(self) -> co.TransferFunction:
        return self.__open_loop

    def __str__(self) -> str:
        return str(self.__system)
