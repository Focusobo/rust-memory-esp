# rust-memory-esp user installer
# Run from an elevated PowerShell on Windows 10/11.
param(
    [string]$InstallDir = "$env:LOCALAPPDATA\rust-memory-esp",
    [string]$PythonExe  = "python"
)

Write-Host "[*] Installing rust-memory-esp into $InstallDir"
New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
Copy-Item -Recurse -Force .\src\*        $InstallDir
Copy-Item -Force .\offsets\offsets.json  $InstallDir
Copy-Item -Recurse -Force .\config\*     $InstallDir

Push-Location $InstallDir
& $PythonExe -m venv .venv
& "$InstallDir\.venv\Scripts\python.exe" -m pip install --upgrade pip
& "$InstallDir\.venv\Scripts\python.exe" -m pip install -r requirements.txt
Pop-Location

Write-Host "[+] Done. Launch with:"
Write-Host "    $InstallDir\.venv\Scripts\python.exe -m esp_app.bootstrap"