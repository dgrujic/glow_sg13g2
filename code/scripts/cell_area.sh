#!/bin/bash

find . -type f -name "*.gds" -exec bash -c '
    for file; do
        dir=$(dirname "$file")
        base_ext=$(basename "$file")
        base="${base_ext%.gds}"
        
        (cd "$dir" && gdsinfo "$base_ext" --area 189,0)
    done
' _ {} +

