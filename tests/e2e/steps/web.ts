import { Given, When, Then } from '@badeball/cypress-cucumber-preprocessor'
import { casosRegistrados } from '../support/fixtures'
import '../specs/contactos-completo.cy'
import '../specs/contactos-happy-path.cy'
import '../specs/contactos-validaciones.cy'
import '../specs/nucleo-comun.cy'
import '../specs/solicitudes-completo.cy'
import '../specs/transferencias-contactos.cy'
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
