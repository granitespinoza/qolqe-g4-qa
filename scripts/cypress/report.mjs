import { readFileSync } from 'node:fs'
import { spawn } from 'node:child_process'
import { pathToFileURL, fileURLToPath } from 'node:url'
import path from 'node:path'
process.chdir(path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..'))
const latest = JSON.parse(readFileSync('reports/cypress/latest.json', 'utf8'))
const file = path.resolve(latest.runDir, 'html/index.html')
console.log(file)
if (process.platform === 'win32') spawn('explorer.exe', [file], { windowsHide: true, detached: true, stdio: 'ignore' }).unref()
else console.log(pathToFileURL(file).href)
