import { test } from 'node:test'
import assert from 'node:assert/strict'
import { stabilityVerdict } from './evidence.mjs'
const run=()=>({code:0,expectedSpecs:['a'],specs:['a'],revision:'head',browser:'electron',sutRevision:'sut',sourceFingerprint:{hash:'same'},endFingerprint:'same',specErrors:[],tests:[{spec:'a',title:['A']}],counts:{total:1,passed:1,failed:0,pending:0,skipped:0}})
test('requires three full successful executions of identical sources and cases',()=>assert.equal(stabilityVerdict([run(),run(),run()],'same').achieved,true))
test('repeated failures do not count as stability achieved',()=>{const a=run();a.code=1;a.counts.failed=1;a.counts.passed=0;assert.equal(stabilityVerdict([a,a,a],'same').achieved,false)})
test('rejects changed sources, skipped tests, empty suites and only two runs',()=>{
 for(const mutate of [r=>r.endFingerprint='changed',r=>r.counts.skipped=1,r=>r.counts.total=0,r=>r.tests[0].title=['different']]) {const a=run();mutate(a);assert.equal(stabilityVerdict([run(),a,run()],'same').achieved,false)}
 assert.equal(stabilityVerdict([run(),run()],'same').achieved,false)
})

test('rejects the same incomplete subset three times',()=>{const a=run();a.expectedSpecs=['a','b'];assert.equal(stabilityVerdict([a,a,a],'same').achieved,false)})
