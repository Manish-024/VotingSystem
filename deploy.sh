#!/bin/bash

# Blockchain Voting System - Render Deployment Script
# This script prepares and deploys your application to Render

echo "=========================================="
echo "  Blockchain Voting System Deployment"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if git is initialized
if [ ! -d .git ]; then
    echo -e "${YELLOW}📦 Initializing git repository...${NC}"
    git init
    echo -e "${GREEN}✓ Git initialized${NC}"
else
    echo -e "${GREEN}✓ Git repository already exists${NC}"
fi

# Check git status
echo ""
echo -e "${BLUE}📋 Checking git status...${NC}"
git status --short

# Add all files
echo ""
echo -e "${YELLOW}📦 Adding files to git...${NC}"
git add .
echo -e "${GREEN}✓ Files added${NC}"

# Commit changes
echo ""
echo -e "${YELLOW}💾 Committing changes...${NC}"
COMMIT_MSG="${1:-Deploy Blockchain Voting System to Render}"
git commit -m "$COMMIT_MSG" || echo -e "${YELLOW}⚠️  No changes to commit${NC}"

# Check if remote exists
echo ""
REMOTE_URL=$(git remote get-url origin 2>/dev/null)
if [ -z "$REMOTE_URL" ]; then
    echo -e "${RED}⚠️  No git remote configured!${NC}"
    echo ""
    echo -e "${YELLOW}Please add your GitHub repository:${NC}"
    echo -e "  ${BLUE}git remote add origin https://github.com/Manish-024/VotingSystem.git${NC}"
    echo ""
    echo -e "${YELLOW}Then run this script again.${NC}"
    exit 1
else
    echo -e "${GREEN}✓ Git remote: ${REMOTE_URL}${NC}"
fi

# Push to GitHub
echo ""
echo -e "${YELLOW}🚀 Pushing to GitHub...${NC}"
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Successfully pushed to GitHub!${NC}"
else
    echo -e "${RED}✗ Failed to push to GitHub${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}=========================================="
echo "  ✅ Deployment Preparation Complete!"
echo -e "==========================================${NC}"
echo ""
echo -e "${BLUE}📝 Next Steps:${NC}"
echo ""
echo "1. Go to Render Dashboard:"
echo -e "   ${BLUE}https://dashboard.render.com/${NC}"
echo ""
echo "2. Click 'New +' → 'Web Service'"
echo ""
echo "3. Connect your GitHub repository:"
echo -e "   ${BLUE}Manish-024/VotingSystem${NC}"
echo ""
echo "4. Configure:"
echo "   - Name: blockchain-voting-system"
echo "   - Runtime: Python 3"
echo "   - Build: pip install -r requirements.txt"
echo "   - Start: gunicorn app:app"
echo ""
echo "5. Click 'Create Web Service'"
echo ""
echo -e "${GREEN}Your app will be live in 3-5 minutes! 🎉${NC}"
echo ""
echo -e "${YELLOW}📖 For detailed guide, see: RENDER_DEPLOYMENT.md${NC}"
echo ""
