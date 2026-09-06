# ---------------------------------------------------------------------------
# pluginkey.ps1 -- commercial-plugin key + signing helper (marketplace side).
#
# One keypair per plugin (the developer keeps the private key; the public key
# is shipped INSIDE the package as plugin.pub and its SHA-256 fingerprint is
# pinned in the marketplace listing). zanc and the IDE never trust a package
# whose payload signature does not verify against plugin.pub.
#
#   keygen : scripts/pluginkey.ps1 keygen -Dir <dir> [-Bits 2048]
#            -> <dir>/plugin.key (private, PKCS#8 PEM) + <dir>/plugin.pub
#   sign   : scripts/pluginkey.ps1 sign -Dir <dir> -Pkg <package-dir>
#            -> hashes every payload file into plugin.manifest, signs it
#               into <package-dir>/plugin.sig
#   verify : scripts/pluginkey.ps1 verify -Pkg <package-dir> [-Pub <pem>]
#            -> recompute manifest + verify plugin.sig with plugin.pub
#
# Payload message = manifest text (sorted "sha256  relpath" lines, LF):
# the signature covers the manifest (zan.pkg incl. plugin_id) AND every
# stdlib source file, so neither can be edited without invalidating it.
# ---------------------------------------------------------------------------
param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Cmd,
    [string]$Dir,
    [string]$Pkg,
    [string]$Pub,
    [int]$Bits = 2048
)
$ErrorActionPreference = "Stop"

function ManifestText([string]$pkgDir) {
    $lines = @()
    $full = (Resolve-Path -LiteralPath $pkgDir).Path
    Get-ChildItem -LiteralPath $pkgDir -Recurse -File |
        Where-Object { $_.Name -notin @("plugin.sig") } |
        ForEach-Object {
            $rel = $_.FullName.Substring($full.Length).Replace("\", "/").TrimStart("/")
            $h = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLower()
            $lines += ("{0}  {1}" -f $h, $rel)
        }
    $lines = $lines | Sort-Object
    return ($lines -join "`n") + "`n"
}

switch ($Cmd) {
    "keygen" {
        if (-not $Dir) { Write-Error "keygen needs -Dir"; exit 1 }
        New-Item -ItemType Directory -Force -Path $Dir | Out-Null
        & openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:$Bits `
            -out (Join-Path $Dir "plugin.key") 2>$null
        & openssl pkey -in (Join-Path $Dir "plugin.key") -pubout `
            -out (Join-Path $Dir "plugin.pub")
        if ($LASTEXITCODE -ne 0) { Write-Error "openssl failed"; exit 1 }
        Write-Output ("KEYGEN_OK " + (Join-Path $Dir "plugin.key") + " + plugin.pub")
    }
    "sign" {
        if (-not $Dir -or -not $Pkg) { Write-Error "sign needs -Dir (key) and -Pkg (package dir)"; exit 1 }
        $manifest = ManifestText $Pkg
        $tmp = [IO.Path]::GetTempFileName()
        [IO.File]::WriteAllText($tmp, $manifest)
        $sigFile = Join-Path $Pkg "plugin.sig"
        & openssl dgst -sha256 -sign (Join-Path $Dir "plugin.key") `
            -out $sigFile $tmp 2>$null
        if ($LASTEXITCODE -ne 0) { Remove-Item $tmp; Write-Error "openssl sign failed"; exit 1 }
        Remove-Item $tmp
        Write-Output ("SIGN_OK " + $sigFile + " bytes=" + (Get-Item $sigFile).Length)
    }
    "verify" {
        if (-not $Pkg) { Write-Error "verify needs -Pkg"; exit 1 }
        $pub = if ($Pub) { $Pub } else { Join-Path $Pkg "plugin.pub" }
        $manifest = ManifestText $Pkg
        $tmp = [IO.Path]::GetTempFileName()
        [IO.File]::WriteAllText($tmp, $manifest)
        & openssl dgst -sha256 -verify $pub -signature (Join-Path $Pkg "plugin.sig") $tmp
        $code = $LASTEXITCODE
        Remove-Item $tmp
        exit $code
    }
    default { Write-Error "unknown command: $Cmd (keygen|sign|verify)"; exit 1 }
}
