Write-Host "Smoke test: backend health"
$baseUrl = $env:BASE_URL
if (-not $baseUrl) { $baseUrl = "http://localhost:8000" }
try {
  $health = Invoke-RestMethod "$baseUrl/api/health"
  Write-Host "Health:" ($health | ConvertTo-Json -Compress)
} catch {
  Write-Host "Health check failed:" $_
}

Write-Host "Smoke test: archive weeks (may fail if not configured)"
try {
  $archive = Invoke-RestMethod "$baseUrl/api/archive/weeks"
  Write-Host "Archive weeks:" ($archive | ConvertTo-Json -Compress)
} catch {
  Write-Host "Archive weeks failed:" $_
}
