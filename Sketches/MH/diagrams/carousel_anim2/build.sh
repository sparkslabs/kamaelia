#!/bin/sh

gifsicle --disposal=bg --colors 256 --loop \
--delay=400 01.gif        \
--delay=200 02.gif        \
--delay=100 03.gif        \
--delay=200 04.gif        \
> carousel_anim2.gif

cp carousel_anim2.gif ../
