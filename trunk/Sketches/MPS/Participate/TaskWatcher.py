#!/usr/bin/python
"""
Sketchcode outline of task list manager for Kamaelia (and software in general)
"""

import shelve
import pprint

# -- Conceptual------------------------------------------------
class _spec_descripton(object):
    "# added "
    goal = "Short one line of what the task is designed to achieve/create."
    result = "A practical, clear result of what will be possible as a result of achieving this task. This is best described in the case of a user story."
    context = "The context in which this task sits. Has this task any history? Is it the result of any previous tasks - either within the project or outside."
    benefits = "What benefits will be gained by working on this task, and achieving its goals? Speculative as well as certained/realistically expected benefits are valid here."

class _spec_dashboard(object):
    "# added "
    status = "(Started|Running|Completed|Dropped|Stasis|Blocked)"
    status_text = "Associated single sentence (eg why blocked)"
    currentdevelopers = "you!"
    devlocation = "Normally /Sketches/ initially"
    startdate = "date"
    milestonedate ="date"
    milestonetag = "(met|slipped|missed)"
    expectedenddate = "(date|n/a)"
    enddate = "date"
    dateupdated = "date"
    estimatedeffortsofar = "int"

class _spec_comment(object):
    "# added "
    who = "name"
    when = "timedate"
    what = "string"

class _spec_update(object):
    what = ""
    who = "name"
    date = "date"
    timespent = "in 1/4 days"
    output = "if anything"
    statuschange = "if appropriate"


class _spec_requirement(object):
    "# added "
    reqtype = "(MUST|SHOULD|MAY|WOULDLIKE)"
    whofrom = "name"
    what = "string describing the requirement"

class _spec_inputs(object):
    "# added "
    tasksponsor = "WHO is the sponsor - (can be main developer)"
    taskowner = "WHO is the owner - (likely to be main developer)"
    developers = list("name") # (if empty list, assert task.dashboard.status == "stasis"
    users = list( "name" ) 
    interestedparties = list( "name" )
    requirements = list ( [ _spec_requirement ] )
    influencingfactors = list ( "strings" )

class _spec_output(object):
    "# added "
    outputtype = "(code|presentation|documentation)"
    location = list ( "string" )

class _spec_outputs(object):
    "# added "
    expected = list ( "strings" )
    actual = list ([ _spec_output ])
    arisingpossilities = list ( "Realistic possibility arising as a result of activity on this task" )

class _spec_microtask(object):
    "# added "
    description = "subtasks as bullet points with the sort of information you'd put on a project task page, but for which it seems overkill to create a project task page for."


class _spec_relatedtasks(object):
    "# added "
    tasksenablingthis = list ( "Task" )
    subtasks = list  ([_spec_microtask , "Task"])
    cotasks = list ( "Task" )


class _spec_Task(object):
    "# added "
    taskid = int
    _spec_descripton
    _spec_dashboard
    _spec_inputs
    _spec_outputs
    _spec_relatedtasks
    tasklog = list ([ _spec_update ])
    discussion = list ([ _spec_comment ])
    consolidateddiscussion = "string"

# -- Concrete ------------------------------------------------

class Requirement(object):
    def __init__(self, reqtype, who, what, when="", by="", why=""):
        self.reqtype = reqtype
        self.who = who
        self.what = what
        self.when = when
        self.by = by
        self.why = why
    def asdict(self):
        return {
            "reqtype" : self.reqtype,
            "who" : self.who,
            "what" : self.what,
            "when" : self.when,
            "by" : self.by,
            "why" : self.why,
        }
    def ashtml(self):
        return """<div class="requirement">
            <div class="reqtype"> %(reqtype)s </div>
            <div class="who"> %(who)s </div>
            <div class="what"> %(what)s </div>
            <div class="when"> %(when)s </div>
            <div class="by"> %(by)s </div>
            <div class="why"> %(why)s </div>
        </div>""" % self.asdict()

class Inputs(object):
    def __init__(self):
        self.tasksponsor = ""
        self.taskowner = ""
        self.developers = []
        self.users = []
        self.interestedparties = []
        self.influencingfactors = []
        self.requirements = []
    def asdict(self):
        return {
            "tasksponsor" : self.tasksponsor,
            "taskowner" : self.taskowner,
            "developers" : self.developers,
            "users" : self.users,
            "interestedparties" : self.interestedparties,
            "influencingfactors" : self.influencingfactors,
            "requirements" : [ x.asdict() for x in self.requirements],
        }
    def developers_ashtml(self):
        R = []
        for D in self.developers:
            R.append("<div class='dev'>"+D+"</div>")
        return "\n".join(R)
    def users_ashtml(self):
        R = []
        for D in self.users:
            R.append("<div class='user'>"+D+"</div>")
        return "\n".join(R)
    def interested_ashtml(self):
        R = []
        for D in self.users:
            R.append("<div class='interested'>"+D+"</div>")
        return "\n".join(R)
    def factors_ashtml(self):
        if self.influencingfactors == []:
            return ""
        R = ["<ul>"]
        for i in self.influencingfactors:
            R.append("\n<li class='factor'>")
            R.append(i)
        R.append("\n</ul>")
        return "".join(R)
    def reqs_ashtml(self):
        R = []
        for req in self.requirements:
            R.append(req.ashtml())
        return "".join(R)
    def ashtml(self):
        X = self.asdict()
        X["tasksponsor"] = "<div class='label'>Sponsor</div> <div class='sponsor'>" + X["tasksponsor"] +"</div>"
        X["taskowner"] = "<div class='label'>Owner</div>  <div class='owner'>" + X["taskowner"] + "</div>"
        X["developers"] = "<div class='label'>Developers</div> <div class='developers'>" + self.developers_ashtml() + "</div>"
        X["users"] = "<div class='label'>Users</div> <div class='users'>" + self.users_ashtml() + "</div>"
        X["interestedparties"] = "<div class='label'>Interested Parties</div> <div class='interestedparties'>" + self.interested_ashtml() + "</div>"
        X["influencingfactors"] = "<div class='label'>Influencing Factors</div> <div class='factors'>" + self.factors_ashtml()+ "</div>"
        X["requirements"] = "<div class='label'>Requirements</div> <div class='requirements'>" + self.reqs_ashtml() + "</div>"
        return """
<div class="Inputs">
%(tasksponsor)s
%(taskowner)s
%(developers)s
%(users)s
%(interestedparties)s
%(influencingfactors)s
%(requirements)s
</div>
""" % X




















# -------------------------- TO BE DIVVED ----------------------------------------------------

class Update(object):
    def __init__(self, what, who, when, timespent, output, statuschange):
        self.what = what
        self.who = who
        self.when = when
        self.timespent = timespent
        self.output = output
        self.statuschange = statuschange
    def asdict(self):
        return {
            "what" : self.what,
            "who" : self.who,
            "date" : self.when,
            "timespent" : self.timespent,
            "output" : self.output,
            "statuschange" : self.statuschange,
        }

class Comment(object):
    def __init__(self, who, when , what ):
        self.who = who
        self.when = when
        self.what = what
    def asdict(self):
        return {
            "who" : self.who,
            "when" : self.when,
            "what" : self.what,
        }

class Dashboard(object):
    def __init__(self):
        self.status = ""
        self.status_text = ""
        self.currentdevelopers = ""
        self.devlocation = ""
        self.startdate = ""
        self.milestonedate = ""
        self.milestonetag = ""
        self.expectedenddate = ""
        self.enddate = ""
        self.dateupdated = ""
        self.estimatedeffortsofar = ""

    def asdict(self):
        return {
            "status": self.status,
            "status_text": self.status_text,
            "currentdevelopers": self.currentdevelopers,
            "devlocation": self.devlocation,
            "startdate": self.startdate,
            "milestonedate": self.milestonedate,
            "milestonetag": self.milestonetag,
            "expectedenddate": self.expectedenddate,
            "enddate": self.enddate,
            "dateupdated": self.dateupdated,
            "estimatedeffortsofar": self.estimatedeffortsofar,
        }
    def ashtml(self):
        X = self.asdict()
        return """
<div class="Dashboard">
%(status)s
%(status_text)s
%(currentdevelopers)s
%(devlocation)s
%(startdate)s
%(milestonedate)s
%(milestonetag)s
%(expectedenddate)s
%(enddate)s
%(dateupdated)s
%(estimatedeffortsofar)s
</div>
""" % X

class Descripton(object):
    def __init__(self):
        self.goal = ""
        self.result = ""
        self.context = ""
        self.benefits = []

    def asdict(self):
        return {
            "goal": self.goal,
            "result" : self.result,
            "context" : self.context,
            "benefits" : self.benefits,
        }
    def ashtml(self):
        X = self.asdict()
        return """
<div class="Description">
%(goal)s
%(result)s
%(context)s
%(benefits)s
</div>
""" % X


class Output(object):
    def __init__(self, output_type, location, description):
        self.output_type = output_type
        self.location = location
        self.description = description
    def asdict(self):
        return {
            "output_type" : self.output_type,
            "location" : self.location,
            "description" : self.description,
        }
    def ashtml(self):
        X = self.asdict()
        return """
<div class="Output">
%(output_type)s
%(location)s
%(description)s
</div>
""" % X

class Outputs(object):
    def __init__(self):
        self.expected = []
        self.actual = []
        self.arisingpossibilities = []
    def asdict(self):
        return {
            "expected" : self.expected,
            "actual" : [ x.asdict() for x in self.actual ],
            "arisingpossibilities" : self.arisingpossibilities,
        }
    def ashtml(self):
        X = self.asdict()
        return """
<div class="Outputs">
%(expected)s
%(actual)s
%(arisingpossibilities)s
</div>
""" % X

class Relatedtasks(object):
    def __init__(self):
        self.tasksenablingthis = []
        self.subtasks = []
        self.cotasks = []
    def asdict(self):
        return {
            "tasksenablingthis" : self.tasksenablingthis,
            "subtasks" : self.subtasks,
            "cotasks" : self.cotasks,
        }
    def ashtml(self):
        X = self.asdict()
#        X["description"] = X.ashtml()
#        X["dashboard"] = X.ashtml()
#        X["inputs"] = X.ashtml()
#        X["outputs"] = X.ashtml()
#        X["relatedtasks"] = X.ashtml()
        return """
<div class="Relatedtasks">
%(tasksenablingthis)s
%(subtasks)s
%(cotasks)s
</div>
""" % X


class Task(object):
    def __init__(self, taskid):
        self.taskid =  taskid              # OK
        self.description = Descripton()    # OK
        self.dashboard = Dashboard()       # OK
        self.inputs = Inputs()             # OK
        self.outputs = Outputs()           # OK
        self.relatedtasks = Relatedtasks() # 
        self.tasklog = []                  # OK
        self.discussion = []               # OK
        self.consolidateddiscussion = ""   # OK

    def asdict(self):
        return {
            "taskid" :  self.taskid,
            "description" : self.description.asdict(),
            "dashboard" : self.dashboard.asdict(),
            "inputs" : self.inputs.asdict(),
            "outputs" : self.outputs.asdict(),
            "relatedtasks" : self.relatedtasks.asdict(),
            "tasklog" : [x.asdict() for x in self.tasklog],
            "discussion" : [x.asdict() for x in self.discussion],
            "consolidateddiscussion" : self.consolidateddiscussion ,
        }
    def ashtml(self):
        X = self.asdict()
        X["description"] = self.description.ashtml()
        X["dashboard"] = self.dashboard.ashtml()
        X["inputs"] = self.inputs.ashtml()
        X["outputs"] = self.outputs.ashtml()
        X["relatedtasks"] = self.relatedtasks.ashtml()
        return """\
<div class="Task">
<div class="taskheader">Task</div>
<div class="taskid">%(taskid)s</div>
%(description)s
%(dashboard)s
%(inputs)s
%(outputs)s
%(relatedtasks)s
<div class="tasklog">%(tasklog)s</div>
<div class="discussion">%(discussion)s</div>
<div class="consolidateddiscussion">%(consolidateddiscussion)s</div>
</div>
""" % X

class Tasks(object):
    def __init__(self, filename):
        self.filename = shelve
        self.db = shelve.open(filename, "c")
        self.meta = shelve.open(filename+".meta", "c")
    def new_task(self):
        try:
            x = self.meta["highest"]
        except KeyError:
            x = 0
        x = x + 1
        self.meta["highest"] = x
        return Task(x)

    def zap(self):
        for i in self.meta.keys():
            del self.meta[i]
        for i in self.db.keys():
            del self.db[i]

    def store_task(self,task):
        self.db[str(task.taskid)] = task

    def close(self):
        self.db.close()

    def get_task(self, taskid):
        return self.db[str(taskid)]

T = Tasks("taskfile")
T.zap()

task = T.new_task()

task.description.goal = "Short one line of what the task is designed to achieve/create."
task.description.result = "A practical, clear result of what will be possible as a result of achieving this task. This is best described in the case of a user story."
task.description.context = "The context in which this task sits. Has this task any history? Is it the result of any previous tasks - either within the project or outside."
task.description.benefits.append( "What benefits will be gained by working on this task")
task.description.benefits.append( "... and achieving its goals?")
task.description.benefits.append("Speculative as well as certained/realistically expected benefits are valid here.")

task.dashboard.status = "(Started|Running|Completed|Dropped|Stasis|Blocked)"
task.dashboard.status_text = "Associated single sentence (eg why blocked)"
task.dashboard.currentdevelopers = "you!"
task.dashboard.devlocation = "Normally /Sketches/ initially"
task.dashboard.startdate = "date"
task.dashboard.milestonedate ="date"
task.dashboard.milestonetag = "(met|slipped|missed)"
task.dashboard.expectedenddate = "(date|n/a)"
task.dashboard.enddate = "date"
task.dashboard.dateupdated = "date"
task.dashboard.estimatedeffortsofar = "int"

task.discussion.append( Comment(who = "name1", when = "timedate", what = "YES!") )
task.discussion.append( Comment(who = "name1", when = "timedate", what = "NO!") )
task.discussion.append( Comment(who = "name1", when = "timedate", what = "MAYBE!") )

task.consolidateddiscussion = "--\n".join([ x.what for x in task.discussion ])

task.tasklog.append( Update(what="what", who="name", when="now", timespent="5", output="", statuschange="") )
task.tasklog.append( Update(what="what", who="name", when="now", timespent="5", output="", statuschange="") )
task.tasklog.append( Update(what="what", who="name", when="now", timespent="5", output="", statuschange="") )

task.inputs.tasksponsor = "Tom"
task.inputs.taskowner = "Tom"
task.inputs.developers.append( "Tom" )
task.inputs.users.append( "Tom" )
task.inputs.users.append( "Dick" )
task.inputs.users.append( "Harry" )
task.inputs.interestedparties.append("Jane")
task.inputs.interestedparties.append("Deliah")
task.inputs.influencingfactors.append("Would be really cool")
task.inputs.influencingfactors.append("Wanted this for ages!")

task.inputs.requirements.append( Requirement(reqtype="MUST", who="Jane", what="Pink") )
task.inputs.requirements.append( Requirement(reqtype="SHOULD", who="Jane", what="Chocolate") )
task.inputs.requirements.append( Requirement(reqtype="MAY", who="Tom", what="Work") )
task.inputs.requirements.append( Requirement(reqtype="WOULDLIKE", who="Deliah", what="Fluffy") )

task.outputs.expected.append("The widget should curl")
task.outputs.expected.append("The widget should frown")
task.outputs.expected.append("The widget should stamp")

task.outputs.actual.append(Output(output_type="code", location="svn://.../..py",description="fish"))
task.outputs.actual.append(Output(output_type="presentation", location="PYCONUK08",description="Woo"))
task.outputs.actual.append(Output(output_type="documentation", location="http:/..../",description="Docs"))
task.outputs.actual.append(Output(output_type="other", location="Kitchen",description="Cake"))

task.outputs.arisingpossibilities.append("Should be able to sing a musical!")
task.outputs.arisingpossibilities.append("Should be able to put on a show!")

task.relatedtasks.tasksenablingthis.append( 2 )
task.relatedtasks.tasksenablingthis.append( 3 )
task.relatedtasks.tasksenablingthis.append( 4 )

task.relatedtasks.subtasks.append( ("microtask", "Step to the left" ))
task.relatedtasks.subtasks.append( ("microtask", "jump to the right" ))
task.relatedtasks.subtasks.append( ("microtask", "pull knees in tight" ))
task.relatedtasks.subtasks.append( ("task", 5 ))
task.relatedtasks.subtasks.append( ("task", 6 ))
task.relatedtasks.subtasks.append( ("task", 7 ))

task.relatedtasks.cotasks.append( 8 )
task.relatedtasks.cotasks.append( 9 )
task.relatedtasks.cotasks.append( 10 )

# pprint.pprint ( task.asdict(), width=170 )

T.store_task(task)
T.close()

U = Tasks("taskfile")
foo = U.get_task(1)
# print "========================================================================================================="
# pprint.pprint ( foo.asdict(), width=170 )
U.close()

def dumptask(D,indent=0):
    def mydisplay(D,indent=0):
        if type(D) == dict:
            for K in D:
                print indent*"   "+K+":",
                if type(D[K])== list or type(D[K]) ==dict:
                    print
                mydisplay(D[K], indent+1)
        elif type(D) == list:
            for I in D:
                if (type(I) != list) and (type(I) != dict):
                  print indent*"   ",
                  mydisplay(I, indent+1)
                elif type(I) == dict:
                    print indent*"   ","{{{"
                    mydisplay(I, indent+1)
                    print indent*"   ","}}}"
                else:
                    mydisplay(I, indent+1)
        elif type(D) == str:
            print repr(D)
        elif type(D) == tuple:
            for I in D:
                print repr(I),
            print
        elif type(D) == int:
            print repr(D)
        else:
            raise ValueError("Unexpected type for D:"+str(type(D)))

    print "========================================================================================================="
    print "TASK:"
    mydisplay(D,1)

# dumptask(foo.asdict())

# FIXME - currently this STILL outputs things like (...,...,...) and some lists.
# Generally where there is a list or dict or tuple of base types
print foo.ashtml()




