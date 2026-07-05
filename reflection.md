# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
  - My initial UML design was to be simple while having 4 different classes. Each class have their own unique information and methods. 
- What classes did you include, and what responsibilities did you assign to each?
  - I chose to have 4 classes; Owner, Pet, Task, and Scheduler. The Owner class contains information such as id, name, preferences, and available time. They also have methods to add, edit, and remove pets and tasks. The Pet class is in charge of getting assigned tasks that the Owner class manages. The Task class is managed by the Owner. The Scheduler class organizes Tasks.

**b. Design changes**

- Did your design change during implementation?
  - Yes.
- If yes, describe at least one change and why you made it.
  - One change I made was that my Task class was missing pet_id so that task can be assigned to that particular pet.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
  - My scheduler considers time and priority.
- How did you decide which constraints mattered most?
  - I felt like time and priority is the most important when scheduling tasks. Just like real life, people focus on the most important tasks.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
  - One tradeoff my scheduler makes is the generate_plan function. The tasks are sorted by priority, then is added one by one until there is no more time budget. Time and priority might fight over each other.
- Why is that tradeoff reasonable for this scenario?
  - The tradeoff is reasonable for this because the code more easy to understand but is not guranteed to maximize on tasks scheduled that are within the time budget.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
  - I used Claude Code to help brainstorm, come up with fixes, and to explain their code and thought process.
- What kinds of prompts or questions were most helpful?
  - Prompts such as "Act as a python developer..." and "Review these files: ..." were the most helpful. Having the AI act as this helps make the process more professional and realistic. Double checking code for certain contraints or bugs helped make sure the code quality was up to standard.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
  - One moment where I did not accept an AI suggestion was when I asked it to do something like "help implement this feature", and the AI ended up changing almost the whole file.
- How did you evaluate or verify what the AI suggested?
  - I evaluated the AI's suggestion by checking the rubric and my UML design diagram. If it is doing too much I would most likely reject them.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
  - I tested if the Streamlit app would work properly and was responsive. I also tested adding owners, pets, assigning tasks, and generating a schedule.
- Why were these tests important?
  - These tests are important because they are the main features for the app. If they weren't tested, the app could end up not working as expected. Testing main features should be prioritized.

**b. Confidence**

- How confident are you that your scheduler works correctly?
  - I am confident that my scheduler works correctly because of the tests I have done in main.py and test_pawpal.py.
- What edge cases would you test next if you had more time?
  - Edge cases I would test if I had more time would be testing the max amount of owners, pets, and tasks before the app may start slowing down or stop working.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
  - I am most satisfied with how my project is responsive and seem to have very few bugs.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
  - If I had another iteration, I would try to improve code readability.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
  - One important thing I learned while working with AI on this project is that you have to review everything the AI suggests. If you don't review, you can run into errors that might affect the whole codebase.