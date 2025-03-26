#!/bin/sh

dest="/docker-entrypoint-initdb.d"
mkdir -p "$dest"

counter=2

for filepath in /tables/*/init.sql; do
    # Extract components
    dir1=$(echo "$filepath" | cut -d'/' -f3) # chair1, chair2

    # Generate new filename
    newname=$(printf "%03d_%s_init.sql" "$counter" "$dir1")

    # Move and rename
    mv "$filepath" "$dest/$newname"

    counter=$((counter + 1))
done

for filepath in /tables/*/*/table.sql; do
    # Extract components
    dir1=$(echo "$filepath" | cut -d'/' -f3) # chair1, chair2
    dir2=$(echo "$filepath" | cut -d'/' -f4) # bigmachine, smallmachine

    # Generate new filename
    newname=$(printf "%03d_%s_%s.sql" "$counter" "$dir1" "$dir2")

    # Move and rename
    mv "$filepath" "$dest/$newname"

    counter=$((counter + 1))
done