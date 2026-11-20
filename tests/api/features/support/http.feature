@ignore
Feature: Adaptador HTTP compartido
Scenario:
  Given url baseUrl
  And path route
  And header Authorization = karate.get('token') ? 'Bearer ' + token : null
  And request karate.get('body', null)
  And params karate.get('query', {})
  When method method
  * def result = response
  * def statusCode = responseStatus
