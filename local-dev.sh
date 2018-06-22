#!/bin/sh
set -e

# Cleanup
rm -rf .local_dev/
mkdir .local_dev/

# Copy files
cp -r sources/server/ .local_dev/
cp -r sources/webapp/ .local_dev/
cd .local_dev/

# Replace place holders
find . -type f | xargs sed -i "s/__PACKAGE_NAME__/localdev/g"
find . -type f | xargs sed -i "s/__PACKAGE_DESC__/Running application locally/g"
find . -type f | xargs sed -i "s/__VERSION__/0.0.1/g"
find . -type f | xargs sed -i "s/__DATE__/01-01-1970/g"

# Build Vue application with DevTools enabled (Firefox or Chrome plugin)
cd webapp/
sed -i '/Vue.config.productionTip = false/a Vue.config.devtools = true' src/main.js
npm install
npm run lint
npm run build
cd ..

# Prepare application
cd server/
mkdir templates/
mkdir static/
cp ../webapp/dist/*.html templates/
cp -r ../webapp/dist/static/* static/
cd ..

# Run application locally on port :5000 (Press CTRL+C to quit)
cd server/
python application.py
