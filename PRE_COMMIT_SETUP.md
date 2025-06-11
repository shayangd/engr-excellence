# Pre-Commit Hook Setup

## 🎯 Overview

This repository now includes a pre-commit hook that **prevents commits with more than 1000 lines of changes**. This encourages better development practices by promoting smaller, more focused commits.

## ✅ Installation Status

✅ **Pre-commit hook is installed and active**

The hook is located at `.git/hooks/pre-commit` and will automatically run before every commit.

## 🚀 Quick Start

### Normal Usage
```bash
# Make your changes
git add .

# Commit (hook will automatically check line count)
git commit -m "Your commit message"
```

### If Your Commit is Too Large
```bash
# The hook will show you something like this:
📊 Commit Statistics:
   Lines added:   850
   Lines deleted: 300
   Total changes: 1150
   Limit:         1000

ERROR: Commit rejected: Too many lines changed!
```

### Bypass Hook (Use Sparingly)
```bash
# Only when absolutely necessary
git commit --no-verify -m "Large refactoring commit"
```

## ⚙️ Configuration

### Quick Configuration Changes

Edit `.git/hooks/pre-commit-config` to customize:

```bash
# Change the line limit
MAX_LINES=2000

# Show detailed file statistics
SHOW_DETAILED_STATS=true

# Only count additions (ignore deletions)
COUNT_ADDITIONS_ONLY=true

# Exclude certain file patterns
EXCLUDE_PATTERNS="*.min.js *.bundle.* package-lock.json"
```

### Environment Variable Override
```bash
# Temporarily change limit for current session
export PRE_COMMIT_MAX_LINES=2000
git commit -m "Your message"
```

## 🛠️ Testing

Test the hook to ensure it's working:

```bash
./scripts/test-pre-commit-hook.sh
```

This will run several test scenarios and confirm the hook is functioning correctly.

## 💡 Strategies for Large Changes

### 1. Split by Functionality
```bash
# Commit core changes first
git add src/core/
git commit -m "Add core functionality"

# Then commit tests
git add tests/
git commit -m "Add tests for core functionality"

# Finally commit documentation
git add docs/
git commit -m "Add documentation"
```

### 2. Interactive Staging
```bash
# Stage parts of files interactively
git add -p
git commit -m "Part 1: Data models"

git add -p
git commit -m "Part 2: Business logic"
```

### 3. Use Stashing
```bash
# Stash some changes
git stash push -m "UI changes" src/components/

# Commit remaining changes
git add .
git commit -m "Backend API implementation"

# Restore and commit UI changes
git stash pop
git add .
git commit -m "UI components for new feature"
```

## 🔧 Advanced Configuration

### File Exclusions

To exclude certain files from line counting, edit `.git/hooks/pre-commit-config`:

```bash
# Exclude generated files, minified files, and lock files
EXCLUDE_PATTERNS="*.min.js *.min.css *.bundle.* package-lock.json yarn.lock *.generated.*"
```

### Detailed Statistics

Enable detailed per-file statistics:

```bash
# In .git/hooks/pre-commit-config
SHOW_DETAILED_STATS=true
```

This will show:
```
📊 Commit Statistics:
   Lines added:   45
   Lines deleted: 12
   Total changes: 57
   Limit:         1000
   
   src/app.py: +30 -5
   tests/test_app.py: +15 -7
   README.md: +0 -0
```

## 🐛 Troubleshooting

### Hook Not Running
```bash
# Check if hook exists and is executable
ls -la .git/hooks/pre-commit

# Make executable if needed
chmod +x .git/hooks/pre-commit
```

### Hook Errors
```bash
# Test hook manually
.git/hooks/pre-commit

# Check for syntax errors
bash -n .git/hooks/pre-commit
```

### Disable Hook Temporarily
```bash
# Rename to disable
mv .git/hooks/pre-commit .git/hooks/pre-commit.disabled

# Restore to enable
mv .git/hooks/pre-commit.disabled .git/hooks/pre-commit
```

## 📚 Additional Resources

- **Full Documentation**: See `docs/PRE_COMMIT_HOOKS.md`
- **Test Script**: Run `./scripts/test-pre-commit-hook.sh`
- **Configuration**: Edit `.git/hooks/pre-commit-config`

## 🤝 Best Practices

1. **Commit Early, Commit Often**: Make small, frequent commits
2. **Logical Grouping**: Group related changes together
3. **Clear Messages**: Write descriptive commit messages
4. **Review Before Commit**: Use `git diff --cached` to review staged changes
5. **Use Feature Branches**: Create branches for larger features

## 🆘 Need Help?

If you encounter issues or need to make exceptions:

1. **Check the documentation**: `docs/PRE_COMMIT_HOOKS.md`
2. **Run the test script**: `./scripts/test-pre-commit-hook.sh`
3. **Review your changes**: `git diff --cached --stat`
4. **Consider splitting**: Use `git add -p` for partial commits

Remember: The hook is there to help maintain code quality and review-ability. When in doubt, smaller commits are usually better!
