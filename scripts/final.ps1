param([ValidateSet('audit','report','images','open','web','api','kiwi')][string]$Action='open')
$ErrorActionPreference='Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
$pythonFinal = Join-Path $PWD '.venv/Scripts/python.exe'
if (!(Test-Path -LiteralPath $pythonFinal)) { throw 'Preparar .venv: ver README.' }
switch ($Action) {
  audit { & $pythonFinal scripts/final_delivery.py audit }
  report { & $pythonFinal scripts/final_delivery.py report --evidence none }
  images { $env:QA_EVIDENCE='images'; & $pythonFinal scripts/final_delivery.py report --evidence images }
  web { & $pythonFinal scripts/ci_run.py web }
  api { & $pythonFinal scripts/ci_run.py api }
  kiwi { & $pythonFinal scripts/kiwi_sync.py }
  open { Start-Process 'http://localhost:8765/apidoc/final/' }
}
if ($LASTEXITCODE -ne 0 -and $Action -ne 'open') { exit $LASTEXITCODE }
