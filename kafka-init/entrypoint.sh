#!/bin/bash

sleep 30
for f in *.sh; do
  echo "Running $f"
  bash "$f" 
done
