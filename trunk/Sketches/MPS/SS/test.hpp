#ifndef __TEST_HPP
#define __TEST_HPP

#include "builtin.hpp"

using namespace __shedskin__;
namespace __test__ {

class microprocess;
class scheduler;
class component;
class postman;
class Producer;
class Consumer;

typedef __iter<int> *(*lambda0)(microprocess *);
typedef __iter<int> *(*lambda1)(component *);
typedef __iter<int> *(*lambda2)(postman *);
typedef __iter<int> *(*lambda3)(Producer *);
typedef __iter<int> *(*lambda4)(Consumer *);

extern class_ *cl_microprocess;
class microprocess : public pyobj {
public:
    static void *__init__;

    str *name;

    microprocess();
    microprocess(str *name);
};

extern class_ *cl_scheduler;
class scheduler : public microprocess {
public:
    list<__iter<int> *> *newqueue;
    list<__iter<int> *> *active;

    int activateMicroprocess(lambda0 some_gen, microprocess *some_obj);
    int activateMicroprocess(lambda1 some_gen, component *some_obj);
    int activateMicroprocess(lambda2 some_gen, postman *some_obj);
    int activateMicroprocess(lambda3 some_gen, Producer *some_obj);
    int activateMicroprocess(lambda4 some_gen, Consumer *some_obj);
    scheduler();
};

extern class_ *cl_component;
class component : public microprocess {
public:
    dict<str *, list<str *> *> *boxes;

    str *recv(str *inboxname);
    int send(str *value, str *outboxname);
    int dataReady(str *inboxname);
    component();
};

extern class_ *cl_postman;
class postman : public microprocess {
public:
    str *sinkbox;
    Producer *source;
    Consumer *sink;
    str *sourcebox;

    postman(Producer *source, str *sourcebox, Consumer *sink, str *sinkbox);
};

extern class_ *cl_Producer;
class Producer : public component {
public:
    str *message;

    Producer(str *message);
};

extern class_ *cl_Consumer;
class Consumer : public component {
public:

    Consumer();
};

__iter<int> *scheduler_main(scheduler *zelf);
__iter<int> *postman_main(postman *zelf);
__iter<int> *Producer_main(Producer *zelf);
__iter<int> *Consumer_main(Consumer *zelf);

} // module namespace
#endif
