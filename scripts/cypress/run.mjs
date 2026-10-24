import { spawn, spawnSync } from 'node:child_process'
import { existsSync, mkdirSync, writeFileSync, createWriteStream } from 'node:fs'
import { fileURLToPath } from 'node:url'
import path from 'node:path'
import net from 'node:net'
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..')
process.chdir(root)
const mode = process.argv[2] || 'regression'
if (!['open','smoke','regression','ai','ai-open','failure'].includes(mode)) throw new Error('Modo desconocido')
const major = Number(process.versions.node.split('.')[0])
if (![22,24].includes(major) && major < 26) throw new Error('Cypress 16 requiere Node 22, 24 o >=26. Usa Node 24 LTS.')
const python = process.env.QA_PYTHON || path.join(root, '.venv', process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python')
if (!existsSync(python)) throw new Error('Falta Python del proyecto. Ejecuta npm run cy:setup.')
// No reutilizamos servidores ajenos ni tocamos sus datos.
await new Promise((resolve, reject) => {
  const probe = net.createServer()
  probe.once('error', () => reject(new Error('Puerto 8011 ocupado. Cierra la ejecución Cypress anterior.')))
  probe.listen(8011, '127.0.0.1', () => probe.close(resolve))
})
const runDir = `reports/cypress/${new Date().toISOString().replace(/[:.]/g, '-')}-${mode}`
mkdirSync(runDir, { recursive: true })
const log = createWriteStream(`${runDir}/server.log`)
const server = spawn(python, ['scripts/cypress/server.py'], { cwd: root, windowsHide: true, stdio: ['ignore','pipe','pipe'] })
server.stdout.pipe(log); server.stderr.pipe(log)
let stopped = false
function stop() { if (!stopped) { stopped = true; server.kill(); log.end() } }
process.on('exit', stop)
process.on('SIGINT', () => { stop(); process.exit(130) })
process.on('SIGTERM', () => { stop(); process.exit(143) })
server.on('error', error => { console.error(error); process.exit(1) })
const started = Date.now()
let ready = false
while (Date.now() - started < 90000) {
  if (server.exitCode !== null) break
  try { const r = await fetch('http://127.0.0.1:8011/api/salud', { signal: AbortSignal.timeout(2000) }); if (r.ok) { ready = true; break } } catch {}
  await new Promise(resolve => setTimeout(resolve, 300)) // Sondeo de disponibilidad, no espera de UI.
}
if (!ready) { stop(); throw new Error(`Servidor no disponible. Revisa ${runDir}/server.log`) }
const interactive = ['open', 'ai-open'].includes(mode)
const args = [interactive ? 'open' : 'run', '--e2e', '--browser', process.env.CY_BROWSER || 'chrome']
if (mode === 'smoke') args.push('--spec', 'cypress/e2e/contactos-happy-path.cy.ts')
const env = { ...process.env, CY_RUN_DIR: runDir, CY_DEMO: mode.startsWith('ai') ? 'ai' : mode === 'failure' ? 'failure' : '' }
// El entorno del desktop puede heredar esta opción de Electron y romper Cypress.
delete env.ELECTRON_RUN_AS_NODE
const child = spawn(process.execPath, ['node_modules/cypress/bin/cypress', ...args], { env, stdio: 'inherit', windowsHide: !interactive })
child.on('error', error => { console.error(error); stop(); process.exit(1) })
const code = await new Promise(resolve => child.once('exit', code => resolve(code ?? 1)))
stop()
const revision = spawnSync('git', ['rev-parse','HEAD'], { encoding:'utf8', windowsHide:true }).stdout?.trim()
writeFileSync(`${runDir}/execution.json`, JSON.stringify({ mode, code, revision, started: new Date(started).toISOString(), ended: new Date().toISOString(), node: process.version, sutRevision: '8c7d2f0c939ede7765b7b80b98c10c3905693fda', aiVerification: mode.startsWith('ai') ? 'Consultar resultado real; requiere Cloud' : 'No ejecutada en este modo' }, null, 2))
if (!interactive) writeFileSync('reports/cypress/latest.json', JSON.stringify({ mode, code, runDir }, null, 2))
console.log(`\nEvidencia: ${runDir}\nReporte: ${runDir}/html/index.html`)
process.exitCode = Number(code)
