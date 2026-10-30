import './commands'
import 'cypress-mochawesome-reporter/register'


// Reloj exclusivo del servidor Cypress: se restablece a la hora real al empezar cada test.
// El reloj de Qolqe avanza normalmente; las pruebas de frontera usan su API de adelanto.
beforeEach(() => {
  cy.request({method:'DELETE',url:'/api/pruebas/reloj',log:false,retryOnNetworkFailure:false}).then(r => {
    expect(r.status).to.eq(200)
  })
})
