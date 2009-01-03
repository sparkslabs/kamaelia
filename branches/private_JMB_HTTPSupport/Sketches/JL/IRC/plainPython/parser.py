#! /usr/bin/env python

def parseRpl(segment):
    after_number = segment.find('</a>')
    number = segment[after_number-3:after_number]
    
    at_name = segment.find('</td><td class="t">') + len('</td><td class="t">')
    after_name = segment.find('</td>', at_name)
    if segment[at_name:at_name + 7] == '<a href':
        after_name = segment.find('</a>', after_number + 1)
        at_name = segment.find('>', at_name) + 1
    name = segment[at_name:after_name]
    name = name.rstrip()

    at_format = segment.find('</td><td class="t">', after_name) + len('</td><td class="t">')
    after_format = segment.find('\n', at_format)
    format = segment[at_format: after_format]
    format = format.replace('&gt;', '>')
    format = format.replace('&lt;', '<')

    at_comments = segment.find('</td><td>', after_format) + len('</td><td>')
    comments = segment[at_comments:]

    return number, name, format, comments

def appendParsed(lines, number, name, format, comments):
    tab = '    '
    if len(lines) > 0:
        lastNumber = lines[-3][0:2]
        if number == lastNumber:
            return
    lines.append(number + tab + name + tab + '"'+format+'"' + "\n")
    lines.append( '### ' + comments)
    lines.append("\n") 

    
read = open("/home/jlei/files/irc2numerics.html", "r")
write = open("/home/jlei/files/numeric_replies.txt", "w")
text = read.read()
read.close()
text = text.split('</td></tr>')
write.write("###courtesy of pickle@alient.net.au, at http://www.alien.net.au/irc/irc2numerics.html\n\n")
lines = []
for segment in text:
    number, name, format, comments = parseRpl(segment)
    appendParsed(lines, number, name, format, comments)
write.writelines(lines)
