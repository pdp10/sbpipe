
# Guidelines for the developer


## Introduction
This guide is meant for developers and aims to fix some common practices for developing this project. 


## Development Model
This project follows the Feature-Branching model. Briefly, there are two main branches: `master` and `devel`. The former contains the history of stable releases, the latter contains the history of development. The `master` branch only serves as checkout points for production hotfixes or as merge point for release-x.x.x branches. The `devel` branch only serves for feature-bugfix integration and as checkout point. Nobody should directly develop in here. The `devel` branch is versionless (just call it *-devel*)
Due to the existence of unrelated pipelines, a separate branch for each pipeline was created. These branches resemble the idea of the `devel` branch in the context of single pipelines. These are called `devel_PIPELINE`, where `PIPELINE` is the pipeline name. **[If these branches are not practical, they might be removed in the future]**.


### Conventions
- Each new feature is developed in a separate branch called featureNUMBER, where NUMBER is the number of the issue discussing this feature. The first line of each commit message for this branch should report (Issue #NUMBER) at the end before the dot. Doing so, the commit is automatically recorded by the Issue Tracking System for that specific Issue. Note that `#` is required.  
- Same for each new bug-fix, but in this case the branch name is called bugfixNUMBER.
- Same for each new hot-fix, but in this case the branch name is called hotfixNUMBER.


### Work Flow
- Each new pipeline feature is checked out from the specific branch `devel_PIPELINE` we want to add functionalities / fix bugs.
- Same for new pipeline bug fixes.
- Each new hot-fix is checked out from the `master` branch.
- Each new generic feature (common things to all pipelines. It can be lib/) is checked out from the `devel` branch.
- Same for new generic bug fixes.

The procedure for checking out a new feature from the `devel` branch is: 
```
$ git checkout -b feature10 devel
```
This creates the `feature10` branch off `devel`. 
When you are ready to add and commit your work, run:
```
$ git commit -am "Summary of the changes (Issue #10). Detailed description of the changes, if any."
$ git push origin feature10       # sometimes and at the end.
```

When `feature10` is completed and tested, merge this branch to `devel` WITHOUT a fast-forward, so that the history of `feature10` is also recorded (= we know that there was a branch, which is very useful for debugging). 
```
$ git pull origin devel         # update the branch devel in the local repository. Don't do this on master.
$ git checkout devel            # switch to devel
$ git merge --no-ff feature10  
```


Alternatively, use a pull request to open a discussion. 

When the integration tests are successful, then: 
```
$ git branch -d feature10      # delete the branch feature10 (locally)
```

Finally, push everything to the server:
```
$ git push origin devel
$ git push origin feature10   # if not done before
```

### New releases:
When the `devel` branch includes all the desired feature for a release, it is time to checkout this 
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
$ git clone https://YOURUSERNAME@server/YOURUSERNAME/SB_pipe.git   # to clone the master
$ git checkout -b devel origin/devel                               # to get the devel branch
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
git checkout devel
git merge upstream/devel
```
