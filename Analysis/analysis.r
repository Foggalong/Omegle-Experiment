#!/usr/bin/env R

# R code for analysing data from the example Omegle experiment. After
# loading the data and plots a butterfly chart to compare frequencies
# of the numbers picked for the different phrases.

load.dat <- function(filename) {
     # load data in the appropriate format and convert to frequency table
     freqs = table(read.table(file=filename, header=F, fill=T))
     # pre-allocate output array so null values also counted 
     output = rep(0, 100)
     # populate output array with non-zero frequencies 
     output[as.numeric(names(freqs))] = as.vector(freqs)
     return(output)
}

png("output.png", width=15, height=10, units="cm", res=800)
colors = c("lightblue", "pink")  # save colours for repeated use
barplot(
     load.dat("phrase0.dat"),
     ylim = c(-60,60),  # including negative axis reserves space for next
     col = colors[1], border = colors[1],
     xlab = "Number (invalid choices excluded)", ylab = "Frequency",
     main = "Frequency of Chosen Number by Phrasing"
)
par(new = TRUE)
barplot(
     load.dat("phrase1.dat"),
     ylim = c(60,-60),  # reversed order flips the data into negative axis
     col = colors[2], border = colors[2],
     axes = FALSE, xlab = "", ylab = "", main = ""  # don't redraw  
)
grid(nx = NA, ny = NULL, lty = 2, col = "gray", lwd = 1)
legend(c("Phrase 1", "Phrase 2"), x="topright", col=colors, lwd=10)
# need to add an x-axis manually; 100 data points across 120 ticks
axis(side = 1, c(1, seq(12,120,12)), c(1, seq(10, 100, 10)))

dev.off()
