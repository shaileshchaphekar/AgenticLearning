# Auto-sync script for pushing changes to remote repository
$repoPath = 'c:\Users\shailesh.chaphekar\OneDrive - Accenture\AgenticLearning'

Set-Location $repoPath

# Get current branch
$currentBranch = git rev-parse --abbrev-ref HEAD

Write-Host "📤 Syncing branch: $currentBranch"

# Stage and commit any changes
$status = git status --porcelain

if ($status) {
    Write-Host "📝 Changes detected. Creating commit..."
    git add .
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    git commit -m "Auto-sync: $timestamp"
    Write-Host "✅ Committed changes"
} else {
    Write-Host "✨ No changes to commit"
}

# Push to remote
Write-Host "🚀 Pushing to remote..."
git push origin $currentBranch

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Sync completed successfully!"
} else {
    Write-Host "❌ Sync failed. Please check your connection."
}
