import { LoginPage } from '../pages/LoginPage'
import { ContactosPage } from '../pages/ContactosPage'

describe('Regresión | HU-G4-01 CA1', () => {
  it('E2E-G4-002 @HU-G4-01 @TC-E2E-G4-002 rechaza alias de 2 caracteres sin crear un contacto', () => {
    cy.prepararContactos().then(({ propietario, contacto }) => {
      const pagina = new ContactosPage()
      new LoginPage().ingresar(propietario.celular, propietario.pin)
      pagina.abrir()
      cy.intercept('POST', '/api/contactos').as('crear')
      pagina.agregar(contacto.celular, 'Lu')
      cy.wait('@crear').then(({ response }) => {
        expect(response?.statusCode).to.eq(422)
        expect(response?.body.codigo).to.eq('ALIAS_INVALIDO')
      })
      pagina.error().should('be.visible').and('contain.text', '3 y 20')
      cy.reload()
      pagina.contador().should('contain.text', '0 de 15')
      pagina.filas().should('not.exist')
    })
  })
  it('E2E-G4-003 @HU-G4-01 @TC-E2E-G4-003 rechaza celular duplicado y conserva un único contacto', () => {
    cy.prepararContactos().then(({ propietario, contacto }) => {
      const pagina = new ContactosPage()
      new LoginPage().ingresar(propietario.celular, propietario.pin)
      pagina.abrir()
      cy.intercept('POST', '/api/contactos').as('crear')
      pagina.agregar(contacto.celular, 'Ana Cypress')
      cy.wait('@crear').its('response.statusCode').should('eq', 201)
      pagina.filas().should('have.length', 1)
      pagina.agregar(contacto.celular, 'Otro alias')
      cy.wait('@crear').then(({ response }) => {
        expect(response?.statusCode).to.eq(409)
        expect(response?.body.codigo).to.eq('CONTACTO_EXISTENTE')
      })
      pagina.error().should('be.visible').and('not.have.text', '')
      cy.reload()
      pagina.filas().should('have.length', 1).and('contain.text', 'Ana Cypress').and('not.contain.text', 'Otro alias')
      pagina.contador().should('contain.text', '1 de 15')
    })
  })
})
