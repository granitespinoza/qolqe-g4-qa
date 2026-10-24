import { spawnSync } from 'node:child_process'
import { existsSync, mkdirSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import path from 'node:path'
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..')
process.chdir(root)
const revision = '8c7d2f0c939ede7765b7b80b98c10c3905693fda'
function run(command, args) {
  const r = spawnSync(command, args, { stdio: 'inherit', windowsHide: true })
  if (r.error || r.status !== 0) throw r.error || new Error(`${command} falló (${r.status})`)
}
mkdirSync('referencias', { recursive: true })
if (!existsSync('referencias/qolqe-wallet/.git')) run('git', ['clone', 'https://github.com/cjudihtroj/qolqe-wallet.git', 'referencias/qolqe-wallet'])
const git = spawnSync('git', ['-C', 'referencias/qolqe-wallet', 'rev-parse', 'HEAD'], { encoding: 'utf8', windowsHide: true })
if (git.status !== 0) throw new Error('No se pudo identificar la revisión de Qolqe')
if (git.stdout.trim() !== revision) {
  const state = spawnSync('git', ['-C', 'referencias/qolqe-wallet', 'status', '--porcelain'], { encoding: 'utf8', windowsHide: true })
  if (state.status !== 0 || state.stdout.trim()) throw new Error('Referencia con cambios: revisar antes de cambiar de revisión')
  run('git', ['-C', 'referencias/qolqe-wallet', 'checkout', '--detach', revision])
}
const python = path.join(root, '.venv', process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python')
if (!existsSync(python)) {
  if (process.env.QA_PYTHON) run(process.env.QA_PYTHON, ['-m', 'venv', '.venv'])
  else if (process.platform === 'win32') run('py', ['-3.12', '-m', 'venv', '.venv'])
  else run('python3', ['-m', 'venv', '.venv'])
}
run(python, ['-m', 'pip', 'install', '-r', 'scripts/cypress/requirements.txt'])
console.log('Preparado. npm run cy:smoke inicia y detiene su propio servidor.')
