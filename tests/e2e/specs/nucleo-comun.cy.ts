import { actores, caso, ingresar, saldo, api, comprobarSaldo } from '../support/fixtures'
import { ui } from '../pages/Ui'
import { TransferenciasPage } from '../pages/TransferenciasPage'

describe('Núcleo común | acceso y perfil', () => {
  caso('E2E-G4-401',[],'@HU-N-02 Login válido navega a inicio',()=>{
    actores(1).then(([a])=>{ingresar(a);cy.contains('h1','Inicio').should('be.visible');ui('saludo').should('contain.text','Hola')})
  })
  caso('E2E-G4-402',[],'@HU-N-02 Credenciales inválidas mantienen el login y muestran mensaje genérico',()=>{
    actores(1).then(([a])=>{cy.visit('/login');cy.intercept('POST','/api/auth/login').as('loginInvalido');ui('input-celular').type(a.celular);ui('input-pin').type('9876',{log:false});ui('boton-ingresar').click();cy.wait('@loginInvalido').its('response.statusCode').should('eq',401);ui('login-error').should('be.visible');cy.location('pathname').should('eq','/login')})
  })
  caso('E2E-G4-403',[],'@HU-N-04 Saldo preparado visible y opción de ocultar',()=>{
    actores(1).then(([a])=>{saldo(a,'123.45');ingresar(a);ui('saldo-valor').should('contain.text','123.45');ui('boton-ocultar-saldo').click();ui('boton-ocultar-saldo').should('have.attr','aria-pressed','true');ui('boton-ocultar-saldo').click();ui('saldo-valor').should('contain.text','123.45')})
  })
  caso('E2E-G4-404',[],'@HU-N-04 Perfil conserva celular y enmascara DNI',()=>{
    actores(1).then(([a])=>{ingresar(a);cy.visit('/perfil');ui('perfil-celular').should('have.text',a.celular);ui('perfil-nombres').should('have.text',a.nombres);ui('perfil-dni').should('contain.text',a.celular.slice(-4)).and('not.have.text',a.celular.slice(1))})
  })
  caso('E2E-G4-405',[],'@HU-N-05 Edición de nombres persiste tras recargar',()=>{
    actores(1).then(([a])=>{ingresar(a);cy.visit('/perfil');ui('input-nombres').should('have.value',a.nombres).clear().type('Perfil Actualizado');cy.intercept('PUT','/api/cuentas/me').as('editarPerfil');ui('boton-guardar-perfil').click();cy.wait('@editarPerfil').its('response.statusCode').should('eq',200);cy.reload();ui('perfil-nombres').should('have.text','Perfil Actualizado')})
  })
  caso('E2E-G4-406',[],'@HU-N-01 Registro por UI crea cuenta y permite iniciar sesión',()=>{
    const dni=String(Cypress._.random(10000000,99999999)),cell='9'+dni
    cy.visit('/registro');ui('input-dni').type(dni);ui('input-nombres').type('Registro Web');ui('input-celular').type(cell);ui('input-pin').type('4826',{log:false});ui('input-pin-confirmacion').type('4826',{log:false});cy.intercept('POST','/api/usuarios').as('registro');ui('boton-registrar').click();cy.wait('@registro').its('response.statusCode').should('eq',201)
    cy.visit('/login');ui('input-celular').clear().type(cell);ui('input-pin').type('4826',{log:false});ui('boton-ingresar').click();cy.location('pathname').should('eq','/inicio');ui('saldo-valor').should('contain.text','0.00')
  })
  caso('E2E-G4-407',[],'@HU-N-03 Cerrar sesión limpia la UI, revoca su token y conserva otra sesión',()=>{
    actores(1).then(([a])=>{
      cy.intercept('POST','/api/auth/login').as('sesionWeb');ingresar(a)
      cy.wait('@sesionWeb').then(({response})=>{
        const token=response!.body.access_token as string
        cy.intercept('POST','/api/auth/logout').as('cerrarSesion');ui('boton-cerrar-sesion').click()
        cy.wait('@cerrarSesion').its('response.statusCode').should('eq',204);cy.location('pathname').should('eq','/login')
        cy.visit('/perfil');cy.location('pathname').should('eq','/login')
        api('GET','/api/cuentas/me/saldo',a).its('saldo').should('eq','0.00')
        cy.request({url:'/api/cuentas/me/saldo',headers:{Authorization:`Bearer ${token}`},failOnStatusCode:false,retryOnNetworkFailure:false,log:false})
          .then(r=>expect(r.status,'Token de la sesión cerrada debe quedar revocado').to.eq(401))
      })
    })
  })
  caso('E2E-G4-408',[],'@HU-N-06 Cerrar cuenta con saldo cero y PIN impide volver a ingresar',()=>{
    actores(1).then(([a])=>{
      ingresar(a);cy.visit('/perfil');ui('boton-cerrar-cuenta').click();ui('dialogo-formulario').should('be.visible');ui('input-pin-cierre').type(a.pin,{log:false})
      cy.intercept('POST','/api/cuentas/me/cierre').as('cerrarCuenta');ui('boton-guardar-dialogo').click();cy.wait('@cerrarCuenta').its('response.statusCode').should('eq',204)
      cy.location('pathname').should('eq','/login');api('POST','/api/auth/login',undefined,{celular:a.celular,pin:a.pin},401).its('codigo').should('eq','CUENTA_CERRADA')
    })
  })
  caso('E2E-G4-409',[],'@HU-N-07 Transferencia directa por celular muestra comprobante y acredita al destinatario',()=>{
    actores().then(([a,b])=>{
      saldo(a,'100.00');ingresar(a);new TransferenciasPage().abrir();ui('input-celular-destino').type(b.celular)
      const pagina=new TransferenciasPage();pagina.preparar('10.00','Transferencia núcleo');ui('confirmar-comision').should('contain.text','0.00')
      cy.intercept('POST','/api/transferencias').as('transferenciaDirecta');pagina.confirmar()
      cy.wait('@transferenciaDirecta').then(({response})=>{
        expect(response!.statusCode).to.eq(201);const codigo=response!.body.codigo_operacion
        pagina.comprobante();ui('comprobante-codigo').should('have.text',codigo);ui('comprobante-total').should('contain.text','10.00')
        comprobarSaldo(a,'90.00');comprobarSaldo(b,'10.00');api('GET',`/api/movimientos/${codigo}`,a).its('monto').should('eq','10.00');api('GET',`/api/movimientos/${codigo}`,b).its('monto').should('eq','10.00')
      })
    })
  })
  caso('E2E-G4-410',[],'@HU-N-08 Transferencia interbancaria cobra comisión y enmascara el CCI',()=>{
    actores(1).then(([a])=>{
      saldo(a,'200.00');ingresar(a);new TransferenciasPage().abrir();ui('pestana-interbancaria').click();ui('input-cci').type('12345678901234567890')
      const pagina=new TransferenciasPage();pagina.preparar('100.00');ui('confirmar-comision').should('contain.text','1.50');ui('confirmar-total').should('contain.text','101.50')
      cy.intercept('POST','/api/transferencias').as('transferenciaBanco');pagina.confirmar();cy.wait('@transferenciaBanco').then(({response})=>{
        expect(response!.statusCode).to.eq(201);pagina.comprobante();ui('comprobante-saldo').should('contain.text','98.50');comprobarSaldo(a,'98.50')
        api('GET',`/api/movimientos/${response!.body.codigo_operacion}`,a).its('contraparte').should('eq','****************7890')
      })
    })
  })
  caso('E2E-G4-411',[],'@HU-N-09 Simular comisión y cancelar conserva saldo y no crea movimientos',()=>{
    actores(1).then(([a])=>{
      saldo(a,'200.00');ingresar(a);new TransferenciasPage().abrir();ui('pestana-interbancaria').click();ui('input-cci').type('12345678901234567890')
      cy.intercept('GET','/api/transferencias/comision*').as('simularComision');new TransferenciasPage().preparar('100.00')
      cy.wait('@simularComision').its('response.statusCode').should('eq',200);ui('confirmar-comision').should('contain.text','1.50');ui('confirmar-total').should('contain.text','101.50')
      ui('boton-cancelar').click();ui('dialogo-confirmacion').should('not.be.visible');ui('comprobante').should('not.be.visible');comprobarSaldo(a,'200.00')
      api('GET','/api/movimientos/recientes?limite=5',a).should('have.length',0)
    })
  })
})
