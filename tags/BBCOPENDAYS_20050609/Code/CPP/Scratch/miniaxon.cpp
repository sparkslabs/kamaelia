/*
 * (C) 2004 British Broadcasting Corporation and Kamaelia Contributors(1)
 *     All Rights Reserved.
 *
 * You may only modify and redistribute this under the terms of any of the
 * following licenses(2): Mozilla Public License, V1.1, GNU General
 * Public License, V2.0, GNU Lesser General Public License, V2.1
 *
 * (1) Kamaelia Contributors are listed in the AUTHORS file and at
 *     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
 *     not this notice.
 * (2) Reproduced in the COPYING file, and at:
 *     http://kamaelia.sourceforge.net/COPYING
 * Under section 3.5 of the MPL, we are using this text since we deem the MPL
 * notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
 * notice is prohibited.
 *
 * Please contact us via: kamaelia-list-owner@lists.sourceforge.net
 * to discuss alternative licensing.
 *
 * -------------------------------------------------------------------------
 *
 * This file contains a microcosm proof of concept implementation of a
 * subset of Axon & a simple producer consumer system using this.
 *
 * Compile:
 *  > g++ -o miniaxon miniaxon.cpp
 *
 * Run:
 *  > ./miniaxon
 *
 *
 * This is a rather icky implementation of Axon now, which has many of the
 * normal features of axon - the ability to link arbitrary outboxes to
 * arbitrary inboxes, multiple named inboxes/outboxes, arbitrary message
 * passing. (Subclass IPC_S, and place what you want in a .payload
 * attribute. (doesn't have to have a .payload though).
 *
 */

#include "generators.hpp"
#include <iostream>
#include <list>
#include <map>

using namespace std;

/* Base class for IPC objects */
struct IPC_S {
   virtual string __str__() { }; // Force polymorphic
   int payload;
};

struct Microprocess : public Generator {
    Microprocess()  {     };
    ~Microprocess() {     };
    virtual int next() {
    GENERATOR_CODE_START
        cout << "X Hello!" << endl;
        YIELD(-1);
    GENERATOR_CODE_END
    };
    virtual void run() {
    // This would not normally be run on a microprocess, but may be useful
    // for some circumstances, such as testing.
       int r;
       while(r!= -1) {
          r = next();
       }
    }
};


struct Scheduler : public Microprocess {
    list<Microprocess*> active;
    list<Microprocess*> newqueue;
    list<Microprocess*>::iterator current;

    int i;
    virtual int next() {
    GENERATOR_CODE_START
        i = 0;
        YIELD(1);
        for(i=0; i< 100; i++) {
           newqueue.resize(0);
           for(current=active.begin(); current != active.end(); current++) {
               int result;
               try {
                  result = (*current)->next();
                  if (result != -1) {
                     newqueue.push_back(*current);
                  };
               } catch (StopIteration null){
                  int k;
                  k =1;
               };
           }
           active.resize(0);  // Empty the active queue (unnecessary?)
           active = newqueue; // _Copies_ vector newqueue to active
           YIELD(1);
        };
        YIELD(-1);
    GENERATOR_CODE_END
    };
    void activateMicroprocess(Microprocess* m) {
        active.push_back(m);
    };
};


/* Simplificaton of Component, need to check what it's now missing
 */
struct SimpleComponent : public Microprocess {
    map<string,list<IPC_S*> > outboxes;
    map <string, list<IPC_S*> > inboxes;

    SimpleComponent()  {
       inboxes["inbox"];
       outboxes["outbox"];
    };
    ~SimpleComponent() {     };

    virtual int next() {
    GENERATOR_CODE_START
        cout << "SimpleComponent" << endl;
        YIELD(-1);
    GENERATOR_CODE_END
    };

    void send(IPC_S *value) {   send(value,"outbox"); }
    void send(IPC_S *value, string somebox) {
       outboxes[somebox].push_back(value);
    }

    IPC_S *recv() {   return recv("inbox"); }
    IPC_S *recv(string somebox) {
        IPC_S *result;
        result = *(inboxes[somebox].begin());
        inboxes[somebox].erase(inboxes[somebox].begin());
        return result;
    }

    void deliver(IPC_S *value, string somebox) {
       inboxes[somebox].push_back(value);
    }
    IPC_S *collect(string somebox) {
        IPC_S *result;
        result = *(outboxes[somebox].begin());
        outboxes[somebox].erase(outboxes[somebox].begin());
        return result;
    }
    bool dataReady() { return dataReady("inbox");    }
    bool dataReady(string somebox) {
       return ! inboxes[somebox].empty();
    }
    bool dataOutReady(string somebox) {
       return ! outboxes[somebox].empty();
    }
};

struct Postman : public SimpleComponent {
    SimpleComponent* source;
    string sourcebox;
    SimpleComponent* destination;
    string destbox;
    IPC_S * temp;
    Postman(SimpleComponent* s, SimpleComponent* d)  {
       source = s;
       destination = d;
       sourcebox = "outbox";
       destbox = "inbox";
    };
    Postman(SimpleComponent* s, string sbox, SimpleComponent* d, string dbox)  {
       source = s;
       destination = d;
       sourcebox = sbox;
       destbox = dbox;
    };
    ~Postman() {     };

    virtual int next() {
    GENERATOR_CODE_START
        while (1) {
           if (source->dataOutReady(sourcebox)) {
              temp = source->collect(sourcebox);
              destination->deliver(temp,destbox);
           };
           YIELD(1);
        };
    GENERATOR_CODE_END
    };
};

/**********************************************************************
 *
 * Sample Producer/Consumer system, passing IPC messages with a string as
 * payload.
 *
 */

struct mystring : public IPC_S{
   string payload;
};

struct Producer : public SimpleComponent {

    mystring msg;
    Producer()  {     };
    ~Producer() {     };

    virtual int next() {
    GENERATOR_CODE_START
        while(1) {
           msg.payload = "hello world!";
           send(&msg);
           YIELD(1);
        };
    GENERATOR_CODE_END
    };
};

struct Consumer : public SimpleComponent {
    mystring *result;

    Consumer()  {     };
    ~Consumer() {     };

    virtual int next() {
    GENERATOR_CODE_START
        while (1) {
            if (dataReady()) {
               result = dynamic_cast<mystring *>(recv());
               cout << "! " << result->payload << endl;
            };
            YIELD(1);
        };
    GENERATOR_CODE_END
    };
};

/*
 * End of sample system.
 *
 **********************************************************************/

int main(int, char **) {
   Scheduler scheduler;

   Producer P;
   Consumer C;
   Postman postie(&P,"outbox", &C, "inbox"); // Same as postie(&P,&C)
   scheduler.activateMicroprocess(&P);
   scheduler.activateMicroprocess(&C);
   scheduler.activateMicroprocess(&postie);
   scheduler.run();

   return 0;
}
