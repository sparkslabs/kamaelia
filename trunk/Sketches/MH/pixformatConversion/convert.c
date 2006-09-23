/** Pixel type conversion routines **/


int YUV422_to_RGB(unsigned char *y_input,
                  unsigned char *u_input,
                  unsigned char *v_input,
                  unsigned char *rgb_output,
                  int width, int height)
{
    int R, G, B;
    int Y, U, V;

    int row;
    int col;

    for (row=0; row<height; row++)
    {
        for(col=0; col<width; col=col+2)
        {
            // even numbered pixel
            Y = (int)(*(y_input++));
            U = (int)(*(u_input)) - 128;
            V = (int)(*(v_input)) - 128;

            R = ((298 * Y           + 409 * V + 128) >> 8);
            G = ((298 * Y - 100 * U - 208 * V + 128) >> 8);
            B = ((298 * Y + 516 * U           + 128) >> 8);

            *(rgb_output++) = (unsigned char)( (R<0) ? 0 : ((R>255) ? 255 : R) );
            *(rgb_output++) = (unsigned char)( (G<0) ? 0 : ((G>255) ? 255 : G) );
            *(rgb_output++) = (unsigned char)( (B<0) ? 0 : ((B>255) ? 255 : B) );

            // odd numbered pixel
            Y = (int)(*(y_input++));
            U = (U + (int)(*(u_input++)) - 128)>>1;    // average of previous and next
            V = (V + (int)(*(v_input++)) - 128)>>1;    // average of previous and next

            R = ((298 * Y           + 409 * V + 128) >> 8);
            G = ((298 * Y - 100 * U - 208 * V + 128) >> 8);
            B = ((298 * Y + 516 * U           + 128) >> 8);

            *(rgb_output++) = (unsigned char)( (R<0) ? 0 : ((R>255) ? 255 : R) );
            *(rgb_output++) = (unsigned char)( (G<0) ? 0 : ((G>255) ? 255 : G) );
            *(rgb_output++) = (unsigned char)( (B<0) ? 0 : ((B>255) ? 255 : B) );
        }
    }
    
    return 0;
}



int YUV420_to_RGB(unsigned char *y_input,
                  unsigned char *u_input,
                  unsigned char *v_input,
                  unsigned char *rgb_output,
                  int width, int height)
{
    int R, G, B;
    int Y, U, V;

    int row;
    int col;

    unsigned char *u_inputA;
    unsigned char *v_inputA;
    unsigned char *u_inputB;
    unsigned char *v_inputB;

    for (row=0; row<height; row=row+2)
    {
        u_inputA = u_input;     // remember for when we get to the next row
        v_inputA = v_input;

        //even numbered row
        for(col=0; col<width; col=col+2)
        {
            // even numbered pixel
            Y = (int)(*(y_input++));
            U = (int)(*(u_input)) - 128;
            V = (int)(*(v_input)) - 128;

            R = ((298 * Y           + 409 * V + 128) >> 8);
            G = ((298 * Y - 100 * U - 208 * V + 128) >> 8);
            B = ((298 * Y + 516 * U           + 128) >> 8);

            *(rgb_output++) = (unsigned char)( (R<0) ? 0 : ((R>255) ? 255 : R) );
            *(rgb_output++) = (unsigned char)( (G<0) ? 0 : ((G>255) ? 255 : G) );
            *(rgb_output++) = (unsigned char)( (B<0) ? 0 : ((B>255) ? 255 : B) );

            if (!(col < width)) break;

            // odd numbered pixel
            Y = (int)(*(y_input++));
            U = (U + (int)(*(u_input++)) - 128)>>1;    // average of previous and next
            V = (V + (int)(*(v_input++)) - 128)>>1;    // average of previous and next

            R = ((298 * Y           + 409 * V + 128) >> 8);
            G = ((298 * Y - 100 * U - 208 * V + 128) >> 8);
            B = ((298 * Y + 516 * U           + 128) >> 8);

            *(rgb_output++) = (unsigned char)( (R<0) ? 0 : ((R>255) ? 255 : R) );
            *(rgb_output++) = (unsigned char)( (G<0) ? 0 : ((G>255) ? 255 : G) );
            *(rgb_output++) = (unsigned char)( (B<0) ? 0 : ((B>255) ? 255 : B) );
        }

        if (!(row < height)) break;

        u_inputB = u_input;
        v_inputB = v_input;

        //odd numbered row
        for(col=0; col<width; col=col+2)
        {
            // even numbered pixel
            Y = (int)(*(y_input++));
            U = ((int)(*(u_inputA)) - 128 + (int)(*(u_inputB)) - 128) >> 1;
            V = ((int)(*(v_inputA)) - 128 + (int)(*(v_inputB)) - 128) >> 1;

            R = ((298 * Y           + 409 * V + 128) >> 8);
            G = ((298 * Y - 100 * U - 208 * V + 128) >> 8);
            B = ((298 * Y + 516 * U           + 128) >> 8);

            *(rgb_output++) = (unsigned char)( (R<0) ? 0 : ((R>255) ? 255 : R) );
            *(rgb_output++) = (unsigned char)( (G<0) ? 0 : ((G>255) ? 255 : G) );
            *(rgb_output++) = (unsigned char)( (B<0) ? 0 : ((B>255) ? 255 : B) );

            if (!(col < width)) break;

            // odd numbered pixel
            Y = (int)(*(y_input++));
            U = (U + (((int)(*(u_inputA++)) - 128 + (int)(*(u_inputB++)) - 128) >> 1))>>1;    // average of previous and next
            V = (V + (((int)(*(v_inputA++)) - 128 + (int)(*(v_inputB++)) - 128) >> 1))>>1;    // average of previous and next

            R = ((298 * Y           + 409 * V + 128) >> 8);
            G = ((298 * Y - 100 * U - 208 * V + 128) >> 8);
            B = ((298 * Y + 516 * U           + 128) >> 8);

            *(rgb_output++) = (unsigned char)( (R<0) ? 0 : ((R>255) ? 255 : R) );
            *(rgb_output++) = (unsigned char)( (G<0) ? 0 : ((G>255) ? 255 : G) );
            *(rgb_output++) = (unsigned char)( (B<0) ? 0 : ((B>255) ? 255 : B) );
        }
    }
    
    return 0;
}
