Here's my first go at webGL! I spent a ton of time figuring
out how it works and getting it working in the first place, so there aren't a ton of incredible graphics, but I'm very excited to have them all rendered live in the web browser.

A bit about my code: index.html is the main file, which can be opened by a web browser and is also hosted at http://people.reed.edu/~dblount/gfx/hw1a . This links to several javascript files in the js folder. I wrote script.js (the main JS file) and shape.js, which contains a little lightweight 3d-shape describing class that is mimics the conventions of OBJ files and also plays nicely with some of the more technical buffer-y parts of webGL. These files are diligently commented, as I was pretty much learning javascript and WebGL to write them, so I think you'll be able to see what's going on.

In skeleton: upon index.html's loading, webGLStart from script.js is run. This function uses other funcs to set up the gl instance, buffers, shaders etc, and then set in motion the 'tick' function, which is called once each frame (interestingly, each call of 'tick' calls the next call of 'tick'). That's it!

I went through the first few chapters of the great online tutorial, {{{{ . Some of that example code remains in my final product, but probably less than the amount of your python code that I would have used were I to do this assignment in python.