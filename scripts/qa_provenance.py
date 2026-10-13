"""Vincula un reporte a sus fuentes y a una ejecución concreta."""
from pathlib import Path
import hashlib, subprocess
ROOT=Path(__file__).resolve().parents[1]
def snapshot():
    files=sorted((ROOT/'features').rglob('*.feature'))+[ROOT/'karate-config.js',ROOT/'data/casos.json',ROOT/'scripts/concurrency_probe.py']
    return {'reference_commit':subprocess.check_output(['git','-C',str(ROOT/'referencias/qolqe-wallet'),'rev-parse','HEAD'],text=True).strip(),'source_hashes':{str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
def validate(manifest):
    current=snapshot()
    if any(manifest.get(k)!=v for k,v in current.items()):
        raise SystemExit('Reporte desactualizado: cambió la referencia o el diseño. Ejecuta Karate antes de generar documentación.')
    path=(ROOT/manifest['report_dir']).resolve()
    if not path.is_relative_to((ROOT/'reports/raw').resolve()):raise SystemExit('Directorio de reportes fuera del proyecto')
    if 'finished_at' not in manifest:raise SystemExit('La ejecución todavía no terminó')
    return path
