import { Given, When, Then } from '@badeball/cypress-cucumber-preprocessor'
import { casosRegistrados } from '../support/fixtures'
import '../e2e/contactos-completo.cy'
import '../e2e/contactos-happy-path.cy'
import '../e2e/contactos-validaciones.cy'
import '../e2e/nucleo-comun.cy'
import '../e2e/solicitudes-completo.cy'
import '../e2e/transferencias-contactos.cy'
let seleccionado: string | undefined
let ejecutado: string | undefined
Given('un contexto aislado para {string}', (id:string)=>{
  expect(casosRegistrados.has(id),'Implementación única del escenario').to.eq(true)
  seleccionado=id;ejecutado=undefined
})
When('realizo {string} en {string}', (_accion:string, id:string)=>{
  expect(id).to.eq(seleccionado)
  casosRegistrados.get(id)!()
  cy.then(()=>{ejecutado=id})
})
Then('verifico las reglas y la persistencia de {string}', (id:string)=>{
  cy.then(()=>expect(ejecutado,'Acciones y aserciones de negocio completadas').to.eq(id))
})
