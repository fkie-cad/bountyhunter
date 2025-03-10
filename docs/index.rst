Welcome to Bounty Hunter's documentation!
===================================

**Bounty Hunter** is a custom Caldera Plugin developed and implemented by Fraunhofer FKIE.
The biggest asset of the Bounty Hunter Plugin is the new Bounty Hunter Planner that allows the emulation of complete, realistic cyberattack chains.

To get an idea of the Bounty Hunter's capabilities, its key features are described below.
Furthermore, since it might seem similar to existing Caldera planners at first glance, e.g., the Look-Ahead Planner, their differences are described as well.

- **Weighted-Random Attack Behavior.** The Bounty Hunter's attack behavior is goal-oriented and reward-driven, similar to the Look-Ahead Planner. But, instead of picking the ability with the highest future reward value every time, it offers the possibility to pick the next ability weighted-randomly. This adds an uncertainty to the planner's behavior which allows repeated runs of the same operation with completely different results. This might be very useful in some cases, e.g., in training environments.

- **Support for Initial Access and Privilege Escalation.**  At the moment, no Caldera planner offers support for Initial Access or Privilege Escalation methods. The Bounty Hunter extends Caldera's capabilities by offering support for both in a fully autonomous manner. This enables it to emulate complete cyberattack chains.

- **Further Configurations for more sophisticated and realistic Attack Behavior.**  The Bounty Hunter offers various configuration parameters, e.g., "locking" abilities, reward updates, and final abilities, to customize the emulated attack behavior (see section "Bounty Hunter Configuration" below). For example, the ability `Compress staged directory` can be configured as "locked" and only be "unlocked" by executing `Stage sensitive files` in order to prevent that an empty staging directory gets compressed and exfiltrated. This example of how to use these parameters is described in more detail in the section "Locked Abilities and Manual Reward Updates".

.. note::

   This project is under active development.

Contents
--------

.. toctree::

   basic_usage
