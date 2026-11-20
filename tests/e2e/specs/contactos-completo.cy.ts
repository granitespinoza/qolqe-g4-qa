import { ContactosPage } from '../pages/ContactosPage'
import { ui, cerrarDialogo, toast } from '../pages/Ui'
import { actores, api, caso, cerrar, ingresar, lista, observar, respuesta, saldo, vincular, pedir, avanzar, renovar } from '../support/fixtures'

const p = new ContactosPage()
describe('Parte 2 | Contactos | requisitos reales sin exclusiones', () => {
  caso('E2E-G4-101',['WEB-G4-01-CA1-01'],'Alta en límites 3/20, tildes, números y persistencia',() => {
    actores(5).then(([a,...otros]) => {
      ingresar(a); p.abrir(); observar('POST','/api/contactos')
      cy.wrap(['Ana','A'.repeat(20),'José','A1 B']).each((alias: string,i: number) => {
        p.agregar(otros[i].celular,alias); respuesta(201).its('alias').should('eq',alias)
        p.filas().should('have.length',i+1).and('contain.text',alias)
      })
      cy.reload(); p.contador().should('contain.text','4 de 15')
    })
  })
  caso('E2E-G4-102',['WEB-G4-01-CA1-01'],'[D-01] ñ debe ser válida al crear',() => {
    actores().then(([a,b]) => { ingresar(a); p.abrir(); observar('POST','/api/contactos'); p.agregar(b.celular,'Niño'); respuesta(201); p.filas().should('contain.text','Niño') })
  })
  caso('E2E-G4-103',['WEB-G4-01-CA1-02'],'Recorta espacios y rechaza duplicado por mayúsculas',() => {
    actores(3).then(([a,b,c]) => {
      ingresar(a); p.abrir(); observar('POST','/api/contactos'); p.agregar(b.celular,' Ana ')
      respuesta(201).its('alias').should('eq','Ana'); p.filas().should('have.length',1)
      p.agregar(c.celular,'ANA'); respuesta(409,'ALIAS_DUPLICADO'); p.error().should('be.visible')
      cy.reload(); p.filas().should('have.length',1).and('contain.text',b.celular)
    })
  })
  caso('E2E-G4-104',['WEB-G4-01-CA1-02'],'[D-02] duplicado con espacios debe rechazarse',() => {
    actores(3).then(([a,b,c]) => { vincular(a,b); ingresar(a); p.abrir(); observar('POST','/api/contactos'); p.agregar(c.celular,' Ana '); respuesta(409,'ALIAS_DUPLICADO'); p.filas().should('have.length',1) })
  })
  caso('E2E-G4-105',['WEB-G4-01-CA1-03'],'Alias vacío, espacios, 2/21 caracteres y símbolos no crean datos',() => {
    actores().then(([a,b]) => {
      ingresar(a); p.abrir(); observar('POST','/api/contactos')
      cy.wrap(['','   ','Lu','A'.repeat(21),'Ana@']).each((alias: string) => {
        p.agregar(b.celular,alias); respuesta(422,'ALIAS_INVALIDO'); p.error().should('be.visible')
      })
      cy.reload(); p.contador().should('contain.text','0 de 15'); p.filas().should('not.exist')
    })
  })
  caso('E2E-G4-106',['WEB-G4-01-CA1-04'],'Celular inválido, propio e inexistente; límite de longitud UI',() => {
    actores().then(([a]) => {
      ingresar(a); p.abrir(); observar('POST','/api/contactos')
      ui('input-celular').should('have.attr','maxlength','9')
      cy.wrap([{cell:'123',status:422,code:'CELULAR_INVALIDO'},{cell:'812345678',status:422,code:'CELULAR_INVALIDO'},
        {cell:'9abcdefgh',status:422,code:'CELULAR_INVALIDO'},{cell:a.celular,status:422,code:'CONTACTO_PROPIO'},
        {cell:'909999999',status:404,code:'CELULAR_NO_REGISTRADO'} ]).each((v: {cell: string; status: number; code: string}) => {
          p.agregar(v.cell,'Valido'); respuesta(v.status,v.code); p.error().should('be.visible')
        })
      cy.reload(); p.filas().should('not.exist')
    })
  })
  caso('E2E-G4-107',['WEB-G4-01-CA1-04'],'Cuenta cerrada se trata como celular no registrado',() => {
    actores().then(([a,b]) => { cerrar(b); ingresar(a); p.abrir(); observar('POST','/api/contactos'); p.agregar(b.celular,'Cerrado'); respuesta(404,'CELULAR_NO_REGISTRADO'); p.error().should('be.visible'); p.filas().should('not.exist') })
  })
  caso('E2E-G4-108',['WEB-G4-01-CA1-05','WEB-G4-02-CA1-02'],'Contacto 15 permitido, 16 rechazado; paginación 10+5',() => {
    lista(14).then(({a}) => actores(2).then(([b,c]) => {
      ingresar(a); p.abrir(); observar('POST','/api/contactos'); p.agregar(b.celular,'Ultimo'); respuesta(201)
      p.contador().should('contain.text','15 de 15'); p.filas().should('have.length',10)
      p.agregar(c.celular,'Exceso'); respuesta(422,'LIMITE_CONTACTOS'); p.error().should('be.visible')
      p.siguiente(); p.filas().should('have.length',5); ui('indicador-pagina').should('have.text','Página 2 de 2')
      cy.reload(); p.contador().should('contain.text','15 de 15'); api('GET','/api/contactos',a).its('total').should('eq',15)
    }))
  })
  caso('E2E-G4-109',['WEB-G4-02-CA1-01','WEB-G4-02-CA1-02'],'Lista vacía y frontera de páginas 10/11',() => {
    actores().then(([a]) => { ingresar(a); p.abrir(); ui('lista-vacia').should('contain.text','Aún no tienes'); ui('boton-anterior').should('be.disabled'); ui('boton-siguiente').should('be.disabled') })
    lista(10).then(({a}) => {
      ingresar(a); p.abrir(); p.filas().should('have.length',10); ui('boton-siguiente').should('be.disabled')
      actores(1).then(([b]) => { observar('POST','/api/contactos'); p.agregar(b.celular,'Ultimo'); respuesta(201) })
      p.contador().should('contain.text','11 de 15'); p.siguiente(); p.filas().should('have.length',1)
      p.anterior(); p.filas().should('have.length',10); ui('indicador-pagina').should('have.text','Página 1 de 2')
    })
  })
  caso('E2E-G4-110',['WEB-G4-02-CA1-01','WEB-G4-02-CA3-01'],'Favoritos primero, orden y nombre enmascarado',() => {
    lista(4,['Zeta','Beta','Alfa','Omega']).then(({a,otros,contactos}) => {
      api('PUT',`/api/contactos/${contactos[0].id}`,a,{favorito:true}); api('PUT',`/api/contactos/${contactos[3].id}`,a,{favorito:true})
      ingresar(a); p.abrir(); ui('contacto-alias').then(items => expect([...items].map(e=>e.textContent)).to.deep.eq(['Omega','Zeta','Alfa','Beta']))
      p.fila(contactos[0].id).find('[data-testid="contacto-detalle"]').should('contain.text',contactos[0].nombre).and('contain.text',otros[0].celular).and('not.contain.text',otros[0].nombres)
      p.fila(contactos[0].id).find('[data-testid="boton-favorito"]').should('have.attr','aria-pressed','true')
      p.fila(contactos[1].id).find('[data-testid="boton-favorito"]').should('have.attr','aria-pressed','false')
    })
  })
  caso('E2E-G4-111',['WEB-G4-02-CA2-01','WEB-G4-02-CA2-02'],'Búsqueda parcial sin mayúsculas/tildes, vacío y limpiar',() => {
    lista(2,['José oficina','Ana casa']).then(({a}) => {
      ingresar(a); p.abrir(); p.buscar('JOSE'); p.filas().should('have.length',1).and('contain.text','José oficina')
      p.buscar('OFIC'); p.filas().should('have.length',1).and('contain.text','José oficina')
      p.buscar('ZZZZ'); p.filas().should('not.exist'); ui('lista-vacia').should('contain.text','Ningún contacto')
      p.buscar(''); p.filas().should('have.length',2); p.contador().should('contain.text','2 de 15')
    })
  })
  caso('E2E-G4-112',['WEB-G4-03-CA1-01','WEB-G4-03-CA1-02'],'Editar sin duplicarse a sí mismo; límites, tilde y persistencia',() => {
    lista(1,['Ana']).then(({a,contactos:[c]}) => {
      ingresar(a); p.abrir(); observar('PUT',`/api/contactos/${c.id}`)
      cy.wrap(['Ana','A'.repeat(20),'José',' A1 B ']).each((alias: string) => {
        p.editar(c.id,alias); respuesta(200).its('alias').should('eq',alias.trim()); ui('dialogo-formulario').should('not.exist')
        p.fila(c.id).should('contain.text',alias.trim())
      })
      cy.reload(); p.fila(c.id).should('contain.text','A1 B')
    })
  })
  caso('E2E-G4-113',['WEB-G4-03-CA1-02'],'[D-01] ñ debe ser válida al editar',() => {
    lista(1).then(({a,contactos:[c]}) => { ingresar(a); p.abrir(); observar('PUT',`/api/contactos/${c.id}`); p.editar(c.id,'Niño'); respuesta(200); p.fila(c.id).should('contain.text','Niño') })
  })
  caso('E2E-G4-114',['WEB-G4-03-CA1-02'],'Edición inválida y duplicado por mayúsculas conservan datos',() => {
    lista(2,['Ana','Otro']).then(({a,contactos:[,c]}) => {
      ingresar(a); p.abrir(); observar('PUT',`/api/contactos/${c.id}`)
      cy.wrap(['','Lu','A'.repeat(21),'Ana@']).each((alias: string) => { p.editar(c.id,alias); respuesta(422,'ALIAS_INVALIDO'); ui('dialogo-error').should('be.visible'); cerrarDialogo(); p.fila(c.id).should('contain.text','Otro') })
      p.editar(c.id,'ANA'); respuesta(409,'ALIAS_DUPLICADO'); ui('dialogo-error').should('be.visible'); cerrarDialogo()
      cy.reload(); p.fila(c.id).should('contain.text','Otro')
    })
  })
  caso('E2E-G4-115',['WEB-G4-03-CA1-02'],'[D-02] alias duplicado con espacios al editar debe rechazarse',() => {
    lista(2,['Ana','Otro']).then(({a,contactos:[,c]}) => { ingresar(a); p.abrir(); observar('PUT',`/api/contactos/${c.id}`); p.editar(c.id,' Ana '); respuesta(409,'ALIAS_DUPLICADO'); p.fila(c.id).should('contain.text','Otro') })
  })
  caso('E2E-G4-116',['WEB-G4-03-CA1-03'],'Favoritos 5/6, desmarcar y persistencia',() => {
    lista(6).then(({a,contactos}) => {
      contactos.slice(0,4).forEach(c=>api('PUT',`/api/contactos/${c.id}`,a,{favorito:true}))
      ingresar(a); p.abrir(); observar('PUT','/api/contactos/*'); p.favorito(contactos[4].id); respuesta(200)
      p.fila(contactos[4].id).find('[data-testid="boton-favorito"]').should('have.attr','aria-pressed','true')
      p.favorito(contactos[5].id); respuesta(422,'LIMITE_FAVORITOS'); toast('5 contactos favoritos')
      p.fila(contactos[5].id).find('[data-testid="boton-favorito"]').should('have.attr','aria-pressed','false')
      p.favorito(contactos[4].id); respuesta(200); p.fila(contactos[4].id).find('[data-testid="boton-favorito"]').should('have.attr','aria-pressed','false')
      cy.reload(); api('GET','/api/contactos',a).then(r=>expect(r.contactos.filter((x:{favorito:boolean})=>x.favorito)).to.have.length(4))
    })
  })
  caso('E2E-G4-117',['WEB-G4-04-CA1-01','WEB-G4-04-CA1-02'],'Eliminar conserva la transferencia y su movimiento',() => {
    lista(1).then(({a,otros:[b],contactos:[c]}) => {
      saldo(a,'100.00'); api('POST','/api/transferencias',a,{contacto_id:c.id,monto:'10.00'},201).then(tx => {
        ingresar(a); p.abrir(); observar('DELETE',`/api/contactos/${c.id}`); p.eliminar(c.id); respuesta(204)
        p.filas().should('not.exist'); cy.reload(); p.contador().should('contain.text','0 de 15')
        api('GET',`/api/movimientos/${tx.codigo_operacion}`,a).its('monto').should('eq','10.00')
        api('GET',`/api/movimientos/${tx.codigo_operacion}`,b).its('monto').should('eq','10.00')
        cy.visit('/historial'); ui('tabla-movimientos').should('contain.text','10.00')
      })
    })
  })
  ;(['enviada','recibida'] as const).forEach((tipo,i) => {
    caso(`E2E-G4-${118+i}`,['WEB-G4-04-CA2-01'],`Bloquear eliminación con solicitud ${tipo}`,() => {
      lista(1).then(({a,otros:[b],contactos:[c]}) => {
        if(tipo==='enviada') pedir(a,c)
        else vincular(b,a).then(inverso=>pedir(b,inverso))
        ingresar(a); p.abrir(); observar('DELETE',`/api/contactos/${c.id}`); p.eliminar(c.id); respuesta(409,'SOLICITUDES_PENDIENTES'); toast()
        cy.reload(); p.fila(c.id).should('exist')
      })
    })
  })
  ;(['resuelta','vencida'] as const).forEach((tipo,i) => {
    caso(`E2E-G4-${120+i}`,['WEB-G4-04-CA2-02'],`Eliminar con solicitud ${tipo}`,() => {
      lista(1).then(({a,contactos:[c]}) => pedir(a,c).then(s => {
        if(tipo==='resuelta') api('POST',`/api/solicitudes/${s.id}/cancelar`,a)
        else { avanzar(2880); renovar(a) }
        ingresar(a); p.abrir(); observar('DELETE',`/api/contactos/${c.id}`); p.eliminar(c.id); respuesta(204)
        cy.reload(); p.filas().should('not.exist')
      }))
    })
  })
})
