---
pagename: Developers/Projects/TestingFramework
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Kamaelia: Testing Framework {#head-c56d7c932f5d44641046aae5892bb3342b553c19}
---------------------------

What is it? {#head-cb43cfbe3084966a3a3d76039ca664b41579c854}
-----------

::: {.boxright}
**NOTE/WARNING:** this is a speculative project that may become \"the\"
testing framework. It does not have that status yet.
:::

Kamaelia Testing Framework aims to be a testing framework that will let
developers write automated tests of kamaelia components easily.

NOTE: this documentation is related to the first stage of the project,
which has been suggested to be rewritten, so it may change completely in
the near future.\

Where do I get it & install it? {#head-4ae61e667b2c73bd4538b78f2443acaacfb3a7e7}
-------------------------------

**developers**

It is currenty available in the private\_PO\_Tests branch. So, step by
step:**\
**

-   svn co
    https://kamaelia.svn.sourceforge.net/svnroot/kamaelia/branches/private\_PO\_Tests/

-   cd Axon; sudo python setup.py \# Axon is not changed from the /trunk
    version

-   cd Kamaelia; sudo python setup.py

Enjoy\
\

**How do I use it?**
--------------------

Once the system is installed, you can do the tests you want wherever you
want (i.e. in your /Sketches, in /tmp, etc.).

You need to import the class \"KamTestCase\" from the package
Kamaelia.Testing.KamTestCase and subclass it

In this subclass, you can use setUp and tearDown just as you would do in
PyUnit.

You can test code that has nothing to do with Axon.

If using Axon (which is the normal thing):

-   You will first create the component under test
-   Then, you will call \"initializeSystem\" with the component under
    test as an argument
-   Then, you will be able to put messages to inboxes with the \"put\"
    method. This is, self.put(\'message\',\'inbox\').\
-   You can also retrieve messages from the outboxes with the \"get\"
    method. You may use only a single parameter (the outbox name), or
    two parameter (the outbox name and the timeout in seconds). This is,
    self.get(\'outbox\',timeout=2).\
-   You can also check that a certain outbox of a component is empty
    after a period of time. This is,
    self.assertOutboxEmpty(\'outbox\',timeout=5)
-   You can check that a component has or has not finished in a certain
    period of time this is, self.assertFinished(timeout=5) or
    self.assertNotFinished(timeout=5)
-   You can use all the assert\* and fail\* methods of a
    unittest.TestCase, which are documented
    [here](http://docs.python.org/lib/testcase-objects.html), to ensure
    that the output of the component is the one expected
-   You can skip output from a component (i.e. waiting from a certain
    output). In order to define the output you are waiting for, you can
    use a simple KamExpectMatcher.Matcher object, which just checks the
    == operator, or you can use KamExpectMatcher.RegexpMatcher, which
    uses regular expressions, or you can subclass
    KamExpectMatcher.Matcher for other behaviour. Then you can use it as
    of self.expect(matcherObject, \'outbox\', timeout=5).
-   You can provide mock components to avoid dealing with resources that
    may be difficult to handle with during testing \[i.e. disk or
    networks usage\]

In order to provide some working examples, you can check:

-   A simple example that tests a very simple component, but does all
    the very basic steps to test it.
    [Here](https://kamaelia.svn.sourceforge.net/svnroot/kamaelia/trunk/Sketches/PO/test_examples/example1.py).\
-   A simple example that interacts with a very simple component,
    providing inputs and outputs.
    [Here](https://kamaelia.svn.sourceforge.net/svnroot/kamaelia/trunk/Sketches/PO/test_examples/example2.py).\
-   A simple example that interacts with the same component in the
    previous example, but that skips some outputs using the
    KamExpectMatcher.\* matchers.
    [Here](https://kamaelia.svn.sourceforge.net/svnroot/kamaelia/trunk/Sketches/PO/test_examples/example3.py).\
-   A simple example that interacts with a component that uses another
    component which would be difficult to deal with and may be mocked.
    [Here](https://kamaelia.svn.sourceforge.net/svnroot/kamaelia/trunk/Sketches/PO/test_examples/example4.py).

There are some other (more complex) tests added:\

-   A clone of the first block of tests found in
    [here](https://kamaelia.svn.sourceforge.net/svnroot/kamaelia/trunk/Sketches/MPS/GSOC08/MultiPipeTest.py)
    can be found
    [here](https://kamaelia.svn.sourceforge.net/svnroot/kamaelia/trunk/Sketches/PO/testingMulticore/tests/test_Multicore.py).
-   A couple of tests of HTTPClient can be found
    [here](http://kamaelia.svn.sourceforge.net/svnroot/kamaelia/branches/private_PO_Tests/Kamaelia/Test/Protocol/HTTP/test_SimpleHTTPClient.py).
-   Note that the tests added
    [here](http://kamaelia.svn.sourceforge.net/svnroot/kamaelia/branches/private_PO_Tests/Kamaelia/Test/Testing/)
    test the testing framework, and thus they don\'t rely on it (and
    thus they are not tested as the tests above).

Since it relies on PyUnit, it can easily be integrated in continuous
integration servers with the existing tools for integrating PyUnit on
them.

-   The existing tools for running the tests nightly in Kamaelia will
    work as expected. Since the runner used is unittest, the -v flag
    still works and thus you can run the tests and it will return the
    \_\_doc\_\_ and the state of the test (i.e. \"Check Addition and
    Deletion of Inboxes \... ok\").
-   The [existing tools](http://www.rittau.org/python/cruisecontrol/)
    used for integrating PyUnit in CruiseControl may be used \"out of
    the box\" to integrate Kamaelia tests in this continuous integration
    server.
-   The same probably applies to other existing automated code testers
    (i.e. apycot)\

Planned Schedule (July 7th: redefining it): {#head-ab982e78aa80eb65225e149907cae69c7abf9889}
-------------------------------------------

June 6

-   Finish Unit-testing KamPlanet using the first approach\
    (modify the approach as problems arise).
-   Start mocking \"problematic\" components (i.e. those which\
    require network/disk/\... access; file reader and http client) to
    test\
    the interaction of all the components (except for the mocked ones)
    of\
    KamPlanet.

June 13

-   Finish integration-testing KamPlanet by using these mock\
    objects.
-   For this case (KamPlanet), add also integration testing with\
    real HTTP servers (i.e. using python\'s SimpleHTTPServer etc.).
-   Start testing other kamaelia apps/libs reusing the same\
    approach/objects, adapting them when problems arise. Order/number
    of\
    these applications not yet decided (the most different the
    applications\
    are, the best; GUI, network\...), the number mainly depends on how
    many\
    new problems raise while testing each new application.

June 20

-   (Keep testing other kamaelia apps/libs). Note that the aim of\
    this task is not to test apps/libs but to check that the approach
    being\
    used is good enough by testing apps/libs; a couple of apps/libs
    getting\
    tested is only a collateral benefit. But, \*at this stage\*, I
    wouldn\'t\
    worry too much if while improving the approach/framework when
    testing\
    the 3rd app/lib I break the tests on the 1st app/lib.

June 27

-   (Keep testing other kamaelia apps/libs).

July 4

-   Freeze the testing framework API and complete/clean the\
    tests of the tested apps/libs so that all of them work correctly
    with\
    the current approach.
-   Finish code-documenting the framework and write a small\
    tutorial on how to use it.
-   Start integrating the configuration on a continuous\
    integration server (i.e. CruiseControl; it should be quite easy) or
    similar frameworks (APyCoT).

July 11

-   Finish integrating the testing framework with a continuous\
    integration server (i.e. CruiseControl) or similar frameworks
    (APyCoT).
-   Complete last week\'s tutorial with a simple sample app\
    developed using Test-Driven-Development and Continuous Integration.
    This\
    (now bigger) tutorial will assume that Kamaelia installed and basic\
    notions of Kamaelia; it will include a small introduction to TDD/CI;
    it\
    will only reference the installation of the CI server but it will\
    include its configuration for the sample app; the main point is\
    including a big. The simple app should use the components that were\
    especially difficult to work with in June.\

*(not added Logging Framework schedule)*\

Progress (dates related to the weekly meeting - these are the \"DONE\" lines) {#head-38c970225e454db55841fa5cd8c542a5e0948c10}
-----------------------------------------------------------------------------

-   Started unit-testing KamPlanet, working on the unit-testing
    infrastructure.

-   KamPlanet modules mostly unit-tested with the new infrastructure,
    Tools and doc to deploy KamPlanet and more KamPlanet tests added,
    Mock infrastructure started and used

-   Moved all the test framework to internally use LikeFile, replaced
    previous implementations. Adapted all the KamPlanet tests to the new
    implementation. Started integration testing kamplanet.

-   Tested some stuff at HTTPClient/HTTPParser, a couple of bugs found
    and fixed, trying to put the changes in a branch. Improvements,
    stats and tests in KamPlanet. Tried to move from
    private\_MPS\_Scratch/\*\*/LikeFile to trunk/\*\*/Handle in order to
    make the branch from trunk for testing other stuff; still on it.

-   Branch created for the testing framework, with a minor modifications
    in {Protocol.HTTP,Schedule}, tests and the testing framework itself.
    In process of migrating to Handle (it still fails \~20% of times) to
    replace LikeFile-based working testing framework, adding examples as
    documentation

Log/Discussion {#head-105aec3df2ff0e4fd9e666bbf89cba1902e148a1}
--------------

First approach:\

scheduler steps-based. 

-   It counts how many steps it takes to do a task. If it takes too many
    steps, the testing framework asserts that it failed.\
-   Advantage: when using a single processor, the results should be the
    same in different machines, so it becomes quite deterministic, which
    is very interesting when unit testing. This doesn\'t happen whenever
    you are testing components that use intrinsically not-deterministic
    components (such as those using the network, file system, external
    processes, etc.)

Available prior to r4391 (with examples in KamPlanet tests), still
available as KamPlanetTestCaseOld.py

Second approach:

time-based and expect command based

Suggested by ms-

Now it asserts that the task has failed when certain seconds have passed

You can also assert that you wait for a certain output, discarding all
the previous output. Or that the component output is empty (equivalent
to expect\'s EOF).\

-   For this, you pass a Matcher subclass (which can be a Matcher -such
    as \"I wait for a 5, or a \'hello world\', or an instance of an
    object, for example, and it must be exactly that object-, or a
    RegexpMatcher -I\'m waiting for something like \'.\*\[A-Z\]+\'
    message-). In the future other Matchers could be implemented (like
    one comparing xmls as http://xmlunit.sf.net/ does)

Advantage: it is more realistic than the previous approach, and more
compfortable.

\
