import string, random, re
from api import wordbank
import functools
from datetime import date

def isWild(pattern):
    return pattern.startswith("!")


def randomizers(bank=None):
    patterns = {"positive": [["!positivetraits"]], 
                "negative": [["!negativetraits"]], 
                "neutral": [["!neutraltraits"]], 
                #"quirk": [["!quirks"]],
                "trait": [["!positivetraits"], ["!negativetraits"], ["!neutraltraits"]],
                "jewelry": [[(("!gem", 2), .3), ["!rare_metal", "!commonMaterial"], "!jewelry", (["!gemConnector", ("!gem", 2)], .3)]],
                "clothing": [[("!clothesdescriptor", .4), ("!color", 2), "!fabric", "!clothing"]], 
                "drink": [["!drink", "!plant"], ["!plant", "!drink"], ["!drink", "of", "!plant"]],
                #"need": [["!needs"]], 
                #"childhood": [["!childhoodevents"]],
               }

    ret = {k: Randomizer(k, bank, patterns=v) for k, v in patterns.items()}
    ret["food"] = FoodRandomizer("food", bank)
    ret["character"] = CharacterCreator("character", bank)

    return ret

class Randomizer():

    """These are little connectors I use to help make phrases. If a word starts with ! it 
    will be replaced with a word from the corresponding wordlist. Otherwise it will be 
    used verbatim."""
    subPatterns = {
                 "connector": set(["of", "in", "with", "and"]), 
                 "food": set(["!meat", "!fruit", "!vegetable"]),
                 "plant": set(["!fruit", "!vegetable"]),
                 "fabric": set(["!industrial", "!preindustrial"]),
                 "commonMaterial": set(["!common_metal", "!jewelry_material"]),
                 "gemConnector": set(["Banded with", "with a Large", "with a Small", "with Channel Set", "Paved with"])
    }

    extensions = {}

    def __init__(self, name, bank=None, pattern=None, patterns=[]):
        self.name = name

        #If the user doesn't pass in a word bank to use, use the default bank. Otherwise use the
        #bank the user tells us to
        if not bank:
            self.bank = wordbank.bank()
        else:
            self.bank = bank

        """Subpatterns and extensions can both be overridden by subclasses. Let me know if you
        don't know how inheritance in classes works"""
        self.bank.addSubPatterns(self.subPatterns)
        self.bank.addSubPatterns(self.extensions)

        """patterns and patterns may also be set by subclasses"""
        if not hasattr(self, "pattern"):
            self.pattern = pattern

        if not hasattr(self, "patterns"):
            self.patterns = patterns

    """This is for the REST api"""
    def on_get(self, req, res, count=1):
        count = int(count)
        res.media = self.get_response(count)

    """This is for the REST api"""
    def get_response(self, count=1):
        return {"data": [self.getMany(count)], "name": self.name}

    @functools.singledispatch
    def interpret(token, bank):
        raise NotImplementedError("Found an unknown type in a pattern: %s"%str(token))

    @interpret.register(str)
    def _(token, bank):
        #print("String: ", token)
        if token.startswith("!"):
            return bank.pickOne(token)
        return token

    @interpret.register(set)
    def _(token, bank):
        #print("Set: ", token)
        return bank.joinOne(list(token))

    @interpret.register(list)
    def _(token, bank):
        #print("List: ", token)
        return Randomizer._make(token, bank)

    @interpret.register(tuple)
    def _(token, bank):
        #print("Tuple: ", token)
        if token[1] >= 1:
            picks = [token[0]] * random.randint(1, token[1])
            if len(picks) >= 2:
                picks.insert(-1, "and")
            return picks

        if random.random() < token[1]:
            return ""
        return token[0]

    def getMany(self, count):
        return [self.make() for i in range(count)]

    def make(self):
        if self.pattern:
            pattern = self.pattern
        else:
            pattern = random.choice(self.patterns)

        return string.capwords(self._fixPunctuation(Randomizer._make(pattern, self.bank)))

    def _make(pattern, bank):
        ret = [Randomizer.interpret(t, bank) for t in pattern]

        #Chance to infinitely loop if your patterns have a loop. Keep it a tree.
        while not all([isinstance(r, str) and not isWild(r) for r in ret]):
            #uncomment this to watch the substitutions.
            #print(ret)
            ret = [Randomizer.interpret(t, bank) for t in ret]

        return " ".join(ret)

    """I honestly can't remember this regular expression. I think it removes any punctuation 
    and makes the final string lowercase."""
    def _fixPunctuation(self, pattern):
        return re.sub(r'\s([?.!,"](?:\s|$))', r'\1', pattern)

"""This subclass extends the randomizer with a custom set of patterns and extensions because
the food is extra complicated"""
class FoodRandomizer(Randomizer):
    patterns = [[("!descriptor",.2), ("!preparation", .2), "!food", ("!sub1", .3)],
                [("!descriptor",.2), "!food", ("!preparation", .2), ("!sub1", .3)]]

    extensions = {"sub1": [True, "!connector", ("!descriptor", .05), "!food", "!sauce"]}

"""This subclass technically extends Randomizer, but it actually replaces everything.
If you'll notice, its make() function is completely different, so it doesn't use the notions
of patterns like the actual randomizer does.

It's all pretty simple, I think. There are just a lot of components that it picks from randomly"""
class CharacterCreator(Randomizer):
    speechFiles = ["affirmation", "denial", "exultation", "greeting", "farewell", "frustration", "preface", "request"]

    def on_get(self, req, res, count=1):
        count = 1
        res.media = {"data": self.make(), "name": self.name}

    def randomNeutral(self, count):
        return [i.capitalize() for i in self.bank.pickMany("!neutraltraits", count)]        

    def randomPositive(self, count):
        return [i.capitalize() for i in self.bank.pickMany("!positivetraits", count)]

    def randomNegative(self, count):
        return [i.capitalize() for i in self.bank.pickMany("!negativetraits", count)]

    def randomTrait(self):
        return self.bank.pickOne(random.choice(["!positivetraits", "!negativetraits", "!neutraltraits"])).capitalize()

    def randomQuirk(self, count):
        return [i.capitalize() for i in self.bank.pickMany("!quirks", count)]

    def need(self):
        return self.bank.pickOne("!needs").capitalize()

    def speechHabits(self):
        return ["{}: {}".format(s.capitalize(), self.bank.pickOne("!%s"%s)) for s in self.speechFiles]

    def archetype(self, gender):
        if gender == "male":
            return self.bank.pickOne("!malearchetype")
        else:
            return self.bank.pickOne("!femalearchetype")

    def hobbies(self, count):
        count = random.randint(1, count)
        return self.bank.pickMany("!hobby", count)

    def make(self, gender="random"):
        class Appearance():
            pass

        app = Appearance()
        app.gender = gender.lower()
        if app.gender == "random":
            app.gender = random.choice(["male", "female"])

        app.height = self.height()
        app.hair = self.hairColor()
        app.length = "" if gender != "female" else " %s"%self.hairLengthFemale()
        app.noun = "woman" if app.gender is "female" else "man"
        app.pronoun = "she" if app.gender == "female" else "he"
        app.eyeColor = self.eyeColor()    
        app.skinColor = self.skinColor()

        return [[self.assembleAppearance(app)],
                [ "Birthday: %s"%self.birthday(),
                    "Positive Traits: %s"%", ".join(self.randomPositive(4)),
                    "Negative Traits: %s"%", ".join(self.randomNegative(2)), 
                    "Need: %s"%self.need(),
                    "Big five: %s"%self.bigfive(), 
                    "MBTI: %s"%self.mbti(), 
                    "Persona: %s %s"%(self.randomTrait(), self.bank.pickOne("!agentnouns")),
                    "Archetype: %s"%self.archetype(app.gender),
                    "Hobbies: %s"%", ".join(self.hobbies(3))
                    ]
                , self.speechHabits(),
                ]

    def assembleAppearance(self, app):
        if app.gender == "female":
            return "A {height} {noun} with {eyeColor} eyes, {length} {hair} hair, and {skinColor} skin.".format(**app.__dict__)
        else:
            return "A {height} {noun} with {eyeColor} eyes, {hair} hair, and {skinColor} skin.".format(**app.__dict__)


    def height(self):
        return random.choice(["very short", "very tall"] + ["short", "tall"] * 2 + 
                                ["medium height"] * 3)

    def hairColor(self):
        return random.choice(["red"]*3 + ["dark brown", "brown", "auburn"] + 
                            ["light brown", "blonde brown"] * 2 + ["dark blonde"] + 
                            ["golden blonde", "ash blonde"] + ["black"] * 4 + 
                            ["white", "grey", "dyed"])

    def hairLengthFemale(self):
        return random.choice(["waist length", "mid-back"] + ["shoulder length"] * 4 + 
                                ["ear length"] * 5 + ["pixie cut"])

    def eyeColor(self):
        return random.choice(["light blue", "gray", "blue gray", "blue-green", "blue", 
            "green", "amber", "hazel"] + ["light brown"] * 3 + ["dark brown"] * 5)

    def skinColor(self):
        return random.choice(["pale", "fair", "light"] + ["light brown"] * 3 + 
                                ["olive"] * 2 + ["medium brown"] * 2 + ["dark brown", "black"])

    def bigfive(self):
        levels = ["Very high", "Very low"] + ["High", "Medium", "Low"] * 3
        categories = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]

        return " ".join("%s %s."%(random.choice(levels), c) for c in categories)

    def mbti(self):
        pairs = [["Introverted", "Extroverted"], ["Intuiting", "Sensing"], 
                    ["Thinking", "Feeling"], ["Judging", "Perceiving"]]
        abbrs = {"Introverted" :"I", "Extroverted": "E", "Intuiting": "N", "Sensing": "S", 
                    "Thinking": "T",  "Feeling": "F", "Judging": "J", "Perceiving": "P"}

        picks = [random.choice(p) for p in pairs]
        abbr = "".join(abbrs[p] for p in picks)
        return "%s - %s"%(abbr, ", ".join(picks))

    def birthday(self):
        dayofyear = random.randint(1, 365)
        d = date.fromordinal(dayofyear)
        return d.strftime("%B %d")

if __name__ == "__main__":
    bank = wordbank.bank()
    randomizers = randomizer.randomizers(bank)
    clothing = randomizers["clothing"]
    print(clothing.make())
    