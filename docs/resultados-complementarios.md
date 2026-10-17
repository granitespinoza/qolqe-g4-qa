# Resultados complementarios

Ejecución: `20261017T022208Z-161b94`. Separados del catálogo inicial de 116 casos.

65 escenarios: 59 aprobados, 6 fallidos, 0 pendientes.

| Tag | Variante ejecutada | Resultado | Evidencia |
|---|---|---|---|
| CF-01 | Editar alias válido en límites y clases permitidas | APROBADO | [HTTP real](../evidencias/CF-01-27.html) |
| CF-01 | Editar alias válido en límites y clases permitidas | APROBADO | [HTTP real](../evidencias/CF-01-28.html) |
| CF-01 | Editar alias válido en límites y clases permitidas | APROBADO | [HTTP real](../evidencias/CF-01-29.html) |
| CF-01 | Editar alias válido en límites y clases permitidas | FALLÓ | [HTTP real](../evidencias/CF-01-30.html) |
| CF-01 | Editar alias válido en límites y clases permitidas | APROBADO | [HTTP real](../evidencias/CF-01-31.html) |
| CF-02 | Editar alias inválido conserva el contacto original | APROBADO | [HTTP real](../evidencias/CF-02-45.html) |
| CF-02 | Editar alias inválido conserva el contacto original | APROBADO | [HTTP real](../evidencias/CF-02-46.html) |
| CF-02 | Editar alias inválido conserva el contacto original | APROBADO | [HTTP real](../evidencias/CF-02-47.html) |
| CF-03 | Editar alias duplicado tras normalizar | APROBADO | [HTTP real](../evidencias/CF-03-61.html) |
| CF-03 | Editar alias duplicado tras normalizar | FALLÓ | [HTTP real](../evidencias/CF-03-62.html) |
| CF-04 | Buscar por fragmento del alias | APROBADO | [HTTP real](../evidencias/CF-04-65.html) |
| CF-05 | Eliminar contacto ajeno responde 404 y conserva el recurso | APROBADO | [HTTP real](../evidencias/CF-05-75.html) |
| CT-01 | POST rechaza alias omitido sin crear contacto | APROBADO | [HTTP real](../evidencias/CT-01-29.html) |
| CT-01 | POST rechaza celular omitido sin crear contacto | APROBADO | [HTTP real](../evidencias/CT-01-30.html) |
| CT-01 | POST rechaza alias nulo sin crear contacto | APROBADO | [HTTP real](../evidencias/CT-01-31.html) |
| CT-01 | POST rechaza celular nulo sin crear contacto | APROBADO | [HTTP real](../evidencias/CT-01-32.html) |
| CT-01 | POST rechaza alias numerico sin crear contacto | APROBADO | [HTTP real](../evidencias/CT-01-33.html) |
| CT-01 | POST rechaza alias booleano sin crear contacto | APROBADO | [HTTP real](../evidencias/CT-01-34.html) |
| CT-01 | POST rechaza alias objeto sin crear contacto | APROBADO | [HTTP real](../evidencias/CT-01-35.html) |
| CT-01 | POST rechaza alias arreglo sin crear contacto | APROBADO | [HTTP real](../evidencias/CT-01-36.html) |
| CT-01 | POST rechaza celular numerico sin crear contacto | APROBADO | [HTTP real](../evidencias/CT-01-37.html) |
| CT-01 | POST rechaza celular booleano sin crear contacto | APROBADO | [HTTP real](../evidencias/CT-01-38.html) |
| CT-01 | POST rechaza celular objeto sin crear contacto | APROBADO | [HTTP real](../evidencias/CT-01-39.html) |
| CT-01 | POST rechaza celular arreglo sin crear contacto | APROBADO | [HTTP real](../evidencias/CT-01-40.html) |
| CT-01 | POST rechaza cuerpo ausente sin crear contacto | APROBADO | [HTTP real](../evidencias/CT-01-41.html) |
| CT-01 | POST rechaza cuerpo arreglo sin crear contacto | APROBADO | [HTTP real](../evidencias/CT-01-42.html) |
| CT-01 | POST rechaza cuerpo objeto vacio sin crear contacto | APROBADO | [HTTP real](../evidencias/CT-01-43.html) |
| CT-01 | POST rechaza celular ocho digitos sin crear contacto | APROBADO | [HTTP real](../evidencias/CT-01-44.html) |
| CT-01 | POST rechaza celular diez digitos sin crear contacto | APROBADO | [HTTP real](../evidencias/CT-01-45.html) |
| CT-01 | POST rechaza celular inicia en 8 sin crear contacto | APROBADO | [HTTP real](../evidencias/CT-01-46.html) |
| CT-01 | POST rechaza celular con letras sin crear contacto | APROBADO | [HTTP real](../evidencias/CT-01-47.html) |
| CT-02 | PUT rechaza alias numerico sin modificar contacto | APROBADO | [HTTP real](../evidencias/CT-02-61.html) |
| CT-02 | PUT rechaza alias booleano sin modificar contacto | APROBADO | [HTTP real](../evidencias/CT-02-62.html) |
| CT-02 | PUT rechaza alias objeto sin modificar contacto | APROBADO | [HTTP real](../evidencias/CT-02-63.html) |
| CT-02 | PUT rechaza alias arreglo sin modificar contacto | APROBADO | [HTTP real](../evidencias/CT-02-64.html) |
| CT-02 | PUT rechaza alias menor a 3 sin modificar contacto | APROBADO | [HTTP real](../evidencias/CT-02-65.html) |
| CT-02 | PUT rechaza alias mayor a 20 sin modificar contacto | APROBADO | [HTTP real](../evidencias/CT-02-66.html) |
| CT-02 | PUT rechaza favorito texto true sin modificar contacto | FALLÓ | [HTTP real](../evidencias/CT-02-67.html) |
| CT-02 | PUT rechaza favorito texto false sin modificar contacto | FALLÓ | [HTTP real](../evidencias/CT-02-68.html) |
| CT-02 | PUT rechaza favorito entero uno sin modificar contacto | FALLÓ | [HTTP real](../evidencias/CT-02-69.html) |
| CT-02 | PUT rechaza favorito entero cero sin modificar contacto | FALLÓ | [HTTP real](../evidencias/CT-02-70.html) |
| CT-02 | PUT rechaza favorito objeto sin modificar contacto | APROBADO | [HTTP real](../evidencias/CT-02-71.html) |
| CT-02 | PUT rechaza favorito arreglo sin modificar contacto | APROBADO | [HTTP real](../evidencias/CT-02-72.html) |
| CT-02 | PUT rechaza cuerpo ausente sin modificar contacto | APROBADO | [HTTP real](../evidencias/CT-02-73.html) |
| CT-02 | PUT rechaza cuerpo arreglo sin modificar contacto | APROBADO | [HTTP real](../evidencias/CT-02-74.html) |
| CT-03 | PUT permite campos opcionales y nulos expresamente admitidos | APROBADO | [HTTP real](../evidencias/CT-03-85.html) |
| CT-03 | PUT permite campos opcionales y nulos expresamente admitidos | APROBADO | [HTTP real](../evidencias/CT-03-86.html) |
| CT-03 | PUT permite campos opcionales y nulos expresamente admitidos | APROBADO | [HTTP real](../evidencias/CT-03-87.html) |
| CT-03 | PUT permite campos opcionales y nulos expresamente admitidos | APROBADO | [HTTP real](../evidencias/CT-03-88.html) |
| CT-04 | GET rechaza pagina fuera del contrato | APROBADO | [HTTP real](../evidencias/CT-04-97.html) |
| CT-04 | GET rechaza pagina fuera del contrato | APROBADO | [HTTP real](../evidencias/CT-04-98.html) |
| CT-04 | GET rechaza pagina fuera del contrato | APROBADO | [HTTP real](../evidencias/CT-04-99.html) |
| CT-04 | GET rechaza pagina fuera del contrato | APROBADO | [HTTP real](../evidencias/CT-04-100.html) |
| CT-05 | Identificador de ruta debe ser entero | APROBADO | [HTTP real](../evidencias/CT-05-109.html) |
| CT-05 | Identificador de ruta debe ser entero | APROBADO | [HTTP real](../evidencias/CT-05-110.html) |
| CT-06 | Contrato de respuestas en recorrido CRUD válido | APROBADO | [HTTP real](../evidencias/CT-06-113.html) |
| CT-07 | Operaciones protegidas rechazan peticiones sin token | APROBADO | [HTTP real](../evidencias/CT-07-142.html) |
| CT-07 | Operaciones protegidas rechazan peticiones sin token | APROBADO | [HTTP real](../evidencias/CT-07-143.html) |
| CT-07 | Operaciones protegidas rechazan peticiones sin token | APROBADO | [HTTP real](../evidencias/CT-07-144.html) |
| CT-07 | Operaciones protegidas rechazan peticiones sin token | APROBADO | [HTTP real](../evidencias/CT-07-145.html) |
| CT-08 | Bearer con token malformado no autentica operaciones protegidas | APROBADO | [HTTP real](../evidencias/CT-08-161.html) |
| CT-08 | Bearer con token malformado no autentica operaciones protegidas | APROBADO | [HTTP real](../evidencias/CT-08-162.html) |
| CT-08 | Bearer con token malformado no autentica operaciones protegidas | APROBADO | [HTTP real](../evidencias/CT-08-163.html) |
| CT-08 | Bearer con token malformado no autentica operaciones protegidas | APROBADO | [HTTP real](../evidencias/CT-08-164.html) |
| CT-09 | Editar alias con símbolo prohibido conserva el contacto | APROBADO | [HTTP real](../evidencias/CT-09-167.html) |
