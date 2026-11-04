(() => {
  const $ = (id) => document.getElementById(id)
  const route = [...document.querySelectorAll('.route a')]
  const stages = route.map((link) => $(link.hash.slice(1)))
  const dialogs = [...document.querySelectorAll('dialog')]
  const motion = matchMedia('(prefers-reduced-motion: reduce)')
  let current = 0
  let animation

  function animate(elements, distance = 12) {
    animation?.revert()
    if (!motion.matches && window.gsap) {
      animation = window.gsap.context(() => {
        window.gsap.fromTo(elements, { opacity: 0, x: distance },
          { opacity: 1, x: 0, duration: .22, stagger: .035, ease: 'power2.out', clearProps: 'opacity,transform' })
      })
    }
  }

  motion.addEventListener('change', () => { if (motion.matches) animation?.revert() })

  function navigate(index, { focus = true, updateURL = true } = {}) {
    if (!stages[index]) return
    const direction = Math.sign(index - current)
    current = index
    stages.forEach((stage, i) => { stage.hidden = i !== index })
    route.forEach((link, i) => {
      if (i === index) {
        link.setAttribute('aria-current', 'step')
        link.dataset.visited = ''
      } else link.removeAttribute('aria-current')
    })
    $('position').textContent = `${String(index + 1).padStart(2, '0')} / ${String(stages.length).padStart(2, '0')}`
    $('previous').disabled = index === 0
    $('next').disabled = index === stages.length - 1
    if (updateURL && location.hash !== route[index].hash) history.pushState(null, '', route[index].hash)
    if (focus) {
      stages[index].querySelector('h1').focus({ preventScroll: true })
      if (document.fullscreenElement) $('portal').scrollTop = 0
      else window.scrollTo(0, 0)
    }
    if (direction) animate(stages[index], direction * 16)
  }

  function syncRoute(focus = true) {
    const index = route.findIndex((link) => link.hash === location.hash)
    navigate(index < 0 ? 0 : index, { focus, updateURL: false })
  }

  window.addEventListener('popstate', () => syncRoute())
  window.addEventListener('hashchange', () => {
    if (route[current].hash !== location.hash) syncRoute()
  })
  $('previous').onclick = () => navigate(current - 1)
  $('next').onclick = () => navigate(current + 1)
  document.addEventListener('keydown', (event) => {
    if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey ||
      event.target.closest('input, select, textarea, [contenteditable="true"]') ||
      dialogs.some((dialog) => dialog.open)) return
    if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
      event.preventDefault()
      navigate(current + (event.key === 'ArrowRight' ? 1 : -1))
    }
  })

  const tools = {
    contract: ['Esquema OpenAPI', 'Peticiones generadas y comprobaciones', 'Petición, respuesta y señal de contrato', 'Una señal generada necesita revisión antes de clasificarla como defecto.'],
    api: ['Regla y datos del caso', 'Aserciones de respuesta, estado y efectos', 'Escenario con esperado y resultado real', 'El equipo diseña los casos y prepara su contexto.'],
    web: ['Recorrido y datos de prueba', 'Interfaz real, respuesta de API y persistencia', 'Resultado del caso y reporte de ejecución', 'Los selectores identifican controles y las aserciones esperan el estado requerido.']
  }
  document.querySelectorAll('[data-tool]').forEach((button) => button.addEventListener('click', () => {
    document.querySelectorAll('[data-tool]').forEach((b) => b.setAttribute('aria-pressed', String(b === button)))
    const values = tools[button.dataset.tool]
    const fields = ['tool-input', 'tool-check', 'tool-output', 'tool-note']
    fields.forEach((id, i) => { $(id).textContent = values[i] })
    animate($('tool-flow').children, 8)
  }))

  document.querySelectorAll('[data-case]').forEach((button) => button.addEventListener('click', () => {
    const index = Number(button.dataset.case)
    document.querySelectorAll('[data-case]').forEach((b) => b.setAttribute('aria-pressed', String(b === button)))
    const panels = [...document.querySelectorAll('.case-panel')]
    panels.forEach((panel, i) => { panel.hidden = index !== i })
    animate(panels[index])
  }))

  const rows = [...document.querySelectorAll('#matrix tbody tr')]
  const pageSize = 8
  let page = 0
  function filter(reset = false) {
    if (reset) page = 0
    const query = $('search').value.trim().toLocaleLowerCase('es')
    const state = $('state').value
    const matches = rows.filter((r) => r.textContent.toLocaleLowerCase('es').includes(query) && (!state || r.dataset.state.startsWith(state)))
    const pages = Math.max(1, Math.ceil(matches.length / pageSize))
    page = Math.max(0, Math.min(page, pages - 1))
    const visible = new Set(matches.slice(page * pageSize, (page + 1) * pageSize))
    rows.forEach((row) => { row.hidden = !visible.has(row) })
    $('match-count').textContent = `${matches.length} coincidencias · Página ${page + 1} de ${pages}`
    $('matrix-previous').disabled = page === 0
    $('matrix-next').disabled = page + 1 >= pages
  }
  $('search').oninput = () => filter(true)
  $('state').onchange = () => filter(true)
  $('matrix-previous').onclick = () => { page--; filter() }
  $('matrix-next').onclick = () => { page++; filter() }

  function openPanel(name, query) {
    const panel = $(name)
    if (panel.open) return
    if (name === 'matrix') {
      if (query !== undefined) {
        $('search').value = query
        $('state').value = ''
      }
      filter(query !== undefined)
    }
    panel.showModal()
  }

  document.addEventListener('click', (event) => {
    const button = event.target.closest('[data-open]')
    if (button) return openPanel(button.dataset.open, button.dataset.query)
    const run = event.target.closest('[data-run]')
    if (run) {
      const content = $(run.dataset.run).content.cloneNode(true)
      const time = content.querySelector('time')
      const date = new Date(time.dateTime)
      if (!Number.isNaN(date.valueOf())) {
        time.textContent = new Intl.DateTimeFormat('es-PE', { dateStyle: 'medium', timeStyle: 'medium', timeZone: 'America/Lima' }).format(date) + ' (Lima)'
      }
      $('run-content').replaceChildren(content)
      return openPanel('run-detail')
    }
    const link = event.target.closest('a[href^="#"]')
    if (link && !event.metaKey && !event.ctrlKey && !event.shiftKey && !event.altKey) {
      const index = route.findIndex((item) => item.hash === link.hash)
      if (index >= 0) {
        event.preventDefault()
        navigate(index)
      }
    }
  })

  if (document.fullscreenEnabled && $('portal').requestFullscreen) {
    $('fullscreen').hidden = false
    $('fullscreen').onclick = async () => {
      try {
        if (document.fullscreenElement) await document.exitFullscreen()
        else await $('portal').requestFullscreen()
      } catch {
        $('fullscreen').textContent = 'Pantalla completa no disponible'
      }
    }
    document.addEventListener('fullscreenchange', () => {
      $('fullscreen').textContent = document.fullscreenElement ? 'Salir de pantalla completa' : 'Pantalla completa'
    })
  }
  syncRoute(false)
  if (location.hash === '#matriz') openPanel('matrix')
  if (location.hash === '#reportes') openPanel('reports')
})()
