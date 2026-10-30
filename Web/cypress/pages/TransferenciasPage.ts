import { ui, escribir } from './Ui'
export class TransferenciasPage {
  preparar(monto: string, descripcion = '') {
    escribir('input-monto',monto); escribir('input-descripcion',descripcion); ui('boton-continuar').click()
  }
  confirmar() { ui('dialogo-confirmacion').should('be.visible'); ui('boton-confirmar').click() }
  error() { return ui('transferencia-error').should('be.visible').and('not.have.text','') }
  comprobante() { return ui('comprobante').should('be.visible') }
}
