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
 * @author josephl
 *
 * To change the template for this generated type comment go to
 * Window - Preferences - Java - Code Generation - Code and Comments
 */
public class TCPConnection implements Runnable
{
    DataParser sink;
//    DataReceiver sink;
    boolean connected = false;
    String address;
    InputStream is;
    OutputStream os;
    SocketConnection stream;
    Exception lastexception;
    Display disp;
    TCPConnection(DataParser tp, Display dis)//DataReceiver datasink)
    {
        sink = tp;
        disp = dis;
    }
    
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

    /* (non-Javadoc)
     * @see DataReceiver#handleData(java.lang.Byte[])
     */
    public boolean handleData(byte[] data)
    {
        return sendData(data);
    }
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
    

    /* (non-Javadoc)
     * @see java.lang.Runnable#run()
     */
    public void run()
    {
        while(connected)
        {
            readDataRobust();
        }
        
    }
    
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
     * 
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
    
    byte readByte() throws IOException
    {
        int tmp;
        tmp = is.read();
        if(tmp ==-1)
        {
            throw new IOException("End of connection.");
        }
        return (byte)tmp;
    }

    /**
     * 
     */
    private void reconnect()
    {
        // TODO Auto-generated method stub
        disconnect();
        while(!connected)
        {
        try
        {
        connect(address);
        }
        catch(Exception e)
        {
            
        }
        try
        {
        Thread.sleep(500);
        }
        catch(Exception e){}
        }
    }

    /**
     * 
     */
    public void disconnect()
    {
        // TODO Auto-generated method stub
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
