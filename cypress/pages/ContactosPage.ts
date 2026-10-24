export class ContactosPage {
  abrir() { cy.visit('/contactos'); return cy.contains('h1', 'Contactos frecuentes').should('be.visible') }
  agregar(celular: string, alias: string) {
    cy.get('[data-testid="input-celular"]').clear().type(celular)
    cy.get('[data-testid="input-alias"]').clear().type(alias)
    return cy.get('[data-testid="boton-agregar-contacto"]').click()
  }
  filas() { return cy.get('[data-testid="contacto"]') }
  error() { return cy.get('[data-testid="contactos-error"]') }
  contador() { return cy.get('[data-testid="contador-contactos"]') }
}
