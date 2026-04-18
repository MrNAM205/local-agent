#!/usr/bin/env bash
set -e

echo "Cleaning node_modules, dist, and logs..."

rm -rf gui/node_modules
rm -rf gui/dist
rm -rf gui/out
rm -rf logs/*

echo "Done."