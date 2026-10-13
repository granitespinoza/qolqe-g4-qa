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
    var login = karate.call(http, {route:'/api/auth/login',method:'POST',body:{celular:cell,pin:'4826'}});
    if (login.statusCode != 200) karate.fail('No se pudo autenticar contexto');
    return {cell:cell, token:login.result.access_token, id:reg.result.id};
  }
  """
  * def a = create('Granit Prueba')
  * def b = create('Franco Prueba')
  * def c = create('Tercero Prueba')
  * def add = function(cell, alias, token){ return karate.call(http, {route:'/api/contactos',method:'POST',token:token,body:{celular:cell,alias:alias}}); }
  * def requestMoney = function(id, amount, reason){ return karate.call(http, {route:'/api/solicitudes',method:'POST',token:a.token,body:{contacto_id:id,monto:amount,motivo:reason}}); }
  * def login = function(user){ return karate.call(http,{route:'/api/auth/login',method:'POST',body:{celular:user.cell,pin:'4826'}}).result.access_token; }
