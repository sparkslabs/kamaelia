/** Cut detector **/


double ComputeMAD( unsigned char *prev,
                   unsigned char *curr,
                   int size
                 )
{
    unsigned int total;

    unsigned char *prevpixel = prev + size;
    unsigned char *currpixel = curr + size;

    total = 0;

    while (prevpixel > prev)
    {
        currpixel--;
        prevpixel--;

        total += abs((*prevpixel) - (*currpixel));
    }
    
    return ((double)total) / ((double)(size));
};


