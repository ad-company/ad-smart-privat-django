heroku login
heroku config:set DISABLE_COLLECTSTATIC=1
git status
git add .
git status
git commit
git push -u origin master