
#
# Collection of support functions from the greylister.
#
# Some of these are likely to be reusable with some work. In their current
# form they're a little too specialised, but still, putting them here allows
# that work to happen.
#


import copy

def SlurpFile(filename):
    f = open(filename)
    lines = f.readlines()
    f.close()
    return lines

openConfig = SlurpFile

def parseConfigFile(lines, default_config,
                    things_which_are_ints = [ "port", "smtp_port", "inactivity_timeout" ],
                   ):
    config = copy.deepcopy(default_config)
    l = 0
    while l<len(lines):
        line = lines[l][:-1] # remove newline
        line = line.rstrip()
        if len(line) != 0:
            if "#" == line[0]:
                pass # skip - it's a comment

            elif "=" in line:
                # This means it's a simple config value
                bits = line.split("=")
                thing = bits[0].strip().rstrip()
                what = bits[1].strip().rstrip()
                if thing in things_which_are_ints:
                    what = int(what)
                config[thing] = what

            else:
                # Otherwise...
                if line[-1] == ":":
                    # It's something that takes a list of things to define it.
                    thing = line[:-1]
                    if config.get(thing) == None:
                        config[thing] = []
                    while (l+1)<len(lines):
                        l+=1
                        line = lines[l][:-1] # remove newline
                        x = line.rstrip()
                        y = line.strip()
                        if x==y:
                            break
                        if " " in y:
                            config[thing].append(tuple(y.split(" ")))
                        else:
                            config[thing].append(y)
                    l-=1
        l+=1
    return config
