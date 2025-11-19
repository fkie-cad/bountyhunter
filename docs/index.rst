Welcome to Bounty Hunter's documentation!
=========================================

**Bounty Hunter** is a custom Caldera Plugin developed and implemented by Fraunhofer FKIE.
The biggest asset of the Bounty Hunter Plugin is the new Bounty Hunter Planner that allows the automated emulation of comprehensive, realistic cyberattack chains.
To get an idea of Bounty Hunter's capabilities, its key features are described below.

**Autonomous, reward-driven planning.**
To allow users to run emulations without the need to define playbooks or provide detailed information, Bounty Hunter autonomously pursues its user-defined goal ability.
It utilizes facts and requirements to link abilities and calculates anticipated future rewards of abilities for its reward-driven decision making.

**Autonomous initial access and privilege escalation.**
At the moment, no Caldera planner offers support for initial access or privilege escalation methods.
Bounty Hunter extends Caldera's capabilities by offering support for both in a fully autonomous manner.
This enables it to emulate complete cyberattack chains.

**Adaptable adversarial attributes.**
Bounty Hunter allows the emulation of adversaries with desired attributes, e.g., stealthy vs. easy-to-detect.
To do so, it employs properties of abilities and custom parameters during its future reward calculation.

**Weighted-random attack behavior.**
Bounty Hunter's attack behavior is goal-oriented and reward-driven, similar to the Look-Ahead Planner.
But, instead of picking the ability with the highest future reward value every time, it offers the possibility to pick the next ability weighted-randomly.
This adds an uncertainty to the planner's behavior which allows repeated runs of the same operation with completely different results.
This allows repeating scenarios in training environments with variety in the emulated attacks.

**Further configurations for more sophisticated and realistic attack behavior.**
Bounty Hunter offers various configuration parameters, e.g., "locking" abilities, reward updates, and final abilities, to customize the emulated attack behavior (see "Bounty Hunter configuration").

.. note::

   This project and this documentation are under active development.
   Please reach out to us on GitHub if you encounter any mistakes or issues.

.. toctree::
   :caption: Basic Information

   basic/installation.md
   basic/getting_started.md
   basic/planning.md
   basic/tactics.md
   basic/properties.md
   basic/random.md

.. toctree::
   :caption: Example Scenarios
   :maxdepth: 1
   :glob:

   scenarios/*

.. toctree::
   :caption: Advanced Information
   :glob:

   advanced/*