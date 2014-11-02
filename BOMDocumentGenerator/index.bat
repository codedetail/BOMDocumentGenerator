echo %~dp0
cd %~dp0
git pull
grep -H -e "^##[^#]" *.md | sed -e "s/^\(.*\).md:##\s*\(.*\)/1. <a href='\1'> \2: **\1**<\/a><br>/"  -e "s/(UNUSED)/{UNUSED}/" | sort -k 4 > .Index.md
git add .
git commit -m "refreshed index"
git push 
