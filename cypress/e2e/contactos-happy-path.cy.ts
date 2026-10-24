import { LoginPage } from '../pages/LoginPage'
import { ContactosPage } from '../pages/ContactosPage'

describe('Smoke | HU-G4-01 CA1 | Contactos reales', () => {
  it('E2E-G4-001 agrega un contacto y conserva sus datos al recargar', () => {
    cy.prepararContactos().then(({ propietario, contacto }) => {
      const pagina = new ContactosPage()
      new LoginPage().ingresar(propietario.celular, propietario.pin)
      pagina.abrir()
      pagina.contador().should('contain.text', '0 de 15')
      cy.intercept('POST', '/api/contactos').as('crearContacto') // Observa la API real.
      pagina.agregar(contacto.celular, 'Ana Cypress')
      cy.wait('@crearContacto').then(({ response }) => {
        expect(response?.statusCode).to.eq(201)
        expect(response?.body).to.include({ alias: 'Ana Cypress', celular: contacto.celular, favorito: false })
      })
      pagina.filas().should('have.length', 1).and('contain.text', 'Ana Cypress').and('contain.text', contacto.celular)
      pagina.filas().find('[data-testid="boton-favorito"]').should('have.attr', 'aria-pressed', 'false')
      cy.reload()
      pagina.filas().should('have.length', 1).and('contain.text', 'Ana Cypress').and('contain.text', contacto.celular)
      pagina.contador().should('contain.text', '1 de 15')
    })
  })
})
