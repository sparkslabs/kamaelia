#!/bin/sh

gifsicle --disposal=bg --colors 256 --loop \
--delay=400 carousel_anim01.gif        \
--delay=400 carousel_anim02.gif        \
--delay=500 carousel_anim03.gif        \
--delay=200 carousel_anim04.gif        \
--delay=350 carousel_anim05.gif        \
--delay=500 carousel_anim06.gif        \
--delay=400 carousel_anim07.gif        \
--delay=200 carousel_anim08.gif        \
> carousel_anim.gif

cp carousel_anim.gif ../
