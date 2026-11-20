export const ui = (id: string) => cy.get(`[data-testid="${id}"]`)
export function escribir(id: string, value: string) {
  ui(id).clear()
  if (value) ui(id).type(value, { delay: 0, parseSpecialCharSequences: false })
}
export function confirmar() { ui('dialogo-confirmar').should('be.visible'); ui('boton-confirmar-accion').click() }
export function cerrarDialogo() { ui('boton-cancelar-dialogo').click(); ui('dialogo-formulario').should('not.exist') }
export function toast(texto?: string) {
  const alert = ui('toast').should('be.visible')
  return texto ? alert.should('contain.text',texto) : alert.should('not.have.text','')
}
