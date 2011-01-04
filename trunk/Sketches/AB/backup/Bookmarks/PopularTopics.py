# This is a trial script to show the popular topics within a given programme with a view to using parts of it in the main application.
# This could be used to generate current BBC trending topics.

import os
import re
import string
import sys

import MySQLdb
import cjson
import nltk
from nltk import FreqDist

def spellingFixer(text):
        # Fix ahahahahahaha and hahahahaha
        text = re.sub("(ha){1,}$","haha",text,re.I)
        # fix looooooool and haaaaaaaaaaa - fails for some words at the mo, for example welllll will be converted to wel, and hmmm to hm etc
        # Perhaps we could define both 'lol' and 'lool' as words, then avoid the above problem by reducing repeats to a max of 2
        x = re.findall(r'((\D)\2*)',text,re.I)
        for entry in sorted(x,reverse=True):
                if len(entry[0])>2:
                        text = text.replace(entry[0],entry[1])
                if len(text) == 1:
                        text += text
        return text


if __name__ == "__main__":

    # TODO NTLK does weird stuff with apostrophes in tokenization by default that I've still got to fathom out
    # Will probably replace it with my own splitter for this purpose

    exclusions = ["a","able","about","across","after","all","almost","also","am",\
                    "among","an","and","any","are","as","at","be","because","been","but",\
                    "by","can","cannot","could","dear","did","do","does","either","else",\
                    "ever","every","for","from","get","got","had","has","have","he","her",\
                    "hers","him","his","how","however","i","if","in","into","is","it",\
                    "its","just","least","let","like","likely","may","me","might","most",\
                    "must","my","neither","no","nor","not","of","off","often","on","only",\
                    "or","other","our","own","rather","said","say","says","she","should",\
                    "since","so","some","than","that","the","their","them","then","there",\
                    "these","they","this","tis","to","too","twas","up","us","wants","was","we",\
                    "were","what","when","where","which","while","who","whom","why","will",\
                    "with","would","yet","you","your","via","rt"]

    # Load Config
    try:
        homedir = os.path.expanduser("~")
        file = open(homedir + "/twitter-login.conf")
    except IOError, e:
        print ("Failed to load login data - exiting")
        sys.exit(0)

    raw_config = file.read()
    file.close()

    # Read Config
    config = cjson.decode(raw_config)
    dbuser = config['dbuser']
    dbpass = config['dbpass']

    db = MySQLdb.connect(user=dbuser,passwd=dbpass,db="twitter_bookmarks",use_unicode=True,charset="utf8")
    cursor = db.cursor()

    pid = raw_input("Please enter a pid to view the popular topics for: ")

    while len(pid) != 8:
        print ("This pid appears to be invalid, please try again")
        pid = raw_input("Please enter a pid to view the popular topics for: ")

    filter = ""
    while filter != "yes" and filter != "no":
        filter = raw_input("Would you like to filter out programme keywords (yes/no)?: ")

    # Find all matching keywords
    if filter == "yes":
        cursor.execute("""SELECT keyword FROM keywords WHERE pid = %s""",(pid))
        result = cursor.fetchall()

        if len(result) > 0:
            keywords = list()
            for row in result:
                keywords.append(string.lower(row[0]))

    # Find all matching tweets
    cursor.execute("""SELECT text FROM rawdata WHERE pid = %s""",(pid))
    result = cursor.fetchall()

    if len(result) > 0:
        progtext = list()
        rawprogtext = list()
        for row in result:
            data = string.lower(row[0])
            rawprogtext.append(row[0])

            # Filter out e-mail addresses, web addresses, retweets etc
            data = re.sub("^\s","",re.sub("((^|\S{0,}\s){1,})(RT|rt|Rt|rT)\s@\S{1,}","",data,re.I))
            data = re.sub("\s(via|Via|VIA)\s@\S{1,}$","",data,re.I)
            # Web address filter
            data = re.sub("http://\S{1,}","",data,re.I)
            # E-mail filter
            data = re.sub("\S{1,}@\S{1,}.\S{1,}","",data,re.I)

            # Strip out words matching keywords
            if filter == "yes":
                for word in keywords:
                    if "^" in word:
                        wordbits = word.split("^")
                        if wordbits[0] in data and wordbits[1] in data:
                            data = data.replace(wordbits[0],"")
                            data = data.replace(wordbits[1],"")
                    else:
                        data = data.replace(word,"")
            progtext.append(data)

        # Split the text into words and pass to NLTK
        rawtext = "".join(progtext)

        tokens = rawtext.split()
        #for token in tokens:
        #    if token.lower() in exclusions:
        #        tokens.pop(tokens.index(token))
        #tokens = nltk.word_tokenize(rawtext)

        #tokens = nltk.regexp_tokenize(rawtext,pattern)
        newtokenlist = list()

        for token in tokens:
            newtokenlist.append(spellingFixer(token))

        nltktext = nltk.Text(newtokenlist)
        collocations = nltktext.collocations()
        word_fd = FreqDist(tokens)
        index = 0
        print "\nPopular words:"
        for entry in word_fd:
            if re.match("\W",entry) != None or entry.lower() in exclusions:
                index -= 1
                # Ignore this one, it's just symbols
            else:
                print entry
            index += 1
            if index == 10:
                break
        print "\nPopular topics:"
        bigram_fd = FreqDist(nltk.bigrams(tokens))
        index = 0
        for entry in bigram_fd:
            if (re.match("\W",entry[0]) != None or re.match("\W",entry[1]) != None) or (entry[0].lower() in exclusions or entry[1].lower() in exclusions):
                index -= 1
                # Ignore this one, it's just symbols
            #elif re.match("\W",entry[0]) != None or re.match("\W",entry[1]) != None:
            #    print entry[0] + entry[1]
            else:
                print entry[0], entry[1]
            index += 1
            if index == 10:
                break

        # The below experimentation creates many amusing fails, including the evaluation of 'Monster Munch' as a person and 'LOL' as an organisation.
        # It also appears to evaluate anything after an @ as an organisation - some Twitter convention filtering needed.

        print "\nMore trials:"
        #print rawtext

        #taggedsents = nltk.corpus.nps_chat.tagged_posts()
        #unigram_tagger = nltk.UnigramTagger(taggedsents)

        # Remove unicode:
        for sentence in rawprogtext:
            rawprogtext[rawprogtext.index(sentence)] = re.sub("\\u\w\w\w\w","",sentence,re.I)
        #for sentence in rawprogtext:
        #    rawprogtext[rawprogtext.index(sentence)] = re.sub("\\[x\w\w]","",sentence,re.I)
        words = [nltk.word_tokenize(sent) for sent in rawprogtext]
        #print words
        #progtext = nltk.word_tokenize(rawtext)
        #print progtext
        #words = [nltk.pos_tag(word) for word in progtext]
        #print words
        words = [nltk.pos_tag(word) for word in words]
        #words2 = [unigram_tagger.tag(word) for word in words]
        print words

#        for sentence in words2:
#            newsentence = ""
#            for word in sentence:
#                if word[1] == None:
#                    print word
#                    print word[0]
#                    print word[1]
#                    newsentence = unigram_tagger.tag(nltk.untag(sentence))
#                    break
#            if newsentence != "":
#                words2[words2.index(sentence)] = newsentence
#                print "Using standard corpus"
#            else:
#                print "Using chat corpus"
                
        #print words2
        for item in words:
            try:
                printrec = nltk.ne_chunk(item)
                entityrec = str(printrec)
                #print entityrec
                if "ORGANIZATION" in entityrec or "PERSON" in entityrec or "GPE" in entityrec or "LOCATION" in entityrec or "DATE" in entityrec or "TIME" in entityrec or "MONEY" in entityrec or "PERCENT" in entityrec or "FACILITY" in entityrec:
                    print printrec
            except UnicodeEncodeError, e:
                print "Unicode error - ignoring these for now"
            except AttributeError, e:
                print "Attribute error - ignoring these for now"
        #nps_chat_train = nltk.corpus.brown.tagged_sents(categories='a')[100:]
        #unigram_tagger = nltk.UnigramTagger(nps_chat_train)
        #print nltk.tag.untag(nltk.corpus.brown.tagged_sents(categories='b')[:100][0])
        #unigram_tagger.tag()
        


    else:
        print ("No tweets found for the entered pid")