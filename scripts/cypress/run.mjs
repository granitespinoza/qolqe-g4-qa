import { sourceFingerprint, readResults } from './evidence.mjs'
import { spawn, spawnSync } from 'node:child_process'
import { existsSync, mkdirSync, writeFileSync, createWriteStream, rmSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import path from 'node:path'
import net from 'node:net'
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..')
process.chdir(root)
const sutRevision = spawnSync('git',['-C','referencias/qolqe-wallet','rev-parse','HEAD'],{encoding:'utf8',windowsHide:true})
const sutState = spawnSync('git',['-C','referencias/qolqe-wallet','status','--porcelain'],{encoding:'utf8',windowsHide:true})
if(sutRevision.status!==0 || sutRevision.stdout.trim()!=='8c7d2f0c939ede7765b7b80b98c10c3905693fda' || sutState.status!==0 || sutState.stdout.trim()) throw new Error('La referencia debe estar limpia y en la versión fijada')
const source = sourceFingerprint(root)
const expectedSpecs = Object.keys(source.files).filter(f=>f.startsWith('Web/cypress/e2e/') && f.endsWith('.cy.ts'))
const mode = process.argv[2] || 'regression'
if (!['open','smoke','regression','ai','ai-open','failure'].includes(mode)) throw new Error('Modo desconocido')
const major = Number(process.versions.node.split('.')[0])
if (![22,24].includes(major) && major < 26) throw new Error('Cypress 16 requiere Node 22, 24 o >=26. Usa Node 24 LTS.')
const python = process.env.QA_PYTHON || path.join(root, '.venv', process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python')
if (!existsSync(python)) throw new Error('Falta Python del proyecto. Ejecuta npm run cy:setup.')
const runtimeProbe=spawnSync(python,['-c', 'import json,platform,importlib.metadata as m; print(json.dumps(dict(python=platform.python_version(),fastapi=m.version("fastapi"),starlette=m.version("starlette"))))'],{encoding:'utf8',windowsHide:true})
if(runtimeProbe.status!==0) throw new Error('No se pudo verificar el entorno Python de Cypress')
const runtime=JSON.parse(runtimeProbe.stdout)
// No reutilizamos servidores ajenos ni tocamos sus datos.
await new Promise((resolve, reject) => {
  const probe = net.createServer()
  probe.once('error', () => reject(new Error('Puerto 8011 ocupado. Cierra la ejecución Cypress anterior.')))
  probe.listen(8011, '127.0.0.1', () => probe.close(resolve))
})
const runDir = `reports/cypress/${new Date().toISOString().replace(/[:.]/g, '-')}-${mode}`
mkdirSync(runDir, { recursive: true })
const databaseRoot = path.resolve(root,'.tools','cypress-runs')
const databaseDir = path.resolve(databaseRoot,path.basename(runDir))
if (path.dirname(databaseDir)!==databaseRoot || existsSync(databaseDir)) throw new Error('Directorio temporal no exclusivo')
const log = createWriteStream(`${runDir}/server.log`)
const server = spawn(python, ['scripts/cypress/server.py'], { cwd: root, windowsHide: true, env: { ...process.env, CY_DATABASE_DIR: databaseDir }, stdio: ['ignore','pipe','pipe'] })
server.stdout.pipe(log,{end:false}); server.stderr.pipe(log,{end:false})
const serverClosed = new Promise(resolve => server.once('close',resolve))
let stopped = false
function stop() { if (!stopped) { stopped = true; server.kill() } }
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
if (mode === 'smoke') args.push('--spec', 'Web/cypress/e2e/contactos-happy-path.cy.ts')
const env = { ...process.env, CY_RUN_DIR: runDir, CY_DEMO: mode.startsWith('ai') ? 'ai' : mode === 'failure' ? 'failure' : '' }
// El entorno del desktop puede heredar esta opción de Electron y romper Cypress.
delete env.ELECTRON_RUN_AS_NODE
const child = spawn(process.execPath, ['node_modules/cypress/bin/cypress', ...args], { env, stdio: 'inherit', windowsHide: !interactive })
child.on('error', error => { console.error(error); stop(); process.exit(1) })
const code = await new Promise(resolve => child.once('exit', code => resolve(code ?? 1)))
stop()
await serverClosed
log.end()
let databaseRemoved = false
if (process.env.CY_KEEP_DB !== '1') {
  try { rmSync(databaseDir,{recursive:true,force:true,maxRetries:5,retryDelay:200}); databaseRemoved=true }
  catch(error) { console.warn('No se pudo retirar la base temporal:',error.message) }
}
const revision = spawnSync('git', ['rev-parse','HEAD'], { encoding:'utf8', windowsHide:true }).stdout?.trim()
writeFileSync(`${runDir}/execution.json`, JSON.stringify({ mode, code, revision, expectedSpecs, runtime, databaseRemoved, videoEnabled: process.env.CY_VIDEO==='1', pipelineUrl: process.env.GITHUB_ACTIONS ? `https://github.com/${process.env.GITHUB_REPOSITORY}/actions/runs/${process.env.GITHUB_RUN_ID}` : null, browser: process.env.CY_BROWSER || 'chrome', worktreeDirty: Boolean(spawnSync('git',['status','--porcelain'],{encoding:'utf8',windowsHide:true}).stdout?.trim()), sourceFingerprint: source, endFingerprint: sourceFingerprint(root).hash, ...readResults(runDir), started: new Date(started).toISOString(), ended: new Date().toISOString(), node: process.version, sutRevision: '8c7d2f0c939ede7765b7b80b98c10c3905693fda', aiVerification: mode.startsWith('ai') ? 'Consultar resultado real; requiere Cloud' : 'No ejecutada en este modo' }, null, 2))
if (!interactive) writeFileSync('reports/cypress/latest.json', JSON.stringify({ mode, code, runDir }, null, 2))
console.log(`\nEvidencia: ${runDir}\nReporte: ${runDir}/html/index.html`)
process.exitCode = Number(code)
