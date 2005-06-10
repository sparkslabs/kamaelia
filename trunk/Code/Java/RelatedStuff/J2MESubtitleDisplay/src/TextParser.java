/*
 * Created on 10-May-2005
 *
 * To change the template for this generated file go to
 * Window - Preferences - Java - Code Generation - Code and Comments
 */

/**
 * @author josephl
 *
 * To change the template for this generated type comment go to
 * Window - Preferences - Java - Code Generation - Code and Comments
 */
public class TextParser
{
    private TextDisplayCanvas target;
    private int colour = 0xFF0000;
    private int countcolour = 0;
    private boolean inmarkup = false;
    private String leftover = "";
    /**
     * 
     */
    public TextParser(TextDisplayCanvas sink)
    {
        super();
        target = sink;
    }
    
    void handleString(String newstring)
    {
//        if(++countcolour > 4)
//        {
//            countcolour = 0;
//            switch(colour)
//            {
//            case 0xFF0000:
//                colour = 0x00FF00;
//                break;
//            case 0x00FF00:
//                colour = 0xFFFF00;
//                break;
//            case 0xFFFF00:
//                colour = 0xFFFFFF;
//                break;
//            default:
//                colour = 0xFF0000;                
//            }
//        }
        int pos = 0;
        int startpos = 0;
        char curchar;
        newstring = leftover + newstring;

        for(;pos < newstring.length(); ++pos)
        {
            curchar = newstring.charAt(pos);
            if(inmarkup)
            {
                switch(curchar)
                {
                case '/':
                    if(pos + 1 < newstring.length())
                    {
                        if(newstring.charAt(pos+1)=='>')
                    	{
                        	parseMarkup(newstring, startpos, pos +1);
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
     * @param newstring
     * @param startpos
     * @param i
     */
    private void parseMarkup(String newstring, int startpos, int endpos)
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
                    
                }
            }
        }
        else // Don't recognise the markup - do nothing!
        {}
        
    }

    /* (non-Javadoc)
     * @see StringHandler#input(java.lang.String)
     */
/*    public void handledata(char nc)
    {
        input(nc);
    }
    public void input(char nextChar)
    {
            switch(nextChar)
            {
            case ' ':
                target.addWord((nextChar), colour, true);
                break;
            case '-':
                ++pos;
                target.addWord((nextChar), colour, false);
                break;
            default:
                break;
            }
        target.addWord((nextChar), colour, false);
    }*/
}
