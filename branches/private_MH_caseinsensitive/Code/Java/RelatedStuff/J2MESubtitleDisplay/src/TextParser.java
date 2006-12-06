/*
 * Created on 10-May-2005
 */

/**
 * @author Joseph Lord
 * 
 * This parses the subtitle stream to split it into words.  It also filters out
 * the tags and identifies colour tags.
 * 
 * At the moment it sends the text to a TextDisplayCanvas and it might make
 * sense to generalise this by adding an interface such as WordReceiver to the
 * system and making TextDisplayCanvas implement that interface and sending the
 * text to a target of that type. 
 * 
 * TextParser could also be made to implement some generic text receiving
 * interface. 
 *
 */
public class TextParser
{
    /**
     * The destination of the words.
     */
    private TextDisplayCanvas target;
    /**
     * The current colour which will start red and then be the latest received.
     */
    private int colour = 0xFF0000;
    /**
     * Notes whether parsing state is currently inside a tag.  That is between a "<" and a "/>"
     */
    private boolean inmarkup = false;
    /**
     * Received data that could not be completely parsed without further data for some reason.
     */
    private String leftover = "";
    /**
     * 
     * @param sink The sink is the TextDisplayCanvas object that words should be sent to for disply
     */
    public TextParser(TextDisplayCanvas sink)
    {
        super();
        target = sink;
    }
    /**
     * Received text and passes on to the sink that was set at construction.
     * It passes on text when it gets to the end of a word or at the end of the
     * received text if it is not in the middle of a tag.  Tags are handled by
     * parseMarkup().
     * 
     * There is a deliberate delay between words added of 0.1 seconds so that
     * the user can see the text appearing and track it better than if large
     * amounts appeared instantly causing several lines to scroll in a blink.
     * 
     * @param newstring The new text to process.
     */
    void handleString(String newstring)
    {
        int pos = 0;
        int startpos = 0;
        char curchar;
        newstring = leftover + newstring;
        leftover = "";
        for(;pos < newstring.length(); ++pos)
        {
            curchar = newstring.charAt(pos);
            if(inmarkup) // see if we have reached end of the markup.
            {
                switch(curchar)
                {
                case '/':
                    if(pos + 1 < newstring.length())
                    {
                        if(newstring.charAt(pos+1)=='>') // We really have found the end of the markup.
                    	{
                        	parseMarkup(newstring, startpos); // Process tag.
                        	pos = pos + 1;
                        	startpos = pos + 1;
                        	inmarkup = false;
                    	}
                    }
                    break;
                    
                }
                
            }
            else
            {
                switch(curchar)
                {
                case '<':
                    target.addWord(newstring.substring(startpos, pos), colour, false);
                    startpos = pos;
                    inmarkup = true;
                    break;
                case ' ':
                case '\r':
                case '\n':
                    target.addWord(newstring.substring(startpos, pos), colour, true);
                    startpos = pos + 1;
                    try{
                    Thread.sleep(100);
                    }catch(InterruptedException e){}
                    break;
                case '-':
                    target.addWord(newstring.substring(startpos, pos + 1), colour, false);
                    startpos = pos + 1;
                    break;
                default:
                    break;
                }
            }
        }
        if(inmarkup)
        {
            leftover = newstring.substring(startpos, pos);
        }
        else
        {
            target.addWord(newstring.substring(startpos, pos), colour, false);
        }
         
    }

    /**
     * This function handles the response to tags that have already been found.
     * 
     * Recognised tags and effect:
     * 	<clear/> = Calls TestDisplayComponent.clear()
     *  <br/>    = Calls TestDisplayComponent.newline()
     *  <font color="#89ABCD"\> = Sets the current colour to value recognised as hex.
     * 
     * All other tags and unrecognised numbers etc are silently ignored!!!
     * 
     * Note that currently the server strips out the <clear/> command and
     * doesn't send <br/> commands so only the <font color...> is really tested. 
     * 
     * @param newstring The string containing the markup.
     * @param startpos The index of the start of the markup in the newstring.
     */
    private void parseMarkup(String newstring, int startpos)
    {
        if(newstring.regionMatches(true, startpos, "<clear/>", 0, 8))
        {
            target.clear();
            return;
        }
        else if (newstring.regionMatches(true, startpos, "<br/>", 0, 5))
        {
            target.newline();
        }
        else if (newstring.regionMatches(true, startpos, "<font color=\"#", 0, 14))
        {
            int numend = newstring.indexOf('\"', 14 + startpos);
//            target.addWord("" + startpos + " " + Integer.toString(numend), 0x0000FF, true);
            if (numend != -1)
            {
//                target.addWord(newstring.substring(startpos + 14, numend), 0x00FF00, true);
                try
                {
                    colour = Integer.parseInt(newstring.substring(startpos + 14, numend), 16);
                }
                catch(NumberFormatException e)
                {// Ignore silently and exit with no effect.
                 //  If it isn't a number just ignore it and carry on.
                }
            }
        }
        else // Don't recognise the markup - do nothing!
        {}
        
    }
}
