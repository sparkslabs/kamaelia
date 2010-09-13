#! /usr/bin/python

# Analyses saved data in DB to give something more useful. Saves to output DB ready for display in web interface
# Need word freq analysis, tweet rate analysis etc
# Any looking at natural language engines / subtitles should be done here or in components following this
# This component probably needs the original keywords etc too TODO as it needs to separate both programmes and channels
# When analysing, look for mentions of just first names used with #programme etc, as people are unlikely to describe presenters etc with full names (could actually modify the original search to do this) TODO
# Watch out for repeated tweets - could be user or Twitter error
# Need to ensure one rogue user can't cause a trend - things must be mentioned by several

# This was copied and pasted - never tested
class WordFreqAnalysis(component):
    Inboxes = ["inbox", "control"]
    Outboxes = ["outbox", "signal"]

    def __init__(self, useexclusions = False):
        super(WordFreqAnalysis, self).__init__()
        self.exclusions = ["a","able","about","across","after","all","almost","also","am",\
                        "among","an","and","any","are","as","at","be","because","been","but",\
                        "by","can","cannot","could","dear","did","do","does","either","else",\
                        "ever","every","for","from","get","got","had","has","have","he","her",\
                        "hers","him","his","how","however","i","if","in","into","is","it",\
                        "its","just","least","let","like","likely","may","me","might","most",\
                        "must","my","neither","no","nor","not","of","off","often","on","only",\
                        "or","other","our","own","rather","said","say","says","she","should",\
                        "since","so","some","than","that","the","their","them","then","there",\
                        "these","they","this","tis","to","too","twas","us","wants","was","we",\
                        "were","what","when","where","which","while","who","whom","why","will",\
                        "with","would","yet","you","your"]
        self.useexclusions = useexclusions

    def main(self):
        while 1:
            if self.dataReady("inbox"):
                text = self.recv("inbox")
                text = string.lower(text)
                # Remove punctuation
                for items in """!"#$%&()*+,-./:;<=>?@[\\]?_~'`{|}?""":
                    text = string.replace(text,items,"")
                    words = string.split(text)
                # Remove common words (if requested)
                if self.useexclusions:
                    for word in words:
                        if word not in self.exclusions:
                            filteredwords = word
                    # Use 'filteredwords' from here
                    counts = {}
                    for word in filteredwords:
                        try:
                            counts[w] = counts[w] + 1
                        except KeyError:
                            counts[w] = 1
                else:
                    # Use 'words' from here
                    for word in words:
                        try:
                            counts[w] = counts[w] + 1
                        except KeyError:
                            counts[w] = 1

                self.send(counts,"outbox")

            self.pause()
            yield 1