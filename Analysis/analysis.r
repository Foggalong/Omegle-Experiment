#!/usr/bin/env R

# This R program analyses the data as part of the Omegle experiment. It
# plots two bar graphs of the frequency of numbers piced, sorted by #.
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

# PDF for data output
pdf("output.pdf", width=6, height=10)
attach(mtcars)
par(mfrow=c(2,1))

# Phrase 0
data_file = read.table(file="phrase0.dat", header=F, fill=T)
data = table(c(data_file$V1))
barplot(data, main="Phrase 0")

# Phrase 1
data_file = read.table(file="phrase1.dat", header=F, fill=T)
data = table(c(data_file$V1))
barplot(data, main="Phrase 1")

