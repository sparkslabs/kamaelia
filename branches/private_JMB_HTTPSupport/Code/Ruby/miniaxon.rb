#!/usr/bin/ruby

class Coroutine
   def initialize(proc, *args)
      @proc = proc
      @args = args
      @alive = true
   end
   def alive?
      @alive
   end
   def _next
      pause_block = lambda do |value|
         @alive = true
         callcc do  |@resume_cc|
            @pause_cc.call(value)
         end
      end
      callcc do |@pause_cc|
         if @alive == true
            @alive = false
            @resume_cc.call(*@args, &pause_block) if @resume_cc
            @proc.call(*@args, &pause_block)
            @pause_cc.call(nil)
         end
      end
   end
end

def coroutine(proc, *args)
   Coroutine.new(proc, *args)
end

class Microprocess
   def initialize(*args)
      @uthread = nil
   end
   def main
   end
   def activate
      @uthread = coroutine(method(:main))
   end
   def uthread
       @uthread
   end
   def next
       @uthread._next
   end
end

class Scheduler < Microprocess
   def initialize
      super
      @active = []
      @newqueue = []
   end
   def main
      100.times do |i|
         @active.each do |current|
             yield 1
             result = current.next
             if result != nil:
                 @newqueue.push current
             end
         end
         @active = @newqueue
         @newqueue = []
      end
   end
   def activateMicroprocess(someprocess)
      someprocess.activate
      @newqueue.push someprocess
   end
end

def run(s)
   s.activate
   loop do
      j =s.next
      if j== nil
         break
      end
   end
end

class Printer < Microprocess
   def initialize(tag)
      super
      @tag = tag
   end
   def main
       loop do
          yield 1
          puts @tag
       end
   end
end

class Postman < Microprocess
   def initialize(source, sourcebox, sink, sinkbox)
      super
      @source = source
      @sourcebox = sourcebox
      @sink = sink
      @sinkbox = sinkbox
   end
   def main
      loop do
         yield 1
         if @source.dataReady(@sourcebox)
            d = @source.recv(@sourcebox)
            @sink.send(d, @sinkbox)
         end
      end
   end
end

class Component < Microprocess
   @@Boxes = {
     "inbox" => "This is where we expect to receive messages",
     "outbox" => "This is where we send results/messages",
   }
   @@name = "Component"
   def initialize(*args)
      super
      @@boxes = {}
      @@Boxes.each_key do |name|
         @@boxes[name] = []
      end
   end
   def send(value, outboxname="outbox")
      @@boxes[outboxname].push value
   end
   def recv(inboxname)
      showboxes if $debug
      result = @@boxes[inboxname].shift
      result
   end
   def dataReady(inboxname)
      @@boxes[inboxname].size
   end
   def showboxes
      print "Component : "; puts @@name
      @@boxes.each_key do |name|
         print name + " ["
         @@boxes[name].each do |item|
             print item.to_s + ", "
         end
         puts "]"
      end
   end
end

# Component.new()
class Producer < Component
   @@name = "Producer"
   def initialize(message)
      super
      @message = message
   end
   def main
      loop do
         yield 1
         send @message, "outbox"
         showboxes if $debug
      end
   end
end

class Consumer < Component
   @@name = "Consumer"
   def main
      count = 0
      loop do
         yield 1
         count = count +1
         if dataReady("inbox")
            data = recv("inbox")
            print data, " ", count, "\n"
         end
      end
   end
end

section = 3
if section == 1
   def generate_fibonacci(a, b)
      loop do
         yield a
         a,b = b, a+b
      end
   end
   fib = coroutine(method(:generate_fibonacci),1,1)
   10.times do
      puts fib._next
   end
end

if section == 2
   s = Scheduler.new()
   p = Printer.new("Hello World")
   q = Printer.new("Game Over")
   s.activateMicroprocess(p)
   s.activateMicroprocess(q)
   run(s)
end

if section == 3
   p = Producer.new("Hello World")
   c = Consumer.new()
   postie = Postman.new(p, "outbox", c, "inbox")

   myscheduler = Scheduler.new()
   myscheduler.activateMicroprocess(p)
   myscheduler.activateMicroprocess(c)
   myscheduler.activateMicroprocess(postie)

   run(myscheduler)
end
