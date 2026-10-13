from pathlib import Path
import os, sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'referencias'/'qolqe-wallet'))
os.environ['QOLQE_MODO_PRUEBA'] = '1'
os.environ['QOLQE_BD'] = str(ROOT/'.tools'/'qolqe-qa.db')
os.environ['QOLQE_BD_PLANTILLA'] = str(ROOT/'.tools'/'plantilla-qa.db')
import uvicorn
if __name__ == '__main__':
    uvicorn.run('qolqe.main:app', host='127.0.0.1', port=int(os.environ.get('QA_PORT',8000)))
