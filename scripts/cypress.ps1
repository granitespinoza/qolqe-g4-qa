param([ValidateSet('install','setup','open','smoke','regression','ai','ai-open','failure','typecheck','report')][string]$Action = 'smoke')
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
$nodeCy = (Get-Command node -ErrorAction SilentlyContinue).Source
$bundledCy = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe'
if (!$nodeCy -or [int]((& $nodeCy -p 'parseInt(process.versions.node)')) -lt 22) {
    if (Test-Path -LiteralPath $bundledCy) { $nodeCy = $bundledCy }
    else { throw 'Instala Node.js 24 LTS y vuelve a abrir PowerShell.' }
}
$majorCy = [int](& $nodeCy -p 'parseInt(process.versions.node)')
if ($majorCy -notin @(22,24) -and $majorCy -lt 26) { throw 'Usa Node.js 24 LTS.' }
$env:PATH = (Split-Path $nodeCy) + ';' + $env:PATH
$gitBundledCy = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd'
if (Test-Path -LiteralPath $gitBundledCy) { $env:PATH = $gitBundledCy + ';' + $env:PATH }
Write-Host "Node: $(& $nodeCy --version) | Accion: $Action"
switch ($Action) {
    'install' {
        $npmCy = (Get-Command npm.cmd -ErrorAction Stop).Source
        $npmCliCy = Join-Path (Split-Path $npmCy) 'node_modules\npm\bin\npm-cli.js'
        if (!(Test-Path -LiteralPath $npmCliCy)) { throw 'No se encontró npm-cli.js. Instala Node.js 24 LTS con npm.' }
        & $nodeCy $npmCliCy ci --no-audit --no-fund
    }
    'setup' { & $nodeCy scripts/cypress/setup.mjs }
    'typecheck' { & $nodeCy node_modules/typescript/bin/tsc --noEmit }
    'report' { & $nodeCy scripts/cypress/report.mjs }
    default { & $nodeCy scripts/cypress/run.mjs $Action }
}
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

