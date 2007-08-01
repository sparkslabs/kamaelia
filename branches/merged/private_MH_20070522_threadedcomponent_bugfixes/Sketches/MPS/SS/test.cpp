#include "test.hpp"

namespace __test__ {

str *const_0, *const_1, *const_2, *const_3;

__iter<int> *MT, *__13, *__14;
int __15, i;
postman *postie;
str *__name__;
Consumer *c;
scheduler *myscheduler;
Producer *p;

/**
class microprocess
*/

class_ *cl_microprocess;

microprocess::microprocess() {}
microprocess::microprocess(str *name) {
    this->__class__ = cl_microprocess;
    
    this->name = name;
}

void *microprocess::__init__;

/**
class scheduler
*/

class_ *cl_scheduler;

template<class Klass>
int scheduler::activateMicroprocess(__iter<int> *(*some_gen)(Klass *), Klass *some_obj) {
    __iter<int> *microthread;

    microthread = some_gen(some_obj);
    (this->newqueue)->append(microthread);
    return 0;
}

scheduler::scheduler() : microprocess(const_0) {
    this->__class__ = cl_scheduler;
    
    this->active = (new list<__iter<int> *>());
    this->newqueue = (new list<__iter<int> *>());
}

/**
class component
*/

class_ *cl_component;

str *component::recv(str *inboxname) {
    str *result;

    result = ((this->boxes)->__getitem__(inboxname))->__getfast__(0);
    (this->boxes)->__getitem__(inboxname)->__delete__(0);
    return result;
}

int component::send(str *value, str *outboxname) {
    
    ((this->boxes)->__getitem__(outboxname))->append(value);
    return 0;
}

int component::dataReady(str *inboxname) {
    
    return len((this->boxes)->__getitem__(inboxname));
}

component::component() : microprocess(const_0) {
    this->__class__ = cl_component;
    
    this->boxes = (new dict<str *, list<str *> *>(2, new tuple2<str *, list<str *> *>(2,const_1,(new list<str *>())), new tuple2<str *, list<str *> *>(2,const_2,(new list<str *>()))));
}

/**
class postman
*/

class_ *cl_postman;

postman::postman(Producer *source, str *sourcebox, Consumer *sink, str *sinkbox) : microprocess(const_0) {
    this->__class__ = cl_postman;
    
    this->source = source;
    this->sourcebox = sourcebox;
    this->sink = sink;
    this->sinkbox = sinkbox;
}

/**
class Producer
*/

class_ *cl_Producer;

Producer::Producer(str *message) : component() {
    this->__class__ = cl_Producer;
    
    this->message = message;
}

/**
class Consumer
*/

class_ *cl_Consumer;

Consumer::Consumer() : component() {
    this->__class__ = cl_Consumer;
    
}

void __init() {
    const_0 = new str("hello");
    const_1 = new str("inbox");
    const_2 = new str("outbox");
    const_3 = new str("Hello World");

    __name__ = new str("__main__");

    cl_postman = new class_("postman", 32, 32);
    cl_Producer = new class_("Producer", 34, 34);
    cl_microprocess = new class_("microprocess", 31, 36);
    cl_component = new class_("component", 33, 35);
    cl_scheduler = new class_("scheduler", 36, 36);
    cl_Consumer = new class_("Consumer", 35, 35);

    p = (new Producer(const_3));
    c = (new Consumer());
    postie = (new postman(p, const_2, c, const_1));
    myscheduler = (new scheduler());
    myscheduler->activateMicroprocess(Consumer_main, c);
    myscheduler->activateMicroprocess(Producer_main, p);
    myscheduler->activateMicroprocess(postman_main, postie);
    MT = scheduler_main(myscheduler);

    FOR_IN(i,MT,14)
    END_FOR

}

class __gen_scheduler_main : public __iter<int> {
public:
    int a;
    StopIteration *__5;
    int c;
    __iter<int> *b;
    int __11;
    scheduler *zelf;
    int __10;
    int i;
    __iter<int> *current;
    int __4;
    int __7;
    int __6;
    int __1;
    int __0;
    __iter<__iter<int> *> *__3;
    list<__iter<int> *> *__2;
    __iter<__iter<int> *> *__9;
    list<__iter<int> *> *__8;
    int __12;
    int result;
    int __last_yield;

    __gen_scheduler_main(scheduler *zelf) {
        this->zelf = zelf;
        __last_yield = -1;
    }

    int next() {
        switch(__last_yield) {
            case 0: goto __after_yield_0;
            default: break;
        }
        result = 1;

        FAST_FOR(i,0,100,1,0,1)

            FOR_IN_SEQ(current,zelf->active,2,4)
                __last_yield = 0;
                return 1;
                __after_yield_0:;
                try {
                    result = current->next();
                    if ((result!=-1)) {
                        (zelf->newqueue)->append(current);
                    }
                } catch (StopIteration *) {
                }
            END_FOR


            FAST_FOR(a,0,len(zelf->active),1,6,7)
                (zelf->active)->pop();
            END_FOR


            FOR_IN_SEQ(b,zelf->newqueue,8,10)
                (zelf->active)->append(b);
            END_FOR


            FAST_FOR(c,0,len(zelf->newqueue),1,11,12)
                (zelf->newqueue)->pop();
            END_FOR

        END_FOR

        throw new StopIteration();
    }

};

__iter<int> *scheduler_main(scheduler *zelf) {
    return new __gen_scheduler_main(zelf);

}

class __gen_postman_main : public __iter<int> {
public:
    postman *zelf;
    str *d;
    int __last_yield;

    __gen_postman_main(postman *zelf) {
        this->zelf = zelf;
        __last_yield = -1;
    }

    int next() {
        switch(__last_yield) {
            case 0: goto __after_yield_0;
            default: break;
        }

        while(1) {
            __last_yield = 0;
            return 1;
            __after_yield_0:;
            if ((zelf->source)->dataReady(zelf->sourcebox)) {
                d = (zelf->source)->recv(zelf->sourcebox);
                (zelf->sink)->send(d, zelf->sinkbox);
            }
        }
        throw new StopIteration();
    }

};

__iter<int> *postman_main(postman *zelf) {
    return new __gen_postman_main(zelf);

}

class __gen_Producer_main : public __iter<int> {
public:
    Producer *zelf;
    int __last_yield;

    __gen_Producer_main(Producer *zelf) {
        this->zelf = zelf;
        __last_yield = -1;
    }

    int next() {
        switch(__last_yield) {
            case 0: goto __after_yield_0;
            default: break;
        }

        while(1) {
            __last_yield = 0;
            return 1;
            __after_yield_0:;
            zelf->send(zelf->message, const_2);
        }
        throw new StopIteration();
    }

};

__iter<int> *Producer_main(Producer *zelf) {
    return new __gen_Producer_main(zelf);

}

class __gen_Consumer_main : public __iter<int> {
public:
    int count;
    str *data;
    Consumer *zelf;
    int __last_yield;

    __gen_Consumer_main(Consumer *zelf) {
        this->zelf = zelf;
        __last_yield = -1;
    }

    int next() {
        switch(__last_yield) {
            case 0: goto __after_yield_0;
            default: break;
        }
        count = 0;

        while(1) {
            __last_yield = 0;
            return 1;
            __after_yield_0:;
            count += 1;
            if (zelf->dataReady(const_1)) {
                data = zelf->recv(const_1);
                print("%s %d\n", data, count);
            }
        }
        throw new StopIteration();
    }

};

__iter<int> *Consumer_main(Consumer *zelf) {
    return new __gen_Consumer_main(zelf);

}

} // module namespace

int main(int argc, char **argv) {
    __shedskin__::__init();
    __test__::__init();
    __shedskin__::__exit();
}
