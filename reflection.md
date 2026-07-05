# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
  My initial UML design was to be simple while having 4 different classes. Each class have their own unique information and methods. 
- What classes did you include, and what responsibilities did you assign to each?
  I chose to have 4 classes; Owner, Pet, Task, and Scheduler. The Owner class contains information such as id, name, preferences, and available time. They also have methods to add, edit, and remove pets and tasks. The Pet class is in charge of getting assigned tasks that the Owner class manages. The Task class is managed by the Owner. The Scheduler class organizes Tasks.

**b. Design changes**

- Did your design change during implementation?
  Yes
- If yes, describe at least one change and why you made it.
  One change I made was that my Task class was missing pet_id so that task can be assigned to that particular pet.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
  My scheduler considers time and priority.
- How did you decide which constraints mattered most?
  I felt like time and priority is the most important when scheduling tasks. Just like real life, people focus on the most important tasks.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
  One tradeoff my scheduler makes is the generate_plan function. The tasks are sorted by priority, then is added one by one until there is no more time budget. Time and priority might fight over each other.
- Why is that tradeoff reasonable for this scenario?
  The tradeoff is reasonable for this because the code more easy to understand but is not guranteed to maximize on tasks scheduled that are within the time budget.

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
