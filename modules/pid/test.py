from pid import PID
import tunning_methods as tn
from unittest import TestCase

# Teste de skogestad abaixo:

def test_skogestad_second_case(): # 
    pid_test = PID(num=[1], den=[0.603, 1], tune = "skogestad", filter = 0, type = "parallel")
    kp,ki,kd = pid_test.get_pid_parameters()
    print("os valores de kp, ki e kd são: kp = 1.42, ki = 0.603, e kd = 0")
    print(f"os valores de kp, ki e kd calculados pelo PID foram de :{kp}, {ki}, {kd} ")

def test_skogestad_third_case(): # 
    pid_test = PID(num=[1], den=[1, 2, 0], tune = "skogestad", filter = 0, type = "parallel")
    kp,ki,kd = pid_test.get_pid_parameters()
    print("os valores de kp, ki e kd são: kp = 5.71, ki = 1.4, e kd = 0.5")
    print(f"os valores de kp, ki e kd calculados pelo PID foram de :{kp}, {ki}, {kd} ")

def test_skogestad_fourth_case(): # 
    pid_test = PID(num=[1], den=[1, 6, 5], tune = "skogestad", filter = 0, type = "parallel" )
    kp,ki,kd = pid_test.get_pid_parameters()
    print("os valores de kp, ki e kd são: kp = 7.14, ki = 1, e kd = 0.2")
    print(f"os valores de kp, ki e kd calculados pelo PID foram de :{kp}, {ki}, {kd} ")

def test_skogestad_last_case(): # 
    pid_test = PID(num=[2], den=[2, 0, 0], tune = "skogestad", filter = 0, type = "parallel" )
    kp,ki,kd = pid_test.get_pid_parameters()
    print("os valores de kp, ki e kd são: kp = 0.127, ki = 2.8, e kd = 2.8")
    print(f"os valores de kp, ki e kd calculados pelo PID foram de :{kp}, {ki}, {kd} ")

# Teste de sistemas de primeira ordem com atraso:

def test_ziegle_nichols_pid():
    pid_test = PID(num=[1/20], den=[1, 1/20], tune = "ziegle_pid", filter = 0, type = "parallel", delay = 5) 
    kp,ki,kd = pid_test.get_pid_parameters()
    print("os valores de kp, ki e kd são: kp = 4.8, ki = 10, e kd = 2.5")
    print(f"os valores de kp, ki e kd calculados pelo PID foram de :{kp}, {ki}, {kd} ")

def test_ziegle_nichols_pi():
    pid_test = PID(num=[1], den=[20, 1], tune = "ziegle_pi", filter = 0, type = "parallel", delay = 5) 
    kp,ki,kd = pid_test.get_pid_parameters()
    print("os valores de kp, ki e kd são: kp = 3.6, ki = 16.5, e kd = 0")
    print(f"os valores de kp, ki e kd calculados pelo PID foram de :{kp}, {ki}, {kd} ")

def test_chr_pid():
    pid_test = PID(num=[1], den=[20, 1], tune = "chr_pid", filter = 0, type = "parallel", delay = 5) 
    kp,ki,kd = pid_test.get_pid_parameters()
    kp_calc = (0.6*20)/(1*5)
    ki_calc = 20
    kd_calc = 5/2
    print(f"os valores de kp, ki e kd são: kp = {kp_calc}, ki = {ki_calc}, e kd = {kd_calc}")
    print(f"os valores de kp, ki e kd calculados pelo PID foram de :{kp}, {ki}, {kd} ")

def test_chr_pi():
    pid_test = PID(num=[1], den=[20, 1], tune = "chr_pi", filter = 0, type = "parallel", delay = 5) 
    kp,ki,kd = pid_test.get_pid_parameters()
    kp_calc = (0.35*20)/(1*5)
    ki_calc = 1.16*20
    kd_calc = 0
    print(f"os valores de kp, ki e kd são: kp = {kp_calc}, ki = {ki_calc}, e kd = {kd_calc}")
    print(f"os valores de kp, ki e kd calculados pelo PID foram de :{kp}, {ki}, {kd} ")

def test_chr20_pid():
    pid_test = PID(num=[1], den=[20, 1], tune = "chr20_pid", filter = 0, type = "parallel", delay = 5) 
    kp,ki,kd = pid_test.get_pid_parameters()
    kp_calc = (0.95*20)/(1*5)
    ki_calc = 1.357*20
    kd_calc = 5*0.473
    print(f"os valores de kp, ki e kd são: kp = {kp_calc}, ki = {ki_calc}, e kd = {kd_calc}")
    print(f"os valores de kp, ki e kd calculados pelo PID foram de :{kp}, {ki}, {kd} ")

def test_chr20_pi():
    pid_test = PID(num=[1], den=[20, 1], tune = "chr20_pi", filter = 0, type = "parallel", delay = 5) 
    kp,ki,kd = pid_test.get_pid_parameters()
    kp_calc = (0.6*20)/(1*5)
    ki_calc = 20
    kd_calc = 0
    print(f"os valores de kp, ki e kd são: kp = {kp_calc}, ki = {ki_calc}, e kd = {kd_calc}")
    print(f"os valores de kp, ki e kd calculados pelo PID foram de :{kp}, {ki}, {kd} ")

# Teste de tunelamentos para funções de segunda ordem com atraso:





# Executor da função de testes
 
if __name__ == "__main__":
    #test_skogestad()
    test_chr20_pid()
