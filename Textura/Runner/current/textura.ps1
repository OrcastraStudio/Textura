[CmdletBinding(PositionalBinding=$false)]
param([Parameter(ValueFromRemainingArguments=$true)][string[]]$TexturaArguments)
$ErrorActionPreference = 'Stop'
$texturaPython = $env:TEXTURA_PYTHON
if (-not $texturaPython) {
    $texturaCommand = Get-Command python -ErrorAction SilentlyContinue
    if ($texturaCommand) { $texturaPython = $texturaCommand.Source }
}
if (-not $texturaPython) { throw 'Python 3.11 or newer is required. Set TEXTURA_PYTHON to its executable path.' }
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONUTF8 = '1'
& $texturaPython (Join-Path $PSScriptRoot 'textura.py') @TexturaArguments
exit $LASTEXITCODE
