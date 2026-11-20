"""Instancia local Kiwi: TLS propio, secretos ignorados y sincronización real."""
from pathlib import Path
import argparse,datetime as dt,ipaddress,json,os,secrets,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'integrations/kiwi';LOCAL=BASE/'.local'
def compose(*args,**kwargs):
 return subprocess.run(['docker','compose','--project-name','qolqe-kiwi','--env-file',str(BASE/'.env'),'-f',str(BASE/'compose.yml'),*args],check=True,**kwargs)
def prepare(renew=False):
 LOCAL.mkdir(parents=True,exist_ok=True)
 if not(BASE/'.env').exists():
  (BASE/'.env').write_text('\n'.join(k+'='+secrets.token_urlsafe(36)for k in ['KIWI_DB_PASSWORD','KIWI_ROOT_PASSWORD','KIWI_SECRET_KEY'])+'\n',encoding='utf-8')
 ssl=LOCAL/'ssl';ssl.mkdir(exist_ok=True)
 if renew or not(ssl/'localhost.crt').exists():
  from cryptography import x509
  from cryptography.hazmat.primitives import hashes,serialization
  from cryptography.hazmat.primitives.asymmetric import rsa
  from cryptography.x509.oid import NameOID,ExtendedKeyUsageOID
  now=dt.datetime.now(dt.timezone.utc);ca_key=rsa.generate_private_key(public_exponent=65537,key_size=2048)
  ca_name=x509.Name([x509.NameAttribute(NameOID.COMMON_NAME,'Qolqe Kiwi local CA')])
  ca=x509.CertificateBuilder().subject_name(ca_name).issuer_name(ca_name).public_key(ca_key.public_key()).serial_number(x509.random_serial_number()).not_valid_before(now-dt.timedelta(minutes=5)).not_valid_after(now+dt.timedelta(days=365)).add_extension(x509.BasicConstraints(ca=True,path_length=0),critical=True).add_extension(x509.SubjectKeyIdentifier.from_public_key(ca_key.public_key()),critical=False).add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_key.public_key()),critical=False).add_extension(x509.KeyUsage(digital_signature=True,content_commitment=False,key_encipherment=False,data_encipherment=False,key_agreement=False,key_cert_sign=True,crl_sign=True,encipher_only=False,decipher_only=False),critical=True).sign(ca_key,hashes.SHA256())
  key=rsa.generate_private_key(public_exponent=65537,key_size=2048)
  cert=x509.CertificateBuilder().subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME,'localhost')])).issuer_name(ca_name).public_key(key.public_key()).serial_number(x509.random_serial_number()).not_valid_before(now-dt.timedelta(minutes=5)).not_valid_after(now+dt.timedelta(days=365)).add_extension(x509.BasicConstraints(ca=False,path_length=None),critical=True).add_extension(x509.SubjectKeyIdentifier.from_public_key(key.public_key()),critical=False).add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_key.public_key()),critical=False).add_extension(x509.KeyUsage(digital_signature=True,content_commitment=False,key_encipherment=True,data_encipherment=False,key_agreement=False,key_cert_sign=False,crl_sign=False,encipher_only=False,decipher_only=False),critical=True).add_extension(x509.SubjectAlternativeName([x509.DNSName('localhost'),x509.IPAddress(ipaddress.ip_address('127.0.0.1'))]),critical=False).add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]),critical=False).sign(ca_key,hashes.SHA256())
  (ssl/'ca.crt').write_bytes(ca.public_bytes(serialization.Encoding.PEM))
  (ssl/'localhost.crt').write_bytes(cert.public_bytes(serialization.Encoding.PEM)+ca.public_bytes(serialization.Encoding.PEM))
  (ssl/'localhost.key').write_bytes(key.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.TraditionalOpenSSL,serialization.NoEncryption()))
 account=LOCAL/'account.json'
 if not account.exists():account.write_text(json.dumps({'username':'qolqe-admin','password':secrets.token_urlsafe(30),'email':'qa@example.invalid'}),encoding='utf-8')
 return json.loads(account.read_text())
def initialize():
 account=prepare();compose('up','-d','--wait','--wait-timeout','180')
 compose('exec','-T','web','/Kiwi/manage.py','migrate','--noinput')
 compose('exec','-T','web','/Kiwi/manage.py','set_domain','localhost:8443')
 compose('exec','-T','web','/Kiwi/manage.py','refresh_permissions')
 code='''import json,sys
from django.contrib.auth import get_user_model
from tcms.management.models import Classification,Product,Version,Build
from tcms.testcases.models import Category
from tcms.testplans.models import TestPlan,PlanType
from tcms.testcases.models import TestCaseStatus
from tcms.testruns.models import TestExecutionStatus
account=json.loads(ACCOUNT_JSON)
u,created=get_user_model().objects.get_or_create(username=account['username'],defaults={'email':account['email'],'is_staff':True,'is_superuser':True,'is_active':True})
if created:u.set_password(account['password']);u.save()
classification,_=Classification.objects.get_or_create(name='Proyecto académico')
product,_=Product.objects.get_or_create(name='Qolqe Wallet G4',defaults={'classification':classification})
version,_=Version.objects.get_or_create(product=product,value='entrega-final')
build,_=Build.objects.get_or_create(version=version,name='Qolqe referencia 8c7d2f0')
category,_=Category.objects.get_or_create(product=product,name='Automatización API y Web')
type=PlanType.objects.first()
assert type is not None,'Faltan tipos iniciales de plan'
plan,_=TestPlan.objects.get_or_create(name='Consolidado final Qolqe G4',product=product,defaults={'product_version':version,'author':u,'type':type,'text':'Casos versionados; resultados crudos separados del quality gate. Cada corrida y repetición conserva su identidad.'})
assert TestCaseStatus.objects.filter(name='CONFIRMED').exists(),'Falta estado CONFIRMED'
assert TestExecutionStatus.objects.filter(name='FAILED').exists(),'Falta estado FAILED'
print('QOLQE_IDS='+json.dumps({'KIWI_PRODUCT_ID':product.pk,'KIWI_CATEGORY_ID':category.pk,'KIWI_BUILD_ID':build.pk,'KIWI_PLAN_ID':plan.pk,'KIWI_MANAGER_ID':u.pk}))
'''.replace('ACCOUNT_JSON',repr(json.dumps(account)))
 result=compose('exec','-T','web','/Kiwi/manage.py','shell',input=code,capture_output=True,text=True,encoding='utf-8')
 marker=next(x.split('=',1)[1]for x in result.stdout.splitlines()if x.startswith('QOLQE_IDS='));ids=json.loads(marker)
 config={'KIWI_URL':'https://localhost:8443/xml-rpc/','KIWI_USER':account['username'],'KIWI_PASSWORD':account['password'],**ids,'SSL_CERT_FILE':str(LOCAL/'ssl/ca.crt'),'REQUESTS_CA_BUNDLE':str(LOCAL/'ssl/ca.crt')}
 (LOCAL/'connection.json').write_text(json.dumps(config,indent=2),encoding='utf-8')
 image_ref=next(x.split('image:',1)[1].strip()for x in (BASE/'compose.yml').read_text(encoding='utf-8').splitlines()if 'image:'in x and 'kiwitcms/'in x)
 info={'url':'https://localhost:8443','plan_id':ids['KIWI_PLAN_ID'],'initialized':True,'tls_verified_by_client':False,'image':subprocess.check_output(['docker','image','inspect',image_ref,'--format','{{index .RepoDigests 0}}'],text=True).strip()}
 (LOCAL/'instance.json').write_text(json.dumps(info,indent=2),encoding='utf-8')
 print('Kiwi iniciado. Credenciales locales en integrations/kiwi/.local/account.json (ignorado por Git). Plan:',ids['KIWI_PLAN_ID'])
def sync(report=None):
 config=json.loads((LOCAL/'connection.json').read_text(encoding='utf-8'));env={**os.environ,**{k:str(v)for k,v in config.items()}}
 subprocess.run([sys.executable,str(ROOT/'scripts/kiwi_sync.py')]+(['--report',str(report)]if report else[]),env=env,check=True,cwd=ROOT)
 info=json.loads((LOCAL/'instance.json').read_text());info['tls_verified_by_client']=True;(LOCAL/'instance.json').write_text(json.dumps(info,indent=2),encoding='utf-8')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','start','sync','stop','status']);p.add_argument('--report',type=Path);a=p.parse_args()
 if a.action=='prepare':prepare();print('Certificados y secretos locales preparados.')
 if a.action=='start':initialize()
 if a.action=='sync':sync(a.report)
 if a.action=='stop':compose('stop')
 if a.action=='status':compose('ps')
