import { actores, caso, ingresar, saldo } from '../support/fixtures'
import { ui } from '../pages/Ui'

describe('Núcleo común | acceso y perfil', () => {
  caso('E2E-G4-401',[],'@HU-N-02 Login válido navega a inicio',()=>{
    actores(1).then(([a])=>{ingresar(a);cy.contains('h1','Inicio').should('be.visible');ui('saludo').should('contain.text','Hola')})
  })
  caso('E2E-G4-402',[],'@HU-N-02 Credenciales inválidas mantienen el login y muestran mensaje genérico',()=>{
    actores(1).then(([a])=>{cy.visit('/login');cy.intercept('POST','/api/auth/login').as('loginInvalido');ui('input-celular').type(a.celular);ui('input-pin').type('9876',{log:false});ui('boton-ingresar').click();cy.wait('@loginInvalido').its('response.statusCode').should('eq',401);ui('login-error').should('be.visible');cy.location('pathname').should('eq','/login')})
  })
  caso('E2E-G4-403',[],'@HU-N-04 Saldo preparado visible y opción de ocultar',()=>{
    actores(1).then(([a])=>{saldo(a,'123.45');ingresar(a);ui('saldo-valor').should('contain.text','123.45');ui('boton-ocultar-saldo').click();ui('boton-ocultar-saldo').should('have.attr','aria-pressed','true');ui('boton-ocultar-saldo').click();ui('saldo-valor').should('contain.text','123.45')})
  })
  caso('E2E-G4-404',[],'@HU-N-04 Perfil conserva celular y enmascara DNI',()=>{
    actores(1).then(([a])=>{ingresar(a);cy.visit('/perfil');ui('perfil-celular').should('have.text',a.celular);ui('perfil-nombres').should('have.text',a.nombres);ui('perfil-dni').should('contain.text',a.celular.slice(-4)).and('not.have.text',a.celular.slice(1))})
  })
  caso('E2E-G4-405',[],'@HU-N-05 Edición de nombres persiste tras recargar',()=>{
    actores(1).then(([a])=>{ingresar(a);cy.visit('/perfil');ui('input-nombres').should('have.value',a.nombres).clear().type('Perfil Actualizado');cy.intercept('PUT','/api/cuentas/me').as('editarPerfil');ui('boton-guardar-perfil').click();cy.wait('@editarPerfil').its('response.statusCode').should('eq',200);cy.reload();ui('perfil-nombres').should('have.text','Perfil Actualizado')})
  })
  caso('E2E-G4-406',[],'@HU-N-01 Registro por UI crea cuenta y permite iniciar sesión',()=>{
    const dni=String(Cypress._.random(10000000,99999999)),cell='9'+dni
    cy.visit('/registro');ui('input-dni').type(dni);ui('input-nombres').type('Registro Web');ui('input-celular').type(cell);ui('input-pin').type('4826',{log:false});ui('input-pin-confirmacion').type('4826',{log:false});cy.intercept('POST','/api/usuarios').as('registro');ui('boton-registrar').click();cy.wait('@registro').its('response.statusCode').should('eq',201)
    cy.visit('/login');ui('input-celular').clear().type(cell);ui('input-pin').type('4826',{log:false});ui('boton-ingresar').click();cy.location('pathname').should('eq','/inicio');ui('saldo-valor').should('contain.text','0.00')
  })
})
