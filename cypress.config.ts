import createBundler from '@bahmutov/cypress-esbuild-preprocessor'
import { addCucumberPreprocessorPlugin } from '@badeball/cypress-cucumber-preprocessor'
const { createEsbuildPlugin } = require('@badeball/cypress-cucumber-preprocessor/esbuild')
import { defineConfig } from 'cypress'
import fs from 'node:fs'
import path from 'node:path'

const runDir = process.env.CY_RUN_DIR || 'reports/cypress/interactive'
const demo = process.env.CY_DEMO
const images = process.env.QA_EVIDENCE === 'images'
export default defineConfig({
  ...(process.env.CYPRESS_PROJECT_ID ? { projectId: process.env.CYPRESS_PROJECT_ID } : {}),
  viewportWidth: 1280, viewportHeight: 800,
  video: process.env.CY_VIDEO === '1', screenshotOnRunFailure: images, trashAssetsBeforeRuns: false,
  screenshotsFolder: `${runDir}/screenshots`, videosFolder: `${runDir}/videos`,
  reporter: 'cypress-mochawesome-reporter',
  reporterOptions: { reportDir: `${runDir}/html`, reportFilename: 'index', embeddedScreenshots: images, inlineAssets: true, saveJson: true, charts: true },
  retries: 0,
  e2e: {
    baseUrl: 'http://127.0.0.1:8011', testIsolation: true,
    specPattern: demo === 'ai' ? 'tests/e2e/demos/contactos-ia.cy.ts' : demo === 'failure' ? 'tests/e2e/demos/evidencia-fallo.cy.ts' : process.env.CY_MODE === 'smoke' ? ['features/e2e/**/*.feature','features/smoke/**/*.feature'] : 'features/e2e/**/*.feature',
    supportFile: 'tests/e2e/support/e2e.ts',
    async setupNodeEvents(on, config) {
      const originalOn = on
      const listeners: Record<string, ((...args: any[]) => any)[]> = {}
      on = ((event: any, handler: any) => {
        if (typeof handler !== 'function') return originalOn(event, handler)
        if (!listeners[event]) {
          listeners[event] = []
          originalOn(event, (async (...args: any[]) => {
            let result: any
            for (const fn of listeners[event]) { const value = await fn(...args); if (value !== undefined) result = value }
            return result
          }) as any)
        }
        listeners[event].push(handler)
      }) as Cypress.PluginEvents
      config.expose = {...config.expose, gherkin: !demo, reportImages: images}
      await addCucumberPreprocessorPlugin(on, config)
      on('file:preprocessor', createBundler({plugins:[createEsbuildPlugin(config)]}))
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
