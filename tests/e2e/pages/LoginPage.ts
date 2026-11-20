export class LoginPage {
  ingresar(celular: string, pin: string) {
    cy.visit('/login')
    cy.get('[data-testid="input-celular"]').type(celular)
    cy.get('[data-testid="input-pin"]').type(pin, { log: false })
    cy.get('[data-testid="boton-ingresar"]').click()
    return cy.location('pathname').should('eq', '/inicio')
  }
}
