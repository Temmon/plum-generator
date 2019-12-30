import os
import random

class WordBank():

    def addSubPatterns(self, subs):
        self.categories = dict(self.categories, **subs)

    def containsCategory(self, name):
        return name in self.categories

    def pickOne(self, cat):
        if cat.startswith("!"):
            ret = list(self.categories[cat[1:]])
            if ret and ret[0] is True:
                return ret[1:]
            return random.choice(ret)
            
        return cat

    def pickMany(self, cat, count):
        return random.sample(self.categories[cat[1:]], count)

    def _join(self, cats):
        literals = [c for c in cats if not c.startswith("!")]
        return sum([self.categories[c[1:]] for c in cats if c.startswith("!")], literals)

    def joinOne(self, cats):
        return random.choice(self._join(cats))

    def joinMany(self, cats, count):
        return random.sample(self._join(cats), count)

    def setStatic(self, name, vals):
        self.categories[name] = vals

    def add(self, lines, key):
        if key in self.categories:
            cat = set([c.lower() for c in self.categories[key]])
            lines = [l for l in lines if x not in cat]

        self.bank.words.insert({"data": lines, "name": key})      

    def dump(self):
        if not os.path.exists("lists"):
            os.mkdir("lists")
        for key in self.categories:
            with open(os.path.join("lists", "%s.txt"%key), "w") as outFile:
                outFile.write("\n".join(self.categories[key]))
      

class TextBank(WordBank):
    def __init__(self, path):
        self.path = path
        self.categories = {}
        self.load()

    def load(self):
        files = os.listdir(self.path)
        for f in files:
            name = os.path.splitext(f)[0]
            with open(os.path.join(self.path, f), "r") as inFile:
                lines = inFile.readlines()
                self.categories[name] = [l.strip() for l in lines]


#Call this to get your word bank.
def bank():
    return TextBank("lists")

if __name__ == "__main__":

    bank().dump()

