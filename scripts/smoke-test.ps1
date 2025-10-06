# Smoke test for Akij MonitorX (PowerShell)
# - Starts the Node server in background
# - Runs the agent once to send metrics
# - Hits /api/metrics and exits

param()

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

Write-Host "Starting smoke test..." -ForegroundColor Cyan

# Start node server in background using Start-Process
$serverProcess = Start-Process -FilePath "node" -ArgumentList "src/server.js" -NoNewWindow -PassThru
Start-Sleep -Seconds 2

# Run agent once (we'll run agent script and stop it quickly)
Write-Host "Running agent to send a batch of metrics..." -ForegroundColor Cyan
$agentProcess = Start-Process -FilePath "node" -ArgumentList "src/agent.js" -NoNewWindow -PassThru
Start-Sleep -Seconds 4

# Attempt to fetch metrics
try {
    $resp = Invoke-RestMethod -Uri http://localhost:3000/api/metrics -Method GET -TimeoutSec 5
    Write-Host "API /api/metrics response:" -ForegroundColor Green
    $resp | ConvertTo-Json -Depth 4 | Write-Host
    $success = $true
} catch {
    Write-Host "Failed to get /api/metrics:" -ForegroundColor Red
    Write-Host $_.Exception.Message
    $success = $false
}

# Clean up started processes
if ($agentProcess -and !$agentProcess.HasExited) {
    $agentProcess.Kill()
}

if ($serverProcess -and !$serverProcess.HasExited) {
    $serverProcess.Kill()
}

if ($success) {
    Write-Host "Smoke test succeeded." -ForegroundColor Green
    exit 0
} else {
    Write-Host "Smoke test failed." -ForegroundColor Red
    exit 1
}
