# Guion de sustentación — G4 Contactos

Duración orientativa: 10 minutos más demo. La presentación del HTML es el recorrido principal; estas notas son para ensayar. No se puede garantizar una calificación: la defensa depende de comprender y demostrar el trabajo.

## 1. Qué probamos y con qué

**Qué decir:**

> Profesora, escogimos Agregar un contacto por su prioridad Alta y porque permite demostrar particiones y límites con poco contexto. Elegimos Karate para ejecutar estos escenarios; Schemathesis lo complementa revisando el contrato.

**Qué mostrar:** Abrir HU-G4-01 y el endpoint POST /api/contactos.

**Por qué:** Karate reduce código de enlace HTTP y evita mantener una colección separada de los .feature. Aceptamos Java y un DSL técnico.

## 2. Qué exige la documentación

**Qué decir:**

> Estas son las condiciones que debemos comprobar. En cada escenario mantenemos válidas las demás entradas para identificar qué condición produjo el resultado.

**Qué mostrar:** Contrastar R-G4-02 con el esquema SolicitudContacto.

**Por qué:** El resultado esperado se obtiene del requisito. OpenAPI describe la petición y la respuesta; no reemplaza la regla de negocio.

## 3. Por qué elegimos esos datos

**Qué decir:**

> Para longitud aplicamos límites de dos puntos: cada extremo permitido y su vecino inválido. Para estado y unicidad usamos particiones. Niño representa una letra expresamente permitida, no un dato elegido al azar.

**Qué mostrar:** Consultar G4-004, G4-007, G4-008 y G4-019.

**Por qué:** Los límites prueban las fronteras; las particiones representan condiciones de negocio diferentes. No necesitamos repetir datos sin una razón.

## 4. El escenario que ejecutamos

**Qué decir:**

> Esta es la implementación real en Karate. Los usuarios se preparan por API; el escenario hace la petición y verifica creación. No es un ejemplo decorativo: tiene una etiqueta y un registro de ejecución.

**Qué mostrar:** Mostrar los pasos y después abrir el registro HTTP.

**Por qué:** Así aislamos el uso de ñ. Un celular inválido o una lista llena ocultaría la regla del alias.

## 5. Resultado 1: una letra permitida se rechaza

**Qué decir:**

> El dato cumplía las condiciones. Obtuvimos ALIAS_INVALIDO. Concluimos que hay un defecto porque contradice la regla explícita. Si la prueba se detuvo en el código HTTP, no afirmamos que sus pasos posteriores hayan sido ejecutados.

**Qué mostrar:** Petición con Niño y cuerpo del rechazo.

**Por qué:** Es un incumplimiento funcional y del contrato, no una preferencia visual. La prueba esperaba éxito y por eso falla.

## 6. Resultado 2: normalizar antes de comparar

**Qué decir:**

> La API admite el segundo registro. La normalización debe aplicarse antes de decidir la unicidad. La conducta observada contradice la regla; cualquier hipótesis de causa en el código se distingue de esta evidencia.

**Qué mostrar:** Comparar el dato enviado y el alias devuelto.

**Por qué:** Con ANA se comprueba capitalización; con « Ana » se comprueba el efecto de normalizar. Son condiciones distintas.

## 7. Contrato y semántica HTTP

**Qué decir:**

> No decimos que todo error sea 400 ni que 201 pertenezca exclusivamente a POST. El rechazo de Niño no es incorrecto porque use 422 para un error; es incorrecto porque un alias permitido no debía rechazarse.

**Qué mostrar:** Abrir la comparación entre las tres fuentes.

**Por qué:** La semántica HTTP ayuda a interpretar; requisitos y contrato fijan expectativas del proyecto. Si discrepan, se documenta la contradicción.

## 8. Qué aportó Schemathesis

**Qué decir:**

> Reproducimos y contrastamos cada señal. Un caso con solo contacto_id fue marcado como válido, pero el snapshot exige también monto y motivo: rechazarlo es correcto. Por eso no presentamos las cuatro señales como cuatro defectos confirmados.

**Qué mostrar:** Abrir el reporte y su interpretación.

**Por qué:** Un aviso de herramienta no se convierte automáticamente en bug. Una respuesta 409 por contacto duplicado no demuestra que se aceptó un alias inválido.

## 9. Demostración y límites

**Qué decir:**

> Los resultados tienen versión y ejecución identificadas. Podemos localizar otra HU y justificar sus datos. Presentamos los pendientes de forma explícita; el reporte no demuestra por sí solo ausencia de defectos.

**Qué mostrar:** Usar filtro de historias para responder a la pregunta al azar.

**Por qué:** Tener escenarios para cada HU no equivale a cubrir todas sus variantes. Las heurísticas de usabilidad quedan como plan para la entrega web.

## Preguntas de defensa

- ¿Por qué Karate y no Postman? .feature ejecutable y menor mantenimiento de correspondencias; Postman sigue siendo válido para exploración.
- ¿Por qué no pytest-bdd? Menos código de enlace HTTP; aceptar que pytest-bdd ofrece pasos de negocio propios en Python.
- ¿Por qué 2/3 y 20/21? Límites de dos puntos. Probar esos valores no garantiza detectar todos los errores.
- ¿Por qué Niño? La ñ está expresamente permitida. Se mantienen válidas las demás condiciones.
- ¿Por qué es defecto? Comparar requisito y contrato con petición/respuesta obtenidas. No decidir solo porque una prueba está roja.
- ¿Por qué 422 no implica un código equivocado? Es válido para rechazar datos en Qolqe; aquí el dato no debía rechazarse.
- ¿Qué cubrió Schemathesis? Mostrar su reporte y sus advertencias; no presentar cuatro señales como cuatro bugs.
- ¿Qué historia te falta? Consultar cobertura y explicar los pendientes.
- ¿Cómo reproduzco? Preparar la API y ejecutar la etiqueta del caso; si solo mostramos evidencia registrada, decirlo.
- ¿Por qué usabilidad? Complemento para la entrega web, todavía sin evaluación ejecutada.

## Ensayo

Lee docs/como-estudiar.md. Practica un caso sin leer el guion. Luego elige una HU al azar y localiza su regla, técnica y evidencia. No memorices números sin entender la respuesta y los efectos.
