heroku login
heroku config:set DISABLE_COLLECTSTATIC=1
git status
echo "Please commit your chage to master to get update"
git add .
git commit -m "Deploying Production"
git push -u origin master