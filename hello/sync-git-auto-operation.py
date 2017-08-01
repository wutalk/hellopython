from git import Git
from git import Repo

git_repo = 'd:/projects/common-lib/nbi'
repo = Repo(git_repo)
git = repo.git

if str(repo.active_branch) != 'master':
    git.checkout('master')

print repo.active_branch
if str(repo.active_branch) != 'master':
    print 'error: fail to switch to master'
    print 'exit...'
    exit(1)

print git.pull()
print '--------------master is update to date'

git.checkout('version_auto_update')
print git.status()
print '--------------branch status checked'

print git.rebase('master')
print '----------end rebase master to branch'

print 'merge SVN version to branch'
# ...
msg = '%FIN IWI: update dependencies version; %CR PP: auto\n' \
      'Replace version 10.18.178 with 10.18.181 for audit-trail-InterfaceVersion'


print 'commit and review'
idx = repo.index
idx.add(git_repo + '/nbi-common-lib/implementation/version-selectors/if-version-spec-inter-pipe/pom.xml')
git.commit(msg)

# g = Git(git_repo)
# print g.checkout('nbi-common-lib/implementation/version-selectors/if-version-spec-inter-pipe/pom.xml')
