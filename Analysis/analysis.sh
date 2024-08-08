#!/usr/bin/env bash

# This is a quick script which cleans up the data recieved from the bot
# so that it can be graphed easily by R.

# Fetches data
cp ../Bot/output.dat output.dat
phrase=""

while read p; do
    # Sorts data by question
    if [[ "$p" == phrase* ]]; then
        phrase="$p"
        touch "$p".dat
        touch "$p".junk
    else
        # Filters non-number messages
        if [[ "$p" =~  ^([1-9][0-9]?|100)$ ]]; then
            echo "$p" >> "$phrase".dat
        else
        	echo "$p" >> "$phrase".junk
        fi
    fi
done < output.dat

# Runs R analysis
R -q --no-save < analysis.r >> /dev/null 2>&1

# Clean up
rm *.junk *.dat
