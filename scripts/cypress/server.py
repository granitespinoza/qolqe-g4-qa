"""Servidor exclusivo de Cypress. No modifica la aplicación de referencia."""
from pathlib import Path
import os
import sys
import uvicorn

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'referencias' / 'qolqe-wallet'))
os.environ['QOLQE_MODO_PRUEBA'] = '1'
db_dir = Path(os.environ.get('CY_DATABASE_DIR', str(ROOT / '.tools' / 'cypress')))
db_dir.mkdir(parents=True, exist_ok=True)
os.environ['QOLQE_BD'] = str(db_dir / 'qolqe.db')
os.environ['QOLQE_BD_PLANTILLA'] = str(db_dir / 'plantilla.db')
if __name__ == '__main__':
    uvicorn.run('qolqe.main:app', host='127.0.0.1', port=8011)
