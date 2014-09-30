#!/usr/bin/env bash

# This is a quick script which cleans up the data recieved from the bot
# so that it can be graphed easily by R.
# Copyright (C) 2014  Joshua Fogg

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

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
