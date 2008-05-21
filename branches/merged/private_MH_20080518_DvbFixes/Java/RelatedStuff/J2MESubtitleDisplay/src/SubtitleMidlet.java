import javax.microedition.lcdui.Alert;

import javax.microedition.lcdui.Display;
//import javax.microedition.media.Manager;
import javax.microedition.midlet.MIDlet;
import javax.microedition.midlet.MIDletStateChangeException;

// Nokia only API.  Can be removed or replace with another method of turning the lights on.
import com.nokia.mid.ui.DeviceControl;

/*
 * Created on 27-Apr-2005
 *
 * To change the template for this generated file go to
 * Window - Preferences - Java - Code Generation - Code and Comments
 */

/**
 * @author Joseph Lord
 * 
 * The top level class of the Subtitle Midlet.  Sets up all the other
 * components, joins them together and sets them running.
 *
 */
public class SubtitleMidlet extends MIDlet
{

    /**
     * 
     */
    public SubtitleMidlet()
    {
        super();
    }

    /**
     * List of things done here:
     * 
     * On Series 40 Nokias it turns on the backlight.
     * 
     * Creates TCPConnecion, connects it and starts the network reading thread.
     * 
     * Creates and sets the display to a TextDisplayCanvas
     * 
     * Creates a TextParser and DataParser set to pass the data through to the TextDisplayCanvas
     * 
     * 
     */
    protected void startApp() throws MIDletStateChangeException
    {
        Thread readthread;
        try
        {
            // This only works on S40 Nokias.  Different versions could probably be
            // built for other phones to turn their backlights on.
            DeviceControl.setLights(0,100); // Turns on the backlight on Nokias.
        }
        finally{}// If DeviceControl does not exist or fails it doesn't matter but backlight may go off.
        try
        {
        TextDisplayCanvas tdc = new TextDisplayCanvas();
        Display.getDisplay(this).setCurrent(tdc);
        TextParser tp = new TextParser(tdc);
        DataParser dp = new DataParser(tp);
        TCPConnection tcpcon = new TCPConnection(dp,Display.getDisplay(this));
        tcpcon.connect("socket://132.185.133.22:1500");
//        DataParser dp = new DataParser(tp);
        readthread = new Thread(tcpcon);
        readthread.start();
        tdc.repaint();
        }
        catch(Exception e)
        {
            Display.getDisplay(this).setCurrent(new Alert("Exception",e.toString(),null,null));
            e.printStackTrace();
        }
    }

    /* (non-Javadoc)
     * @see javax.microedition.midlet.MIDlet#pauseApp()
     */
    protected void pauseApp()
    {
    // TODO Auto-generated method stub

    }

    /* (non-Javadoc)
     * @see javax.microedition.midlet.MIDlet#destroyApp(boolean)
     */
    protected void destroyApp(boolean arg0) throws MIDletStateChangeException
    {
        try
        {
            DeviceControl.setLights(0,0); // Turns off the lights on Nokias.
        }
        finally{}
    }

}
