from pathlib import Path
import os, sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'referencias'/'qolqe-wallet'))
os.environ['QOLQE_MODO_PRUEBA'] = '1'
database_dir = Path(os.environ.get('QA_RUN_DB_DIR', str(ROOT/'.tools')))
database_dir.mkdir(parents=True, exist_ok=True)
os.environ['QOLQE_BD'] = str(database_dir/'qolqe-qa.db')
os.environ['QOLQE_BD_PLANTILLA'] = str(database_dir/'plantilla-qa.db')
import uvicorn
if __name__ == '__main__':
    uvicorn.run('qolqe.main:app', host='127.0.0.1', port=int(os.environ.get('QA_PORT',8000)))
