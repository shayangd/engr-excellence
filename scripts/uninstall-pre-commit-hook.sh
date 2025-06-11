#!/bin/bash

# Script to uninstall the pre-commit hook

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_error() {
    echo -e "${RED}ERROR: $1${NC}" >&2
}

print_success() {
    echo -e "${GREEN}SUCCESS: $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}WARNING: $1${NC}"
}

print_info() {
    echo -e "${BLUE}INFO: $1${NC}"
}

print_header() {
    echo -e "${BLUE}$1${NC}"
}

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    print_error "Not in a git repository"
    exit 1
fi

print_header "🗑️  Pre-Commit Hook Uninstaller"
echo "=================================="
echo ""

HOOK_PATH=".git/hooks/pre-commit"
CONFIG_PATH=".git/hooks/pre-commit-config"
PYTHON_HOOK_PATH=".git/hooks/pre-commit.py"

# Check what exists
hook_exists=false
config_exists=false
python_hook_exists=false

if [ -f "$HOOK_PATH" ]; then
    hook_exists=true
fi

if [ -f "$CONFIG_PATH" ]; then
    config_exists=true
fi

if [ -f "$PYTHON_HOOK_PATH" ]; then
    python_hook_exists=true
fi

if [ "$hook_exists" = "false" ] && [ "$config_exists" = "false" ] && [ "$python_hook_exists" = "false" ]; then
    print_warning "No pre-commit hook found to uninstall"
    exit 0
fi

print_info "Found the following files:"
if [ "$hook_exists" = "true" ]; then
    echo "  ✓ $HOOK_PATH"
fi
if [ "$config_exists" = "true" ]; then
    echo "  ✓ $CONFIG_PATH"
fi
if [ "$python_hook_exists" = "true" ]; then
    echo "  ✓ $PYTHON_HOOK_PATH"
fi
echo ""

echo "Uninstall options:"
echo "  1. Remove hook but keep configuration"
echo "  2. Remove everything (hook + configuration)"
echo "  3. Backup and remove everything"
echo "  4. Cancel"
echo ""
read -p "Choose option (1-4): " choice

case $choice in
    1)
        print_info "Removing hook but keeping configuration..."
        if [ "$hook_exists" = "true" ]; then
            rm "$HOOK_PATH"
            print_success "Removed $HOOK_PATH"
        fi
        if [ "$python_hook_exists" = "true" ]; then
            rm "$PYTHON_HOOK_PATH"
            print_success "Removed $PYTHON_HOOK_PATH"
        fi
        print_info "Configuration preserved at $CONFIG_PATH"
        ;;
    2)
        print_info "Removing all pre-commit hook files..."
        if [ "$hook_exists" = "true" ]; then
            rm "$HOOK_PATH"
            print_success "Removed $HOOK_PATH"
        fi
        if [ "$config_exists" = "true" ]; then
            rm "$CONFIG_PATH"
            print_success "Removed $CONFIG_PATH"
        fi
        if [ "$python_hook_exists" = "true" ]; then
            rm "$PYTHON_HOOK_PATH"
            print_success "Removed $PYTHON_HOOK_PATH"
        fi
        ;;
    3)
        backup_dir=".git/hooks/backup_$(date +%Y%m%d_%H%M%S)"
        mkdir -p "$backup_dir"
        print_info "Creating backup in $backup_dir..."
        
        if [ "$hook_exists" = "true" ]; then
            cp "$HOOK_PATH" "$backup_dir/"
            rm "$HOOK_PATH"
            print_success "Backed up and removed $HOOK_PATH"
        fi
        if [ "$config_exists" = "true" ]; then
            cp "$CONFIG_PATH" "$backup_dir/"
            rm "$CONFIG_PATH"
            print_success "Backed up and removed $CONFIG_PATH"
        fi
        if [ "$python_hook_exists" = "true" ]; then
            cp "$PYTHON_HOOK_PATH" "$backup_dir/"
            rm "$PYTHON_HOOK_PATH"
            print_success "Backed up and removed $PYTHON_HOOK_PATH"
        fi
        print_info "Backup created at: $backup_dir"
        ;;
    4)
        print_info "Uninstall cancelled"
        exit 0
        ;;
    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac

print_success "Pre-commit hook uninstalled successfully!"
print_info ""
print_info "📋 What happened:"
print_info "   • Pre-commit hook is no longer active"
print_info "   • Commits will no longer be checked for line limits"
print_info ""
print_info "🔄 To reinstall:"
print_info "   ./scripts/install-pre-commit-hook.sh"
print_info ""
print_success "Done!"
