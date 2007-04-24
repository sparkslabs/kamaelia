#!/bin/sh
#

mkdir build
# Reason for using python here:
#    1) We're installing python libraries, if this fails, everything else does
#    2) The command syntax for "date" and friends differs on different unix platforms
#    3) By contrast, the example above is the same.

TIME=`python -c 'import time; print time.time()'`
INSTALLLOG=`pwd`/install-TIME.log

(
    cd build
    echo "Unpacking Axon-1.1.2" | tee -a $INSTALLLOG
    tar zxf ../Axon-1.1.2.tar.gz
    cd Axon-1.1.2
    echo "Installing Axon-1.1.2" | tee -a $INSTALLLOG
    sudo python setup.py --quiet install 2>&1 >> $INSTALLLOG
)

(
    cd build
    echo "Unpacking Kamaelia-0.3.0" | tee -a $INSTALLLOG
    tar zxf ../Kamaelia-0.3.0.tar.gz
    cd Kamaelia-0.3.0
    echo "Installing Kamaelia-0.3.0" | tee -a $INSTALLLOG
    sudo python setup.py --quiet install 2>&1 >> $INSTALLLOG
)

(
    cd build
    echo "Unpacking pygame-1.7.1release" | tee -a $INSTALLLOG
    tar zxf ../pygame-1.7.1release.tar.gz
    cd pygame-1.7.1release
    echo "Installing pygame-1.7.1release" | tee -a $INSTALLLOG
    sudo python setup.py --quiet install 2>&1 >> $INSTALLLOG
)

(
    cd build
    echo "Unpacking dirac-0.5.4" | tee -a $INSTALLLOG
    tar zxf ../dirac-0.5.4.tar.gz
    cd dirac-0.5.4
    echo "Installing dirac-0.5.4" | tee -a $INSTALLLOG
    (
       echo "Configuring dirac-0.5.4" &&
       ./configure 2>&1 >> $INSTALLLOG &&
       echo "Building dirac-0.5.4" &&
       make 2>&1 >> $INSTALLLOG && 
       echo "Installing dirac-0.5.4" &&
       sudo make install 2>&1 >> $INSTALLLOG
    )
    sudo /sbin/ldconfig
)

(
    cd build
    echo "Unpacking Pyrex-0.9.3.1" | tee -a $INSTALLLOG
    tar zxf ../Pyrex-0.9.3.1.tar.gz
    cd Pyrex-0.9.3.1
    echo "Installing Pyrex-0.9.3.1" | tee -a $INSTALLLOG
    sudo python setup.py --quiet install 2>&1 >> $INSTALLLOG
)

(
    cd build
    echo "Unpacking Dirac-0.0.1" | tee -a $INSTALLLOG
    tar zxf ../Dirac-0.0.1.tar.gz
    cd Dirac-0.0.1
    echo "Installing Dirac-0.0.1" | tee -a $INSTALLLOG
    sudo python setup.py --quiet install 2>&1 >> $INSTALLLOG
)

(
    cd build
    echo "Unpacking libogg-1.1.3" | tee -a $INSTALLLOG
    tar zxf ../libogg-1.1.3.tar.gz
    cd libogg-1.1.3
    echo "Installing libogg-1.1.3" | tee -a $INSTALLLOG
        (
          echo "Configuring libogg-1.1.3" &&
          ./configure 2>&1 >> $INSTALLLOG &&
          echo "Building libogg-1.1.3" &&
          make 2>&1 >> $INSTALLLOG && 
          echo "Installing libogg-1.1.3" &&
         sudo make install 2>&1 >> $INSTALLLOG
       )
    sudo /sbin/ldconfig
) &&
(
    cd build
    echo "Unpacking libvorbis-1.1.2" | tee -a $INSTALLLOG
    tar zxf ../libvorbis-1.1.2.tar.gz
    cd libvorbis-1.1.2
    echo "Installing libvorbis-1.1.2" | tee -a $INSTALLLOG
        (
          echo "Configuring libvorbis-1.1.2" &&
          ./configure 2>&1 >> $INSTALLLOG &&
          echo "Building libvorbis-1.1.2" &&
          make 2>&1 >> $INSTALLLOG && 
          echo "Installing libvorbis-1.1.2" &&
         sudo make install 2>&1 >> $INSTALLLOG
       )
    sudo /sbin/ldconfig
) &&
(
    cd build
    echo "Unpacking libao-0.8.6" | tee -a $INSTALLLOG
    tar zxf ../libao-0.8.6.tar.gz
    cd libao-0.8.6
    echo "Installing libao-0.8.6" | tee -a $INSTALLLOG
        (
          echo "Configuring libao-0.8.6" &&
          ./configure 2>&1 >> $INSTALLLOG &&
          echo "Building libao-0.8.6" &&
          make 2>&1 >> $INSTALLLOG && 
          echo "Installing libao-0.8.6" &&
         sudo make install 2>&1 >> $INSTALLLOG
       )
    sudo /sbin/ldconfig
)

(
    cd build
    echo "Unpacking vorbissimple-0.0.1" | tee -a $INSTALLLOG
    tar zxf ../vorbissimple-0.0.1.tar.gz
    cd vorbissimple-0.0.1
    ( cd libvorbissimple
        echo "Installing libvorbissimple" | tee -a $INSTALLLOG
        (
          echo "Configuringlibvorbissimple" &&
          ./configure 2>&1 >> $INSTALLLOG &&
          echo "Building libvorbissimple" &&
          make 2>&1 >> $INSTALLLOG && 
          echo "Installing libvorbissimple" &&
         sudo make install 2>&1 >> $INSTALLLOG
       )
        sudo /sbin/ldconfig 
    ) &&
    (
        cd python
        echo "Installing libvorbissimple python bindings" | tee -a $INSTALLLOG
        sudo python setup.py --quiet install  2>&1 >> $INSTALLLOG
    )
)

(
    cd build/
    echo "Unpacking pyao-0.82" | tee -a $INSTALLLOG
    tar zxf ../pyao-0.82.tar.gz
    cd pyao-0.82
    echo "Installing pyao-0.82" | tee -a $INSTALLLOG
    ./config_unix.py
    sudo python setup.py --quiet install 2>&1 >> $INSTALLLOG
)

(
    cd build
    echo "Unpacking python-dvb3-0.0.4" | tee -a $INSTALLLOG
    tar zxf ../python-dvb3-0.0.4.tar.gz
    cd python-dvb3-0.0.4
    echo "Installing python-dvb3-0.0.4" | tee -a $INSTALLLOG
    sudo python setup.py --quiet install 2>&1 >> $INSTALLLOG
)

