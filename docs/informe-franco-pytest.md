# Informe de ejecución — aporte de Franco (pytest + httpx)

## Identificación
- **Curso:** CS5383 Pruebas y Verificación de Software.
- **Proyecto:** Qolqe Wallet, núcleo de autenticación/usuario con integración de acceso a G4 Contactos.
- **Herramienta:** pytest + httpx, Python 3.12.
- **Sistema bajo prueba:** Qolqe original fijado en commit `8c7d2f0c939ede7765b7b80b98c10c3905693fda`.
- **Ejecución CI verificada:** [GitHub Actions #39017257865](https://github.com/granitespinoza/qolqe-g4-qa/actions/runs/39017257865), 17/10/2026.
- **Código de pruebas:** `tests/pytest_franco/`.
- **Rama examinada:** `franco-pytest-login-usuarios`, antes de la creación de este documento.

## Resultado comprobado
**16 casos ejecutados; 16 aprobados; 0 fallidos.** Duración reportada por pytest: **1,85 segundos**. Job `pytest-franco` concluido con **success**. La ejecución se realizó contra Qolqe original levantado automáticamente, no contra mocks.

```text
============================== 16 passed in 1.85s ==============================
```

## Evidencia trazable
- [Ejecución y consola completa](https://github.com/granitespinoza/qolqe-g4-qa/actions/runs/39017257865).
- [Artefacto `evidencias-pytest-franco`](https://github.com/granitespinoza/qolqe-g4-qa/actions/runs/39017257865/artifacts/12095133305): `pytest-franco.xml` y `pytest-franco.txt`. La retención configurada fue de siete días; su disponibilidad actual debe comprobarse.
- [Matriz de diseño](diseno-pruebas-franco.md).
- [Guía de ejecución y alcance](../tests/pytest_franco/README.md).

## Interpretación
- El resultado **16/16 aprobados** significa que en esa ejecución se cumplieron las aserciones implementadas. **No significa 100 % de cobertura** de las HU ni demuestra ausencia de defectos.
- Se comprobaron caminos positivos y negativos en registro y login, bloqueo por intentos, autorización, saldo, perfil, edición y acceso básico a contactos.
- **No se encontraron nuevos defectos en estos escenarios** durante esta ejecución. Los cinco defectos de Granit pertenecen a otros escenarios y se conservan por separado.
- La comparación de porcentajes de aprobados de pytest frente a Karate **no es justa** sin ejecutar casos equivalentes; Karate contiene muchos escenarios negativos adicionales diseñados para hallar defectos.
- La ejecución documentada corresponde al entorno remoto indicado; no acredita otros equipos.

## Conclusión
El aporte implementa un segundo enfoque de automatización HTTP complementario a Karate, con casos trazables y reproducibles. La corrida verificada demuestra que los 16 escenarios implementados funcionaron en ese entorno. Su principal limitación es el **alcance**, no el éxito técnico: no pretende sustituir la batería funcional ni técnica completa de G4.
