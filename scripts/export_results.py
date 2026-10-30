"""Exporta JUnit consolidado sin cambiar FAIL por PASS ni omitir known issues."""
import argparse
import json
import os
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from qa_provenance import validate

ROOT=Path(__file__).resolve().parents[1]

def load(path):return json.loads(path.read_text(encoding='utf-8'))

def api():
    m=load(ROOT/'reports/latest-karate.json')
    if m.get('tag') or m.get('scope')!='all':raise ValueError('Se requiere API completa')
    folder=validate(m);result=ET.Element('testsuites')
    for path in sorted(folder.glob('*.xml')):
        root=ET.parse(path).getroot()
        if root.tag=='testsuite':result.append(root)
        elif root.tag=='testsuites':
            for suite in root.findall('testsuite'):result.append(suite)
    if not list(result):raise ValueError('Falta JUnit de Karate')
    return result

def web():
    pointer=load(ROOT/'reports/cypress/latest-stability.json');m=load(ROOT/pointer['dir']/'stability.json')
    if m.get('completed')!=3:raise ValueError('Faltan tres corridas')
    gate=load(ROOT/'reports/gate/web.json') if (ROOT/'reports/gate/web.json').exists() else {}
    known={t['case']:t for t in gate.get('tests',[])} if gate.get('report_dir')==pointer['dir'] else {}
    result=ET.Element('testsuites')
    for i,run in enumerate(m['runs'],1):
        c=run['counts'];suite=ET.Element('testsuite',name=f'Cypress corrida {i}',tests=str(c['total']),failures=str(c['failed']),errors=str(len(run['specErrors'])),skipped=str(c['skipped']+c['pending']))
        props=ET.SubElement(suite,'properties');ET.SubElement(props,'property',name='raw_exit_code',value=str(run['code']))
        ET.SubElement(props,'property',name='quality_gate',value=gate.get('scenario','pendiente'))
        for t in run['tests']:
            title=' '.join(t['title']);case=ET.SubElement(suite,'testcase',name=title,classname=t['spec'])
            ident=re.search(r'E2E-G4-\d+',title);mapped=known.get(ident.group(),{}) if ident else {}
            if t['state']=='failed':
                failure=ET.SubElement(case,'failure',type='KnownIssue' if mapped.get('status')=='known_issue' else 'AssertionError',message=(t.get('error') or '').split('\n')[0]);failure.text=t.get('error') or 'Fallo sin detalle'
            elif t['state'] in ('skipped','pending'):ET.SubElement(case,'skipped')
        result.append(suite)
        ET.ElementTree(suite).write(ROOT/run['runDir']/'web-results.xml',encoding='utf-8',xml_declaration=True)
    return result

def export(mode):
    dest=ROOT/'results';dest.mkdir(exist_ok=True)
    root=api() if mode=='api' else web()
    path=dest/f'{mode}-results.xml'
    ET.ElementTree(root).write(path,encoding='utf-8',xml_declaration=True)
    return path

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['api','web']);a=p.parse_args()
    print(export(a.mode))
