#!/usr/bin/env python2.3
#
# Full coverage testing of the Internet Connection module.
#

# Test the module loads
import unittest, os, sys
sys.path.append("..")
import InternetConnection

from socket import socket,error
import random

class test_PrimaryListenSocket(unittest.TestCase):
   def test_smokeTest_noPorts(self):
      """Smoke test of PLS, no ports to listen on"""
      PLS=InternetConnection.PrimaryListenSocket()
      self.assertEqual(PLS.listeners, [])
      self.assertEqual(PLS.writers, [])
      self.assertEqual(PLS.allsocks, [])
      self.assertEqual(PLS.lookup, {})
      self.assertEqual(PLS.postoffice.debugname, "PLSPostman")

   def test_smokeTest_withPorts(self):
      """Smoke test of PLS, 3 ports to listen on"""
      ports = [ random.randint(2000,2099), random.randint(3000,3099), random.randint(4000,4099) ]
      PLS=InternetConnection.PrimaryListenSocket(ports)
      self.assert_(PLS.listeners is not None)
      self.assert_(PLS.listeners.__class__ is list)
      self.assertEqual(len(PLS.listeners), len(ports))
      for listener in PLS.listeners:
         self.assert_(listener.__class__ is socket)
      self.assertEqual(PLS.writers, [])

      self.assert_(PLS.allsocks is not None)
      self.assert_(PLS.allsocks.__class__ is list)
      self.assertEqual(len(PLS.allsocks), len(ports))
      for sock in PLS.allsocks:
         self.assert_(sock.__class__ is socket)
      self.assert_(PLS.allsocks is not PLS.listeners)

      self.assertEqual(PLS.lookup, {})
      self.assertEqual(PLS.postoffice.debugname, "PLSPostman")

   def test_makeTCPServerPort_smokeTest(self):
      """Internal Diagnostic: Check that creating a PLS & TCP Server Port functions"""
      PLS=InternetConnection.PrimaryListenSocket()
      s,port = PLS.makeTCPServerPort(minrange=9000,maxrange=9999)

      self.assert_(port.__class__ is int)
      self.assert_(s is not None)
      self.assert_(s.__class__ is socket)
      self.assert_(9000 <= port <= 9999)

   def test_makeTCPServerPort_smokeTest_checkHaveCorrectPort_PlatformAgnostic(self):
      """Internal Diagnostic: Check on TCP server socket opening (platform agnostic)"""
      PLS=InternetConnection.PrimaryListenSocket()
      s,port = PLS.makeTCPServerPort(minrange=9000,maxrange=9999)
      self.assert_(port.__class__ is int)
      self.assert_(s is not None)
      self.assert_(s.__class__ is socket)
      self.assert_(9000 <= port <= 9999)
      # Attempting to reopen a socket on the same port should fail if opening server port worked last time
      self.assertRaises(error, PLS.makeTCPServerPort,port)

   def test_makeTCPServerPort_smokeTest_checkHaveCorrectPort_RequiresLinux(self):
      """Internal Diagnostic: Check on TCP server socket opening (Linux specific, Skipped on other architectures)"""
      PLS=InternetConnection.PrimaryListenSocket()
      s,port = PLS.makeTCPServerPort(minrange=9000,maxrange=9999)
      self.assert_(port.__class__ is int)
      self.assert_(s is not None)
      self.assert_(s.__class__ is socket)
      self.assert_(9000 <= port <= 9999)
      if os.name=="posix":
         unameF=os.popen("uname")
         uname=""
         for i in unameF:
            uname=i
         unameF.close()
         if uname=='Linux\n':
            "-p flag we're relying on I've generally only seen on linux"
            "We're also very specific on python binary name here"
            fh=os.popen("netstat 2>&1 -natp|grep python2.3|grep LISTEN|awk '{print $4}'|cut -d: -f2")
            portString=""
            for i in fh:
               portString=i
            self.assert_(int(portString), port)
            return
      print "WARNING, netstat -p based test not performed. (Linux specific)"

   def test_makeListenPorts(self):
      """Internal Diagnostic: Test that the code for creating a list of ports to listen on works"""
      PLS=InternetConnection.PrimaryListenSocket()
      ports = [ random.randint(2100,2199), random.randint(3100,3199), random.randint(4100,4199) ]
      listeners = PLS.makeListenPorts(ports)
      self.assert_(listeners is not None)
      # Further checks are made in the smoke tests above.

   def test___str__(self):
      """Check expected str of bare PLS"""
      PLS=InternetConnection.PrimaryListenSocket()
      self.assertEqual(str(PLS), "PrimaryListenSocket [[[ Component <class 'InternetConnection.PrimaryListenSocket'>_3 [ inboxes : {'OOBcontrol': [], 'DataSend': [], '_csa_feedback': []} outboxes : {'DataRecieve': [], 'OOBInfo': []} ]]]")


class safesend_Test(unittest.TestCase):
   pass

if 0:
   s,port=makeTestTCPServer()
   print "PORT", port
   import time
   time.sleep(3)
   port=makeTestServer(port)
   print "PORT", port


if __name__=="__main__":
   unittest.main()



