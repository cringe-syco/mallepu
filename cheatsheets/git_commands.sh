#!/bin/bash

# Set global configurations
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global core.editor "vim"
git config --global merge.tool "vimdiff"
git config --global alias.lg "log --graph --oneline --decorate --all"

# Initialize a new repository
git init my_project
cd my_project || exit

# Add a remote repository
git remote add origin https://github.com/yourusername/yourrepo.git
git fetch origin
git checkout -b main origin/main

# Set up tracking for branches
git branch --set-upstream-to=origin/main main

# Create a new branch and switch to it
git checkout -b feature-branch

# Add files and commit
echo "print('Hello, Git!')" > hello.py
git add hello.py
git commit -m "Add hello.py script"

# Push branch to remote
git push -u origin feature-branch

# Merge branch into main
git checkout main
git merge --no-ff feature-branch -m "Merge feature-branch"

# Delete merged branch
git branch -d feature-branch
git push origin --delete feature-branch

# Rebase branch onto main
git checkout -b another-feature
git rebase main

# Stash changes and reapply later
echo "temp changes" > temp.txt
git add temp.txt
git stash
git stash list
git stash pop  # Reapply changes

# Tagging and releases
git tag -a v1.0 -m "Release v1.0"
git push origin v1.0

# Show detailed history
git log --graph --oneline --decorate --all
git reflog

# Undo last commit (soft keeps changes, hard removes them)
git reset --soft HEAD~1
git reset --hard HEAD~1

# Revert a commit
git revert <commit-hash>

# Remove a file from history
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch secret.txt' \
  --prune-empty --tag-name-filter cat -- --all

# Garbage collection and cleanup
git gc --prune=now
git fsck --full

# Show repository status and differences
git status
git diff
git diff --staged

# Clone repository
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo || exit

# Fetch latest changes
git fetch origin
git rebase origin/main

# Cherry-pick a specific commit
git cherry-pick <commit-hash>

# Squash commits interactively
git rebase -i HEAD~3  # Squash last 3 commits

# Show aliases and configuration
git config --list

# === ADVANCED GIT COMMANDS === #

# Git Bisect - find a bug in history
git bisect start
git bisect bad  # Mark current version as bad
git bisect good <commit-hash>  # Mark a known good version
# Git will now guide you through checking commits
git bisect reset  # End bisect session

# Git Blame - see who changed what
git blame hello.py

# Git Worktrees - manage multiple working directories
git worktree add ../feature-worktree feature-branch
cd ../feature-worktree || exit
git status
cd ../my_project || exit
git worktree remove ../feature-worktree

# Git Hooks - Pre-commit example
echo -e "#!/bin/sh\nexec git diff --cached --exit-code" > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Submodules - add, update, remove
git submodule add https://github.com/example/submodule.git submodule-dir
git submodule update --init --recursive
git submodule foreach --recursive git pull origin main
git rm --cached submodule-dir  # Remove submodule

# Show last commit details
git show

# List all branches (local and remote)
git branch -a

# Fetch all remote branches
git fetch --all

# Create a patch from a commit
git format-patch -1 <commit-hash>

# Apply a patch
git apply < patch-file.patch

# Rename a branch locally and remotely
git branch -m old-branch new-branch
git push origin --delete old-branch
git push --set-upstream origin new-branch

# Reset a file to its last committed state
git checkout -- hello.py  # Deprecated
git restore hello.py  # Preferred

# Squash all commits into one (reset + recommit)
git reset --soft $(git merge-base main feature-branch)
git commit -m "Squashed all commits"

# Create an orphan branch (clean history)
git checkout --orphan new-clean-branch
git rm -rf .
echo "Fresh start" > README.md
git add .
git commit -m "New clean branch"

# Amend the last commit
git commit --amend -m "Updated commit message"

# Exit script
echo "Git operations completed successfully!"
