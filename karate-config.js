function fn() {
  return { baseUrl: karate.properties['baseUrl'] || 'http://127.0.0.1:8000', qaPython: karate.properties['qaPython'] || 'python' };
}
