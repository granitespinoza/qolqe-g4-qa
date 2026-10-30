@ignore
Feature: Disponibilidad explícita de una sesión recién emitida, sin repetir el login
Scenario:
  * def waitForSession =
  """
  function(token) {
    var observations = [];
    var started = Date.now();
    var ready = false;
    for (var attempt = 1; attempt <= 20 && Date.now() - started < 2000; attempt++) {
      var r = karate.call('classpath:API/features/support/http.feature', {
        route:'/api/cuentas/me/saldo', method:'GET', token:token
      });
      observations.push({attempt:attempt,status:r.statusCode,codigo:r.result.codigo || null});
      if (r.statusCode == 200) { ready = true; break; }
      if (r.statusCode != 401 || r.result.codigo != 'NO_AUTENTICADO' || r.result.detail != 'La sesión fue cerrada') {
        karate.embed(JSON.stringify({phase:'readiness-sesion',observations:observations}), 'application/json');
        karate.fail('Preparación: nueva sesión no consultable, respuesta inesperada ' + r.statusCode + ' ' + r.result.codigo);
      }
      karate.log('READINESS sesión recién emitida aún no visible; intento', attempt, 'de 20 (plazo 2000ms); siguiente sondeo en 25ms');
      if (attempt < 20) Java.type('java.lang.Thread').sleep(25);
    }
    if (observations.length > 1 || !ready) {
      karate.embed(JSON.stringify({phase:'readiness-sesion',max_attempts:20,deadline_ms:2000,elapsed_ms:Date.now()-started,interval_ms:25,observations:observations}), 'application/json');
    }
    if (!ready) karate.fail('READINESS agotado: token recién emitido 200 no tiene sesión visible; ver adjunto');
  }
  """
  * eval waitForSession(readyToken)
