import { ui, escribir, confirmar } from './Ui'

export class ContactosPage {
  abrir() { cy.visit('/contactos'); cy.contains('h1','Contactos frecuentes').should('be.visible'); return this.contador().should('not.have.text','') }
  agregar(celular: string, alias: string) { escribir('input-celular',celular); escribir('input-alias',alias); return ui('boton-agregar-contacto').click() }
  filas() { return ui('contacto') }
  fila(id: number) { return cy.get(`[data-testid="contacto"][data-id="${id}"]`) }
  error() { return ui('contactos-error') }
  contador() { return ui('contador-contactos') }
  buscar(texto: string) { escribir('input-buscar-contacto',texto) }
  siguiente() { ui('boton-siguiente').click() }
  anterior() { ui('boton-anterior').click() }
  editar(id: number, alias: string) {
    this.fila(id).find('[data-testid="boton-editar-contacto"]').click()
    ui('dialogo-formulario').should('be.visible'); escribir('input-nuevo-alias',alias)
    ui('boton-guardar-dialogo').click()
  }
  favorito(id: number) { this.fila(id).find('[data-testid="boton-favorito"]').click() }
  eliminar(id: number) { this.fila(id).find('[data-testid="boton-eliminar-contacto"]').click(); confirmar() }
  transferir(id: number) { this.fila(id).find('[data-testid="boton-transferir-contacto"]').click(); cy.location('pathname').should('eq','/transferir'); ui('select-contacto').should('have.value',String(id)) }
}
