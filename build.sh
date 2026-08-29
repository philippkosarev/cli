#! /usr/bin/env bash

echo "Deleting 'dist' directory..."
rm ./dist -r
echo "Building..."
python3 -m build

# Publish command:
# python3 -m twine upload --repository pypi dist/*