/** Pixel type conversion routines

(C) 2007 British Broadcasting Corporation and Kamaelia Contributors(1)
    All Rights Reserved.

You may only modify and redistribute this under the terms of any of the
following licenses(2): Mozilla Public License, V1.1, GNU General
Public License, V2.0, GNU Lesser General Public License, V2.1

(1) Kamaelia Contributors are listed in the AUTHORS file and at
    http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
    not this notice.
(2) Reproduced in the COPYING file, and at:
    http://kamaelia.sourceforge.net/COPYING
Under section 3.5 of the MPL, we are using this text since we deem the MPL
notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
notice is prohibited.

Please contact us via: kamaelia-list-owner@lists.sourceforge.net
to discuss alternative licensing.
**/

#include <stdlib.h>

int RGB_to_YUV420(unsigned char *rgb_input,
                  unsigned char *y_output,
                  unsigned char *u_output,
                  unsigned char *v_output,
                  int width, int height)
{
    int R, G, B;
    int Y, U, V;

    int row;
    int col;

    int *uline;
    int *vline;
    int *ubuf;
    int *vbuf;

    int *ulineptr;
    int *vlineptr;
    int *ubufptr;
    int *vbufptr;

    int halfwidth;
    halfwidth = width>>1;

    // allocate temporary buffers for filtering U and V components to allow
    // sensible downsampling
    uline = vline = ubuf = vbuf = NULL;

    uline = (int *)calloc( width+2, sizeof(int) );
    vline = (int *)calloc( width+2, sizeof(int) );
    ubuf  = (int *)calloc( halfwidth*(height+2), sizeof(int) );
    vbuf  = (int *)calloc( halfwidth*(height+2), sizeof(int) );

    if ( uline == NULL || vline == NULL || ubuf == NULL || vbuf == NULL )
    {
        free(uline);
        free(vline);
        free(ubuf);
        free(vbuf);
        return -1;
    }

    // pre-pad buffers with default 'zero' values (128)
    uline[0] = uline[width+1] = 128;
    vline[0] = vline[width+1] = 128;
    for(col=0; col<halfwidth; col++)
    {
        ubuf[col] = ubuf[col + halfwidth*(height+1)] = 128;
        vbuf[col] = ubuf[col + halfwidth*(height+1)] = 128;
    }

    // offset base addresses
    uline = uline + 1;
    vline = vline + 1;
    ubuf = ubuf + halfwidth;
    vbuf = vbuf + halfwidth;

    ubufptr = ubuf;
    vbufptr = vbuf;
    for (row=0; row<height; row=row+1)
    {
        ulineptr = uline;
        vlineptr = vline;

        for(col=0; col<width; col++)
        {
            // even numbered pixel
            R = (int)(*(rgb_input++));
            G = (int)(*(rgb_input++));
            B = (int)(*(rgb_input++));

            Y = (( 66*R + 129*G +  25*B + 128)>>8)+ 16;
            U = ((-38*R -  74*G + 112*B + 128)>>8)+128;
            V = ((112*R -  94*G -  18*B + 128)>>8)+128;

            *(y_output++) = (unsigned char)( (Y<0) ? 0 : ((Y>255) ? 255 : Y) );
            *(ulineptr++) = U;
            *(vlineptr++) = V;
        }

        for(col=0; col<width; col=col+2)
        {
            *(ubufptr++) = ( uline[col-1] + 2*uline[col] + uline[col+1] )>>2;
            *(vbufptr++) = ( vline[col-1] + 2*vline[col] + vline[col+1] )>>2;
        }
    }

    ubufptr = ubuf;
    vbufptr = vbuf;
    for (row=0; row<height; row=row+2)
    {
        for(col=0; col<halfwidth; col++)
        {
            U = ( ubufptr[-halfwidth] + 2*(*ubufptr) + ubufptr[+halfwidth] )>>2;
            V = ( vbufptr[-halfwidth] + 2*(*vbufptr) + vbufptr[+halfwidth] )>>2;

            *(u_output++) = (unsigned char)( (U<0) ? 0 : ((U>255) ? 255 : U) );
            *(v_output++) = (unsigned char)( (V<0) ? 0 : ((V>255) ? 255 : V) );

            ubufptr++;
            vbufptr++;
        }
        ubufptr += halfwidth;
        vbufptr += halfwidth;
    }

    uline = uline - 1;
    vline = vline - 1;
    ubuf = ubuf - halfwidth;
    vbuf = vbuf - halfwidth;

    free(uline);
    free(vline);
    free(ubuf);
    free(vbuf);

    return 0;
}




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
