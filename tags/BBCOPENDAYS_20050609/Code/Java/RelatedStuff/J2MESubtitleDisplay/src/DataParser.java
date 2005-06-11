/*
 * Created on 07-May-2004
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
public class DataParser
{
    //private final int bufsize = 2048;
//    StringBuffer strbuf = new StringBuffer();
    int bufpos = 0;
    int scanpos = 0;
    int nextfree =0;
    
    String delimit;
    
    TextParser sink;
    DataParser(TextParser out)//, String delimter)
    {
        sink = out;
 //       delimit = delimter;
    }
    
    public boolean handleData(byte [] data)
    {
        return handleData(data, data.length);
    }
    /* (non-Javadoc) 
     * @see DataReceiver#handleData(byte[])
     */
    public boolean handleData(byte[] data,int len)
    {
        StringBuffer strbuf = new StringBuffer();
        for(int i = 0; i < len; i++)
        {
            char c = (char)data[i];
            if(c < 0x80 && c != '\r' && c != '\n') // Single byte character - drop all multibyte UTF
            {
                strbuf.append(c);
            }
        }
        String s = strbuf.toString();
        sink.handleString(s);
        return true;
    }
    


    
    
}
