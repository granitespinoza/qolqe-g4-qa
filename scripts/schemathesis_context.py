"""Ejemplos de control con recursos reales; no corrige los casos generados.

Compatible con hooks de Schemathesis 4.17.0. La generación aleatoria conserva
sus datos y respuestas. Solo los ejemplos añadidos aquí preparan su contexto.
"""
import json
import os
from pathlib import Path
import secrets
import time
import urllib.request

import schemathesis

CONTROLS = {}
RECORDS = {}
PREPARATION = []


def save_records():
    directory = Path(os.environ['QA_SCHEMATHESIS_REPORT_DIR'])
    directory.mkdir(parents=True, exist_ok=True)
    (directory/'controles-contexto.json').write_text(
        json.dumps(list(RECORDS.values()), ensure_ascii=False, indent=2), encoding='utf-8')
    (directory/'preparacion-contexto.json').write_text(
        json.dumps(PREPARATION, ensure_ascii=False, indent=2), encoding='utf-8')


@schemathesis.auth()
class DefaultAuth:
    def get(self, case, ctx):
        return os.environ.get('QA_SCHEMATHESIS_TOKEN')

    def set(self, case, data, ctx):
        case.headers['Authorization'] = 'Bearer '+data


def request(method, route, body=None, token=None):
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = 'Bearer '+token
    req = urllib.request.Request('http://127.0.0.1:8000'+route,
        data=json.dumps(body).encode() if body is not None else None,
        headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=15) as response:
        data = response.read()
    return json.loads(data) if data else None


def wait_visible(route, token, predicate, description):
    for attempt in range(1, 11):
        result = request('GET', route, token=token)
        if predicate(result):
            PREPARATION.append({'operation': description, 'attempts': attempt,
                'response_status': 200, 'result': 'precondición visible'})
            save_records()
            return
        PREPARATION.append({'operation': description, 'attempt': attempt,
            'response_status': 200, 'result': 'recurso todavía no visible'})
        save_records()
        time.sleep(0.1)
    raise RuntimeError('La precondición no se hizo visible: '+description)


def actor():
    n = str(secrets.randbelow(89999999)+10000000)
    cell = '9'+n
    request('POST', '/api/usuarios', {'dni': n, 'celular': cell,
        'nombres': 'Contexto Contrato', 'pin': '4826'})
    for attempt in range(1, 4):
        try:
            token = request('POST', '/api/auth/login', {'celular': cell, 'pin': '4826'})['access_token']
            break
        except urllib.error.HTTPError as error:
            if error.code != 401 or attempt == 3:
                raise
            failure=json.loads(error.read())
            PREPARATION.append({'operation': 'login tras registro', 'attempt': attempt,
                'response_status': error.code, 'codigo': failure.get('codigo'),
                'detail': failure.get('detail'),
                'action': 'reintento de preparación tras 0.2 segundos'})
            save_records()
            time.sleep(0.2)
    return cell, token


@schemathesis.hook
def before_add_examples(ctx, examples):
    operation = ctx.operation
    path, method = operation.path, operation.method.upper()
    if not (path.startswith('/api/contactos') or path.startswith('/api/solicitudes')):
        return
    options = {}
    if '{contacto_id}' in path:
        options['path_parameters'] = {'contacto_id': 1}
    if '{solicitud_id}' in path:
        options['path_parameters'] = {'solicitud_id': 1}
    if method == 'POST' and path == '/api/contactos':
        options['body'] = {'celular': '912345678', 'alias': 'Control valido'}
    elif method == 'PUT':
        options['body'] = {'alias': 'Control editado', 'favorito': True}
    elif method == 'POST' and path == '/api/solicitudes':
        options['body'] = {'contacto_id': 1, 'monto': '1.00', 'motivo': 'Control valido'}
    elif path.endswith('/rechazar'):
        options['body'] = {'motivo': 'Control rechazo'}
    if 'body' in options:
        options['media_type'] = 'application/json'
    case = operation.Case(**options)
    CONTROLS[case.id] = (path, method)
    examples.append(case)


@schemathesis.hook
def before_call(ctx, case, kwargs):
    control = CONTROLS.pop(case.id, None)
    if control is None:
        return  # No reescribe entradas generadas ni pruebas de autenticación.
    path, method = control
    owner_cell, owner_token = actor()
    other_cell, other_token = actor()
    token = owner_token
    detail = {'case_id': case.id, 'method': method, 'path': path,
        'kind': 'ejemplo de control con contexto real', 'status': 'preparando'}
    if path.startswith('/api/contactos'):
        if method == 'POST':
            case.body['celular'] = other_cell
        elif '{contacto_id}' in path:
            contact = request('POST', '/api/contactos',
                {'celular': other_cell, 'alias': 'Control inicial'}, owner_token)
            wait_visible('/api/contactos', owner_token,
                lambda data: any(c['id'] == contact['id'] for c in data['contactos']),
                'contacto propio visible tras alta')
            case.path_parameters['contacto_id'] = contact['id']
            detail['contacto_id'] = contact['id']
    elif method != 'GET':
        contact = request('POST', '/api/contactos',
            {'celular': other_cell, 'alias': 'Control inicial'}, owner_token)
        wait_visible('/api/contactos', owner_token,
            lambda data: any(c['id'] == contact['id'] for c in data['contactos']),
            'contacto propio visible tras alta')
        detail['contacto_id'] = contact['id']
        if path == '/api/solicitudes':
            case.body['contacto_id'] = contact['id']
        else:
            money_request = request('POST', '/api/solicitudes',
                {'contacto_id': contact['id'], 'monto': '1.00', 'motivo': 'Control valido'}, owner_token)
            wait_visible('/api/solicitudes', other_token if path.endswith(('/aceptar', '/rechazar')) else owner_token,
                lambda data: any(s['id'] == money_request['id'] for s in data['enviadas']+data['recibidas']),
                'solicitud visible para el participante correcto')
            case.path_parameters['solicitud_id'] = money_request['id']
            detail['solicitud_id'] = money_request['id']
            if path.endswith(('/aceptar', '/rechazar')):
                token = other_token
                detail['rol'] = 'destinatario'
            else:
                detail['rol'] = 'solicitante'
            if path.endswith('/aceptar'):
                request('PUT', '/api/pruebas/saldo', {'celular': other_cell, 'saldo': '10.00'})
    case.headers['Authorization'] = 'Bearer '+token
    # Los Case manuales no pasan por AuthStorage.set en 4.17. Esta marca
    # declara el JWT real y conserva ignored_auth con sus probes sin token.
    case._has_explicit_auth = True
    # requests kwargs pueden llevar encabezados de CLI, cuya precedencia es mayor.
    if kwargs.get('headers') is not None:
        kwargs['headers']['Authorization'] = 'Bearer '+token
    detail['status'] = 'enviado'
    RECORDS[case.id] = detail


@schemathesis.hook
def after_call(ctx, case, response):
    if case.id not in RECORDS:
        return
    RECORDS[case.id]['response_status'] = response.status_code
    save_records()
    # La respuesta se conserva íntegra; este hook no altera ni descarta fallos.
