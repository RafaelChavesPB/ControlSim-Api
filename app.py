from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from utils.exceptions import ComplexCoef, InvalidType
from modules.system import System
import numpy as np
import re

app = Flask(__name__)
CORS(app)



def format_root(root):
    root = re.sub('[iIjJ]', 'j', root)
    root = re.sub('([-+])j$', '\g<1>1j', root)
    root = re.sub('^j$', '1j', root)
    return root


def get_poly(str_input, type):
    if type == 'poly':
        try:
            poly = list(map(float, str_input.split()))
            return poly
        except:
            raise ValueError

    elif type == 'roots':
        try:
            roots = list(map(format_root, str_input.split()))
            roots = list(map(complex, roots))
        except:
            raise ValueError

        poly = [1]
        for r in roots:
            poly = np.convolve(poly, [1, -r])
        poly = np.round(poly, 4)

        if any(np.imag(poly)):
            raise ComplexCoef

        return np.real(poly)

    else:
        raise InvalidType


def process_data(data: dict) -> System:

    # Recebe e trata as informações do sistema
    if 'system' not in data:
        raise Exception("Dados do sistema não informados.")

    system_data = data['system']
   
    gain = float(system_data.get('gain', 1))

    if 'num' not in system_data:
        raise Exception("Numerador do sistema não informado.")
    if 'den' not in system_data:
        raise Exception("Denominador do sistema não informado.")
    if 'num_type' not in system_data:
        raise Exception("Tipo de numerador do sistema não informado.")
    if 'den_type' not in system_data:
        raise Exception("Tipo de denominador do sistema não informado.")

    try:
        field = 'numerador'
        num = get_poly(system_data['num'], system_data.get('num_type'))
        field = 'denominador'
        den = get_poly(system_data['den'], system_data.get('den_type'))
    except ComplexCoef:
        raise Exception(
            f'O polinômio resultante no {field} do sistema possui conficientes complexos.')
    except InvalidType:
        raise Exception(f'Tipo do {field} do sistema não é valido.')
    except ValueError:
        raise Exception(
            f'{field.capitalize()} do sistema possui caracteres incompatíveis.')
    num = get_poly(system_data['num'], system_data.get(
        'num_type'))
    den = get_poly(system_data['den'], system_data.get(
        'den_type'))

    amplitude = float(data.get('amplitude', 1))
    feedback = data.get('feedback', False)
    sys = System(num, den, gain, amplitude, feedback)

    # Recebe e trata as informações do compensador (caso exista)
    if 'comp' in data:    
        comp_data = data['comp']
        gain_comp = float(comp_data.get('gain', 1))
        if 'num' not in comp_data:
            raise Exception("Numerador do compensador não informado.")
        if 'den' not in comp_data:
            raise Exception("Denominador do compensador não informado.")
        if 'num_type' not in comp_data:
            raise Exception("Tipo de numerador do compensador não informado.")
        if 'den_type' not in comp_data:
            raise Exception(
                "Tipo de denominador do compensador não informado.")

        try:
            field = 'numerador'
            num_comp = get_poly(comp_data['num'], comp_data.get('num_type'))
            field = 'denominador'
            den_comp = get_poly(comp_data['den'], comp_data.get('den_type'))
        except ComplexCoef:
            raise Exception(
                f'O polinômio resultante no {field} do compensador possui conficientes complexos.')
        except InvalidType:
            raise Exception(f'Tipo do {field} do compensador não é valido.')
        except ValueError:
            raise Exception(
                f'{field.capitalize()} do compensador possui caracteres incompatíveis.')

        sys.conf_comp(num_comp, den_comp, gain_comp)

    # Recebe e trata as informações do PID (caso exista)
    if 'pid' in data:
        pid_data = data['pid']
        kp = float(pid_data.get('kp', 0))
        kd = float(pid_data.get('kd', 0))
        ki = float(pid_data.get('ki', 0))
        tune = pid_data.get('tune', False)
        filter_ = pid_data.get('filter', False)
        type_ = pid_data.get('type', 'parallel')
        if kp or kd or ki or tune:
            sys.conf_pid(kp, ki, kd, type_, filter_, tune)

    return sys


def process_simulations(data: dict, sys: System) -> dict:
    results = {'plots': {}, 'values': {}}

    if 'plots' in data:
        plots = data['plots']
        if 'impulse_response' in plots:
            results['plots']['impulse_response'] = sys.impulse_response()
        if 'step_response' in plots:
            results['plots']['step_response'] = sys.step_response()
        if 'pzmap' in plots:
            results['plots']['pzmap'] = sys.pzmap()
        if 'rlocus' in plots:
            results['plots']['rlocus'] = sys.rlocus()

        results['values']['tf'] = str(sys)
        results['values']['zeros'] = sys.zeros()
        results['values']['poles'] = sys.poles()

    return results


@app.route('/api/', methods=['post'])
def index():
    try:
        data = request.get_json()
        sys = process_data(data)
        results = process_simulations(data, sys)
    except Exception as error:
        abort(400, description=str(error))
    return jsonify(results), 200

@app.errorhandler(400)
def json_error(e):
    return jsonify(error=e.description), 400


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')