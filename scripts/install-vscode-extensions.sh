#!/bin/bash
# VSCode Extensions Quick Install Script
# Instaluje wszystkie rekomendowane rozszerzenia dla NovaHouse Chatbot

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   VSCode Extensions Installer - NovaHouse Chatbot        ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if code command exists
if ! command -v code &> /dev/null; then
    echo -e "${YELLOW}⚠️  'code' command not found!${NC}"
    echo ""
    echo "Please install VSCode command line tools:"
    echo "  1. Open VSCode"
    echo "  2. Press Cmd+Shift+P (Mac) or Ctrl+Shift+P (Windows)"
    echo "  3. Type 'shell command'"
    echo "  4. Select 'Install code command in PATH'"
    echo ""
    exit 1
fi

echo -e "${BLUE}📦 Installing Essential Extensions...${NC}"
echo ""

# Essential Extensions
declare -a ESSENTIAL=(
    "ms-python.python"
    "ms-python.vscode-pylance"
    "ms-python.black-formatter"
    "ms-python.flake8"
    "ms-azuretools.vscode-docker"
    "eamodio.gitlens"
)

echo -e "${GREEN}🔥 ESSENTIAL (6 extensions)${NC}"
for ext in "${ESSENTIAL[@]}"; do
    echo -n "  Installing $ext... "
    if code --install-extension "$ext" --force &> /dev/null; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${YELLOW}(already installed or failed)${NC}"
    fi
done

echo ""
echo -e "${BLUE}📦 Installing High Priority Extensions...${NC}"
echo ""

# High Priority Extensions
declare -a HIGH_PRIORITY=(
    "usernamehw.errorlens"
    "gruntfuggly.todo-tree"
    "aaron-bond.better-comments"
    "redhat.vscode-yaml"
    "editorconfig.editorconfig"
)

echo -e "${GREEN}⭐ HIGH PRIORITY (5 extensions)${NC}"
for ext in "${HIGH_PRIORITY[@]}"; do
    echo -n "  Installing $ext... "
    if code --install-extension "$ext" --force &> /dev/null; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${YELLOW}(already installed or failed)${NC}"
    fi
done

echo ""
echo -e "${BLUE}📦 Installing Documentation Extensions...${NC}"
echo ""

# Documentation Extensions
declare -a DOCS=(
    "yzhang.markdown-all-in-one"
    "davidanson.vscode-markdownlint"
    "streetsidesoftware.code-spell-checker"
)

echo -e "${GREEN}📚 DOCUMENTATION (3 extensions)${NC}"
for ext in "${DOCS[@]}"; do
    echo -n "  Installing $ext... "
    if code --install-extension "$ext" --force &> /dev/null; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${YELLOW}(already installed or failed)${NC}"
    fi
done

echo ""
echo -e "${BLUE}📦 Installing Development Tools...${NC}"
echo ""

# Development Tools
declare -a DEV_TOOLS=(
    "littlefoxteam.vscode-python-test-adapter"
    "humao.rest-client"
    "njpwerner.autodocstring"
    "cweijan.vscode-database-client2"
)

echo -e "${GREEN}🔧 DEV TOOLS (4 extensions)${NC}"
for ext in "${DEV_TOOLS[@]}"; do
    echo -n "  Installing $ext... "
    if code --install-extension "$ext" --force &> /dev/null; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${YELLOW}(already installed or failed)${NC}"
    fi
done

echo ""
echo -e "${BLUE}📦 Installing UI Enhancements...${NC}"
echo ""

# UI Enhancements
declare -a UI=(
    "pkief.material-icon-theme"
    "oderwat.indent-rainbow"
)

echo -e "${GREEN}🎨 UI ENHANCEMENTS (2 extensions)${NC}"
for ext in "${UI[@]}"; do
    echo -n "  Installing $ext... "
    if code --install-extension "$ext" --force &> /dev/null; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${YELLOW}(already installed or failed)${NC}"
    fi
done

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Installation Complete!${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Optional: GitHub Copilot
echo -e "${YELLOW}🤖 OPTIONAL: GitHub Copilot${NC}"
echo ""
echo "GitHub Copilot is a game-changer but requires a subscription."
echo "Cost: \$10/month (FREE for students with GitHub Student Pack)"
echo ""
read -p "Install GitHub Copilot? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -n "  Installing github.copilot... "
    if code --install-extension "github.copilot" --force &> /dev/null; then
        echo -e "${GREEN}✓${NC}"
    fi
    
    echo -n "  Installing github.copilot-chat... "
    if code --install-extension "github.copilot-chat" --force &> /dev/null; then
        echo -e "${GREEN}✓${NC}"
    fi
    
    echo ""
    echo -e "${GREEN}✅ Copilot installed! Sign in when VSCode prompts.${NC}"
fi

echo ""
echo -e "${BLUE}📊 Summary${NC}"
echo ""
echo "  Essential: 6 extensions"
echo "  High Priority: 5 extensions"
echo "  Documentation: 3 extensions"
echo "  Dev Tools: 4 extensions"
echo "  UI: 2 extensions"
echo "  ────────────────────"
echo "  Total: 20 extensions"
echo ""
echo -e "${GREEN}🎉 All done! Restart VSCode to activate all extensions.${NC}"
echo ""
echo "📖 See VSCODE_EXTENSIONS.md for detailed extension guide."
echo ""
