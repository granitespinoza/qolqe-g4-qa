"""Arranca Qolqe original con rutas exclusivas indicadas por el ejecutor."""
import os, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'referencias/qolqe-wallet'))
if __name__=='__main__':
    import uvicorn
    uvicorn.run('qolqe.main:app',host='127.0.0.1',port=int(os.environ.get('PERF_PORT','8021')),access_log=False,log_level='warning')
