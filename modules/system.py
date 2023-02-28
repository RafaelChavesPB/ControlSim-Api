from io import BytesIO
from turtle import delay
from urllib import parse
from base64 import b64encode
import control as co
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from . import pid

matplotlib.use("Agg")

class System:
    def __init__(self, num: list, den: list, feedback: bool = False, gain: float = 1, delay : int = 0) -> None:
        self.__num = num
        self.__den = den
        self.__delay = delay
        self.__gs = gain*co.tf(num, den)
        self.__comp = co.tf(1, 1)
        self.__pid = co.tf(1, 1)
        self.__pade = co.tf(1 , 1)
        self.__feedback = feedback
        self.__kgain = 1
        self.__put_delay()
        self.__update_system()

    def __update_system(self) -> None:
        self.__open_loop = self.__kgain*self.__gs*self.__comp*self.__pid*self.__pade
        self.__closed_loop = co.feedback(self.__open_loop)
        self.__system = self.__closed_loop if self.__feedback else self.__open_loop

    def conf_gs(self, num: list, den: list, gain: float = 1) -> None:
        self.__gs = gain*co.tf(num, den)
        self.__update_system()

    def __put_delay(self) -> None:
        if self.__delay > 0:
            num,den = co.pade(T = self.__delay, n = 3, numdeg = 3)
            self.__pade = co.tf(num,den)
        

    def conf_kgain(self, k: float):
        self.__kgain = k
        self.__update_system()

    def open_loop(self):
        self.__feedback = False
        self.__update_system()

    def close_loop(self):
        self.__feedback = True
        self.__update_system()

    def conf_pid(self, kp: float, ki: float,  kd: float, pid_type: str, filter: str, tune: str) -> None:
        """ Essa função usa a classe PID para achar o pid, os parâmetros kp,ki,kd podem ser qualquer coisa se
        o tune for "sim", pois o tune irá cacular esses parâmetros, caso contrário o usuário deverá passar valores
        que fazem sentido para esses parâmetros, um pid desintonizado pode fazer a curva divergir, o parâmetros 
        tune deve ser skogestad ou não, o tipo de pid deve ser "series" ou "parallel", e o filtro deve ser um valor.
        Se o filtro não for desejado pelo usuário deve ser passado 0."""

        pid_object = pid.PID(num=self.__num, den=self.__den, kp=kp,
                         ki=ki, kd=kd, tune=tune, type=pid_type, filter=filter, delay = self.__delay)
        pid_num, pid_den = pid_object.get_pid_only()
        self.__pid = co.tf(pid_num, pid_den)
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
