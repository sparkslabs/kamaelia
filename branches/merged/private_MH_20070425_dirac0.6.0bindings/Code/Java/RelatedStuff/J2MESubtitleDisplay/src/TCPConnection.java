import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

import javax.microedition.io.Connector;
import javax.microedition.io.SocketConnection;
import javax.microedition.lcdui.Alert;
import javax.microedition.lcdui.Display;


/*
 * Created on 05-May-2004
 *
 * To change the template for this generated file go to
 * Window - Preferences - Java - Code Generation - Code and Comments
 */

/**
 * @author Joseph Lord
 *
 * Wraps the necessary to handle creation of TCP connection and also
 * reconnection if the connection is lost. 
 *
 */
public class TCPConnection implements Runnable
{
    /**
     * The target to send the data to.
     */
    private DataParser sink;
//    DataReceiver sink;
    /**
     * Determines whether the socket is or should be connected.
     */
    private boolean connected = false;
    /**
     * The address to connect to/we are connected to.
     */
    private String address;
    /**
     * InputStream of the connected socket.
     */
    private InputStream is;
    /**
     * OutputStream of the connected socket - not used ATM in Subtitle Midlet. 
     */
    private OutputStream os;
    /**
     * The SocketConnection which is the source of the input and output streams.
     */
    private SocketConnection stream;
    /**
     * A temporary storage of the last caught and ignored network exception.
     */
    Exception lastexception;
    /**
     * The main display object so that it can display Exception messages, this
     * is useful for debugging but should probably be removed when they are all
     * handled.
     */
    Display disp;
    /**
     * 
     * @param tp The object to pass received data to.
     * @param dis The main Display object so that alerts can be displayed on
     *   exceptions.
     */
    TCPConnection(DataParser tp, Display dis)//DataReceiver datasink)
    {
        sink = tp;
        disp = dis;
    }
    /**
     * Attempts to connect to socket and set it up for ongoing streamed data
     * and to create the associated input and output streams.
     * 
     * @param conaddress The address to connect to in "socket://123.456.789.123:4567" format.
     * @return true if it suceeds in connecting.
     * @throws IOException as thrown by several different socket operations.
     */
    boolean connect(String conaddress) throws IOException
    {
        if(connected)
        {
            return false;
        }
        this.address = conaddress;
        stream = (SocketConnection) Connector.open(address);
        stream.setSocketOption(SocketConnection.KEEPALIVE, 1);
//        stream.setSocketOption(SocketConnection.DELAY, 0);
//        stream.setSocketOption(SocketConnection.RCVBUF, 25);
        is = stream.openInputStream();
        os = stream.openOutputStream();
//        isr = new InputStreamReader(is);
        connected = true;
        return true;
    }

    /**
     * Sends data to the connected socket.  Wrapper round sendData to implement DataReceiver if required.
     * 
     * @param data The data to send.
     * @return true if sending suceeds.
     */
    public boolean handleData(byte[] data)
    {
        return sendData(data);
    }
    /**
     * Sends data to the connected socket.
     * 
     * @param data The data to send.
     * @return true if sending suceeds.
     */
    public boolean sendData(byte[] data)
    {
        if(connected)
        {
            try
            {
                
                os.write(data);
                os.flush();
                return true;
            }
            catch(IOException e)
            {
                lastexception = e;
                return false;
            }
        }
        return false;
    }
    

    /**
     * The socket runs in a thread reading data and passing it on.  This is run when the thread is started.
     */
    public void run()
    {
        while(connected)
        {
            readDataRobust();
        }
        
    }
    
    /**
     * Reads data and passes it to sink.  Catches exceptions and displays an
     * error message.  Tries to reconnect if disconnected.
     *
     */
    public void readDataRobust()
    {
        try
        {
            readData();
        }
        catch(Exception e)
        {
            disp.setCurrent(new Alert("Read Exception",e.toString(),null,null),disp.getCurrent());
            lastexception = e;
            disconnect();
            reconnect();
            
        }
    }

    /**
     * Reads available data from socket and passes to the the sink DataParser.
     * 
     * @throws IOException Any network exception.
     */
         private void readData() throws IOException
    {
//        int ch = isr.read();
        int bufsize = 40;
        byte[] mesage = new byte[bufsize];
        while(connected)
        {
         //   sink.handleData(ch);
         //   ch = isr.read();
            int readydata = is.available();
            if(readydata > 0)
            {
                if(readydata > bufsize)
                {
                    bufsize = readydata;
                    mesage = new byte[bufsize];
                }
                int readdata = is.read(mesage,0, readydata);
                if(readdata > 0)
                {
     //               disp.setCurrent(new Alert("Data", new String(mesage),null,null), disp.getCurrent());
                    sink.handleData(mesage, readdata);
                }
                else if(readdata == -1)
                {
                    break;
                }
            }
            else
            {
                try{
                    Thread.sleep(100);
                }
                catch(Exception e)
                {}
            }
        }
    }
    

    /**
     * Repeatedly tries to reconnect the socket with a short fixed timeout between attempts. 
     */
    private void reconnect()
    {
        disconnect();
        while(!connected)
        {
        try
        {
        connect(address);
        }
        catch(Exception e)
        // TODO This should be far more specific and handle errors better.
        {
            
        }
        try
        {
        Thread.sleep(2000);
        }
        catch(Exception e){}
        }
    }

    /**
     * Disconnects and closes the streams.
     */
    public void disconnect()
    {
        connected = false;
        try
        {
        os.close();
        is.close();
        stream.close();
        }
        catch(Exception e)
        {}
        
    }
    

}
