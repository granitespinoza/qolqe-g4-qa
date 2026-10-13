# Decisiones de G4

| Decisión | Alternativa | Por qué | Limitación aceptada |
|---|---|---|---|
| Karate | Postman + Newman | El .feature forma parte de la ejecución; evitamos mantener una colección adicional y su correspondencia | DSL técnico, aprendizaje y Java |
| Karate | pytest-bdd + httpx | Menos código de enlace HTTP y validaciones integradas | pytest-bdd expresaría mejor pasos propios en español y aprovecha Python |
| Karate 1.5.2 / Java 17 | Actualizar inmediatamente a Karate 2 | Fijar una versión y un runtime reproducibles para la entrega | No es una afirmación de que sea la versión más reciente; actualizaciones se validan aparte |
| Schemathesis 4.17.0 | Redactar todas las combinaciones técnicas | Generación desde contrato, reportes y reproducciones | No cubre reglas ausentes del esquema; contexto y límites de ejecución importan |
| HTTP contra FastAPI real | Mocks / pruebas de funciones | Verificar integración real de rutas, validación y persistencia | No comprueba interfaz ni servicios financieros externos |
| Usuarios nuevos | Compartir contactos semilla | Evitar duplicados y dependencias entre escenarios | Más peticiones y persistencia de datos de prueba; ejecución secuencial |
| Reloj controlado | Esperar 48 horas | Probar frontera temporal sin demora; renovar JWT al avanzar | El reloj es global; no paralelizar escenarios que lo cambian |
| HU-G4-01 para exposición | HU-G4-08 | Prioridad alta, particiones y límites claros con poco contexto | HU-G4-08 queda disponible para mostrar estados y dinero |
| Contrato original conservado | Modificar OpenAPI para hacer pasar las pruebas | Mantener evidencia de discrepancias | Validar una observación antes de atribuir la causa |
| Repo privado | Publicar todo automáticamente | Revisar entregables antes de compartirlos externamente | La docente necesita acceso o un paquete exportado |

## Criterios de diseño
Alias 3–20: fronteras 2, 3, 20, 21. Vacío, espacios y caracteres prohibidos son casos separados, porque pueden recorrer validaciones distintas.
Vencimiento: 47 h 59 min, 48 h y 48 h 1 min. Para esta suite se interpreta que a las 48 h ya está vencida, coherente con «vence a las 48 horas»; si la docente exige otra precisión temporal, ampliar segundos.
No usar una combinación de entradas inválidas para justificar qué campo produjo un error.
Unicidad tras normalización, recursos ajenos y cambios de estado se prueban explícitamente en Karate.
Schemathesis no sustituye la revisión de CA compuestos ni las verificaciones posteriores de saldo, movimientos y SMS.

## Uso de IA y autoría
La estructura, automatización y borradores se prepararon con ayuda de ChatGPT/Codex. Granit y Franco deben revisar y comprender cada decisión antes de sustentar. Los commits describen trabajo asistido real; no se simula una cronología previa ni contribuciones de Franco que no estén verificadas.

## Fuentes
- https://github.com/karatelabs/karate/tree/v1.5.2
- https://schemathesis.readthedocs.io/en/stable/
- https://github.com/cjudihtroj/qolqe-wallet/blob/main/docs/requisitos.md
- Laboratorio 9 y Clase 10 proporcionados por Granit. Los ejemplos de Restful Booker no sustituyen las reglas de Qolqe.
