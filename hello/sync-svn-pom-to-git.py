import subprocess

import xmlformatter
from bs4 import BeautifulSoup

svn_dir = "D:/projects/common-lib/com.nsn.oss.nbi.common.lib/version-selectors/if-version-spec-inter-pipe/"
git_dir = 'D:/projects/common-lib/nbi/nbi-common-lib/implementation/version-selectors/if-version-spec-inter-pipe/'
subprocess.call(["D:/owendir/apps/TortoiseSVN/bin/svn.exe", "up", svn_dir])

f = open(svn_dir + 'pom.xml', 'r')
svn_pom = f.read()
f.close()

dest_f = open(git_dir + 'pom.xml', 'r')
git_pom = dest_f.read()
dest_f.close()

soup = BeautifulSoup(svn_pom, "xml")
props = soup.select_one('project > properties')

git_soup = BeautifulSoup(git_pom, "xml")
git_props = git_soup.select_one('project > properties')

commit_msg = []
for git_if in git_props.children:
    if git_if.name != None:
        # print '[' + git_if.name + ' > ' + git_if.string + ']'
        svn_if = props.find(git_if.name)
        # print '>>[' + svn_if.name + ' > ' + svn_if.string + ']'
        if svn_if != None and svn_if.string > git_if.string:
            commit_msg.append('Replace version ' + git_if.string + ' with ' + svn_if.string + ' for ' + git_if.name)
            git_if.string = svn_if.string

# print soup
# target_str = str(soup.prettify(soup.original_encoding, 'minimal'))

# doc_root = html.fromstring(str(git_soup))
# output_str = etree.tostring(doc_root, encoding=git_soup.original_encoding, pretty_print=False)

for msg in commit_msg:
    print msg
print '%s interfaces changed' % len(commit_msg)

if len(commit_msg) > 0:
    print '%FIN IWI: ' + ', '.join(commit_msg)
    formatter = xmlformatter.Formatter(indent="4", indent_char=" ", encoding_output="utf-8", preserve=["literal"])
    with open(git_dir + "pom.xml", "wb") as pom_file:
        pom_file.write(formatter.format_string(str(git_soup)))
