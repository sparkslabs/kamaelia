import javax.microedition.lcdui.Alert;

import javax.microedition.lcdui.Display;
//import javax.microedition.media.Manager;
import javax.microedition.midlet.MIDlet;
import javax.microedition.midlet.MIDletStateChangeException;


import com.nokia.mid.ui.DeviceControl;

/*
 * Created on 27-Apr-2005
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
public class SubtitleMidlet extends MIDlet
{

    /**
     * 
     */
    public SubtitleMidlet()
    {
        super();
        // TODO Auto-generated constructor stub
    }

    /* (non-Javadoc)
     * @see javax.microedition.midlet.MIDlet#startApp()
     */
    protected void startApp() throws MIDletStateChangeException
    {
        Thread readthread;
        try
        {
            DeviceControl.setLights(0,100); // Turns on the backlight on Nokias.
        }
        finally{}
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
