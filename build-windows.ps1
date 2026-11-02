$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $projectRoot '.venv\Scripts\python.exe'

Push-Location $projectRoot
try {
    if (-not (Test-Path -LiteralPath $python)) {
        & py -3.12 -m venv .venv
        if ($LASTEXITCODE -ne 0) {
            if (Get-Command uv -ErrorAction SilentlyContinue) {
                & uv venv --python 3.12 .venv
                if ($LASTEXITCODE -ne 0) {
                    throw 'Could not create the Python 3.12 virtual environment with uv.'
                }
            }
            else {
                throw 'Could not create a Python 3.12 virtual environment. Install Python 3.12 or uv, then retry.'
            }
        }
    }

    if (Get-Command uv -ErrorAction SilentlyContinue) {
        & uv pip install --python $python -r requirements.txt pyinstaller
    }
    else {
        & $python -m pip install --upgrade pip
        if ($LASTEXITCODE -ne 0) {
            throw 'Could not install or upgrade pip.'
        }
        & $python -m pip install -r requirements.txt pyinstaller
    }
    if ($LASTEXITCODE -ne 0) {
        throw 'Could not install the project and build dependencies.'
    }

    & $python -m PyInstaller --noconfirm --clean --onefile --name MiniAIAssistant --collect-all speech_recognition --collect-all pyaudio --collect-all pyttsx3 --hidden-import pyttsx3.drivers.sapi5 (Join-Path $projectRoot 'main.py')
    if ($LASTEXITCODE -ne 0) {
        throw 'PyInstaller failed to build MiniAIAssistant.exe.'
    }

    Write-Output (Join-Path $projectRoot 'dist\MiniAIAssistant.exe')
}
finally {
    Pop-Location
}

