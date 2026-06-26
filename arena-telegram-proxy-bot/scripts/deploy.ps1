param(
    [string]$HostAlias = "arena-vps",
    [string]$RemoteDir = "/opt/arena-telegram-proxy-bot"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot

Push-Location $ProjectRoot
try {
    $archive = Join-Path $env:TEMP "arena-telegram-proxy-bot.tar"
    if (Test-Path $archive) {
        Remove-Item $archive -Force
    }

    tar --exclude=.git --exclude=.venv --exclude=sessions --exclude=logs -cf $archive .
    ssh $HostAlias "mkdir -p '$RemoteDir'"
    scp $archive "$HostAlias`:/tmp/arena-telegram-proxy-bot.tar"
    ssh $HostAlias "tar -xf /tmp/arena-telegram-proxy-bot.tar -C '$RemoteDir' && rm /tmp/arena-telegram-proxy-bot.tar"
}
finally {
    Pop-Location
}
