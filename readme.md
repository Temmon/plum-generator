RUNNING
==========================

You need python 3.6+ to run this.
Create a virtualenv, which is good practice. I'll talk about why if you want to know.
\> python -m venv env
Activate it
\> source env/bin/activate
Now you can install modules without getting your main Python install bloated and confused.
Install all the required modules for the server. You don't actually need to just to run the generator on the command line
\> pip install -r requirements.txt

To run without the server, open python in the main folder. In the console, run the following:
\> from api import randomizer
\> randomizers = r.randomizers()
Grab the one you want with, for example:
\> clothing = randomizers["clothing"]
\> clothing.make()
  'Carnation And Orange Nylon Panty'

You can also run the server in linux and maybe mac with ./run.sh or on any? platform with python run.py, but this is just the backend so you can't see anything. You can make requests to the REST server that way though.



FOLDERS AND FILES
====================================

Ignore the frontend folders, static, and views. Those are all for making a webpage, but you don't need them to run it (and it's not very good).

The lists folder is the meat of the program. Add a line to the list and you'll get a new adjective/noun in the relevant category. All you have to do is edit a list and restart the program and there's a chance it'll be randomly selected.

The api folder has the actual code for the generators. 

api_server.py starts the REST server that runs the generators in production, but you don't actually need it if you're running it locally. If you're ever curious, I'm using the Falcon framework to do basically all the work for me.

wordbank.py is important to know about, but probably doesn't need to get changed. It's responsible for loading the files into memory and providing the randomizers with words. 

randomizer.py is the most interesting file. It's in charge of actually combining the words and patterns into phrases. I commented it up, so go take a look when you're ready. Come back here when you get confused.





RANDOMIZER.PY
===========================================================

I used Python magic to actually combine the phrases. That's every function that starts with @interpret (which is a decorator and is an intermediate-advanced concept). The end effect is to take a pattern that looks something like this [[("!clothesdescriptor", .4), ("!color", 2), "!fabric", "!clothing"]] and turn it into "Silky Silver And Cobalt Blue Fustian Shawl". It's pretty complicated. You don't really need to know the details of the way it's processed as long as you can figure out what the patterns mean.




SIMPLE EXAMPLE
============================================================

Here's how it works! Some terminology really fast. A list is surrounded with []. A tuple is surrounded with (). And a set is surrounded with set().

Look at it outside in, left to right. We'll start with the traits pattern

[["!positivetraits"], ["!negativetraits"], ["!neutraltraits"]]

This is a list of lists. Each sublist has one string inside it. That string starts with an !.
First it randomly picks which pattern it's going to use, let's pick ["!positivetraits"]. (It has to be enclosed in a list, otherwise it tries to loop over each character in the string and gets confused. You can try removing a set of brackets and seeing what happens.)

It has the list ["!positivetraits"]. There's only one item in the list, but it still picks at random from everything in it, to get "!positivetraits"

Then it sees that it has a string, and that that string is a wild card because it starts with !. It asks the wordbank for a positivetraits, which looks it up, picks one, and returns it.

At this point, it knows that it's only working with a single string that doesn't have any wild cards so it returns the string and you get "Selfless".




MORE COMPLICATED EXAMPLE
================================================================

Let's try this one now: [[("!clothesdescriptor", .4), ("!color", 2), "!fabric", "!clothing"]]

It picks the pattern, stripping off the outermost brackets to get [("!clothesdescriptor", .4), ("!color", 2), "!fabric", "!clothing"]

Then it works left to right. 

("!clothesdescriptor", .4) having a number less than 1 means there's a 40% chance that it will choose an adjective. In this case it does want one, asks the randomizer for one, and returns with "Silky"

["Silky", ("!color", 2), "!fabric", "!clothing"]

("!color", 2) having a number more than 1 means that it will randomly choose to have 1 and n colors. In this case it says that we need two !color and joins them with "and". ["!color", "and", "!color"]

["Silky", ["!color", "and", "!color"], "!fabric", "!clothing"]

"!fabric" and "!clothing" are both simple wordbank requests.

So we end up with ["Silky", ["!color", "and", "!color"], "Fustian", "Shawl"].

It looks over the string and sees that it's not just strings and runs over it again. Any strings are returned as is, because none of them start with !. 

But ["!color", "and", "!color"] turns into "Silver And Cobalt Blue".

Which gets us ["Silky", "Silver And Cobalt Blue", "Fustian", "Shawl"]

That's combined into a single string and returns: "Silky Silver And Cobalt Blue Fustian Shawl".

