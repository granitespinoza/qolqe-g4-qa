import { ContactosPage } from '../pages/ContactosPage'
import { TransferenciasPage } from '../pages/TransferenciasPage'
import { ui } from '../pages/Ui'
import { api, caso, cerrar, comprobarSaldo, ingresar, lista, observar, respuesta, saldo, sms } from '../support/fixtures'
const contactos = new ContactosPage(), p = new TransferenciasPage()

describe('Parte 2 | HU-G4-05 | Transferencias desde contactos', () => {
  ;(['0.01','500.00'] as const).forEach((monto,i) => {
    caso(`E2E-G4-${201+i}`,['WEB-G4-05-CA1-01','WEB-G4-05-CA1-02'],`Transferir ${monto}, comprobante y movimientos persistentes`,() => {
      lista(1).then(({a,otros:[b],contactos:[c]}) => {
        saldo(a,'600.00'); ingresar(a); contactos.abrir(); contactos.transferir(c.id)
        ui('input-celular-destino').should('be.disabled'); ui('input-descripcion').should('have.attr','maxlength','60')
        observar('POST','/api/transferencias'); p.preparar(monto,'D'.repeat(60))
        ui('confirmar-destino').should('contain.text',c.alias); ui('confirmar-total').should('contain.text',monto); p.confirmar()
        respuesta(201).then(tx => {
          p.comprobante(); ui('comprobante-codigo').should('have.text',tx.codigo_operacion)
          ui('comprobante-destino').should('contain.text',c.nombre).and('contain.text',b.celular)
          ui('comprobante-monto').should('contain.text',monto); ui('comprobante-total').should('contain.text',monto)
          ui('comprobante-comision').should('contain.text','0.00'); ui('comprobante-saldo').should('contain.text',(600-Number(monto)).toFixed(2))
          ui('comprobante-fecha').should('not.have.text','')
          comprobarSaldo(a,(600-Number(monto)).toFixed(2)); comprobarSaldo(b,monto)
          api('GET',`/api/movimientos/${tx.codigo_operacion}`,a).its('codigo_operacion').should('eq',tx.codigo_operacion)
          api('GET',`/api/movimientos/${tx.codigo_operacion}`,b).its('codigo_operacion').should('eq',tx.codigo_operacion)
          sms(b,monto); cy.visit('/historial'); ui('tabla-movimientos').should('contain.text',monto)
        })
      })
    })
  })
  caso('E2E-G4-203',['WEB-G4-05-CA1-02'],'Montos 0, negativo, 500.01 y tres decimales: sin transferencia',() => {
    lista(1).then(({a,otros:[b],contactos:[c]}) => {
      saldo(a,'600.00'); ingresar(a); contactos.abrir(); contactos.transferir(c.id)
      cy.intercept('POST','/api/transferencias').as('noTransferir'); observar('GET','/api/transferencias/comision*')
      cy.wrap(['0','-1','500.01','1.001']).each((monto: string)=>{ p.preparar(monto); respuesta(422,'MONTO_INVALIDO'); p.error(); ui('dialogo-confirmacion').should('not.be.visible') })
      cy.get('@noTransferir.all').should('have.length',0); comprobarSaldo(a,'600.00'); comprobarSaldo(b,'0.00')
    })
  })
  ;(['saldo','limite','cerrado'] as const).forEach((tipo,i) => {
    caso(`E2E-G4-${204+i}`,['WEB-G4-05-CA1-03'],`Error ${tipo} conserva el dinero`,() => {
      lista(1).then(({a,otros:[b],contactos:[c]}) => {
        const inicial=tipo==='saldo'?'0.00':'500.00', monto=tipo==='limite'?'101.00':'10.00'
        saldo(a,inicial)
        if(tipo==='limite') api('PUT','/api/limites',a,{limite_diario:'100.00'})
        if(tipo==='cerrado') cerrar(b)
        ingresar(a); contactos.abrir(); contactos.transferir(c.id); observar('POST','/api/transferencias')
        p.preparar(monto); p.confirmar(); respuesta(422,{saldo:'SALDO_INSUFICIENTE',limite:'LIMITE_DIARIO_EXCEDIDO',cerrado:'DESTINO_INACTIVO'}[tipo]); p.error()
        ui('comprobante').should('not.be.visible'); comprobarSaldo(a,inicial)
        if(tipo!=='cerrado') comprobarSaldo(b,'0.00')
        api('GET','/api/movimientos/recientes',a).should('have.length',0)
      })
    })
  })
})
