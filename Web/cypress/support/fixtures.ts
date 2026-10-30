import { LoginPage } from '../pages/LoginPage'

export type Actor = { id: number; celular: string; pin: string; token: string; nombres: string }
export type Contacto = { id: number; alias: string; celular: string; favorito: boolean; nombre: string }
export type Solicitud = { id: number; estado: string; creada_en: string; vence_en: string; codigo_operacion: string | null }

// Las operaciones funcionales se ejecutan una vez. Solo la autenticación de preparación y lecturas de disponibilidad admiten sondeos acotados.
export function api(method: string, url: string, actor?: Actor, body?: object, status = 200) {
  return cy.then(() => cy.request({ method, url, body, headers: actor ? { Authorization: `Bearer ${actor.token}` } : {},
    log: false, failOnStatusCode: false, retryOnNetworkFailure: false, retryOnStatusCodeFailure: false }))
    .then(r => { expect(r.status, `${method} ${url}`).to.eq(status); return r.body })
}

// Visibilidad tras commit: no repetir registros ni operaciones de negocio.
function autenticarPreparacion(celular: string, pin: string, intento = 1): Cypress.Chainable<string> {
  return cy.request({method:'POST',url:'/api/auth/login',body:{celular,pin},log:false,failOnStatusCode:false,retryOnNetworkFailure:false}).then(r => {
    if(r.status===401 && r.body.codigo==='CREDENCIALES_INVALIDAS' && intento<10) {
      Cypress.log({name:'preparación',message:`Registro aún no visible: sondeo ${intento}/10`})
      return autenticarPreparacion(celular,pin,intento+1)
    }
    expect(r.status,'Autenticación de preparación').to.eq(200)
    return cy.wrap(r.body.access_token as string,{log:false})
  })
}

export function esperarLectura(url: string, actor: Actor, condicion: (body: any)=>boolean, intento=1): Cypress.Chainable<any> {
  return cy.request({method:'GET',url,headers:{Authorization:`Bearer ${actor.token}`},log:false,failOnStatusCode:false,retryOnNetworkFailure:false}).then(r=>{
    if((r.status===401 || (r.status===200 && !condicion(r.body))) && intento<10) {
      Cypress.log({name:'preparación',message:`Recurso aún no visible: sondeo ${intento}/10`})
      return esperarLectura(url,actor,condicion,intento+1)
    }
    expect(r.status,`Disponibilidad ${url}`).to.eq(200)
    expect(condicion(r.body),'Precondición visible').to.eq(true)
    return cy.wrap(r.body,{log:false})
  })
}

export function crearActor(nombres = 'Usuario Cypress') {
  const dni=String(Cypress._.random(10000000,99999999)),celular=`9${dni}`,pin='4826'
  return api('POST','/api/usuarios',undefined,{dni,celular,pin,nombres},201).then(registro=>
    autenticarPreparacion(celular,pin).then(token=>{
      const a={id:registro.id as number,celular,pin,nombres,token}
      return esperarLectura('/api/cuentas/me/saldo',a,()=>true).then(()=>a)
    }))
}

export function actores(count = 2) {
  const list: Actor[] = []
  return cy.wrap(Array.from({ length: count }), { log: false }).each((_, i) =>
    crearActor(i === 0 ? 'Franco Cypress' : `Persona Cypress ${i}`).then(a => { list.push(a) })
  ).then(() => list)
}

export function vincular(a: Actor, b: Actor, alias = 'Ana') {
  return api('POST', '/api/contactos', a, { celular: b.celular, alias }, 201).then((c: Contacto)=>esperarLectura(`/api/contactos?buscar=${encodeURIComponent(alias)}`,a,r=>r.contactos.some((x: Contacto)=>x.id===c.id)).then(()=>c))
}
export function ingresar(a: Actor) { return new LoginPage().ingresar(a.celular, a.pin) }
export function renovar(a: Actor) {
  return autenticarPreparacion(a.celular,a.pin).then(token => { a.token=token; return esperarLectura('/api/cuentas/me/saldo',a,()=>true) })
}
export function saldo(a: Actor, valor: string) { return api('PUT', '/api/pruebas/saldo', undefined, { celular: a.celular, saldo: valor }) }
export function comprobarSaldo(a: Actor, valor: string) { return api('GET', '/api/cuentas/me/saldo', a).its('saldo').should('eq', valor) }
export function avanzar(minutos: number) { return api('PUT', '/api/pruebas/reloj', undefined, { avanzar_minutos: minutos }) }
export function cerrar(a: Actor) { return api('POST', '/api/cuentas/me/cierre', a, { pin: a.pin }, 204) }
export function pedir(a: Actor, c: Contacto, monto = '10.00', motivo = 'Almuerzo') {
  return api('POST', '/api/solicitudes', a, { contacto_id: c.id, monto, motivo }, 201).then((s: Solicitud)=>esperarLectura('/api/solicitudes',a,r=>r.enviadas.some((x: Solicitud)=>x.id===s.id)).then(()=>s))
}
export function prepararSolicitud() {
  return actores().then(([a,b]) => vincular(a,b).then(c => pedir(a,c).then(s => ({a,b,c,s}))))
}
export function lista(count: number, aliases?: string[]) {
  return actores(count + 1).then(([a,...otros]) => {
    const contactos: Contacto[] = []
    return cy.wrap(otros, { log: false }).each((b: Actor,i: number) => vincular(a,b,aliases?.[i] || `Contacto ${String(i+1).padStart(2,'0')}`).then(c => { contactos.push(c) }))
      .then(() => ({a,otros,contactos}))
  })
}
export function observar(method: string, url: string) { cy.intercept(method, url).as('accion') }
export function respuesta(status: number, codigo?: string) {
  return cy.wait('@accion').then(({response}) => {
    expect(response, 'respuesta real del servidor').to.exist
    expect(response!.statusCode).to.eq(status)
    if (codigo) expect(response!.body.codigo).to.eq(codigo)
    return response!.body
  })
}
export function sms(a: Actor, texto: string) {
  return api('GET', `/api/pruebas/notificaciones?celular=${a.celular}`).then(rows => {
    expect(rows.some((r: {mensaje: string; celular: string}) => r.celular === a.celular && r.mensaje.includes(texto)), 'SMS al destinatario correcto').to.eq(true)
  })
}
export function caso(id: string, grupos: string[], descripcion: string, test: () => void) {
  const hus = [...new Set(grupos.map(g => '@HU-G4-' + g.split('-')[2]))]
  const defect = ({'E2E-G4-102':'D-01','E2E-G4-104':'D-02','E2E-G4-113':'D-01','E2E-G4-115':'D-02','E2E-G4-117':'D-07','E2E-G4-201':'D-07','E2E-G4-202':'D-07','E2E-G4-206':'D-08','E2E-G4-324':'D-03'} as Record<string,string>)[id]
  const tags = [...hus, '@TC-' + id, ...(defect ? ['@known_issue', '@' + defect] : [])]
  it(`${id} ${tags.join(' ')} | ${grupos.join(' ')} | ${descripcion}`, test)
}
