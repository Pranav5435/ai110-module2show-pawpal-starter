# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
The system is built around four classes: Owner holds a collection of pets, Pet holds a list of tasks, Task describes a specific activity and its attributes, and Scheduler is the brain of the whole thing handling sorting, filtering, and conflict detection. I designed the UML diagram before writing any code so I had a clear picture of how everything connected. Mapping out the relationships first made the actual implementation a lot smoother because I wasn't making structural decisions on the fly. It also made it easier to catch design problems early before they became coding problems.
**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
Owner originally had attributes like age, height, and health conditions, but I cut them because nothing in the system ever actually uses them. Keeping dead attributes around would have just added noise to the design without serving any real purpose. I also updated filter_tasks() to accept completion status and pet name after realizing a parameterless function couldn't return anything targeted or useful. Both changes came from asking whether each piece of the design was actually earning its place.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
The Scheduler weighs time, priority, and duration when organizing tasks, but time ended up being the most important factor. Scheduling is inherently chronological, so if something is due sooner it should come first regardless of how it is labeled. Priority and duration still matter, but they operate within the constraint that time sets. That ordering felt the most intuitive and closest to how someone would actually think about planning a day.
**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
Conflict detection only flags exact time overlaps using task duration and does not account for travel time between tasks. That is a conscious tradeoff though, because this is a simple home based pet care app where all tasks happen in the same location. Travel time just is not a real concern in that context, so adding that complexity would have been over-engineering. The current approach handles the actual use case cleanly without unnecessary overhead.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
I used AI for skeleton generation, algorithm implementation, and test generation across the project. The prompts that worked best were specific and had actual project files attached as context. Vague prompts consistently produced output I had to throw away or heavily rewrite, which cost more time than just being precise upfront. The more context I gave the model, the less cleanup I had to do on the other end.
**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
handle_recurrence() had a bug where it was generating copies of incomplete tasks instead of creating the next occurrence only after completion. I caught it by reading through the generated code carefully before accepting it rather than just running it and hoping for the best. It was a subtle logic error that would have been hard to trace through testing alone. That moment reinforced that critical reading of AI output is just as important as the prompt itself.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
I tested sorting order, conflict detection, recurrence logic, and filter behavior throughout the project. I also made sure to cover edge cases like empty task lists and non overlapping tasks to confirm the conflict detector correctly returns nothing in those situations. Testing the negative cases was just as important as confirming the happy path worked. Those edge cases are where bugs tend to hide in scheduling logic specifically.
**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
I would give my test suite a 4 out of 5 in terms of confidence. The main gaps I would want to fill are tasks with no time set and owners with no pets assigned, both of which are realistic scenarios I have not covered yet. Those cases exist in real usage and could expose assumptions baked into the logic. Filling them in would push my confidence to a solid 5.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
The most satisfying part was getting the algorithmic layer to actually work together as one system. Sorting, filtering, and conflict detection functioning cohesively rather than as three isolated pieces felt like the project finally clicking into place. Getting any one of them working individually was straightforward, but making them interact correctly took real thought. That integration was where the design decisions I made early on either paid off or did not.
**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
If I did this again, I would add a time input field to the UI from day one instead of treating it as something to wire up later. Time is the most central piece of how the scheduler works, so deprioritizing it in the interface never really made sense. Building around it from the start would have made the UI feel more coherent earlier in the process. It is an easy fix in hindsight but a meaningful one.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
The biggest thing AI taught me on this project is that fast code generation means nothing if you do not understand what you are accepting. I had to stay engaged and read critically the entire time rather than just prompting and moving on. The engineer still drives every decision, and AI is just a tool that executes within that direction. That dynamic made the project better, but only because I stayed in control of it.