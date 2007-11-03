#!/usr/bin/python
"""
Sketchcode outline of task list manager for Kamaelia (and software in general)
"""

class dashboard(object):
    status = "(Started|Running|Completed|Dropped|Stasis|Blocked)"
    status_text = "Associated single sentence (eg why blocked)"
    currentdevelopers = "you!"
    devlocation = "Normally /Sketches/ initially"
    startdate = "date"
    milestonedate "date"
    milestonetag = "(met|slipped|missed)"
    expectedenddate = "(date|n/a)"
    enddate = "date"
    dateupdated = "date"
    estimatedeffortsofar = "int"

class update(object):
    what = ""
    who = "name"
    date = "date"
    timespent = "in 1/4 days"
    output = "if anything"
    statuschange = "if appropriate"

class descripton(object):
    goal = "Short one line of what the task is designed to achieve/create."
    result = "A practical, clear result of what will be possible as a result of achieving this task. This is best described in the case of a user story."
    context = "The context in which this task sits. Has this task any history? Is it the result of any previous tasks - either within the project or outside."
    benefits = "What benefits will be gained by working on this task, and achieving its goals? Speculative as well as certained/realistically expected benefits are valid here."

class requirement(object):
    reqtype = "(MUST|SHOULD|MAY|WOULDLIKE)"
    whofrom = "name"
    what = "string describing the requirement"

class inputs(object)
    tasksponsor = "WHO is the sponsor - (can be main developer)"
    taskowner = "WHO is the owner - (likely to be main developer)"
    developers = list of "name" (if empty list, assert task.dashboard.status == "stasis"
    users = list of "name"
    interestedparties = list of "name"
    requirements = list of requirement
    influencingfactors = list of "strings"

class output(object):
    outputtype = "(code|presentation|documentation)"
    location = list of "string"

class outputs(object):
    expected = list of "strings"
    actual = list of output
    arisingpossilities = list of "Realistic possibility arising as a result of activity on this task"

class microtask(object)
    description = "subtasks as bullet points with the sort of information you'd put on a project task page, but for which it seems overkill to create a project task page for."

class relatedtasks(object):
    tasksenablingthis = list of task
    subtasks = list of (microtask/task)
    cotasks = list of task

class comment(object):
    who = "name"
    when = "timedate"
    what = "string"

class Task(object):
    descripton
    dashboard
    tasklog = List of update
    inputs
    outputs
    relatedtasks
    discussion = list of comments
    consolidateddiscussion = "string"
