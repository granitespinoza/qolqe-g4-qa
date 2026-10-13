import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
process.env.RUNTIME_NODE_MODULES='C:/Users/LEGION/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const root=path.resolve('.');
const skill='C:/Users/LEGION/.codex/plugins/cache/openai-primary-runtime/presentations/26.1011.11113/skills/presentations';
const p=Presentation.create({slideSize:{width:1280,height:720}});
const stats=JSON.parse(await fs.readFile('reports/resultados.json','utf8')).stats;
const slides=[
 ['G4 · Contactos','Granit Espinoza + Franco\nPruebas de API · Parte 1','Requisito → técnica → escenario → evidencia'],
 ['Nuestra estrategia','Karate: comportamiento, estados y efectos sobre datos.\nSchemathesis: entradas generadas y conformidad con OpenAPI.\nRevisión manual: comparar contrato con requisitos.','Por qué Karate: .feature ejecutable y menos código de enlace HTTP.\nLímite: DSL técnico y Java; no acredita cobertura total.'],
 ['HU-G4-01 · Agregar un contacto','Celular registrado y activo, distinto del propio y sin repetirse.\nAlias normalizado: 3–20 caracteres; letras, números y espacios.\nMáximo 15 contactos por usuario.','Prioridad Alta · R-G4-01, R-G4-02 y R-G4-03'],
 ['Cómo elegimos los datos','Particiones: activo, cerrado, propio, inexistente y duplicado.\nValores límite: alias de 2, 3, 20 y 21 caracteres.\nCapacidad: crear el contacto 15 y rechazar el 16.','Se cambia una condición por caso; las demás permanecen válidas.\nVacío, espacios y ñ se comprueban como condiciones separadas.'],
 ['Un caso derivado del requisito','Regla R-G4-02: letras, incluidas tildes y ñ.\nDato: alias «Niño»; celular ajeno, activo, nuevo; lista vacía.\nEsperado: 201 y contacto persistido.\nObtenido: 422 ALIAS_INVALIDO.','G4-004 · Evidencia HTTP reproducible · Defecto D-01'],
 ['La normalización también importa','Contexto: existe un contacto con alias «Ana».\nAcción: agregar otro celular con alias « Ana ».\nEsperado: 409 ALIAS_DUPLICADO; conservar un solo contacto.\nObtenido: 201; se permite otro alias «Ana».','G4-018 · Partición de equivalencia · Defecto D-02'],
 ['Resultados de la ejecución',`${stats.executed} escenarios ejecutados · ${stats.passed} aprobados · ${stats.failed} fallaron.\nLos fallos reproducen 5 defectos funcionales.\nLas 10 HU de G4 y 9 del núcleo tienen escenarios.`,`Tener pruebas por HU no significa cobertura total de sus variantes.\nConsultar docs/cobertura.md antes de declarar completa la entrega.`],
 ['Contrato y demostración','Abrir el reporte de Schemathesis y revisar una petición fallida.\nReproducir el cURL con el contexto apropiado.\nComparar requisito, contrato y respuesta.','Demo: portal → HU-G4-01 → escenario → evidencia.\nPara otra HU: filtro por historia y matriz de diseño.'],
 ['Decisiones defendibles','Elegimos una técnica por la condición que debemos comprobar.\nCada conclusión se vincula con una ejecución y una versión.\nLos defectos se conservan; no ajustamos las pruebas para ocultarlos.','Repositorio, informe, features, reportes y capturas disponibles.']
];
function text(s,str,x,y,w,h,size,color='#172b29',bold=false){let sh=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});sh.text=str;sh.text.style={typeface:'Arial',fontSize:size,color,bold};return sh;}
for(let i=0;i<slides.length;i++){
 const [title,body,foot]=slides[i];let s=p.slides.add();s.background.fill='#faf9f5';
 text(s,title,70,65,1140,110,48,'#145449',true);
 text(s,body,75,210,1120,295,30);
 text(s,foot,75,535,1120,105,22,'#66746e');
 text(s,`${i+1} / ${slides.length}`,1120,666,100,24,14,'#66746e');
 s.speakerNotes.text='Fuentes: docs/requisitos.md de Qolqe commit 8c7d2f0c939ede7765b7b80b98c10c3905693fda; docs/diseno-pruebas.md; reports/resultados.json. Ejecución local real. No se afirma cobertura total. Explicar alternativas y límites, no leer la diapositiva.';
 const img=await p.export({slide:s,format:'png',scale:1});await fs.writeFile(`.build/slide-${i+1}.png`,new Uint8Array(await img.arrayBuffer()));
}
await (await PresentationFile.exportPptx(p)).save(path.join(root,'.build/candidate.pptx'));
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
await finalizePresentation({workspaceDir:root,candidatePath:path.join(root,'.build/candidate.pptx'),finalPath:path.join(root,'presentacion/G4-contactos.pptx'),pythonExecutable:'C:/Users/LEGION/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit'],fontPolicy:{basis:'design',families:['Arial']},verifyArtifactToolImport:true,receiptPath:path.join(root,'.build/validation.json')});
console.log('PPTX creada y validada: presentacion/G4-contactos.pptx');
