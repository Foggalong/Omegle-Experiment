# Bot
This is the bot which interacts with the Omegle users, and the library which provides the Omegle interaction functionality. While the backend module has quite a wide range of functionality, for this POC we'll only be using a very small part of it. As an example the bot asks the connected user a question from a predefined list at random, records the question and their response to a data file, and then quits after 10 seconds.

As you can imagine, over a long period of running this will amass quite a lot of data most of which isn't useful. That's why this file is then moved along to the analysis section where it will be cleaned up by an R program.

### Python 2 vs 3
My original intention was to port py-omegle to from 2 in which it was originally written, to 3 the now current version. Despite some of the dependency modules being moved around and/or deprecated I managed to sucessfully port the module, but ran into a bug in upstream python. Because of this the project will use version 2 for the forseeable future. I do still have a copy of my port though so will keep an eye out for fixes landing.