
# Developer guide

Mailing list: sb_pipe AT googlegroups.com


## Introduction
This guide is meant for developers and aims to fix some common practices for developing this project. 


## Development Model
This project follows the Feature-Branching model. Briefly, there are two main branches: `master` and `develop`. The former contains the history of stable releases, the latter contains the history of development. The `master` branch only serves as checkout points for production hotfixes or as merge point for release-x.x.x branches. The `develop` branch only serves for feature-bugfix integration and as checkout point. Nobody should directly develop in here. The `develop` branch is versionless (just call it *-dev*).


### Conventions
- Each new feature is developed in a separate branch called featureNUMBER, where NUMBER is the number of the issue discussing this feature. The first line of each commit message for this branch should report (Issue #NUMBER) at the end or beginning, but before the first dot. Doing so, the commit is automatically recorded by the Issue Tracking System for that specific Issue. Note that `#` is required.
- Same for each new bug-fix, but in this case the branch name is called bugfixNUMBER.
- Same for each new hot-fix, but in this case the branch name is called hotfixNUMBER.


### Work Flow
- Each new feature is checked out from the `develop` branch.
- Same for new generic bug fixes.
- Each new hot-fix is checked out from the `master` branch.


The procedure for checking out a new feature from the `develop` branch is: 
```
$ git checkout -b feature10 develop
```
This creates the `feature10` branch off `develop`. 
When you are ready to add and commit your work, run:
```
$ git commit -am "Summary of the changes (Issue #10). Detailed description of the changes, if any."
$ git push origin feature10       # sometimes and at the end.
```

As of June 2016, the branches `master` and `develop` are protected and a status check using Travis-CI must be performed before merging or pushing into these branches. This automatically forces a merge without fast-forward. 
In order to merge **any** new feature, bugfix or simple edits into `master` or `develop`, a developer **must** checkout a new branch and, once committed and pushed, **merge** it to `master` or `develop` using a `pull request`. To merge `feature10` to `develop`, the pull request will 
look like this:
```
base:develop  compare:feature10   Able to merge. These branches can be automatically merged.

```
A small discussion about feature10 should also be included to allow other users to understand the feature.


**OBSOLETE**
This was used in the past when the branches `master` and `develop` were not protected. At the time a user could push directly into these branches. The procedure worked as follows: `feature10` was merged to `develop` WITHOUT a fast-forward, so that the history of `feature10` was also recorded (= we know that there was a branch, which is very useful for debugging). 
```
$ git pull origin develop         # update the branch develop in the local repository. Don't do this on master.
$ git checkout develop            # switch to develop
$ git merge --no-ff feature10 
$ git push origin develop
```

Finally delete the branch: 
```
$ git branch -d feature10      # delete the branch feature10 (locally)
```


### New releases:
When the `develop` branch includes all the desired feature for a release, it is time to checkout this 
branch in a new one called `release-x.x.x`. It is at this stage that a version is established. Only bug-fixes or hot-fixes are applied to this branch. When this testing/correction phase is completed, the `master` branch will merge with the `release-x.x.x` branch, using the commands above.
To record the release add a tag:
```
git tag -a v1.3 -m "PROGRAM_NAME v1.3"
```
To transfer the tag to the remote server:
```
git push origin v1.3   # Note: it goes in a separate 'branch'
```
To see all the releases:
```
git show
```

## Project Structure:
Not written yet!

## Miscellaneous of Useful Commands:
### Git
##### Startup
```
$ git clone https://YOURUSERNAME@server/YOURUSERNAME/sb_pipe.git   # to clone the master
$ git checkout -b develop origin/develop                           # to get the develop branch
$ for b in `git branch -r | grep -v -- '->'`; do git branch --track ${b##origin/} $b; done     # to get all the other branches
$ git fetch --all    # to update all the branches with remote
```

##### Update
```
$ git pull [--rebase] origin BRANCH  # ONLY use --rebase for private branches. Never use it for shared branches otherwise it breaks the history. --rebase moves your commits ahead. I think for shared branches, you should use `git fetch && git merge --no-ff`. **[FOR NOW, DON'T USE REBASE BEFORE AGREED]**.
```

##### File System
```
$ git rm [--cache] filename 
$ git add filename
```

##### Information
```
$ git status 
$ git log [--stat]
$ git branch       # list the branches
```

##### Maintenance
```
$ git fsck      # check errors
$ git gc        # clean up
```

##### Rename a branch locally and remotely
```
git branch -m old_branch new_branch         # Rename branch locally    
git push origin :old_branch                 # Delete the old branch    
git push --set-upstream origin new_branch   # Push the new branch, set local branch to track the new remote
```

##### Reset
```
git reset --hard HEAD    # to undo all the local uncommitted changes
```

##### Syncing a fork (assumes upstreams are set)
```
git fetch upstream
git checkout develop
git merge upstream/develop
```
