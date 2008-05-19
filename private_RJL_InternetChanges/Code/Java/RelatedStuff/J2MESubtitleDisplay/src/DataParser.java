/*
 * Created on 07-May-2004
 *
 * To change the template for this generated file go to
 * Window - Preferences - Java - Code Generation - Code and Comments
 */
/**
 * @author Joseph Lord
 * 
 * Receives byte arrays and turns them into Strings by naively assumming that
 * it will only receive single byte characters in native character set.  These
 * happen to be correct assumptions for the subtitle data stream so it works
 * here. 
 */
public class DataParser
{
    //private final int bufsize = 2048;
//    StringBuffer strbuf = new StringBuffer();
//    int bufpos = 0;
//    int scanpos = 0;
//    int nextfree =0;
    
//    String delimit;
    
    TextParser sink;
    /**
     * 
     * @param out Set the destination of parsed text.  Could be generalised if TextParser implemented an interface so this could be more generic.
     */
    DataParser(TextParser out)//, String delimter)
    {
        sink = out;
 //       delimit = delimter;
    }
    
    /**
     * The main method that receives and passes on the data.
     * 
     * @param data The raw binary data.
     * @return Always true.
     */
    public boolean handleData(byte [] data)
    {
        return handleData(data, data.length);
    }
    /**
     * Receives a byte sequence and reads from start converting to a String to
     * pass to the sink obect.  It drops anything that won't convert as a
     * single byte character or that is a '/r' or a '/n'.
     *  
     * @param data The binary data to process.
     * @param len The length of the data to process, can be less than the full byte array.
     * @return Always true.
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
