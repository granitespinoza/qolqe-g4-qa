# Guion de exposición — aproximadamente 10 minutos más demo

## 1. Herramienta y estrategia (1 minuto)
Karate ejecuta .feature y valida negocio. Schemathesis genera pruebas del contrato. Preferimos Karate frente a Postman para no mantener colección y Gherkin separados; frente a pytest-bdd para reducir código de enlace HTTP. Aceptamos Java y un DSL técnico.

## 2. HU-G4-01 y criterio (1 minuto)
Mostrar CA1 y R-G4-01, 02 y 03. Prioridad Alta. Todas las condiciones de contexto son válidas excepto la que el escenario pretende comprobar.

## 3. Derivación (3 minutos)
Particiones para celular propio, cerrado, inexistente y duplicado. Valores límite de dos puntos para alias 2/3 y 20/21. Explicar por qué no usar un número aleatorio. Vacío y espacios son casos separados. Contactos 15/16 representan frontera de capacidad.

## 4. Escenario y resultado (2 minutos)
G4-004: Niño debe aceptarse, pero devuelve 422 ALIAS_INVALIDO. G4-018: normalizar antes de comparar unicidad; 201 obtenido frente a 409 esperado. Abrir el feature y evidencia HTTP correspondiente. El fallo no se oculta.

## 5. Contrato y conclusiones (1 minuto)
Schemathesis: 9 operaciones, 400 casos generados, 4 señales y advertencias de contexto. No confundir cantidad de solicitudes con cobertura de negocio. Un rechazo por duplicado puede ocultar validación técnica.

## 6. Demo y pregunta al azar (2 minutos)
Portal: filtrar HU-G4-01, mostrar dos fallos, abrir escenario y registro. Elegir cualquier otra HU desde el filtro. Para HU-G4-08 explicar vigencia 48 h y estados; para núcleo, explicar revocación y concurrencia.

## Preguntas que debemos poder responder
- ¿Por qué Karate y no otra herramienta? Relacionar elección con .feature, mantenimiento y límites.
- ¿Por qué esos datos? Partición o frontera concreta, no selección arbitraria.
- ¿Por qué API y no UI? Reglas y persistencia directamente; UI se verificará en Parte 2.
- ¿Cómo evita dependencias? Usuarios propios, reloj restablecido, secuencia única. El reloj global impide paralelizar esta suite.
- ¿Qué halló Schemathesis? Mostrar reporte y reproducir; no afirmar que resolvió todos los CA.
- ¿Es defecto o convención? Comparar requisito, contrato y respuesta, como indica Clase 10.
- ¿Quién hizo el análisis? Explicar asistencia de IA y revisión personal; no atribuirse trabajo no realizado.

No memorizar resultados sin revisar el registro de la ejecución y los pendientes de cobertura.
