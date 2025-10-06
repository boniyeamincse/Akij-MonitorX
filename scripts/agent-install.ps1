<#
Agent installer for Windows (PowerShell)
Copies files to ProgramFiles and creates a scheduled task to run the agent at startup.
#>

param()

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$installDir = "$env:ProgramFiles\AkijMonitorXAgent"

Write-Host "Installing agent to $installDir"
New-Item -ItemType Directory -Path $installDir -Force | Out-Null
Copy-Item -Path "$projectRoot\*" -Destination $installDir -Recurse -Force

# Create scheduled task to run agent at startup
$action = New-ScheduledTaskAction -Execute "node" -Argument "$installDir\src\agent.js"
$trigger = New-ScheduledTaskTrigger -AtStartup
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "AkijMonitorXAgent" -Description "Akij MonitorX Agent" -User "SYSTEM" -RunLevel Highest -Force

Write-Host "Agent installed. Task 'AkijMonitorXAgent' created."
