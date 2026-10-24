import { defineConfig } from 'cypress'
import fs from 'node:fs'
import path from 'node:path'

const runDir = process.env.CY_RUN_DIR || 'reports/cypress/interactive'
const demo = process.env.CY_DEMO
export default defineConfig({
  ...(process.env.CYPRESS_PROJECT_ID ? { projectId: process.env.CYPRESS_PROJECT_ID } : {}),
  viewportWidth: 1280, viewportHeight: 800,
  video: true, screenshotOnRunFailure: true, trashAssetsBeforeRuns: false,
  screenshotsFolder: `${runDir}/screenshots`, videosFolder: `${runDir}/videos`,
  reporter: 'cypress-mochawesome-reporter',
  reporterOptions: { reportDir: `${runDir}/html`, reportFilename: 'index', embeddedScreenshots: true, inlineAssets: true, saveJson: true, charts: true },
  retries: 0,
  e2e: {
    baseUrl: 'http://127.0.0.1:8011', testIsolation: true,
    specPattern: demo === 'ai' ? 'cypress/demos/contactos-ia.cy.ts' : demo === 'failure' ? 'cypress/demos/evidencia-fallo.cy.ts' : 'cypress/e2e/**/*.cy.ts',
    supportFile: 'cypress/support/e2e.ts',
    setupNodeEvents(on, config) {
      require('cypress-mochawesome-reporter/plugin')(on)
      on('after:spec', (_spec, results) => {
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
