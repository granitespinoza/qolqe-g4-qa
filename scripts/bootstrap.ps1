$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
New-Item -ItemType Directory -Force .tools,reports | Out-Null
if (!(Test-Path referencias/qolqe-wallet/.git)) {
    git clone https://github.com/cjudihtroj/qolqe-wallet.git referencias/qolqe-wallet
}
git -C referencias/qolqe-wallet checkout 8c7d2f0c939ede7765b7b80b98c10c3905693fda
if (!(Test-Path .venv)) { python -m venv .venv }
& ./.venv/Scripts/python.exe -m pip install -r requirements-lock.txt
if ($LASTEXITCODE -ne 0) { throw "No se pudo instalar el entorno QA fijado" }
& ./.venv/Scripts/python.exe -m pip check
if ($LASTEXITCODE -ne 0) { throw "Dependencias incompatibles" }
if (!(Test-Path .tools/karate.jar)) {
    Invoke-WebRequest https://github.com/karatelabs/karate/releases/download/v1.5.2/karate-1.5.2.jar -OutFile .tools/karate.jar
}
if (!(Get-Command java -ErrorAction SilentlyContinue) -and !(Test-Path .tools/java)) {
    Invoke-WebRequest https://api.adoptium.net/v3/binary/latest/17/ga/windows/x64/jre/hotspot/normal/eclipse -OutFile .tools/jre.zip
    Expand-Archive -LiteralPath .tools/jre.zip -DestinationPath .tools/java
}
Write-Output 'Entorno preparado. Terminal 1: ./.venv/Scripts/python.exe scripts/serve_api.py'
Write-Output 'Terminal 2: ./.venv/Scripts/python.exe scripts/run_qa.py karate'
