import importlib.util,json,sqlite3,tempfile,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('perf',Path(__file__).with_name('performance.py'));p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
class PerformanceTests(unittest.TestCase):
 def test_percentile_interpolated(self):self.assertAlmostEqual(p.percentile([100,200,300,400],95),385)
 def test_empty_percentile(self):self.assertIsNone(p.percentile([],95))
 def test_workload_sum_and_business_math(self):
  self.assertEqual(sum(p.CFG['distribucion'].values()),100);self.assertEqual(3000*2/60,100);self.assertEqual(3000*6/3600,5)
 def fixture(self,path):
  c=sqlite3.connect(path);c.executescript('CREATE TABLE cuentas(usuario_id INTEGER,saldo_cent INTEGER);CREATE TABLE transferencias(codigo_operacion TEXT,origen_id INTEGER,destino_id INTEGER,monto_cent INTEGER,comision_cent INTEGER,descripcion TEXT);CREATE TABLE movimientos(codigo_operacion TEXT,usuario_id INTEGER,importe_cent INTEGER);CREATE TABLE recargas(codigo_operacion TEXT,usuario_id INTEGER,celular TEXT,monto_cent INTEGER);CREATE TABLE pagos_servicio(codigo_operacion TEXT,usuario_id INTEGER,deuda_id INTEGER,total_cent INTEGER);CREATE TABLE deudas(id INTEGER,estado TEXT);')
  c.executemany('INSERT INTO cuentas VALUES(?,?)',[(10001,999900),(20001,1000100)]);c.execute("INSERT INTO transferencias VALUES('T1',10001,20001,100,0,'PERF-1-1')");c.executemany("INSERT INTO movimientos VALUES('T1',?,?)",[(10001,-100),(20001,100)]);c.commit();return c
 def reconcile(self,mutate=None):
  with tempfile.TemporaryDirectory()as t:
   out=Path(t);db=out/'test.db';c=self.fixture(db)
   if mutate:mutate(c);c.commit()
   c.close();return p.reconcile(db,{'users':[dict(uid=10001,dest_uid=20001,initial_cent=1000000)]},[dict(vu=1,seq=1,op='transferencias',clase='dinero',ok=True,description='PERF-1-1',amount_cent=100,codes=['T1'])],out)
 def test_balanced_transfer(self):self.assertTrue(self.reconcile()['approved'])
 def test_partial_movement_blocks(self):self.assertFalse(self.reconcile(lambda c:c.execute('DELETE FROM movimientos WHERE usuario_id=20001'))['approved'])
 def test_balance_mismatch_blocks(self):self.assertFalse(self.reconcile(lambda c:c.execute('UPDATE cuentas SET saldo_cent=0 WHERE usuario_id=10001'))['approved'])
 def test_duplicated_transfer_blocks(self):self.assertFalse(self.reconcile(lambda c:c.execute('INSERT INTO transferencias SELECT * FROM transferencias'))['approved'])
 def analyze_fixture(self,slow_payment=False):
  events=[]
  for op,weight in p.CFG['distribucion'].items():
   for i in range(weight*30):events.append(dict(op=op,clase='dinero'if op in ['transferencias','recargas','pagos']else'consulta',ms=2000 if slow_payment and op=='pagos'and i<8 else 100,ok=True,statuses=[200],at=500000))
  events.extend(dict(op='login',clase='consulta',ms=100,ok=True,statuses=[200],at=500000)for _ in range(500))
  with tempfile.TemporaryDirectory()as t:
   return p.analyze(events,[dict(epoch=500,generator_cpu_host_pct=1,app_cpu_host_pct=1,app_rss_mb=20)],'carga',dict(k6_started_epoch=0,k6_completed=True),dict(approved=True),Path(t))
 def test_complete_workload_meets_thresholds(self):self.assertTrue(self.analyze_fixture()['approved'])
 def test_slow_endpoint_not_hidden_by_aggregate(self):
  r=self.analyze_fixture(True);self.assertTrue(r['windows'][0]['latency_ok']);self.assertFalse(r['approved'])

def orphan(c):c.execute("INSERT INTO movimientos VALUES('ORPHAN',10001,0)")
# Added below on the class to keep the fixture focused.
PerformanceTests.test_orphan_movement_blocks=lambda self:self.assertFalse(self.reconcile(orphan)['approved'])
if __name__=='__main__':unittest.main()
