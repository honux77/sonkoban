# run.ps1 - openMSX로 소코반 실행

$openMSX = "C:\Program Files\openMSX\openmsx.exe"
$gameDir  = Join-Path $PSScriptRoot "disk\sokoban.dsk"
$machine  = "Boosted_MSX2+_JP"
# $machine  = "Sony_HB-F1XDJ"          # 소니 MSX2+
# $machine  = "Panasonic_FS-A1WSX"     # 파나소닉 MSX2+
# $machine  = "Panasonic_FS-A1GT"      # 파나소닉 turboR GT
# $machine  = "Panasonic_FS-A1ST"      # 파나소닉 turboR ST

if (-not (Test-Path $openMSX)) {
    Write-Error "openMSX를 찾을 수 없습니다: $openMSX"
    exit 1
}

# 게임 디스크 이미지 생성
python .\scripts\build_sokoban_dsk.py

Write-Host "openMSX 실행 중... (기계: $machine)"
Write-Host "디스크: $gameDir"

& $openMSX -machine $machine -diska $gameDir
