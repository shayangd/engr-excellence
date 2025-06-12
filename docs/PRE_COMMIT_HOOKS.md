# Pre-Commit Hooks Documentation

This repository includes pre-commit hooks to enforce code quality and prevent problematic commits.

## Line Limit Hook

### Overview

The line limit pre-commit hook prevents commits that contain more than 1000 lines of changes (additions + deletions). This encourages:

- Smaller, more focused commits
- Better code review practices
- Easier debugging and rollbacks
- Improved commit history readability

### Installation

The hook is automatically installed in `.git/hooks/pre-commit` and is active for all commits in this repository.

### How It Works

1. **Triggers**: Runs automatically before every `git commit`
2. **Counts**: Total lines added + lines deleted in staged changes
3. **Limit**: Default limit is 1000 lines
4. **Action**: Blocks commit if limit is exceeded

### Example Output

#### Successful Commit (Under Limit)
```
📊 Commit Statistics:
   Lines added:   45
   Lines deleted: 12
   Total changes: 57
   Limit:         1000

SUCCESS: Commit approved: 57 lines changed (within 1000 line limit)
```

#### Blocked Commit (Over Limit)
```
📊 Commit Statistics:
   Lines added:   850
   Lines deleted: 300
   Total changes: 1150
   Limit:         1000

ERROR: Commit rejected: Too many lines changed!

Your commit contains 1150 lines of changes, which exceeds the limit of 1000 lines.

💡 Suggestions:
   1. Split your changes into smaller, more focused commits
   2. Review if all changes are necessary for this commit
   3. Consider using 'git add -p' for partial staging

🚨 To bypass this check (use with caution):
   git commit --no-verify
```

### Bypassing the Hook

**⚠️ Use with caution!** You can bypass the hook when necessary:

```bash
git commit --no-verify -m "Large refactoring commit"
```

### Customizing the Limit

#### Temporary Change (Current Session)
```bash
export PRE_COMMIT_MAX_LINES=2000
git commit -m "Your commit message"
```

#### Permanent Change
Edit the hook file and modify the `MAX_LINES` variable:

**Bash version** (`.git/hooks/pre-commit`):
```bash
MAX_LINES=2000  # Change this value
```

**Python version** (`.git/hooks/pre-commit.py`):
```python
MAX_LINES = int(os.environ.get('PRE_COMMIT_MAX_LINES', '2000'))  # Change default
```

### Strategies for Large Changes

When you need to make large changes:

#### 1. Partial Staging
```bash
# Stage specific files
git add file1.py file2.py
git commit -m "Add new feature components"

# Stage remaining files
git add file3.py file4.py
git commit -m "Add feature tests and documentation"
```

#### 2. Interactive Staging
```bash
# Stage parts of files interactively
git add -p
git commit -m "Part 1: Core functionality"

git add -p
git commit -m "Part 2: Error handling"
```

#### 3. Stashing
```bash
# Stash some changes temporarily
git stash push -m "Secondary changes" file3.py file4.py

# Commit primary changes
git add file1.py file2.py
git commit -m "Primary feature implementation"

# Restore and commit secondary changes
git stash pop
git add file3.py file4.py
git commit -m "Secondary feature enhancements"
```

### Hook Versions

Two implementations are available:

#### 1. Bash Version (Default)
- **File**: `.git/hooks/pre-commit`
- **Pros**: Lightweight, no dependencies
- **Cons**: Basic error handling

#### 2. Python Version (Alternative)
- **File**: `.git/hooks/pre-commit.py`
- **Pros**: Better error handling, more features
- **Cons**: Requires Python 3

To switch to Python version:
```bash
mv .git/hooks/pre-commit .git/hooks/pre-commit.bash
mv .git/hooks/pre-commit.py .git/hooks/pre-commit
```

### Troubleshooting

#### Hook Not Running
```bash
# Check if hook is executable
ls -la .git/hooks/pre-commit

# Make executable if needed
chmod +x .git/hooks/pre-commit
```

#### Hook Errors
```bash
# Test the hook manually
.git/hooks/pre-commit

# Check git configuration
git config --list | grep hook
```

#### Binary Files
The hook automatically skips binary files when counting lines.

### Best Practices

1. **Commit Often**: Make small, frequent commits
2. **Logical Grouping**: Group related changes together
3. **Clear Messages**: Write descriptive commit messages
4. **Review Changes**: Use `git diff --cached` before committing
5. **Use Branches**: Create feature branches for large changes

### Integration with CI/CD

The hook only runs locally. For server-side enforcement, consider:

1. **GitHub Actions**: Add workflow to check commit sizes
2. **GitLab CI**: Add pipeline stage for commit validation
3. **Pre-receive hooks**: Server-side git hooks

### Related Tools

Consider these complementary tools:

- **pre-commit framework**: For additional hooks
- **commitizen**: For conventional commit messages
- **husky**: For Node.js projects
- **lint-staged**: For running linters on staged files
