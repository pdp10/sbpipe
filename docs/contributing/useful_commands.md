## Miscellaneous of useful commands
### Git

**Startup**
```
# clone master
git clone https://github.com/pdp10/sbpipe.git
# get develop branch
git checkout -b develop origin/develop
# to update all the branches with remote
git fetch --all
```

**Update**
```
# ONLY use --rebase for private branches. Never use it for shared 
# branches otherwise it breaks the history. --rebase moves your 
# commits ahead. For shared branches, you should use 
# `git fetch && git merge --no-ff`
git pull [--rebase] origin BRANCH
```

**Managing tags**
```
# Update an existing tag to include the last commits
# Assuming that you are in the branch associated to the tag to update:
git tag -f -a tagName
# push your new commit:
git push
# force push your moved tag:
git push -f --tags

# rename a tag
git tag new old
git tag -d old
git push origin :refs/tags/old
git push --tags
# make sure that the other users remove the deleted tag. Tell them(co-workers) to run the following command:
git pull --prune --tags


# removing a tag remotely and locally
git push --delete origin tagName
git tag -d tagName
```

**File system**
```
git rm [--cache] filename
git add filename
```

**Information**
```
git status
git log [--stat]
git branch       # list the branches
```

**Maintenance**
```
git fsck      # check errors
git gc        # clean up
```

**Rename a branch locally and remotely**
```
git branch -m old_branch new_branch         # Rename branch locally
git push origin :old_branch                 # Delete the old branch
git push --set-upstream origin new_branch   # Push the new branch, set local branch to track the new remote
```

**Reset**
```
git reset --hard HEAD    # to undo all the local uncommitted changes
```

**Syncing a fork (assuming upstreams are set)**
```
git fetch upstream
git checkout develop
git merge upstream/develop
```
