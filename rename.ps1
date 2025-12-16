# 1. Go to the target folder
$folderPath = "C:\Users\Jacob\Videos\MiniFRC event data\MiniFRC 11.5"
Set-Location -Path $folderPath

# 2. Get all JPG files
$files = Get-ChildItem -Filter "*.JPG"

Write-Host "Found $($files.Count) files to rename..." -ForegroundColor Cyan

# 3. Loop through each file and force the rename
foreach ($file in $files) {
    # Define names
    $originalName = $file.Name
    $tempName     = $file.Name + ".temp"
    $finalName    = $file.Name -replace '\.JPG$','.jpg'

    # Step A: Rename to intermediate temp name
    Rename-Item -Path $originalName -NewName $tempName

    # Step B: Rename to final lowercase name
    Rename-Item -Path $tempName -NewName $finalName
    
    Write-Host "Renamed: $originalName -> $finalName" -ForegroundColor Gray
}

Write-Host "All done! Press any key to close." -ForegroundColor Green
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")