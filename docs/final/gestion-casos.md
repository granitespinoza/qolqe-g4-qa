# Gestión de casos y múltiples ejecuciones

Elegimos Kiwi TCMS Community para separar casos, planes, builds y ejecuciones. La API permite importar resultados del mismo caso en distintas corridas sin reemplazar su historial.

| Alternativa | Aporte | Decisión |
|---|---|---|
| CSV / matriz | Portable y fácil de consultar | Conservamos el CSV como exportación, no como único historial |
| Herramienta de gestión alojada | Administración centralizada | Requiere una cuenta y entorno configurados |
| Kiwi TCMS local | Planes, casos versionados, corridas y API verificable | Elegido para demostrar gestión real con datos sintéticos |

## Identidad y estados

- Caso: TC, HU, fuente y versión SHA-256. Un cambio de diseño queda identificado.
- Corrida: herramienta, commit, hash de fuentes, run/attempt, repetición y variantes.
- Estado crudo y decisión del gate permanecen separados: un fallo conocido sigue **FAILED** en Kiwi.
- Los outlines de API se agregan por caso en Kiwi y conservan sus variantes y resultados en comentarios. La matriz HTML/CSV mantiene una fila por variante y ejecución.
- Un reintento no reemplaza un resultado distinto. Si una importación quedó incompleta, solo se completan resultados IDLE y comentarios faltantes.

El historial SQLite local y la caché de Actions conservan importaciones por corrida. La caché puede expirar; no sustituye la instancia persistente ni los artefactos.

## Iniciar en Windows

Requisitos: Docker Desktop con motor Linux y el entorno Python del README.

```powershell
.venv/Scripts/python.exe -m pip install -r requirements-kiwi.txt
.venv/Scripts/python.exe scripts/kiwi_local.py start
.venv/Scripts/python.exe scripts/kiwi_local.py status
```

El lanzador genera secretos propios, aplica migraciones y crea producto, versión, build, categoría y plan. Las imágenes se fijan por digest. Base y archivos utilizan volúmenes persistentes. Los contenedores tienen límites de memoria; el servicio solo escucha en `127.0.0.1:8443`.

Abrimos `https://localhost:8443/plan/1/` en esta instalación. Las credenciales se consultan localmente:

```powershell
notepad integrations/kiwi/.local/account.json
```

`.env` y `.local/` están ignorados por Git. No se incluyen claves privadas ni contraseñas en el repositorio o en el reporte.

## Certificado del navegador

El certificado contiene SAN localhost/127.0.0.1 y una CA propia de esta instalación. El cliente oficial valida TLS usando esa CA; no se desactiva la verificación. El navegador necesita confiar manualmente en `integrations/kiwi/.local/ssl/ca.crt` antes de la exposición. Esa preparación se realiza una vez y bajo control del usuario; no se cambian los almacenes de confianza automáticamente. No se continúa a través de advertencias de seguridad durante la demo.

## Importar resultados reales

```powershell
.venv/Scripts/python.exe scripts/final_delivery.py report --evidence images
.venv/Scripts/python.exe scripts/kiwi_local.py sync
.venv/Scripts/python.exe scripts/final_delivery.py report --evidence images
```

La primera generación reúne las evidencias verificadas. La sincronización crea o reanuda cada corrida. La segunda incorpora al HTML la confirmación de Kiwi cuando coincide el hash del payload. Seleccionar `images` no produce capturas retroactivamente: la suite debe ejecutarse con `QA_EVIDENCE=images`.

```powershell
.venv/Scripts/python.exe scripts/kiwi_local.py stop
```

Detener conserva casos, corridas y volúmenes; volver a usar `start` permite continuar.

## Relación con GitHub Actions

Un runner hospedado de GitHub no puede conectarse al localhost de esta laptop. El pipeline siempre conserva la matriz, historial y payload de importación. La sincronización automática se habilita con una instancia accesible por TLS o un runner propio, y los secretos `KIWI_URL`, `KIWI_USER`, `KIWI_PASSWORD`, `KIWI_PLAN_ID`, `KIWI_BUILD_ID`, `KIWI_MANAGER_ID`, `KIWI_PRODUCT_ID` y `KIWI_CATEGORY_ID`.

La instancia local demuestra uso real de la herramienta. No se afirma que el runner de GitHub sincronice con esta laptop. Sin secretos se registra `not_configured`; con `--dry-run` no hay comunicación remota.

Fuentes: [Docker oficial de Kiwi](https://kiwitcms.readthedocs.io/en/latest/installing_docker.html), [API oficial de Kiwi](https://kiwitcms.readthedocs.io/en/latest/modules/tcms.rpc.api.html) y [cliente tcms-api](https://tcms-api.readthedocs.io/en/latest/modules/tcms_api.html).
