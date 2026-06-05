$ProcessedDir = "D:\IBM SKILLS BUILD 2026 BEMYAPP\decisionlens-wc2026\data\processed"
$ChunkSize = 1000
$Overlap = 200

Write-Output "[+] Launching sliding-window text parsing engine..."

# Target both processed files
$Files = @("laws_of_the_game_parsed.txt", "var_protocol_parsed.txt")

foreach ($FileName in $Files) {
    $FilePath = Join-Path $ProcessedDir $FileName
    if (-not (Test-Path $FilePath)) { continue }
    
    Write-Output "    -> Slicing document structures for: $FileName"
    $RawText = Get-Content $FilePath -Raw
    
    # Simple whitespace split to approximate word bounds safely
    $Words = $RawText -split '\s+'
    $TotalWords = $Words.Length
    
    $CurrentIndex = 0
    $ChunkCount = 0
    $OutputChunks = @()
    
    while ($CurrentIndex -lt $TotalWords) {
        # Determine sliding boundaries
        $EndIndex = [Math]::Min($CurrentIndex + $ChunkSize, $TotalWords)
        $ChunkSlice = $Words[$CurrentIndex..($EndIndex - 1)] -join " "
        
        $ChunkCount++
        $OutputChunks += "--- CHUNK $ChunkCount ---`n$ChunkSlice`n"
        
        # Advance index by step count minus overlap bounds
        $CurrentIndex += ($ChunkSize - $Overlap)
    }
    
    # Save sliced chunks
    $OutPath = $FilePath.Replace("_parsed.txt", "_chunks.txt")
    Set-Content -Path $OutPath -Value ($OutputChunks -join "`n") -Encoding utf8
    Write-Output "[+] Created $ChunkCount context chunks saved to: $OutPath"
}
