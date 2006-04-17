#!/bin/sh
#

TESTS="\
test_ConsoleEcho.py \
test_NullPayloadRTP.py \
test_RtpPacker.py \
test_MimeRequestComponent.py
"

LOGFILE=test.log

cd test

if [ -f $LOGFILE ]; then
   rm $LOGFILE
fi

for i in $TESTS; do
  echo Running $i | tee -a $LOGFILE
  echo Running $i | sed -e "s/./*/g" >> $LOGFILE
   ./$i -v >>$LOGFILE 2>&1
  echo >> $LOGFILE
  echo >> $LOGFILE
done

