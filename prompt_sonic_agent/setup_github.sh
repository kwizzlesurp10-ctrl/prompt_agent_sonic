#!/bin/bash
# GitHub Repository Setup Script
# Run this after creating the repository on GitHub

# Usage: ./setup_github.sh YOUR_USERNAME [REPO_NAME]

if [ -z "$1" ]; then
    echo "Usage: ./setup_github.sh YOUR_USERNAME [REPO_NAME]"
    echo "Example: ./setup_github.sh myusername prompt-sonic-agent"
    exit 1
fi

GITHUB_USERNAME=$1
REPO_NAME=${2:-"prompt-sonic-agent"}

echo "Setting up GitHub remote..."

# Add remote origin
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

# Rename branch to main (GitHub default)
git branch -M main

# Push to GitHub
echo "Pushing to GitHub..."
git push -u origin main

echo ""
echo "Repository successfully connected to GitHub!"
echo "Repository URL: https://github.com/$GITHUB_USERNAME/$REPO_NAME"

