#!/bin/sh

./EIT_Compiler.py -i test_schedule \
    -s service-id-1000.conf \
    -g test_config \
    -c schedule.sections \
    -p pf.sections \
    -t 0 \
    -n 2008-05-24T16:35:00
