import { spawn, spawnSync } from 'node:child_process'
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import path from 'node:path'
import { sourceFingerprint, stabilityVerdict } from './evidence.mjs'

process.chdir(path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..'))
const dir=`reports/cypress/stability-${new Date().toISOString().replace(/[:.]/g,'-')}`
mkdirSync(dir,{recursive:true})
const fingerprint=sourceFingerprint(), runs=[]
let active
process.on('SIGINT',()=>{active?.kill();process.exit(130)})
process.on('SIGTERM',()=>{active?.kill();process.exit(143)})
for(let i=1;i<=3;i++) {
  if(sourceFingerprint().hash!==fingerprint.hash) throw new Error('Cambió el código durante la secuencia; iniciar otra secuencia completa.')
  console.log(`\nESTABILIDAD: ejecución ${i}/3 de la regresión completa, sin reintentos.`)
  const started=Date.now()
  active=spawn(process.execPath,['scripts/cypress/run.mjs','regression'],{stdio:'inherit',windowsHide:true,env:process.env})
  const code=await new Promise((resolve,reject)=>{active.once('error',reject);active.once('exit',c=>resolve(c??1))})
  const latest=JSON.parse(readFileSync('reports/cypress/latest.json','utf8'))
  const run=JSON.parse(readFileSync(`${latest.runDir}/execution.json`,'utf8'))
  if(run.mode!=='regression'||Date.parse(run.started)<started-1000) throw new Error('No se recibió evidencia nueva de la suite completa')
  runs.push({...run,code,runDir:latest.runDir})
  writeFileSync(`${dir}/stability.json`,JSON.stringify({completed:runs.length,required:3,sourceFingerprint:fingerprint,runs,verdict:stabilityVerdict(runs,fingerprint.hash)},null,2))
  console.log(`Corrida ${i}: ${JSON.stringify(run.counts)}`)
}
const verdict=stabilityVerdict(runs,fingerprint.hash)
const result={completed:3,required:3,sourceFingerprint:fingerprint,runs,verdict,
  revision:spawnSync('git',['rev-parse','HEAD'],{encoding:'utf8',windowsHide:true}).stdout.trim(),
  note:'Los defectos conocidos siguen siendo FAIL. Tres resultados iguales no equivalen a tres aprobaciones.'}
writeFileSync(`${dir}/stability.json`,JSON.stringify(result,null,2))
writeFileSync('reports/cypress/latest-stability.json',JSON.stringify({dir,verdict},null,2))
console.log(`\nEstabilidad: ${verdict.achieved?'3/3 APROBADAS':'NO CUMPLIDA'}\nEvidencia: ${dir}/stability.json`)
process.exitCode=verdict.achieved?0:1
