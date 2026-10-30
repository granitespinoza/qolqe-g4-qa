"""Publica enlaces y conteos en Actions sin alterar el resultado de las pruebas."""
import json
import os
from pathlib import Path


def summary(root=Path('.'), env=os.environ):
    tool=env.get('QA_TOOL','desconocido')
    run_url=f"https://github.com/{env.get('GITHUB_REPOSITORY','')}/actions/runs/{env.get('GITHUB_RUN_ID','')}"
    lines=[f'## QA: {tool}', '', f"Estado del job: **{env.get('QA_STATUS','desconocido')}**.", '',
           f"Revisión: `{env.get('GITHUB_SHA','local')}` · [Ejecución]({run_url}).", '']
    artifact=env.get('QA_ARTIFACT')
    lines.append(f'[Descargar reportes]({artifact}).' if artifact else 'No se publicó un artefacto; revisar los logs del job.')
    if tool=='cypress':
        latest=root/'reports/cypress/latest-stability.json'
        if latest.exists():
            pointer=json.loads(latest.read_text(encoding='utf-8'))
            result=json.loads((root/pointer['dir']/'stability.json').read_text(encoding='utf-8'))
            lines += ['', '| Corrida | Total | PASS | FAIL | Omitidos/pendientes |', '|---|---:|---:|---:|---:|']
            for n,r in enumerate(result['runs'],1):
                c=r['counts']
                lines.append(f"| {n} | {c['total']} | {c['passed']} | {c['failed']} | {c['skipped']+c['pending']} |")
            lines += ['', f"Tres corridas verdes: **{'SÍ' if result['verdict']['achieved'] else 'NO'}**.", '',
                      'En el ZIP: abrir el `html/index.html` de cada corrida. El manifiesto `stability.json` y la matriz generada relacionan las pruebas con sus resultados.']
        else:
            lines += ['', 'No se completó una secuencia de tres corridas. Revisar los fallos de preparación o ejecución.']
    else:
        lines += ['', 'El artefacto conserva los reportes propios de Karate o Schemathesis y sus manifiestos; los fallos mantienen el job en rojo.']
    return '\n'.join(lines)+'\n'


if __name__=='__main__':
    result=summary()
    target=os.environ.get('GITHUB_STEP_SUMMARY')
    if target:
        with Path(target).open('a',encoding='utf-8') as f:
            f.write(result)
    else:
        print(result)
