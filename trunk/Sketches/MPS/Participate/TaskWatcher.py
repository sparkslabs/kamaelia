#!/usr/bin/python
"""
Sketchcode outline of task list manager for Kamaelia (and software in general)
"""

import shelve
import pprint

# -- Conceptual------------------------------------------------
class _spec_Description(object):
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
    _spec_Description
    _spec_dashboard
    _spec_inputs
    _spec_outputs
    _spec_relatedtasks
    tasklog = list ([ _spec_update ])
    discussion = list ([ _spec_comment ])
    consolidateddiscussion = "string"

# -- Concrete ------------------------------------------------
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

    def json(self):
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
        X = self.json()
        X["status"] = "<div class='dashitem'><span class='label'>Status</span> <span class='status'>" + X["status"] +"</span></div>"
        X["status_text"] = "<div class='dashitem'><span class='status_text'>" + X["status_text"] +"</span></div>"
        X["currentdevelopers"] = "<div class='dashitem'><span class='label'>Current Developers</span> <span class='currentdevelopers'>" + X["currentdevelopers"] +"</span></div>"
        X["devlocation"] = "<div class='dashitem'><span class='label'>Dev Location</span> <span class='devlocation'>" + X["devlocation"] +"</span></div>"
        X["startdate"] = "<div class='dashitem'><span class='label'>Started</span> <span class='startdate'>" + X["startdate"] +"</span></div>"
        X["milestonedate"] = "<div class='dashitem'><span class='label'>Major Milestone Date</span> <span class='milestonedate'>" + X["milestonedate"] +"</span></div>"
        X["milestonetag"] = "<div class='dashitem'><span class='milestonetag'>" + X["milestonetag"] +"</span></div>"
        X["expectedenddate"] = "<div class='dashitem'><span class='label'>Expected End</span> <span class='expectedenddate'>" + X["expectedenddate"] +"</span></div>"
        X["enddate"] = "<div class='dashitem'><span class='label'>Ended</span> <span class='enddate'>" + X["enddate"] +"</span></div>"
        X["dateupdated"] = "<div class='dashitem'><span class='label'>Last updated</span> <span class='dateupdated'>" + X["dateupdated"] +"</span></div>"
        X["estimatedeffortsofar"] = "<div class='dashitem'><span class='label'>Effort (est, days)</span> <span class='estimatedeffortsofar'>" + X["estimatedeffortsofar"] +"</span></div>"
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

class Description(object):
    def __init__(self):
        self.goal = ""
        self.result = ""
        self.context = ""
        self.benefits = []

    def json(self):
        return {
            "goal": self.goal,
            "result" : self.result,
            "context" : self.context,
            "benefits" : self.benefits,
        }
    def benefits_ashtml(self):
        if self.benefits == []:
            return ""
        R = ["<ul>"]
        for i in self.benefits:
            R.append("\n<li class='benefit'>")
            R.append(i)
        R.append("\n</ul>")
        return "".join(R)
    def ashtml(self):
        X = self.json()
        X["goal"] = "<div class='goal'>" + X["goal"] +"</div>"
        X["result"] = "<div class='result'>" + X["result"] +"</div>"
        X["context"] = "<div class='context'>" + X["context"] +"</div>"
        X["benefits"] = "<div class='label'>Benefits</div> <div class='benefits'>" + self.benefits_ashtml() +"</div>"
        return """
<div class="Description">
<h2 id="description_heading">Description</h2>
%(goal)s
%(result)s
%(context)s
%(benefits)s
</div>
""" % X

class Requirement(object):
    def __init__(self, reqtype, who, what, when="", by="", why=""):
        self.reqtype = reqtype
        self.who = who
        self.what = what
        self.when = when
        self.by = by
        self.why = why
    def json(self):
        return {
            "reqtype" : self.reqtype,
            "who" : self.who,
            "what" : self.what,
            "when" : self.when,
            "by" : self.by,
            "why" : self.why,
        }
    def ashtml(self):
        X = self.json()
        X["who"] = "<span class='who'>"+X["who"] +"</span>"
        X["what"] = "<span class='what'>"+ X["what"] +"</span>"
        if X["when"] != "":
            X["when"] = ", <span class='when'>"+ X["when"] +"</span>"
        if X["by"] != "":
            X["by"] = "By: <span class='by'>"+ X["by"] +"</span>"
        if X["why"] != "":
            X["why"] = "<span class='why'>"+ X["why"] +"</span>"
        X["reqtype"] = "<span class='reqtype'>"+ X["reqtype"] +"</span>"
        return "%(what)s %(by)s %(why)s ( %(who)s %(when)s, %(reqtype)s )" % X

class Inputs(object):
    def __init__(self):
        self.tasksponsor = ""
        self.taskowner = ""
        self.developers = []
        self.users = []
        self.interestedparties = []
        self.influencingfactors = []
        self.requirements = []
    def json(self):
        return {
            "tasksponsor" : self.tasksponsor,
            "taskowner" : self.taskowner,
            "developers" : self.developers,
            "users" : self.users,
            "interestedparties" : self.interestedparties,
            "influencingfactors" : self.influencingfactors,
            "requirements" : [ x.json() for x in self.requirements],
        }
    def developers_ashtml(self):
        R = []
        for D in self.developers:
            R.append("<li class='dev'>"+D)
        return "\n".join(R)
    def users_ashtml(self):
        R = []
        for D in self.users:
            R.append("<li class='user'>"+D)
        return "\n".join(R)
    def interested_ashtml(self):
        R = []
        for D in self.users:
            R.append("<li class='interested'>"+D)
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
        R = ["<ul>"]
        for req in self.requirements:
            R.append("\n<li class='requirement'>")
            R.append(req.ashtml()+"\n")
        R.append("\n</ul>")
        return "".join(R)
    def ashtml(self):
        X = self.json()
        X["tasksponsor"] = "<div class='label'>Sponsor</div> <ul class='sponsor'> <li>" + X["tasksponsor"] +"</ul>"
        X["taskowner"] = "<div class='label'>Owner</div>  <ul class='owner'><li>" + X["taskowner"] + "</ul>"
        X["developers"] = "<div class='label'>Developers</div> <ul class='developers'>" + self.developers_ashtml() + "</ul>"
        X["users"] = "<div class='label'>Users</div> <ul class='users'>" + self.users_ashtml() + "</ul>"
        X["interestedparties"] = "<div class='label'>Interested Parties</div> <ul class='interestedparties'>" + self.interested_ashtml() + "</ul>"
        X["influencingfactors"] = "<div class='label'>Influencing Factors</div> <div class='factors'>" + self.factors_ashtml()+ "</div>"
        X["requirements"] = "<div class='label'>Requirements</div> <div class='requirements'>" + self.reqs_ashtml() + "</div>"
        return """
<div class="Inputs">
<h2 id="input_heading">Inputs</h2>
%(tasksponsor)s
%(taskowner)s
%(developers)s
%(users)s
%(interestedparties)s
%(influencingfactors)s
%(requirements)s
</div>
""" % X


class Output(object):
    def __init__(self, output_type, location, description):
        self.output_type = output_type
        self.location = location
        self.description = description
    def json(self):
        return {
            "output_type" : self.output_type,
            "location" : self.location,
            "description" : self.description,
        }
    def ashtml(self):
        X = self.json()
        return """
<div class="Output">
<b>%(output_type)s</b>
%(location)s
<ul>%(description)s
</ul>
</div>
""" % X

class Outputs(object):
    def __init__(self):
        self.expected = []
        self.actual = []
        self.arisingpossibilities = []
    def json(self):
        return {
            "expected" : self.expected,
            "actual" : [ x.json() for x in self.actual ],
            "arisingpossibilities" : self.arisingpossibilities,
        }
    def expected_ashtml(self):
        if self.expected == []:
            return ""
        R = ["<ul>"]
        for i in self.expected:
            R.append("\n<li class='expected_item'>")
            R.append(i)
        R.append("\n</ul>")
        return "".join(R)
    def arising_ashtml(self):
        if self.arisingpossibilities == []:
            return ""
        R = ["<ul>"]
        for i in self.arisingpossibilities:
            R.append("\n<li class='arisingpossibilities_item'>")
            R.append(i)
        R.append("\n</ul>")
        return "".join(R)
    def actual_ashtml(self):
        if self.actual== []:
            return ""
        R = ["<ul>"]
        for i in self.actual:
            R.append("\n<li class='actual_item'>")
            R.append(i.ashtml())
        R.append("\n</ul>")
        return "".join(R)
    def ashtml(self):
        X = self.json()
        X["expected"] = "<div class='expected'>" + self.expected_ashtml() +"</div>"
        X["actual"] = "<div class='actual'>" + self.actual_ashtml() +"</div>"
        X["arisingpossibilities"] = "<div class=''>" + self.arising_ashtml() +"</div>"
        return """
<div class="Outputs">
<h2 id="outputs_heading">Outputs</h2>
<h3 id="expected_heading">Expected</h3>
%(expected)s
<h3 id="expected_heading">Actual</h3>
%(actual)s
<h3 id="arisingpossibilities_heading">Realistic possibilities arising as a result of activity on this task</h3>
%(arisingpossibilities)s
</div>
""" % X

class Subtask(object):
    def __init__(self, tasktype, what ):
        self.tasktype = tasktype
        self.what = what
    def json(self):
        return {
            "tasktype" : self.tasktype,
            "what" : self.what,
        }

def see_task(taskid):
    # FIXME: This would be nicer to link to where the task is visible, but this is good enough for now.
    return "See task: "+repr(taskid)

class Relatedtasks(object):
    def __init__(self):
        self.tasksenablingthis = []
        self.subtasks = []
        self.cotasks = []
    def json(self):
        return {
            "tasksenablingthis" : self.tasksenablingthis,
            "subtasks" : [x.json() for x in self.subtasks],
            "cotasks" : self.cotasks,
        }
    def subtasks_ashtml(self):
        if self.subtasks== []:
            return ""
        R = ["<ul>"]
        for i in self.subtasks:
            R.append("\n<li class='subtask_item'>")
            if i.tasktype == "task":
                R.append(see_task(i.what))
            elif i.tasktype == "microtask":
                R.append(str(i.what))
            else:
                R.append(repr(i.json()))
        R.append("\n</ul>")
        return "".join(R)

    def tasksenablingthis_ashtml(self):
        if self.tasksenablingthis== []:
            return ""
        R = ["<ul>"]
        for i in self.tasksenablingthis:
            R.append("\n<li class='tasksenablingthis_item'>")
            R.append(see_task(i))
        R.append("\n</ul>")
        return "".join(R)
    def cotasks_ashtml(self):
        if self.cotasks== []:
            return ""
        R = ["<ul>"]
        for i in self.cotasks:
            R.append("\n<li class='cotask_item'>")
            R.append(see_task(i))
        R.append("\n</ul>")
        return "".join(R)
    def ashtml(self):
        X = self.json()
        X["tasksenablingthis"] = "<div class='tasksenablingthis'>" + self.tasksenablingthis_ashtml() +"</div>"
        X["subtasks"] = "<div class='subtasks'>" + self.subtasks_ashtml() +"</div>"
        X["cotasks"] = "<div class='cotasks'>" + self.cotasks_ashtml() +"</div>"
        return """
<div class="Relatedtasks">
<h2 id="relatedtasks_heading">Related Tasks</h2>
<h3 id="tasksenablingthis_heading">Tasks that directly enable this task (dependencies)</h3>
%(tasksenablingthis)s
<h3 id="subtasks_heading">Sub Tasks</h3>
%(subtasks)s
<h3 id="cotasks_heading">Co-Tasks</h3>
%(cotasks)s
</div>
""" % X


# -------------------------- TO BE DIVVED ----------------------------------------------------
class Comment(object):
    def __init__(self, who, when , what ):
        self.who = who
        self.when = when
        self.what = what
    def json(self):
        return {
            "who" : self.who,
            "when" : self.when,
            "what" : self.what,
        }
    def ashtml(self):
        X = self.json()
        return "%(what)s<br>--<span class='commenter'>%(who)s</span>, <span class='commentdate'>%(when)s</span>\n" % X

class Update(object):
    def __init__(self, what, who, when, timespent, output, statuschange):
        self.what = what
        self.who = who
        self.when = when
        self.timespent = timespent
        self.output = output
        self.statuschange = statuschange
    def json(self):
        return {
            "what" : self.what,
            "who" : self.who,
            "date" : self.when,
            "timespent" : self.timespent,
            "output" : self.output,
            "statuschange" : self.statuschange,
        }
    def ashtml(self):
        X = self.json()
        if X["output"] != "":
            X["output"] = "Output: " + X["output"]
        if X["statuschange"] != "":
            X["statuschange"] = "Task status changed:" + X["statuschange"]
        return "%(date)s - %(who)s - %(what)s %(output)s %(statuschange)s , Time spent: %(timespent)s" % X



class Task(object):
    def __init__(self, taskid):
        self.taskid =  taskid              # OK
        self.taskname=  ""                 # OK
        self.description = Description()    # OK
        self.dashboard = Dashboard()       # OK
        self.inputs = Inputs()             # OK
        self.outputs = Outputs()           # OK
        self.relatedtasks = Relatedtasks() # 
        self.tasklog = []                  # OK
        self.discussion = []               # OK
        self.consolidateddiscussion = ""   # OK

    def tasklog_ashtml(self):
        if self.tasklog == []:
            return ""
        R = ["<ul>"]
        for update in self.tasklog:
            R.append("<li class='logupdate'>")
            R.append(update.ashtml())
        R.append("</ul>")
        return "".join(R)

    def discussion_ashtml(self):
        if self.discussion == []:
            return ""
        R = []
        for comment in self.discussion:
            R.append("<div class='discussioncomment'>\n")
            R.append(comment.ashtml())
            R.append("</div>\n")
        return "".join(R)

    def json(self):
        return {
            "taskid" :  self.taskid,
            "taskname" :  self.taskname,
            "description" : self.description.json(),
            "dashboard" : self.dashboard.json(),
            "inputs" : self.inputs.json(),
            "outputs" : self.outputs.json(),
            "relatedtasks" : self.relatedtasks.json(),
            "tasklog" : [x.json() for x in self.tasklog],
            "discussion" : [x.json() for x in self.discussion],
            "consolidateddiscussion" : self.consolidateddiscussion ,
        }
    def ashtml(self):
        X = self.json()
        X["description"] = self.description.ashtml()
        X["dashboard"] = self.dashboard.ashtml()
        X["inputs"] = self.inputs.ashtml()
        X["outputs"] = self.outputs.ashtml()
        X["tasklog"] = self.tasklog_ashtml()
        X["discussion"] = self.discussion_ashtml()
        X["relatedtasks"] = self.relatedtasks.ashtml()
        if X["consolidateddiscussion"] != "":
            X["consolidateddiscussion"] = """<h2 id="consolidateddiscussion_heading">Consensus</h2>\n<div class="consolidateddiscussion">%s</div>\n """ % (X["consolidateddiscussion"] ,)

        return """\
<div class="Task">
<div class="taskheader">Task</div>
<h1 class="taskname"><span class="taskid"># %(taskid)s : </span>%(taskname)s</h1>
%(dashboard)s
%(description)s
%(inputs)s
%(outputs)s
%(relatedtasks)s
<h2 id="tasklog_heading">Task Log</h2>
<div class="tasklog">%(tasklog)s</div>
<h2 id="discussion_heading">Discussion</h2>
<div class="discussion">%(discussion)s</div>
%(consolidateddiscussion)s
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

task.taskname = "Translated Template"
task.description.goal = "Short one line of what the task is designed to achieve/create."
task.description.result = "A practical, clear result of what will be possible as a result of achieving this task. This is best described in the case of a user story."
task.description.context = "The context in which this task sits. Has this task any history? Is it the result of any previous tasks - either within the project or outside."
task.description.benefits.append( "What benefits will be gained by working on this task")
task.description.benefits.append( "... and achieving its goals?")
task.description.benefits.append("Speculative as well as certained/realistically expected benefits are valid here.")

task.dashboard.status = "(Started, Running, Completed, Dropped, Stasis, Blocked)"
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

task.tasklog.append( Update(what="frob the flibble", who="tom", when="then", timespent="5", output="", statuschange="") )
task.tasklog.append( Update(what="jibble the jabble", who="dick", when="now", timespent="5", output="", statuschange="") )
task.tasklog.append( Update(what="bibble bobble", who="harry", when="soon", timespent="5", output="", statuschange="") )

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

task.relatedtasks.subtasks.append( Subtask("microtask", "Step to the left"))
task.relatedtasks.subtasks.append( Subtask("microtask", "jump to the right" ))
task.relatedtasks.subtasks.append( Subtask("microtask", "pull knees in tight" ))
task.relatedtasks.subtasks.append( Subtask("task", 5 ))
task.relatedtasks.subtasks.append( Subtask("task", 6 ))
task.relatedtasks.subtasks.append( Subtask("task", 7 ))

task.relatedtasks.cotasks.append( 8 )
task.relatedtasks.cotasks.append( 9 )
task.relatedtasks.cotasks.append( 10 )

# pprint.pprint ( task.json(), width=170 )

T.store_task(task)
T.close()

U = Tasks("taskfile")
foo = U.get_task(1)
# print "========================================================================================================="
# pprint.pprint ( foo.json(), width=170 )
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

# dumptask(foo.json())

# FIXME - currently this STILL outputs things like (...,...,...) and some lists.
# Generally where there is a list or dict or tuple of base types
print "<html>"
print """<head>
<style>
.taskheader { display: None; }
.label { font-weight: bold; }
h1 {
    font-weight: bold;
    font-size:20pt;
}
h2 {
    font-weight: bold;
    font-size:17pt;
}
.taskname {
    margin-bottom: 1em;
}
.Dashboard {
    width: 20em;
    margin: 5px;
    padding: 5px;
    border-style: solid;
    border-width: thin;
    float: right;
}
.dashitem { clear:both; }
.discussioncomment {
    margin-bottom: 1em;
    clear:both; 
}
.commenter, .commentdate {
    font-style: italic;
}

.goal , .result , .context {
    margin-bottom: 1em;
}
body {
    font-size:10pt;
    font-family:verdana,arial,helvetica,sans-serif;
    line-height:1.5;
    padding: 0 30 0 40;
}
</style>
</head>
"""
print "<body>"
print foo.ashtml()
print "</body></html>"
