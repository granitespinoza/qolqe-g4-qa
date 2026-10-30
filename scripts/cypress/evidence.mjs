import { createHash } from 'node:crypto'
import { existsSync, readdirSync, readFileSync } from 'node:fs'
import path from 'node:path'

export function sourceFingerprint(root = process.cwd()) {
  const walk = dir => readdirSync(path.join(root,dir), { withFileTypes:true }).flatMap(e => e.isDirectory() ? walk(`${dir}/${e.name}`) : [`${dir}/${e.name}`])
  const files = [...walk('Web/cypress'), ...walk('scripts/cypress').filter(p=>/\.(mjs|py|txt)$/.test(p)),
    'cypress.config.ts','package.json','package-lock.json','tsconfig.json','requirements-lock.txt']
    .filter(p=>!p.includes('__pycache__')).sort()
  const hashes = Object.fromEntries(files.map(file=>[file,createHash('sha256').update(readFileSync(path.join(root,file))).digest('hex')]))
  return { hash:createHash('sha256').update(JSON.stringify(hashes)).digest('hex'), files:hashes }
}

export function readResults(runDir) {
  const folder = path.join(runDir,'results')
  const specs = existsSync(folder) ? readdirSync(folder).filter(f=>f.endsWith('.json')).map(f=>JSON.parse(readFileSync(path.join(folder,f),'utf8'))) : []
  const tests = specs.flatMap(s=>(s.tests||[]).map(t=>({...t,spec:s.spec})))
  const counts = { total:tests.length, passed:0, failed:0, pending:0, skipped:0 }
  for (const t of tests) if (t.state in counts && t.state!=='total') counts[t.state]++
  return { specs:specs.map(s=>s.spec), tests, counts, specErrors:specs.filter(s=>s.error).map(s=>({spec:s.spec,error:s.error})) }
}

export function stabilityVerdict(runs, expectedHash) {
  const signatures = runs.map(r=>r.tests.map(t=>`${t.spec}::${t.title.join(' ')}`).sort().join('\n'))
  const sameTests = signatures.length === 3 && Boolean(signatures[0]) && signatures.every(s=>s===signatures[0])
  const sameSources = runs.length === 3 && runs.every(r=>r.sourceFingerprint?.hash===expectedHash && r.endFingerprint===expectedHash)
  const completeSuite = runs.length === 3 && runs.every(r => r.expectedSpecs?.length > 0 && JSON.stringify([...r.specs].sort()) === JSON.stringify([...r.expectedSpecs].sort()))
  const sameEnvironment = runs.length === 3 && runs.every(r => r.revision === runs[0].revision && r.browser === runs[0].browser && r.sutRevision === runs[0].sutRevision && r.node === runs[0].node && JSON.stringify(r.runtime) === JSON.stringify(runs[0].runtime))
  const allPassed = runs.length === 3 && runs.every(r=>r.code===0 && r.counts.total>0 && r.counts.passed===r.counts.total && r.counts.failed===0 && r.counts.pending===0 && r.counts.skipped===0 && r.specErrors.length===0)
  return { sameTests, sameSources, completeSuite, sameEnvironment, allPassed, achieved: sameTests && sameSources && completeSuite && sameEnvironment && allPassed }
}
