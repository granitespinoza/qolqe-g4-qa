import { LoginPage } from '../pages/LoginPage'
import { ContactosPage } from '../pages/ContactosPage'
describe('DEMO DIDÁCTICA | fallo intencional, fuera de regresión', () => {
  it('produce evidencia al esperar incorrectamente dos contactos', () => {
    cy.prepararContactos().then(({ propietario, contacto }) => {
      const pagina = new ContactosPage()
      new LoginPage().ingresar(propietario.celular, propietario.pin)
      pagina.abrir()
      pagina.agregar(contacto.celular, 'Ana Cypress')
      pagina.filas().should('have.length', 1)
      // Expectativa falsa SOLO para mostrar screenshot, video y error.
      pagina.filas().should('have.length', 2)
    })
  })
})
