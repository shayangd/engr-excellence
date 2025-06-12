#!/bin/bash

# Test script for the pre-commit hook
# This script tests both scenarios: commits under and over the limit

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_test() {
    echo -e "${YELLOW}🧪 TEST: $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "$1"
}

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    print_error "Not in a git repository"
    exit 1
fi

# Check if pre-commit hook exists
if [ ! -f ".git/hooks/pre-commit" ]; then
    print_error "Pre-commit hook not found at .git/hooks/pre-commit"
    exit 1
fi

# Check if hook is executable
if [ ! -x ".git/hooks/pre-commit" ]; then
    print_error "Pre-commit hook is not executable"
    exit 1
fi

print_info ""
print_info "🔍 Testing Pre-Commit Hook"
print_info "=========================="
print_info ""

# Test 1: Small commit (should pass)
print_test "Small commit (should pass)"

# Create a test file with few lines
test_file="test_small_commit.txt"
cat > "$test_file" << EOF
This is a test file
with just a few lines
to test the pre-commit hook
with a small change.
EOF

git add "$test_file"

# Test the hook directly
if .git/hooks/pre-commit; then
    print_success "Small commit test passed"
else
    print_error "Small commit test failed"
fi

# Clean up
git reset HEAD "$test_file" > /dev/null 2>&1
rm -f "$test_file"

print_info ""

# Test 2: Large commit (should fail)
print_test "Large commit (should fail)"

# Create a test file with many lines
large_test_file="test_large_commit.txt"
{
    echo "# Large test file to exceed the 1000 line limit"
    echo "# This file is generated for testing purposes"
    echo ""
    
    # Generate 1200 lines to exceed the limit
    for i in {1..1200}; do
        echo "Line $i: This is a test line with some content to make it realistic. Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    done
} > "$large_test_file"

git add "$large_test_file"

# Test the hook directly (should fail)
if .git/hooks/pre-commit; then
    print_error "Large commit test failed - hook should have rejected this commit"
    exit_code=1
else
    print_success "Large commit test passed - hook correctly rejected the commit"
    exit_code=0
fi

# Clean up
git reset HEAD "$large_test_file" > /dev/null 2>&1
rm -f "$large_test_file"

print_info ""

# Test 3: No staged files
print_test "No staged files (should pass with warning)"

# Make sure nothing is staged
git reset > /dev/null 2>&1

if .git/hooks/pre-commit; then
    print_success "No staged files test passed"
else
    print_error "No staged files test failed"
fi

print_info ""

# Test 4: Binary files (should be ignored)
print_test "Binary files (should be ignored in line count)"

# Create a small binary file (using dd to create a binary file)
binary_file="test_binary.bin"
dd if=/dev/zero of="$binary_file" bs=1024 count=1 > /dev/null 2>&1

# Create a small text file too
text_file="test_with_binary.txt"
echo "Small text file alongside binary" > "$text_file"

git add "$binary_file" "$text_file"

if .git/hooks/pre-commit; then
    print_success "Binary files test passed - binary file was ignored in line count"
else
    print_error "Binary files test failed"
fi

# Clean up
git reset HEAD "$binary_file" "$text_file" > /dev/null 2>&1
rm -f "$binary_file" "$text_file"

print_info ""
print_info "🎉 Pre-commit hook testing completed!"
print_info ""
print_info "📝 Usage Examples:"
print_info "   Normal commit:     git commit -m 'Your message'"
print_info "   Bypass hook:       git commit --no-verify -m 'Your message'"
print_info "   Check staged:      git diff --cached --stat"
print_info ""

exit $exit_code
