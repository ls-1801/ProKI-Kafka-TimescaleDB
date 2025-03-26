#!/bin/bash

sleep 30
find /topics -name '*.sh' -print0 | while IFS= read -r -d $'\0' f; do
  echo "Running $f"
  (
    cd "$(dirname "$f")"
    bash "$(basename "$f")"
  )
done
