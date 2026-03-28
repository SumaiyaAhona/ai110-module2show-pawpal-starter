# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design included four main class: Owner, Pet, Task, and Scheduler. The Owner class stores information about the use and manages multiple pets. The Pet class represents each pet and keeps track of its associated tasks. The Task class stores details such as the task name, priority, and status. The Scheduler class is responsible for oprganizing tasks, sorting them by time, and detecting scheduling clashes. This structure will separtes the responsiblities and make it easier to manage. 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes my design changed during implementation as I clarified how tasks were stored and managed. I replaced time as a tring witha datetime object because it didn't allow accurate time comparisons or conflict detection past exact matches. I added duration field so I could detect the overlapping. I also changed the scheduler from storing all tasks in a single list to grouping them by pet using a dictionary. This can help detect conflicts to work per pet, since different pets can have tasks simultaneously. Then I introduced a schedule_task method in Owner and lnked it with Scheduler to make sure the tasks are added in one place, avoiding inconsistencies. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler only detects conflicts when task times overlaps and does not automatically reschedule tasks. This keeps the logic simple, readable, and understandable, which is sufficient for a smal personal pet care app where the owner can manually adjust conflicts.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
