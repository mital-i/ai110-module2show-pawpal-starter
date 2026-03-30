# PawPal+ Project Reflection

## 1. System Design

**Three core actions:** adding a pet, adding tasks for the pet, generate a schedule for the tasks based on constraints

**a. Initial design**

- Briefly describe your initial UML design.
  The initial UML design shows five main classes: Owner, Pet, Task, Scheduler, and Schedule. The Scheduler acts as the main container for the entire program, managing relationships between Owner, Pet, and a set of Tasks to make a Schedule. Relationships include composition (Scheduler has Owner and Pet), aggregation (Scheduler manages Tasks), and dependency (Scheduler generates Schedule).
- What classes did you include, and what responsibilities did you assign to each?

  - Owner - Represents the pet owner, holding information about available time, preferred time slots, and other preferences. Responsible for providing constraints that influence scheduling decisions.
  - Pet - Represents the pet, storing basic details like name, species, age, and special needs. Responsible for providing pet-specific information that may affect task selection.
  - Task - Represents individual pet care activities, containing details like title, duration, priority, category, frequency, and time preferences. Responsible for encapsulating task-specific logic such as priority scoring and due date checking.
  - Schedular - The core logic engine that takes Owner, Pet, and Tasks as input. Responsible for filtering eligible tasks, prioritizing them, resolving conflicts, generating the daily schedule, and explaining choices.
  - Schedule - Represents the output daily plan, containing scheduled tasks with timings and reasons. Responsible for displaying the plan and providing explanations for why tasks were chosen or omitted.

**b. Design changes**

- Did your design change during implementation. Yes
- If yes, describe at least one change and why you made it. I added a Schedular class to manage the rest of the 4 classes so that it would be easier to manage changes to the other objects. Schedular object makes it easy to access attributes and methods in the other 4 classes.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)? The schedule considers time, in particular it makes sure that no tasks for the same pet start at the same time. The tasks are ordered in chronological order by time.
- How did you decide which constraints mattered most? I decided time matters the most because it was important to do certain things in a timely way, such as feeding the pet on time and taking it to the vet. Priority is hard to measure while time is straightforward.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes. The scheduler uses slot-based scheduling (morning, afternoon, evening) where all tasks in the same preferred slot are scheduled starting at the same time, which can lead to overlaps within the slot. This simplifies the logic by avoiding complex algorithms but may result in unrealistic schedules where multiple tasks occur simultaneously for the same pet or across pets. However it also makes it easier to detect conflicts (we just check for overlap within a slot for a particular pet).
- Why is that tradeoff reasonable for this scenario? This tradeoff is reasonable for a pet care app prototype because it prioritizes feasibility of implementation and clear grouping by time preferences, allowing quick detection of time conflicts. In a real-world app, owners can manually adjust timings, and the warnings help identify issues without overcomplicating the core scheduling logic. It also prevents the app from crashing.

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
