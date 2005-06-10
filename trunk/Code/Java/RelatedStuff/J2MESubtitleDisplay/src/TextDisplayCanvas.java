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
 * @author josephl
 *
 * To change the template for this generated type comment go to
 * Window - Preferences - Java - Code Generation - Code and Comments
 */
public class TextDisplayCanvas extends Canvas
{
    private class Line
    {
        private Vector phrases = new Vector(3);
        private int rmargin;
        private int initialpos;
        /**
         * @param rmargin
         * @param initialpos
         */
        Line(int rmargin, int initialpos)
        {
            this.rmargin = rmargin;
            this.initialpos = initialpos;
        }
        String addWord(String s, int colour, boolean addspace)
        {
            
            if(!phrases.isEmpty())
            {
                Phrase cur = ((Phrase)phrases.lastElement());
                if(cur.getColour() == colour) 
                {//New word is same colour as last
                    return cur.addWord(s, addspace);
                }
                else
                {
                    cur = new Phrase(cur.getEndpos(),rmargin,colour,false);
                    String result = cur.addWord(s, addspace);
                    if(!s.equals(result))
                    {
                        phrases.addElement(cur);
                    }
                    return result;
                }
            }
            Phrase initial = new Phrase(initialpos,rmargin,colour,addspace);
            phrases.addElement(initial);
//            try{Manager.playTone(127, 500, 100);}catch (MediaException e) {}
            return initial.addWord(s, addspace);
        }
        void draw(Graphics g, int ypos)
        {
            for(int i = 0; i < phrases.size(); ++i)
            {
                ((Phrase)phrases.elementAt(i)).draw(g, ypos);
            }
        }
        
    }
    private class Phrase
    {
        private int offset;
        private int maxX;
        private int endpos;
        private StringBuffer phrase;
        int spacewidth;
        private int colour;
        private boolean linestart;
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
        protected String addWord(String s, boolean addspace)
        {
            
            int wordwidth = font.stringWidth(s);
            if(wordwidth + endpos <= maxX)
            {
                linestart = false;
                endpos += wordwidth;
                phrase.append(s);
                if(addspace)
                {
                   endpos += spacewidth;
                   phrase.append(' ');
                }
                return null;
            }
            else if(endpos == offset && linestart) //The word is more than a line put as much as possible in.
            {
                char[] ca = s.toCharArray();
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
                return s;
            }
        }
        protected void draw(Graphics g, int ypos)
        {
            g.setColor(colour);
            g.drawString(phrase.toString(), offset, ypos, Graphics.TOP |Graphics.LEFT);
        }
        
        /**
         * @return Returns the colour.
         */
        int getColour()
        {
            return colour;
        }
        /**
         * @return Returns the endpos.
         */
        int getEndpos()
        {
            return endpos;
        }
    }
    private Graphics graphic;
    private Image offScreenImage;
    private int height;
    private int width;
    private int linelength;
    static Font font = Font.getFont(Font.FACE_MONOSPACE, Font.STYLE_PLAIN, Font.SIZE_LARGE);
    private int margin;
    private Line[] lines;
    private Line currentline;
    private int nocurrentline;
    private int[] linepositions;
    //private int colour = 0;
    /**
     * 
     */
    public TextDisplayCanvas()
    {
        super();
        //setFullScreenMode(true);
        height = getHeight();
        width = getWidth();
        offScreenImage = Image.createImage(width, height);
        graphic = offScreenImage.getGraphics();
//        font = Font.getFont(Font.FACE_MONOSPACE, Font.STYLE_PLAIN, Font.SIZE_LARGE);
        graphic.setFont(font);
        linelength = (width * 9)/10;
        margin = width / 20;
        int fontheight = font.getHeight();
        lines = new Line[(height - 8)/fontheight];
        nocurrentline = -1;
        currentline = addEmptyLine();
        linepositions = new int[lines.length];
        for(int i = 0; i < linepositions.length; ++i)
        {
            linepositions[i] = ((height - 8)%fontheight)/2 + i * fontheight;
        }
        setTitle("BBC News24");
        draw();
        repaint();
//        currentline.addWord(""+height+" "+fontheight, 0xFF0000, false);
    }
    private Line addEmptyLine()
    {
        if(++nocurrentline >= lines.length)
        {
            scroll();
        }
        return lines[nocurrentline] = currentline =  new Line(width - margin, margin);
    }
    private void scroll()
    {
        for(int i = 1; i < lines.length; ++i)
        {
            lines[i-1] = lines[i];
        }
        lines[--nocurrentline] = null;
    }

    /* (non-Javadoc)
     * @see javax.microedition.lcdui.Canvas#paint(javax.microedition.lcdui.Graphics)
     */
    protected void paint(Graphics g)
    {
        g.drawImage(offScreenImage, 0, 0, Graphics.TOP|Graphics.LEFT );
    }
    
    public void addWord(String word, int colour,boolean addSpace)
    {
        String overflow = currentline.addWord(word, colour, addSpace);
        while(overflow != null)
        {
            addEmptyLine();
            overflow = currentline.addWord(overflow, colour, addSpace);
        }
        draw();
        repaint();
    }
    private void draw()
    {
        graphic.setColor(0x0);
        graphic.fillRect(0, 0, width, height);
        for(int i = 0; i <= nocurrentline; ++i)
        {
            ((Line)lines[i]).draw(graphic, linepositions[i]);
        }
        repaint();
    }
    /**
     * 
     */
    public void clear()
    {
        // TODO Auto-generated method stub
        for(int i = 0; i < nocurrentline; ++i)
        {
            lines[i] = null;
        }
        nocurrentline = -1;
        currentline = addEmptyLine();
        draw();
        repaint();
    }
    /**
     * 
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
