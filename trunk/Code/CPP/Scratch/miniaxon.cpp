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
 */

#include "generators.hpp"
#include <iostream>
#include <list>

using namespace std;

struct Microprocess : public Generator {
    Microprocess()  {     };
    ~Microprocess() {     };
    virtual int next() {
    GENERATOR_CODE_START
        cout << "X Hello!" << endl;
        YIELD(-1);
    GENERATOR_CODE_END
    };
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

/* Simplificaton of Component that just has 1 inbox, 1 outbox, and these may
 * only contain strings.
 */

struct VerySimpleComponent : public Microprocess {
    list<string> inbox;
    list<string> outbox;

    VerySimpleComponent()  {     };
    ~VerySimpleComponent() {     };

    virtual int next() {
    GENERATOR_CODE_START
        cout << "VerySimpleComponent" << endl;
        YIELD(-1);
    GENERATOR_CODE_END
    };

    void send(string value) {
       outbox.push_back(value);
    }
    string recv() {
        string result;
        result = *(inbox.begin());
        inbox.erase(inbox.begin());
        return result;
    }

    void deliver(string value) {
       inbox.push_back(value);
    }
    string collect() {
        string result;
        result = *(outbox.begin());
        outbox.erase(outbox.begin());
        return result;
    }
    bool dataReady() {
       return ! inbox.empty();
    }
    bool dataOutReady() {
       return ! outbox.empty();
    }
};

struct Postman : public VerySimpleComponent {
    VerySimpleComponent* source;
    VerySimpleComponent* destination;
    string temp;
    Postman(VerySimpleComponent* s, VerySimpleComponent* d)  {
       source = s;
       destination = d;
    };
    ~Postman() {     };

    virtual int next() {
    GENERATOR_CODE_START
        while (1) {
           if (source->dataOutReady()) {
              temp = source->collect();
              destination->deliver(temp);
           };
           YIELD(1);
        };
    GENERATOR_CODE_END
    };
};


struct Producer : public VerySimpleComponent {

    Producer()  {     };
    ~Producer() {     };

    virtual int next() {
    GENERATOR_CODE_START
        while(1) {
           send("hello world");
           YIELD(1);
        };
    GENERATOR_CODE_END
    };
};

struct Consumer : public VerySimpleComponent {
    string result;
    Consumer()  {     };
    ~Consumer() {     };

    virtual int next() {
    GENERATOR_CODE_START
        while (1) {
            if (dataReady()) {
               result = recv();
               cout << "! " << result << endl;
            };
            YIELD(1);
        };
    GENERATOR_CODE_END
    };
};

void runScheduler(Scheduler* scheduler) {
   int r;
   while(r!= -1) {
      r = scheduler->next();
   }
}

int main(int, char **) {
   Scheduler scheduler;

//   VerySimpleComponent X;
//   VerySimpleComponent Y;
//   scheduler.activateMicroprocess(&X);
//   scheduler.activateMicroprocess(&Y);
   Producer P;
   Consumer C;
   Postman postie(&P,&C);
   scheduler.activateMicroprocess(&P);
   scheduler.activateMicroprocess(&C);
   scheduler.activateMicroprocess(&postie);
   runScheduler(&scheduler);

   return 0;
}
