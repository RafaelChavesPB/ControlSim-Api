from flask import Flask, request, jsonify
from utils.system import System
import numpy as np
import re

app = Flask(__name__)

def format_root(root):
    root = re.sub('[iIjJ]', 'j', root)
    root = re.sub('([-+])j$', '\g<1>1j', root)
    root = re.sub('^j$', '1j', root)
    return root

def get_poly(str_input, type='poly'):
    if type == 'poly':
        poly = list(map(float, str_input.split()))
        return poly

    elif type == 'roots':
        roots = list(map(format_root, str_input.split()))
        roots = list(map(complex, roots))

        poly = [1]
        for r in roots:
            poly = np.convolve(poly, [1, -r])
        poly = np.round(poly, 4)

        if any(np.imag(poly)):
            raise ValueError()

        return np.real(poly)

    else:
        raise ValueError()


def process_system(system_data: dict) -> System:
    if 'num' not in system_data or 'den' not in system_data:
        raise ValueError()

    num = get_poly(system_data['num'], system_data.get('num_type'))
    den = get_poly(system_data['den'], system_data.get('den_type'))

    gain = system_data.get('gain', 1)
    feedback = system_data.get('feedback', False)

    sys = System(num, den, feedback, gain)

    if 'comp' in system_data:
        comp_data = system_data['comp']

        if 'num' not in comp_data or 'den' not in comp_data:
            raise ValueError()

        num = get_poly(comp_data['num'], comp_data.get('num_type'))
        den = get_poly(comp_data['den'], comp_data.get('den_type'))
        gain = comp_data.get('gain', 1)
        sys.conf_comp(num, den, gain)

    if 'pid' in system_data:
        pid_data = system_data['pid']

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
            results['plots']['pzmap'] = sys.rlocus()

    if 'values' in data:
        values = data['values']
        if 'system' in values:
            results['values']['system'] = str(sys)
        if 'zeros' in values:
            results['values']['zeros'] = sys.zeros()
        if 'poles' in values:
            results['values']['poles'] = sys.poles()

    return results

def process_json(data: dict) -> dict:
    sys = process_system(data['system'])
    results = process_simulations(data, sys)
    return results 

@app.route('/', methods=['get'])
def alive():
    return 'Server Alive!'

@app.route('/', methods=['post'])
def index():
    data = request.get_json()
    if 'system' in data:
        results = process_json(data)
    return jsonify(results = results), 200
