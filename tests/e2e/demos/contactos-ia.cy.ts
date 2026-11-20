import { LoginPage } from '../pages/LoginPage'
import { ContactosPage } from '../pages/ContactosPage'

describe('DEMO IA | requiere sesión Cypress Cloud | Chromium', () => {
  it('genera acciones con cy.prompt y verifica persistencia con aserciones explícitas', () => {
    cy.prepararContactos().then(({ propietario, contacto }) => {
      const pagina = new ContactosPage()
      new LoginPage().ingresar(propietario.celular, propietario.pin)
      pagina.abrir()
      cy.intercept('POST', '/api/contactos').as('crearIA')
      cy.prompt([
        'Type {{phone}} in the input labeled Celular inside Agregar contacto',
        'Type {{alias}} in the input labeled Alias',
        'Click the button labeled Agregar',
        "Verify that the text \"Contacto IA\" is visible in the list under \"Mis contactos\"",
      ], { placeholders: { phone: contacto.celular, alias: 'Contacto IA' } })
      cy.wait('@crearIA').its('response.statusCode').should('eq', 201)
      cy.reload()
      pagina.filas().should('have.length', 1).and('contain.text', 'Contacto IA').and('contain.text', contacto.celular)
    })
  })
})
