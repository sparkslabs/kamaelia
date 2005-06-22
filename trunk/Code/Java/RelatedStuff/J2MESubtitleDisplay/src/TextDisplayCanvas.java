import java.util.Vector;

import javax.microedition.lcdui.Canvas;
import javax.microedition.lcdui.Font;
import javax.microedition.lcdui.Graphics;
import javax.microedition.lcdui.Image;

/*
 * Created on 28-Apr-2005
 *
 * To change the template for this generated file go to
 * Window - Preferences - Java - Code Generation - Code and Comments
 */

/**
 * @author Joseph Lord
 *
 * The main display class for the SubtitleMidlet.  It is a scrolling ticker for
 * multicolour text filling most of the screen. 
 */
public class TextDisplayCanvas extends Canvas
{
    
    /**
     * @author Joseph Lord
     *
     * Contains a sequence of Phrase objects that can be drawn on a
     * single line.  It represents a single line of text and where to draw it,
     * and what colour it should be.
     * 
     */
    private class Line
    {
        private Vector phrases = new Vector(3);
        private int rmargin;
        private int initialpos;
        /**
         * @param rmargin The right hand margin position.
         * @param initialpos The left hand margin position.
         */
        Line(int rmargin, int initialpos)
        {
            this.rmargin = rmargin;
            this.initialpos = initialpos;
        }
        /**
         * Adds an additional word to the line if there is room.
         * 
         * @param word A string to add without line breaks if possible 
         * @param colour The colour of the added word.
         * @param addspace Whether the word should be followed by a space if not at the end of a line.
         * @return null if the word was successfully added otherwise what couldn't be added.  This will usually be the whole word except where that is too long to fit on a single line where it will fit in as much as possible and return the remainder.
         */
        String addWord(String word, int colour, boolean addspace)
        {
            
            if(!phrases.isEmpty())
            {
                Phrase cur = ((Phrase)phrases.lastElement());
                if(cur.getColour() == colour) 
                {//New word is same colour as last
                    return cur.addWord(word, addspace);
                }
                else
                {
                    cur = new Phrase(cur.getEndpos(),rmargin,colour,false);
                    String result = cur.addWord(word, addspace);
                    if(!word.equals(result))
                    {
                        phrases.addElement(cur);
                    }
                    return result;
                }
            }
            Phrase initial = new Phrase(initialpos,rmargin,colour,addspace);
            phrases.addElement(initial);
//            try{Manager.playTone(127, 500, 100);}catch (MediaException e) {}
            return initial.addWord(word, addspace);
        }
        /**
         * Instructs the Line to draw itself onto the given graphics object.
         *  
         * @param g The Graphics object to draw onto.
         * @param ypos The vertical position at which to draw the string.
         */
        void draw(Graphics g, int ypos)
        {
            for(int i = 0; i < phrases.size(); ++i)
            {
                ((Phrase)phrases.elementAt(i)).draw(g, ypos);
            }
        }
        
    }
    /**
     * 
     * @author josephl
     *
     * Contains a string of text and the colour it should be displayed in.
     */
    private class Phrase
    {
        private int offset;
        private int maxX;
        private int endpos;
        private StringBuffer phrase;
        int spacewidth;
        private int colour;
        private boolean linestart;
        /**
         * 
         * @param pos X axis position that the phrase should be drawn at.
         * @param margin Position of right margin in pixels.
         * @param colour The colour of the phrase text.
         * @param startofline If this is true it idicates that the phrase is at the start of the line therefore an addword can be split if it won't fit on a line.
         */
        protected Phrase(int pos, int margin, int colour, boolean startofline)
        {
            offset = pos;
            maxX = margin;
            endpos = offset;
            phrase = new StringBuffer();
            spacewidth = font.charWidth(' ');
            this.colour = colour;
            linestart = startofline;
        }
        /**
         * 
         * Adds a word to the phrase if there is sufficient room before the right margin.
         * 
         * @param word The word to add.
         * @param addspace If there should be whitespace after the word this should be true.
         * @return Whatever wasn't added.  null if succesful otherwise the whole word unless it was also the start of the line when the initial string will be broken.
         */
        protected String addWord(String word, boolean addspace)
        {
            
            int wordwidth = font.stringWidth(word);
            if(wordwidth + endpos <= maxX)
            {
                linestart = false;
                endpos += wordwidth;
                phrase.append(word);
                if(addspace)
                {
                   endpos += spacewidth;
                   phrase.append(' ');
                }
                return null;
            }
            else if(endpos == offset && linestart) //The word is more than a line put as much as possible in.
            {
                char[] ca = word.toCharArray();
                int i = 0;
                while(font.charsWidth(ca, 0, i) < maxX)
                {
                    phrase.append(ca[i]);
                    ++i;
                }
                return new String(ca,i, ca.length - i);
            }
            else
            {
                return word;
            }
        }
        /**
         * Draws the Phrase onto the given graphics object. 
         * 
         * @param g The Graphics object to draw to.
         * @param ypos The height in pixels to draw the Phrase at.
         */
        protected void draw(Graphics g, int ypos)
        {
            g.setColor(colour);
            g.drawString(phrase.toString(), offset, ypos, Graphics.TOP |Graphics.LEFT);
        }
        
        /**
         * Gets the Phrase's colour.
         * 
         * @return Returns the colour.
         */
        int getColour()
        {
            return colour;
        }
        /**
         * Gets the X position of the end of the phrase.
         * 
         * @return Returns the endpos.
         */
        int getEndpos()
        {
            return endpos;
        }
    }
    /**
     * The graphics context associated with the offScreenImage.
     */
    private Graphics graphic;
    /**
     * Image to draw to which is then copied to screen at paint().
     */
    private Image offScreenImage;
    /**
     * The height of the canvas. avoids getHeight() calls for performance.
     */
    private int height;
    /**
     * The width of the canvas. - avoids getWidth() calls for performance
     */
    private int width;
    /**
     * Pixels between left and right margins.
     */
    private int linelength; // 
    /**
     * The font to be used by all drawn text.
     */
    final static Font font = Font.getFont(Font.FACE_MONOSPACE, Font.STYLE_PLAIN, Font.SIZE_LARGE);  // The font that will be used.
    /**
     * The width for the left and right margins.
     */
    private int margin; 
    /**
     * The actual Line objects containing Phrases.
     */
    private Line[] lines;
    /**
     * The currently active line, it will also be in the lines array.
     */
    private Line currentline; // 
    /**
     * The array index of the currentline.
     */
    private int currentLineNumber;
    /**
     * An array to contain the y-positions to draw the lines at.
     */
    private int[] linepositions;
    //private int colour = 0;
    
    public TextDisplayCanvas()
    {
        super();
        // If you want to use the full screen set this here.  Otherwise it will
        // leave a title and menu bar.  If you change this while running it
        // won't change the text or the way it is displayed at all.
        //setFullScreenMode(true);
        
        // These are why you must do setFullScreenMode either first or not at all.
        height = getHeight();
        width = getWidth();
        
        offScreenImage = Image.createImage(width, height);
        graphic = offScreenImage.getGraphics();
        graphic.setFont(font);
        // (width * 9) / 10 is correct length to have 90% of line used and 5% margins both sides.
        linelength = (width * 9)/10;
        margin = width / 20;
        int fontheight = font.getHeight();
        // I've hardcoded te vertical margin to be at least 8 pixels total
        // between top and an bottom.
        int vMarginMinimumTotal = 8;
        
        // See how many lines of the font we will fit in and create the array
        // of lines.
        lines = new Line[(height - vMarginMinimumTotal)/fontheight];
        // Set the currentLineNumber to -1 as line number is incremented when
        // we add a new line and at that point it will be correct.
        currentLineNumber = -1;
        currentline = addEmptyLine();

        // Set up an array of line positions so that we don't have to calculate them repeatedly.
        linepositions = new int[lines.length];
        for(int i = 0; i < linepositions.length; ++i)
        {
            linepositions[i] = ((height - vMarginMinimumTotal)%fontheight)/2 + i * fontheight;
        }
        
        // Set title of canvas, may confuse things if fullScreenMode is set.
        setTitle("BBC News24");
        
        // Draw to offscreen Image.
        draw();
        
//        currentline.addWord(""+height+" "+fontheight, 0xFF0000, false);
    }
    
    /**
     * Adds a new Line to the screen at the current bottom of the array.  If
     * the array is full then the top Line will be discarded and all other
     * Lines will move up one.  
     * @return A reference to the new Line which is also the currentline
     */
    private Line addEmptyLine()
    {
        if(currentLineNumber + 1 >= lines.length)
        {
            scroll();
        }
        ++currentLineNumber;
        return lines[currentLineNumber] = currentline =  new Line(width - margin, margin);
    }
    
    /**
     * This is really a helper function for addEmptyLine().  It moves every
     * line of text up one line discarding the top one and setting to null the
     * currentline as it as scrolled up a place (probably to be replaced as
     * current by a new line).
     *
     */
    private void scroll()
    {
        for(int i = 1; i < lines.length; ++i)
        {
            lines[i-1] = lines[i];
        }
        lines[currentLineNumber] = null;
        currentline = null;
    }

    /* (non-Javadoc)
     * @see javax.microedition.lcdui.Canvas#paint(javax.microedition.lcdui.Graphics)
     */
    protected void paint(Graphics g)
    {
        g.drawImage(offScreenImage, 0, 0, Graphics.TOP|Graphics.LEFT );
    }
    
    /**
     * This is the main interface to this class and how words are added to be
     * displayed.  It also updates the display.
     * 
     * @param word Typically a word but any String you don't want split between lines.
     * @param colour The colour for this word.
     * @param addSpace If true a space or a newline will be added after the word.
     */
    public void addWord(String word, int colour,boolean addSpace)
    {
        String overflow = currentline.addWord(word, colour, addSpace);
        while(overflow != null)
        {
            addEmptyLine();
            overflow = currentline.addWord(overflow, colour, addSpace);
        }
        draw();
    }
    /**
     * Clears the offscreen image by filling with black, draws all the lines at
     * the correct positions and then repaints to onscreen. 
     */
    private void draw()
    {
        graphic.setColor(0x0);
        graphic.fillRect(0, 0, width, height);
        for(int i = 0; i <= currentLineNumber; ++i)
        {
            ((Line)lines[i]).draw(graphic, linepositions[i]);
        }
        repaint();
    }
    /**
     * Blanks all the lines. 
     */
    public void clear()
    {
        for(int i = 0; i < currentLineNumber; ++i)
        {
            lines[i] = null;
        }
        currentLineNumber = -1;
        currentline = addEmptyLine();
        draw();
    }
    /**
     * Creates a new line and sets that as current.  For paragraph breaks etc.
     */
    public void newline()
    {
        // TODO Auto-generated method stub
        addEmptyLine();
    }
    
 /*   public void displaystring(String s)
    {
        graphic.setColor(0x0);
        graphic.fillRect(0, 0, width, height);
        switch(colour)
        {
        case 0:
            graphic.setColor(0xFFFFFF);
            ++colour;
            break;
        case 1:
            graphic.setColor(0xFF0000);
            ++colour;
            break;
        case 2:
            graphic.setColor(0x00FF00);
            ++colour;
            break;
        case 3:
            graphic.setColor(0xFFFF00);
            colour = 0;
        }
        
        char[] message = s.toCharArray();
        int curpos = 0;
        int lastspace = 0;
        int vpos = 10;
        for(int i = 1; i < message.length; ++i)
        {
            if(message[i] == ' ' || message[i]== '-')
            {
                if(linelength <= font.charsWidth(message, curpos, i-curpos+1))
                {
                    if(lastspace == curpos)
                    {
                        graphic.drawChars(message, curpos, i - curpos, margin, vpos, Graphics.TOP|Graphics.LEFT);
                        curpos = i;
                    }
                    else
                    {
                        graphic.drawChars(message, curpos, lastspace - curpos + 1, margin, vpos, Graphics.TOP|Graphics.LEFT);
                        curpos = lastspace + 1;
                    }
                    lastspace = i;
                    vpos += font.getHeight();
                }
                else
                {
                    lastspace = i;
                }
            }
        }
        graphic.drawChars(message, curpos, message.length - curpos, margin, vpos, Graphics.TOP|Graphics.LEFT);
        repaint();
    }*/
}
