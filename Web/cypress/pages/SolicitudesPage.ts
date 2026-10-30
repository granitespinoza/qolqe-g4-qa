import { ui, escribir, confirmar } from './Ui'

export class SolicitudesPage {
  abrir() { cy.visit('/solicitudes'); cy.contains('h1','Solicitudes de dinero').should('be.visible'); return ui('lista-solicitudes').children().should('have.length.at.least',1) }
  crear(contacto: number | null, monto: string, motivo: string) {
    if (contacto !== null) ui('select-solicitud-contacto').select(String(contacto))
    escribir('input-solicitud-monto',monto); escribir('input-solicitud-motivo',motivo); ui('boton-solicitar').click()
  }
  vista(vista: 'enviadas'|'recibidas') { ui('lista-solicitudes').children().should('have.length.at.least',1); ui(`pestana-${vista}`).click().should('have.attr','aria-selected','true') }
  filtrar(estado: string) { ui('select-filtro-estado').select(estado) }
  filas() { return ui('solicitud') }
  fila(id: number) { return cy.get(`[data-testid="solicitud"][data-id="${id}"]`) }
  estado(id: number, estado: string) { return this.fila(id).find('[data-testid="solicitud-estado"]').should('have.text',estado) }
  aceptar(id: number) { this.fila(id).find('[data-testid="boton-aceptar-solicitud"]').click(); confirmar() }
  rechazar(id: number, motivo: string) {
    this.fila(id).find('[data-testid="boton-rechazar-solicitud"]').click()
    ui('dialogo-formulario').should('be.visible'); escribir('input-motivo-rechazo',motivo); ui('boton-guardar-dialogo').click()
  }
  cancelar(id: number) { this.fila(id).find('[data-testid="boton-cancelar-solicitud"]').click(); confirmar() }
}
