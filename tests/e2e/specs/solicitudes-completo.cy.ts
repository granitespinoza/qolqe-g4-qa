import { SolicitudesPage } from '../pages/SolicitudesPage'
import { ui, cerrarDialogo, toast } from '../pages/Ui'
import { actores, api, avanzar, caso, comprobarSaldo, ingresar, lista, observar, pedir, prepararSolicitud, renovar, respuesta, saldo, sms, vincular } from '../support/fixtures'
const p = new SolicitudesPage()

describe('Parte 2 | Solicitudes G4 | estados, permisos y dinero', () => {
  caso('E2E-G4-301',['WEB-G4-06-CA1-01','WEB-G4-06-CA2-01'],'Crear solicitud por UI; 48 horas, SMS y ambas vistas',() => {
    lista(1).then(({a,otros:[b],contactos:[c]}) => {
      ingresar(a); p.abrir(); observar('POST','/api/solicitudes'); p.crear(c.id,'10.00','Almuerzo')
      respuesta(201).then(s => {
        expect(s.estado).to.eq('PENDIENTE')
        expect(Date.parse(s.vence_en+'-05:00')-Date.parse(s.creada_en+'-05:00')).to.eq(48*3600000)
        p.estado(s.id,'Pendiente'); p.fila(s.id).should('contain.text','Almuerzo').and('contain.text','10.00')
        p.fila(s.id).find('[data-testid="solicitud-detalle"]').should('contain.text','Vence el')
        ui('pestana-enviadas').should('have.attr','aria-selected','true'); sms(b,'te solicita S/ 10.00')
        cy.reload(); p.vista('enviadas'); p.estado(s.id,'Pendiente')
        ingresar(b); p.abrir(); p.estado(s.id,'Pendiente'); p.fila(s.id).should('contain.text',a.celular)
      })
    })
  })
  ;([{monto:'0.01',motivo:'Sol'},{monto:'500.00',motivo:'M'.repeat(60)}]).forEach((v,i)=>{
    caso(`E2E-G4-${302+i}`,['WEB-G4-06-CA1-01'],`Límites válidos: ${v.monto}, motivo ${v.motivo.length}`,() => {
      lista(1).then(({a,contactos:[c]})=>{ ingresar(a); p.abrir(); observar('POST','/api/solicitudes'); p.crear(c.id,v.monto,v.motivo); respuesta(201).then(s=>{p.estado(s.id,'Pendiente');p.fila(s.id).should('contain.text',v.motivo)});cy.reload();p.vista('enviadas');p.filas().should('have.length',1) })
    })
  })
  caso('E2E-G4-304',['WEB-G4-06-CA1-01','WEB-G4-06-CA1-02'],'Montos y motivos inválidos no crean solicitudes',() => {
    lista(1).then(({a,contactos:[c]}) => {
      ingresar(a); p.abrir(); observar('POST','/api/solicitudes')
      cy.wrap([{m:'0',r:'Valido'},{m:'-1',r:'Valido'},{m:'500.01',r:'Valido'},{m:'1.001',r:'Valido'},
        {m:'10',r:''},{m:'10',r:'Lu'},{m:'10',r:'M'.repeat(61)}]).each((v: {m: string; r: string})=>{ p.crear(c.id,v.m,v.r); respuesta(422,'SOLICITUD_INVALIDA'); ui('solicitud-mensaje').should('be.visible') })
      api('GET','/api/solicitudes',a).its('enviadas').should('have.length',0)
      cy.reload(); p.vista('enviadas'); p.filas().should('not.exist')
    })
  })
  caso('E2E-G4-305',['WEB-G4-06-CA1-02'],'Sin contacto el formulario explica el error',() => {
    actores(1).then(([a])=>{ ingresar(a);p.abrir();cy.intercept('POST','/api/solicitudes').as('noCrear');p.crear(null,'10','Almuerzo');ui('solicitud-mensaje').should('contain.text','Elige un contacto');cy.get('@noCrear.all').should('have.length',0);p.filas().should('not.exist') })
  })
  caso('E2E-G4-306',['WEB-G4-06-CA1-03'],'Pendiente 10 permitida, 11 rechazada sin alterar el total',() => {
    lista(1).then(({a,contactos:[c]}) => {
      cy.wrap(Array.from({length:9})).each(()=>pedir(a,c,'1.00'))
      ingresar(a);p.abrir();observar('POST','/api/solicitudes');p.crear(c.id,'1.00','Decima');respuesta(201)
      p.filas().should('have.length',10);p.crear(c.id,'1.00','Exceso');respuesta(422,'LIMITE_SOLICITUDES');ui('solicitud-mensaje').should('be.visible')
      cy.reload();p.vista('enviadas');p.filas().should('have.length',10)
    })
  })
  caso('E2E-G4-307',['WEB-G4-07-CA1-01','WEB-G4-07-CA1-02'],'Vistas separadas y filtros de los cinco estados',() => {
    prepararSolicitud().then(({a,b,c}) => {
      avanzar(2880);renovar(a);renovar(b);saldo(b,'100.00')
      pedir(a,c,'1.00','Pendiente')
      pedir(a,c,'1.00','Aceptada').then(s=>api('POST',`/api/solicitudes/${s.id}/aceptar`,b))
      pedir(a,c,'1.00','Rechazada').then(s=>api('POST',`/api/solicitudes/${s.id}/rechazar`,b))
      pedir(a,c,'1.00','Cancelada').then(s=>api('POST',`/api/solicitudes/${s.id}/cancelar`,a))
      vincular(b,a).then(inverso=>pedir(b,inverso,'1.00','Recibida'))
      ingresar(a);p.abrir();p.filas().should('have.length',1).and('contain.text','Recibida')
      p.vista('enviadas');p.filas().should('have.length',5)
      cy.wrap(['PENDIENTE','ACEPTADA','RECHAZADA','CANCELADA','VENCIDA']).each((estado: string)=>{
        p.filtrar(estado);p.filas().should('have.length',1);ui('solicitud-estado').should('have.text',estado.charAt(0)+estado.slice(1).toLowerCase())
      })
      p.filtrar('');p.filas().should('have.length',5);p.vista('recibidas');p.filas().should('have.length',1)
      p.filtrar('ACEPTADA');p.filas().should('not.exist');ui('lista-vacia').should('be.visible')
    })
  })
  ;([2879,2880,2881]).forEach((minutos,i)=>{
    caso(`E2E-G4-${308+i}`,['WEB-G4-07-CA2-01','WEB-G4-08-CA4-02'],`Frontera ${minutos} minutos sin esperas reales`,() => {
      prepararSolicitud().then(({b,s})=>{
        avanzar(minutos);ingresar(b);p.abrir();p.estado(s.id,minutos<2880?'Pendiente':'Vencida')
        p.fila(s.id).find('[data-testid="boton-aceptar-solicitud"]').should(minutos<2880?'exist':'not.exist')
        if(minutos>=2880)p.fila(s.id).find('button').should('not.exist')
      })
    })
  })
  caso('E2E-G4-311',['WEB-G4-08-CA1-01','WEB-G4-08-CA3-01'],'Aceptar: dinero, operación, SMS y persistencia',() => {
    prepararSolicitud().then(({a,b,s})=>{
      saldo(b,'100.00');ingresar(b);p.abrir();observar('POST',`/api/solicitudes/${s.id}/aceptar`);p.aceptar(s.id)
      respuesta(200).then(r=>{
        expect(r.estado).to.eq('ACEPTADA');expect(r.codigo_operacion).to.be.a('string').and.not.empty
        p.estado(s.id,'Aceptada');p.fila(s.id).should('contain.text',r.codigo_operacion)
        comprobarSaldo(a,'10.00');comprobarSaldo(b,'90.00');sms(a,'aceptó tu solicitud');sms(a,r.codigo_operacion)
        api('GET',`/api/movimientos/${r.codigo_operacion}`,a).its('monto').should('eq','10.00')
        api('GET',`/api/movimientos/${r.codigo_operacion}`,b).its('monto').should('eq','10.00')
        cy.reload();p.estado(s.id,'Aceptada');p.fila(s.id).find('button').should('not.exist')
        ingresar(a);p.abrir();p.vista('enviadas');p.estado(s.id,'Aceptada')
      })
    })
  })
  ;(['saldo','limite'] as const).forEach((tipo,i)=>{
    caso(`E2E-G4-${312+i}`,['WEB-G4-08-CA2-01'],`Aceptar con error de ${tipo}: conserva pendiente y dinero`,() => {
      prepararSolicitud().then(({a,b,s})=>{
        if(tipo==='limite'){
          saldo(b,'500.00');api('PUT','/api/limites',b,{limite_diario:'100.00'})
          api('POST','/api/transferencias',b,{celular_destino:a.celular,monto:'100.00'},201)
        }
        ingresar(b);p.abrir();observar('POST',`/api/solicitudes/${s.id}/aceptar`);p.aceptar(s.id)
        respuesta(422,tipo==='saldo'?'SALDO_INSUFICIENTE':'LIMITE_DIARIO_EXCEDIDO');toast()
        p.estado(s.id,'Pendiente');comprobarSaldo(a,tipo==='saldo'?'0.00':'100.00');comprobarSaldo(b,tipo==='saldo'?'0.00':'400.00')
        cy.reload();p.estado(s.id,'Pendiente');api('GET','/api/solicitudes',a).then(r=>expect(r.enviadas[0].codigo_operacion).to.eq(null))
      })
    })
  })
  caso('E2E-G4-314',['WEB-G4-08-CA4-01','WEB-G4-09-CA1-02','WEB-G4-10-CA1-02'],'Acciones visibles solo para el actor correcto',() => {
    prepararSolicitud().then(({a,b,s})=>{
      ingresar(a);p.abrir();p.vista('enviadas');p.fila(s.id).find('[data-testid="boton-cancelar-solicitud"]').should('exist')
      p.fila(s.id).find('[data-testid="boton-aceptar-solicitud"],[data-testid="boton-rechazar-solicitud"]').should('not.exist')
      ingresar(b);p.abrir();p.fila(s.id).find('[data-testid="boton-aceptar-solicitud"]').should('exist');p.fila(s.id).find('[data-testid="boton-rechazar-solicitud"]').should('exist')
      p.fila(s.id).find('[data-testid="boton-cancelar-solicitud"]').should('not.exist')
      actores(1).then(([tercero])=>{ingresar(tercero);p.abrir();p.filas().should('not.exist');p.vista('enviadas');p.filas().should('not.exist')})
    })
  })
  ;(['aceptar','rechazar','cancelar'] as const).forEach((accion,i)=>{
    caso(`E2E-G4-${315+i}`,['WEB-G4-08-CA4-02','WEB-G4-09-CA1-02','WEB-G4-10-CA1-02'],`Solicitud resuelta (${accion}) no ofrece otra transición`,() => {
      prepararSolicitud().then(({a,b,s})=>{
        if(accion==='aceptar')saldo(b,'100.00')
        api('POST',`/api/solicitudes/${s.id}/${accion}`,accion==='cancelar'?a:b)
        ingresar(b);p.abrir();p.fila(s.id).find('button').should('not.exist')
        ingresar(a);p.abrir();p.vista('enviadas');p.fila(s.id).find('button').should('not.exist')
      })
    })
  })
  ;(['','R'.repeat(60)]).forEach((motivo,i)=>{
    caso(`E2E-G4-${318+i}`,['WEB-G4-09-CA1-01'],`Rechazar con motivo de longitud ${motivo.length}, SMS y persistencia`,() => {
      prepararSolicitud().then(({a,b,s})=>{
        ingresar(b);p.abrir();observar('POST',`/api/solicitudes/${s.id}/rechazar`);p.rechazar(s.id,motivo)
        respuesta(200).then(r=>{expect(r.estado).to.eq('RECHAZADA');expect(r.motivo_rechazo).to.eq(motivo||null)})
        p.estado(s.id,'Rechazada');sms(a,'rechazó tu solicitud');cy.reload();p.estado(s.id,'Rechazada')
        if(motivo)p.fila(s.id).should('contain.text',motivo)
      })
    })
  })
  caso('E2E-G4-320',['WEB-G4-09-CA1-02'],'Motivo de rechazo de 61 caracteres conserva pendiente',() => {
    prepararSolicitud().then(({b,s})=>{
      ingresar(b);p.abrir();observar('POST',`/api/solicitudes/${s.id}/rechazar`);p.rechazar(s.id,'R'.repeat(61))
      respuesta(422,'SOLICITUD_INVALIDA');ui('dialogo-error').should('be.visible');cerrarDialogo();p.estado(s.id,'Pendiente')
      cy.reload();p.estado(s.id,'Pendiente')
    })
  })
  caso('E2E-G4-321',['WEB-G4-10-CA1-01'],'Solicitante cancela por UI y persiste CANCELADA',() => {
    prepararSolicitud().then(({a,s})=>{
      ingresar(a);p.abrir();p.vista('enviadas');observar('POST',`/api/solicitudes/${s.id}/cancelar`);p.cancelar(s.id)
      respuesta(200).its('estado').should('eq','CANCELADA');p.estado(s.id,'Cancelada');cy.reload();p.vista('enviadas');p.estado(s.id,'Cancelada')
    })
  })
  ;(['rechazar','cancelar','aceptar'] as const).forEach((accion,i)=>{
    caso(`E2E-G4-${322+i}`,accion==='aceptar'?['WEB-G4-08-CA4-02']:accion==='rechazar'?['WEB-G4-09-CA1-02']:['WEB-G4-10-CA1-02'],
      `${accion==='aceptar'?'[D-03] ':''}Formulario cargado antes de vencer: ${accion} debe responder 409 al vencer`,() => {
      prepararSolicitud().then(({a,b,s})=>{
        saldo(b,'100.00');avanzar(2879);renovar(a);renovar(b)
        ingresar(accion==='cancelar'?a:b);p.abrir();if(accion==='cancelar')p.vista('enviadas');p.estado(s.id,'Pendiente')
        avanzar(1);observar('POST',`/api/solicitudes/${s.id}/${accion}`)
        if(accion==='rechazar')p.rechazar(s.id,'')
        else if(accion==='cancelar')p.cancelar(s.id)
        else p.aceptar(s.id)
        respuesta(409,'ESTADO_INVALIDO')
        if(accion==='rechazar'){ui('dialogo-error').should('be.visible');cerrarDialogo()}else toast()
        cy.reload();if(accion==='cancelar')p.vista('enviadas');p.estado(s.id,'Vencida')
        comprobarSaldo(a,'0.00');comprobarSaldo(b,'100.00')
      })
    })
  })
})
