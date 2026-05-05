#!/bin/bash
# Usage: ./run.sh        → runs latest day
#        ./run.sh 001    → runs Day001

cd "$(dirname "$0")"
git -C .. pull

if [ -n "$1" ]; then
    file=$(ls Sources/algo_template/Day$(printf "%03d" "$1")_*.swift 2>/dev/null | head -1)
else
    file=$(ls Sources/algo_template/Day*.swift 2>/dev/null | sort | tail -1)
fi

if [ -z "$file" ]; then
    echo "No day file found"
    exit 1
fi

name=$(basename "$file" .swift)
echo "Running $name..."

echo "$name.run()" > Sources/algo_template/main.swift
swift build &>/dev/null && .build/debug/algo_template
