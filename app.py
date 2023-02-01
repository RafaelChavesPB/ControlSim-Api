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
    print(data)
    if 'system' not in data:
        raise Exception("Dados do sistema não informados.")

    system_data = data['system']
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
            f'O polinômio resultante do {field} do sistema possui conficiêntes complexos.')
    except InvalidType:
        raise Exception(f'Tipo do {field} do sistema não é valido.')
    except ValueError:
        raise Exception(
            f'{field.capitalize()} do sistema possui caractéres incompatíveis.')
    num = get_poly(system_data['num'], system_data.get(
        'num_type'))
    den = get_poly(system_data['den'], system_data.get(
        'den_type'))

    gain = int(system_data.get('gain', 1))
    feedback = data.get('feedback', False)
    sys = System(num, den, feedback, gain)

    if 'comp' in data:
        comp_data = data['comp']
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
                f'O polinômio resultante do {field} do compensador possui conficiêntes complexos.')
        except InvalidType:
            raise Exception(f'Tipo do {field} do compensador não é valido.')
        except ValueError:
            raise Exception(
                f'{field.capitalize()} do compensador possui caractéres incompatíveis.')

        gain_comp = comp_data.get('gain', 1)
        sys.conf_comp(num_comp, den_comp, gain_comp)

    if 'pid' in data:
        pid_data = data['pid']
        kp = pid_data.get('kp', 0)
        kd = pid_data.get('kd', 0)
        ki = pid_data.get('ki', 0)

        if kp or kd or ki:
            sys.conf_pid(kp, ki, kd)


    return sys


def process_simulations(data: dict, sys: System) -> dict:
    results = {'plots': {}, 'values': {}}

    if 'plots' in data:
        plots = data['plots']
        if 'step_response' in plots:
            results['plots']['step_response'] = sys.step_response()
        if 'pzmap' in plots:
            results['plots']['pzmap'] = sys.pzmap()
        if 'rlocus' in plots:
            results['plots']['rlocus'] = sys.rlocus()

    if 'values' in data:
        values = data['values']
        if 'system' in values:
            results['values']['system'] = str(sys)
        if 'zeros' in values:
            results['values']['zeros'] = sys.zeros()
        if 'poles' in values:
            results['values']['poles'] = sys.poles()

    return results


@app.route('/', methods=['post'])
def index():
    try:
        data = request.get_json()
        sys = process_data(data)
        results = process_simulations(data, sys)
    except Exception as error:
        abort(400, description=str(error))
    return jsonify(results=results), 200


@app.errorhandler(400)
def json_error(e):
    return jsonify(error=e.description), 400
