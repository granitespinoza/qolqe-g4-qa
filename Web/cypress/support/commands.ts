export type UsuarioPrueba = { celular: string; pin: string }
export type Contexto = { propietario: UsuarioPrueba; contacto: UsuarioPrueba }
declare global {
  namespace Cypress {
    interface Chainable { prepararContactos(): Chainable<Contexto> }
  }
}

// Solo datos ficticios. No reinicia bases compartidas ni repite operaciones funcionales.
Cypress.Commands.add('prepararContactos', () => {
  const crear = (nombres: string) => {
    const dni = String(Cypress._.random(10000000, 99999999))
    const usuario = { celular: `9${dni}`, pin: '4826' }
    return cy.request({ method: 'POST', url: '/api/usuarios', body: { dni, nombres, ...usuario }, log: false, retryOnNetworkFailure: false })
      .then(r => { expect(r.status, 'Preparación: registro de usuario').to.eq(201); return usuario })
  }
  return crear('Franco Cypress').then(propietario => crear('Granit Cypress').then(contacto => ({ propietario, contacto })))
})
