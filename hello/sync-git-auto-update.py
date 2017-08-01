from subprocess import Popen
from git import Repo

git_repo = 'd:/projects/common-lib/nbi'
repo = Repo(git_repo)
git = repo.git

print 'update nbi common lib from git repo'
args = ['D:/tmp/auto_update_git.bat', 'hello world']
p = Popen(args)
stdout, stderr = p.communicate()
print stdout
print '------------'
print stderr

# auto update svn and merge to git
# msg will be populated from sync-svn-pom-to-git.py
msg = '%FIN IWI: update dependencies version; %CR PP: owen; change list: ' \
      'Replace version 1.627 with 1.628 for if.version.nasda.platform, ' \
      'Replace version 8.975 with 8.976 for if.version.nasda.services'

git.checkout('version_auto_update')
print '--check if anything updated'
print git.status()
print '--check if anything updated'

args = ['D:/tmp/auto_commit_git.bat', msg]

# p = Popen(args)
# stdout, stderr = p.communicate()
print stdout
print '-----reviewed, waiting for email-------'
print stderr
