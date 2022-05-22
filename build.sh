#!/usr/bin/bash
cd "$(dirname "$0")"

rm -R build/
mkdir build/
cp -r data build/
cp dejavusansmono.ttf build/
pex . pygame -c main -o build/PythonFarmGame.pex
cp build/PythonFarmGame.pex .