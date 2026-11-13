param([ValidateSet('install','referencia','demo','carga','campana','estres','all','report','open')][string]$Action='demo')
$ErrorActionPreference='Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
$perfPython = Join-Path $PWD '.venv\Scripts\python.exe'
if (!(Test-Path -LiteralPath $perfPython)) { throw 'Primero prepara el entorno Python del proyecto en .venv.' }
if ($Action -eq 'install') {
    & $perfPython -m pip install -r tests/performance/requirements.txt
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    $perfTools = Join-Path $PWD '.tools\performance'
    New-Item -ItemType Directory -Force -Path $perfTools | Out-Null
    $perfZip = Join-Path $perfTools 'k6-v2.4.0.zip'
    Invoke-WebRequest 'https://github.com/grafana/k6/releases/download/v2.4.0/k6-v2.4.0-windows-amd64.zip' -OutFile $perfZip
    Expand-Archive -LiteralPath $perfZip -DestinationPath $perfTools -Force
} elseif ($Action -eq 'report') {
    & $perfPython tests/performance/scripts/generar_reportes.py
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} elseif ($Action -eq 'open') {
    $perfIndex = Join-Path $PWD 'tests\performance\resultados\index.html'
    if (!(Test-Path -LiteralPath $perfIndex)) { throw 'Primero ejecuta la acción report.' }
    Start-Process $perfIndex
} else {
    & $perfPython tests/performance/scripts/performance.py $Action
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    & $perfPython tests/performance/scripts/generar_reportes.py
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
