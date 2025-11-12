#!/bin/bash

# Usage: ./script.sh <book_dir> <output_file>
if [ $# -ne 2 ]; then
    echo "Usage: $0 <book_dir> <output_file>"
    exit 1
fi

BOOK_DIR=$1
OUTPUT_FILE=$2

cd "$BOOK_DIR" || { echo "Error: Cannot change to $BOOK_DIR"; exit 1; }

shopt -s nocasematch

read -p "Enter keywords: " KEYWORDS
read -p "Quote headline: " HEADLINE
read -p "Sentence: " STRING

if ! compgen -G "*.epub" > /dev/null; then
    echo "No .epub files found in $BOOK_DIR."
    exit 1
fi

for BOOK in *.epub; do
    if [[ "$BOOK" == *"$KEYWORDS"* ]]; then
        (
            echo "--------"
            echo -e "\nBook Name: ${BOOK}"
            echo -e "Headline: ${HEADLINE}\n"
            epy -d "$BOOK" | grep -i "${STRING}" -C 2
        ) | tee -a "$OUTPUT_FILE"
    fi
done

echo -e "\n --- Quote added to $OUTPUT_FILE! --- "
