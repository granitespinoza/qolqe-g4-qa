import { defineConfig } from 'cypress'
import fs from 'node:fs'
import path from 'node:path'

const runDir = process.env.CY_RUN_DIR || 'reports/cypress/interactive'
const demo = process.env.CY_DEMO
export default defineConfig({
  ...(process.env.CYPRESS_PROJECT_ID ? { projectId: process.env.CYPRESS_PROJECT_ID } : {}),
  viewportWidth: 1280, viewportHeight: 800,
  video: process.env.CY_VIDEO === '1', screenshotOnRunFailure: true, trashAssetsBeforeRuns: false,
  screenshotsFolder: `${runDir}/screenshots`, videosFolder: `${runDir}/videos`,
  reporter: 'cypress-mochawesome-reporter',
  reporterOptions: { reportDir: `${runDir}/html`, reportFilename: 'index', embeddedScreenshots: true, inlineAssets: true, saveJson: true, charts: true },
  retries: 0,
  e2e: {
    baseUrl: 'http://127.0.0.1:8011', testIsolation: true,
    specPattern: demo === 'ai' ? 'Web/cypress/demos/contactos-ia.cy.ts' : demo === 'failure' ? 'Web/cypress/demos/evidencia-fallo.cy.ts' : 'Web/cypress/e2e/**/*.cy.ts',
    supportFile: 'Web/cypress/support/e2e.ts',
    setupNodeEvents(on, config) {
      require('cypress-mochawesome-reporter/plugin')(on)
      on('after:spec', (_spec, results) => {
        const output = path.join(runDir, 'results')
        fs.mkdirSync(output, { recursive: true })
        fs.writeFileSync(path.join(output, `${path.basename(_spec.relative)}.json`), JSON.stringify({
          spec: _spec.relative.replace(/\\/g, '/'),
          tests: results?.tests.map(t => ({ title: t.title, state: t.state, error: t.displayError,
            attempts: t.attempts.map(a => ({ state: a.state, error: (a as {error?: {message?: string}}).error?.message || null })) })) || [],
          error: results?.error || null,
        }, null, 2))
        if (results?.video && !results.tests.some(t => t.attempts.some(a => a.state === 'failed'))) {
          const file = path.resolve(results.video)
          const videoRoot = path.resolve(config.videosFolder) + path.sep
          if (!file.startsWith(videoRoot)) throw new Error('Video fuera del directorio permitido')
          if (fs.existsSync(file)) fs.unlinkSync(file)
        }
      })
      return config
    },
  },
})
