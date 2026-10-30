"""Vincula un reporte a sus fuentes y a una ejecución concreta."""
from pathlib import Path
import hashlib, subprocess
ROOT=Path(__file__).resolve().parents[1]
def snapshot():
    files=sorted((ROOT/'API/features').rglob('*.feature'))+[ROOT/'karate-config.js',ROOT/'data/casos.json',ROOT/'scripts/concurrency_probe.py']
    return {'reference_commit':subprocess.check_output(['git','-C',str(ROOT/'referencias/qolqe-wallet'),'rev-parse','HEAD'],text=True).strip(),'source_hashes':{str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
def validate(manifest):
    current=snapshot()
    if any(manifest.get(k)!=v for k,v in current.items()):
        raise SystemExit('Reporte desactualizado: cambió la referencia o el diseño. Ejecuta Karate antes de generar documentación.')
    path=(ROOT/manifest['report_dir']).resolve()
    if not path.is_relative_to((ROOT/'reports/raw').resolve()):raise SystemExit('Directorio de reportes fuera del proyecto')
    if 'finished_at' not in manifest:raise SystemExit('La ejecución todavía no terminó')
    return path


def execution_context():
    """Record the QA revision and installed environment separately from SUT sources."""
    import importlib.metadata
    import os
    import platform
    revision = subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip()
    dirty = subprocess.check_output(['git', '-C', str(ROOT), 'status', '--porcelain'], text=True).strip()
    files = [p for p in (ROOT/'scripts').rglob('*') if p.suffix in {'.py', '.ps1', '.mjs', '.txt'}]
    files += [ROOT/'requirements-lock.txt', ROOT/'.github/workflows/pruebas.yml']
    return {
        'qa_revision': revision,
        'qa_worktree_dirty': bool(dirty),
        'python_version': platform.python_version(),
        'platform': platform.platform(),
        'installed_dependencies': dict(sorted((d.metadata['Name'], d.version) for d in importlib.metadata.distributions())),
        'harness_hashes': {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)},
        'github_run_url': (os.environ.get('GITHUB_SERVER_URL', 'https://github.com') + '/' + os.environ['GITHUB_REPOSITORY'] + '/actions/runs/' + os.environ['GITHUB_RUN_ID']) if os.environ.get('GITHUB_RUN_ID') else None,
        'isolated_database': bool(os.environ.get('QA_RUN_DB_DIR')),
    }
