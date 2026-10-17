@ignore
Feature: Usuarios propios por escenario, sin mocks
Scenario:
  * def http = 'classpath:features/support/http.feature'
  * def clock = call read(http) { route: '/api/pruebas/reloj', method: 'DELETE' }
  * match clock.statusCode == 200
  * def random = function(){ return '' + Java.type('java.util.concurrent.ThreadLocalRandom').current().nextInt(10000000, 99999999); }
  * def create =
  """
  function(name) {
    var n = random();
    var cell = '9' + n;
    var reg = karate.call(http, { route: '/api/usuarios', method: 'POST', body: {dni:n, nombres:name, celular:cell, pin:'4826'} });
    if (reg.statusCode != 201) karate.fail('No se pudo crear contexto: ' + JSON.stringify(reg.result));
    // Readiness explícito del usuario: no repetir el registro ni acciones funcionales.
    var login;
    var observations = [];
    var started = Date.now();
    for (var attempt = 1; attempt <= 20 && Date.now() - started < 2000; attempt++) {
      login = karate.call(http, {route:'/api/auth/login',method:'POST',body:{celular:cell,pin:'4826'}});
      observations.push({attempt:attempt, status:login.statusCode, codigo:login.result.codigo || null});
      if (login.statusCode == 200) break;
      if (login.statusCode != 401 || login.result.codigo != 'CREDENCIALES_INVALIDAS') {
        karate.embed(JSON.stringify({phase:'readiness-usuario',observations:observations}), 'application/json');
        karate.fail('Preparación: login inesperado ' + login.statusCode + ' ' + login.result.codigo);
      }
      karate.log('READINESS usuario registrado aún no autenticable; intento', attempt, 'de 20 (plazo 2000ms); siguiente sondeo en 25ms');
      if (attempt < 20) Java.type('java.lang.Thread').sleep(25);
    }
    if (observations.length > 1 || login.statusCode != 200) {
      karate.embed(JSON.stringify({phase:'readiness-usuario',max_attempts:20,deadline_ms:2000,elapsed_ms:Date.now()-started,interval_ms:25,observations:observations}), 'application/json');
    }
    if (login.statusCode != 200) karate.fail('READINESS agotado: registro 201 no autentica con las mismas credenciales; ver adjunto');
    karate.call('classpath:features/support/session-ready.feature', {readyToken:login.result.access_token});
    return {cell:cell, token:login.result.access_token, id:reg.result.id};
  }
  """
  * def a = create('Granit Prueba')
  * def b = create('Franco Prueba')
  * def c = create('Tercero Prueba')
  * def add =
  """
  function(cell, alias, token) {
    var created = karate.call(http, {route:'/api/contactos',method:'POST',token:token,body:{celular:cell,alias:alias}});
    // El POST bajo prueba se ejecuta una sola vez y conserva exactamente su retorno.
    if (created.statusCode != 201) return created;
    var observations = [];
    var started = Date.now();
    var visible = false;
    for (var attempt = 1; attempt <= 20 && Date.now() - started < 2000; attempt++) {
      var listed = karate.call(http, {route:'/api/contactos',method:'GET',token:token,query:{pagina:1}});
      if (listed.statusCode != 200) {
        karate.embed(JSON.stringify({phase:'readiness-contacto',contact_id:created.result.id,status:listed.statusCode,observations:observations}), 'application/json');
        karate.fail('Preparación: consulta de visibilidad devolvió ' + listed.statusCode);
      }
      visible = listed.result.contactos.some(function(x){ return x.id == created.result.id; });
      // La capacidad es 15 y el contrato pagina de 10 en 10: mirar también página 2.
      if (!visible && listed.result.total_paginas > 1) {
        var second = karate.call(http, {route:'/api/contactos',method:'GET',token:token,query:{pagina:2}});
        if (second.statusCode != 200) karate.fail('Preparación: segunda página no consultable: ' + second.statusCode);
        visible = second.result.contactos.some(function(x){ return x.id == created.result.id; });
      }
      observations.push({attempt:attempt, status:listed.statusCode, visible:visible});
      if (visible) break;
      karate.log('READINESS contacto creado aún no visible; intento', attempt, 'de 20 (plazo 2000ms); siguiente sondeo en 25ms');
      if (attempt < 20) Java.type('java.lang.Thread').sleep(25);
    }
    if (observations.length > 1 || !visible) {
      karate.embed(JSON.stringify({phase:'readiness-contacto',contact_id:created.result.id,max_attempts:20,deadline_ms:2000,elapsed_ms:Date.now()-started,interval_ms:25,observations:observations}), 'application/json');
    }
    if (!visible) karate.fail('READINESS agotado: contacto creado 201 no visible por GET; ver adjunto');
    return created;
  }
  """
  * def requestMoney = function(id, amount, reason){ return karate.call(http, {route:'/api/solicitudes',method:'POST',token:a.token,body:{contacto_id:id,monto:amount,motivo:reason}}); }
  * def login =
  """
  function(user) {
    var r = karate.call(http,{route:'/api/auth/login',method:'POST',body:{celular:user.cell,pin:'4826'}});
    if (r.statusCode != 200) karate.fail('Preparación: renovación de sesión devolvió ' + r.statusCode);
    // Una sola emisión; el sondeo GET conserva exactamente el token original.
    karate.call('classpath:features/support/session-ready.feature', {readyToken:r.result.access_token});
    return r.result.access_token;
  }
  """
