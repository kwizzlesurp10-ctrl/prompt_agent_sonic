# GitHub Repository Setup Script
# Run this after creating the repository on GitHub

param(
    [Parameter(Mandatory=$true)]
    [string]$GitHubUsername,
    
    [Parameter(Mandatory=$false)]
    [string]$RepoName = "prompt-sonic-agent"
)

Write-Host "Setting up GitHub remote..." -ForegroundColor Green

# Add remote origin
$remoteUrl = "https://github.com/$GitHubUsername/$RepoName.git"
git remote add origin $remoteUrl

# Rename branch to main (GitHub default)
git branch -M main

# Push to GitHub
Write-Host "Pushing to GitHub..." -ForegroundColor Green
git push -u origin main

Write-Host "`nRepository successfully connected to GitHub!" -ForegroundColor Green
Write-Host "Repository URL: $remoteUrl" -ForegroundColor Cyan

