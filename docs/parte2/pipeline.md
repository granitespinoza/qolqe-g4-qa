# Pipeline de la entrega actual

![Pipeline de CI](img/pipeline.svg)

Workflow: `.github/workflows/pruebas.yml`. Tres jobs secuenciales: **job_api → job_web → job_reporting**. Se activa con push/PR a main o ejecución manual. Web y reportería usan `if: always()` para conservar evidencia aunque un trabajo anterior falle.

API ejecuta Karate y Schemathesis. Web ejecuta las 54 pruebas tres veces. Cada trabajo mantiene los códigos y resultados crudos y aplica el Quality Gate del Escenario A. Reportería descarga artefactos del mismo run e intento y comprueba revisión y política antes de consolidar.

[Política y verificaciones](quality-gate.md) · [Guía de ensayo y publicación](entrega.md) · [Defectos y riesgos](defectos-conocidos.md).

Los artefactos conservan HTML, XML, JSON y capturas siete días, comprimidos. El artefacto final contiene la matriz navegable y el PPTX. Descargar, extraer y abrir `apidoc/parte2/index.html`. Esto es CI de pruebas y publicación de evidencia, sin despliegue productivo.

La ejecución local aprueba Escenario A. El run remoto debe comprobarse después de publicar el commit final. Los enlaces del anexo apuntan a main y requieren integrar la entrega allí.

## Zona horaria del navegador

Qolqe calcula «hoy» en hora de Lima (UTC-5) y rechaza un `hasta` posterior (`La fecha 'hasta' no puede ser futura`). La página de historial toma la fecha del navegador. Un runner de GitHub está en UTC: entre las 00:00 y las 05:00 UTC su fecha va un día adelante de la de Lima, la API respondía error y la tabla quedaba vacía, con un texto distinto al registrado para D-07. Por eso `job_web` fija `TZ: America/Lima`, la zona documentada de la aplicación. No se modifica Qolqe ni se cambia ninguna firma del gate.
