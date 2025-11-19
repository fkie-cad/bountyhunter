# Getting started

To get an idea of how to configure Bounty Hunter and how to run an assessment with it, we refer to the "Initial Access and Privilege Escalation" example scenario.

**Usage notes:**
- The initial access phase of Bounty Hunter can be skipped by assigning the initial agent to the group `target`.
- When running multiple scenarios or repeating a scenario, make sure to terminate agents that are running on a target machine. Otherwise, Bounty Hunter will use those agents and skip the initial access phase.
- Initial Access and Privilege Escalation methods are only implemented as "weak" proof of concept for Windows and Linux targets.
