<#
.SYNOPSIS
  Pulls ACC abstract data from the Congress Library for the tiering experiment.
  Run this on the VDI (congress-dev.merck.com is not reachable from the laptop).

  Step 1: Lists all congresses and finds ACC by name.
  Step 2: Fetches all abstracts for that congress.
  Step 3: Saves the full list + a summary to acc-abstracts.json / acc-abstracts-summary.txt.

  Copy acc-abstracts.json back to the laptop (OneDrive or git) and run
  build_tiering_pdf.py --input acc-abstracts.json to generate the tiering PDF.

.NOTES
  Run from the tiering_experiment folder:
    .\fetch-acc-abstracts.ps1

  Or specify a known congress ID directly:
    .\fetch-acc-abstracts.ps1 -CongressId "some-uuid-here"

  Uses the same header-role auth as the debrief engine's GET endpoints
  (no bearer token needed).
#>

param(
  [string]$CongressId = "",
  [string]$UserId = "oremland",
  [string]$CongressName = "ACC"
)

$ErrorActionPreference = "Stop"

# --- UTF-8 helpers (from debrief engine) ---
$Utf8NoBom = [System.Text.UTF8Encoding]::new($false)

function Write-Utf8([string]$Path, [string]$Text) {
  $full = if ([System.IO.Path]::IsPathRooted($Path)) { $Path }
          else { [System.IO.Path]::GetFullPath((Join-Path (Get-Location).ProviderPath $Path)) }
  [System.IO.File]::WriteAllText($full, $Text, $Utf8NoBom)
}

function Invoke-CurlUtf8([string[]]$CurlArgs) {
  $tmp = New-TemporaryFile
  try {
    $status = curl.exe -s -o $tmp.FullName -w "%{http_code}" @CurlArgs
    $body = [System.IO.File]::ReadAllText($tmp.FullName, [System.Text.Encoding]::UTF8)
  } finally {
    Remove-Item $tmp.FullName -ErrorAction SilentlyContinue
  }
  return [pscustomobject]@{ Status = ("$status").Trim(); Body = $body }
}

function Get-CongressJson([string]$Url) {
  $r = Invoke-CurlUtf8 @("-X", "GET", $Url, "-H", "x-user-id: $UserId", "-H", "x-user-role: Admin")
  if ($r.Status -ne "200") { throw "GET $Url returned HTTP $($r.Status): $($r.Body)" }
  return ($r.Body | ConvertFrom-Json)
}

$baseUrl = "https://congress-dev.merck.com/api"

# --- Step 1: Find the congress ID ---
if (-not $CongressId) {
  Write-Output "Fetching congress list to find '$CongressName'..."
  $response = Get-CongressJson "$baseUrl/summary/congresses"

  if ($response -is [System.Array]) { $list = $response }
  elseif ($response.congresses)     { $list = $response.congresses }
  elseif ($response.data)           { $list = $response.data }
  else                              { $list = @($response) }

  Write-Output "Total congresses in library: $($list.Count)"

  # Find matching congress (case-insensitive, partial match)
  $matches = $list | Where-Object { $_.name -match $CongressName }

  if ($matches.Count -eq 0) {
    Write-Output "`nNo congress matching '$CongressName'. Available congresses:"
    $list | Where-Object { $_.name -notmatch "test|TEST|crud" } |
      Select-Object name, congress_id, startDate, endDate, abstractCount |
      Sort-Object endDate -Descending |
      Format-Table -AutoSize
    exit 1
  }

  if ($matches.Count -gt 1) {
    Write-Output "`nMultiple congresses match '$CongressName':"
    $matches |
      Select-Object name, congress_id, startDate, endDate, abstractCount |
      Sort-Object endDate -Descending |
      Format-Table -AutoSize
    Write-Output "Pick one and re-run with: .\fetch-acc-abstracts.ps1 -CongressId '<id>'"
    Write-Output "(or add -CongressName to narrow, e.g. -CongressName 'ACC 2026')"
    exit 1
  }

  $congress = $matches[0]
  $CongressId = $congress.congress_id
  Write-Output "Found: $($congress.name) | ID: $CongressId | Abstracts: $($congress.abstractCount)"
} else {
  Write-Output "Using provided congress ID: $CongressId"
}

# --- Step 2: Fetch all abstracts ---
Write-Output "`nFetching abstracts for congress $CongressId..."
$response = Get-CongressJson "$baseUrl/database/abstracts_by_congress/$CongressId"

if ($response -is [System.Array]) { $abstracts = $response }
elseif ($response.abstracts)      { $abstracts = $response.abstracts }
elseif ($response.data)           { $abstracts = $response.data }
else                              { $abstracts = @($response) }

Write-Output "Retrieved $($abstracts.Count) abstracts"

# --- Step 3: Save ---
$jsonOut = $abstracts | ConvertTo-Json -Depth 10
Write-Utf8 "acc-abstracts.json" $jsonOut
Write-Output "Wrote acc-abstracts.json ($([math]::Round($jsonOut.Length / 1024))KB)"

# Quick summary
$summaryLines = @("ID | Title (first 80 chars)")
$summaryLines += @("---|---")
foreach ($a in $abstracts | Select-Object -First 50) {
  $id = if ($a.abstractNo) { $a.abstractNo } elseif ($a.id) { $a.id } else { "?" }
  $title = if ($a.title) { $a.title } else { "(no title)" }
  if ($title.Length -gt 80) { $title = $title.Substring(0, 80) + "..." }
  $summaryLines += "$id | $title"
}
if ($abstracts.Count -gt 50) { $summaryLines += "... and $($abstracts.Count - 50) more" }

Write-Utf8 "acc-abstracts-summary.txt" ($summaryLines -join "`n")
Write-Output "Wrote acc-abstracts-summary.txt (first 50 abstracts)"
Write-Output "`nDone. Copy acc-abstracts.json to the laptop and run:"
Write-Output "  python build_tiering_pdf.py --input acc-abstracts.json"
