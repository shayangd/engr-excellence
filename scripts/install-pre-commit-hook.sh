#!/bin/bash

# Script to install or reinstall the pre-commit hook

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

print_header "🔧 Pre-Commit Hook Installer"
echo "================================"
echo ""

# Check if hook already exists
HOOK_PATH=".git/hooks/pre-commit"
CONFIG_PATH=".git/hooks/pre-commit-config"

if [ -f "$HOOK_PATH" ]; then
    print_warning "Pre-commit hook already exists"
    echo ""
    echo "Options:"
    echo "  1. Backup existing and install new"
    echo "  2. Overwrite existing"
    echo "  3. Cancel installation"
    echo ""
    read -p "Choose option (1-3): " choice
    
    case $choice in
        1)
            backup_name="${HOOK_PATH}.backup.$(date +%Y%m%d_%H%M%S)"
            mv "$HOOK_PATH" "$backup_name"
            print_info "Existing hook backed up to: $backup_name"
            ;;
        2)
            print_info "Overwriting existing hook"
            ;;
        3)
            print_info "Installation cancelled"
            exit 0
            ;;
        *)
            print_error "Invalid choice"
            exit 1
            ;;
    esac
fi

# Create the hook script
print_info "Installing pre-commit hook..."

cat > "$HOOK_PATH" << 'EOF'
#!/bin/bash

# Pre-commit hook to prevent commits with more than 1000 lines of changes
# This hook counts the total number of lines added and deleted in staged changes

set -e

# Load configuration from config file if it exists
CONFIG_FILE="$(dirname "$0")/pre-commit-config"
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
fi

# Configuration (with defaults)
MAX_LINES=${MAX_LINES:-1000}
SHOW_DETAILED_STATS=${SHOW_DETAILED_STATS:-false}
COUNT_ADDITIONS_ONLY=${COUNT_ADDITIONS_ONLY:-false}
EXCLUDE_PATTERNS=${EXCLUDE_PATTERNS:-""}
ALLOW_BYPASS=${ALLOW_BYPASS:-true}
REJECTION_MESSAGE=${REJECTION_MESSAGE:-"Commit contains too many changes. Consider splitting into smaller commits."}
USE_COLORS=${USE_COLORS:-true}

# Color configuration
if [ "$USE_COLORS" = "true" ]; then
    RED='\033[0;31m'
    YELLOW='\033[1;33m'
    GREEN='\033[0;32m'
    NC='\033[0m' # No Color
else
    RED=''
    YELLOW=''
    GREEN=''
    NC=''
fi

# Function to print colored output
print_error() {
    echo -e "${RED}ERROR: $1${NC}" >&2
}

print_warning() {
    echo -e "${YELLOW}WARNING: $1${NC}" >&2
}

print_success() {
    echo -e "${GREEN}SUCCESS: $1${NC}" >&2
}

print_info() {
    echo -e "$1" >&2
}

# Check if this is an initial commit
if git rev-parse --verify HEAD >/dev/null 2>&1; then
    against=HEAD
else
    # Initial commit: diff against an empty tree object
    against=$(git hash-object -t tree /dev/null)
fi

# Get the list of staged files
staged_files=$(git diff --cached --name-only --diff-filter=ACMR)

if [ -z "$staged_files" ]; then
    print_warning "No staged files found. Nothing to commit."
    exit 0
fi

# Count lines added and deleted
lines_added=0
lines_deleted=0

# Get diff stats for staged changes
diff_stats=$(git diff --cached --numstat)

if [ -n "$diff_stats" ]; then
    while IFS=$'\t' read -r added deleted filename; do
        # Skip binary files (marked with -)
        if [ "$added" != "-" ] && [ "$deleted" != "-" ]; then
            # Check if file should be excluded
            should_exclude=false
            if [ -n "$EXCLUDE_PATTERNS" ]; then
                for pattern in $EXCLUDE_PATTERNS; do
                    if [[ "$filename" == $pattern ]]; then
                        should_exclude=true
                        break
                    fi
                done
            fi
            
            if [ "$should_exclude" = "false" ]; then
                lines_added=$((lines_added + added))
                if [ "$COUNT_ADDITIONS_ONLY" != "true" ]; then
                    lines_deleted=$((lines_deleted + deleted))
                fi
                
                # Show detailed stats if enabled
                if [ "$SHOW_DETAILED_STATS" = "true" ]; then
                    print_info "   $filename: +$added -$deleted"
                fi
            else
                if [ "$SHOW_DETAILED_STATS" = "true" ]; then
                    print_info "   $filename: excluded (matches pattern)"
                fi
            fi
        fi
    done <<< "$diff_stats"
fi

if [ "$COUNT_ADDITIONS_ONLY" = "true" ]; then
    total_lines=$lines_added
else
    total_lines=$((lines_added + lines_deleted))
fi

print_info ""
print_info "📊 Commit Statistics:"
print_info "   Lines added:   ${lines_added}"
print_info "   Lines deleted: ${lines_deleted}"
print_info "   Total changes: ${total_lines}"
print_info "   Limit:         ${MAX_LINES}"
print_info ""

# Check if the total exceeds the limit
if [ $total_lines -gt $MAX_LINES ]; then
    print_error "Commit rejected: Too many lines changed!"
    print_info ""
    print_info "$REJECTION_MESSAGE"
    print_info "Your commit contains ${total_lines} lines of changes, which exceeds the limit of ${MAX_LINES} lines."
    print_info ""
    print_info "💡 Suggestions:"
    print_info "   1. Split your changes into smaller, more focused commits"
    print_info "   2. Review if all changes are necessary for this commit"
    print_info "   3. Consider using 'git add -p' for partial staging"
    print_info ""
    print_info "🚨 To bypass this check (use with caution):"
    print_info "   git commit --no-verify"
    print_info ""
    exit 1
fi

print_success "Commit approved: ${total_lines} lines changed (within ${MAX_LINES} line limit)"
exit 0
EOF

# Make the hook executable
chmod +x "$HOOK_PATH"

# Create default configuration if it doesn't exist
if [ ! -f "$CONFIG_PATH" ]; then
    print_info "Creating default configuration..."
    
    cat > "$CONFIG_PATH" << 'EOF'
# Pre-commit hook configuration
# This file contains settings for the pre-commit hook

# Maximum number of lines allowed in a single commit (additions + deletions)
MAX_LINES=1000

# Whether to show detailed file-by-file statistics
SHOW_DETAILED_STATS=false

# Whether to count only additions (ignore deletions)
COUNT_ADDITIONS_ONLY=false

# File patterns to exclude from line counting (space-separated)
# Examples: "*.min.js *.bundle.* package-lock.json"
EXCLUDE_PATTERNS=""

# Whether to allow bypassing the hook with --no-verify
ALLOW_BYPASS=true

# Custom message for when commits are rejected
REJECTION_MESSAGE="Commit contains too many changes. Consider splitting into smaller commits."

# Whether to use colored output
USE_COLORS=true
EOF
fi

print_success "Pre-commit hook installed successfully!"
print_info ""
print_info "📋 What was installed:"
print_info "   • Hook script: $HOOK_PATH"
print_info "   • Configuration: $CONFIG_PATH"
print_info ""
print_info "🧪 Test the installation:"
print_info "   ./scripts/test-pre-commit-hook.sh"
print_info ""
print_info "⚙️  Customize settings:"
print_info "   Edit $CONFIG_PATH"
print_info ""
print_info "📚 Documentation:"
print_info "   See PRE_COMMIT_SETUP.md for usage guide"
print_info "   See docs/PRE_COMMIT_HOOKS.md for detailed docs"
print_info ""
print_success "Ready to use! The hook will run automatically on your next commit."
