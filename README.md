# Bounty Hunter

Bounty Hunter is a Plugin for [MITRE Caldera](https://github.com/mitre/caldera) developed and implemented by Fraunhofer FKIE.
The biggest asset of the Bounty Hunter Plugin is the new Bounty Hunter Planner that allows the emulation of comprehensive, realistic cyberattack chains.

To get an idea of Bounty Hunter's capabilities, its key features are described below.

- **Autonomous, reward-driven planning.** To allow users to run emulations without the need to define playbooks or provide detailed information, Bounty Hunter tries to autonomously reach its user-defined goal. It utilizes facts and requirements to link abilities and calculates anticipated future rewards of abilities for its reward-driven decision making.

- **Support for initial access and privilege escalation.**  At the moment, no Caldera planner offers support for initial access or privilege escalation methods. Bounty Hunter extends Caldera's capabilities by offering support for both in a fully autonomous manner. This enables it to emulate complete cyberattack chains.

- **Adaptable adversarial attributes.** Bounty Hunter allows the emulation of adversaries with desired attributes, e.g., stealthy vs. easy-to-detect. To do so, it employs properties of abilities and custom parameters during its future reward calculation.

- **Weighted-random attack behavior.** Bounty Hunter's attack behavior is goal-oriented and reward-driven, similar to the Look-Ahead Planner. But, instead of picking the ability with the highest future reward value every time, it offers the possibility to pick the next ability weighted-randomly. This adds an uncertainty to the planner's behavior which allows repeated runs of the same operation with completely different results. This might be very useful in some cases, e.g., when repeating scenarios in training environments.

- **Further configurations for more sophisticated and realistic attack behavior.**  Bounty Hunter offers various configuration parameters, e.g., "locking" abilities, reward updates, and final abilities, to customize the emulated attack behavior (see "Bounty Hunter configuration").

# Resources
For further information, we refer to the following resources:

- [📜 Documentation](https://bounty-hunter.readthedocs.io/en/latest/)
- [✍️ Blog Post](https://lolcads.github.io/posts/2024/09/bountyhunter/)

# Installation

- Download the plugin
- Copy the `bountyhunter` directory into `caldera/plugins` and enable the plugin in the Caldera server's configuration (`caldera/conf/<config>.yml`)
- Install requirements: `pip install -r requirements.txt`
- Unzip `caldera/plugins/bountyhunter/payloads/payloads.zip` to `caldera/plugins/bountyhunter/payloads`
- Remember to add the `--build` flag when starting the Caldera server with Bounty Hunter for the first time
- Note: Bounty Hunter works with Caldera v5.0.0 or v4.2.0

## Docker Deployment
- Download the plugin from the GitHub repository
- Copy the `bountyhunter` directory into `caldera/plugins` and enable the plugin in the Caldera server's configuration (`caldera/conf/<config>.yml`)
- Add the following lines to the `caldera/Dockerfile` to install the Bounty Hunter requirements during the docker build process, e.g., at line 77 after the installation of the emu plugins requirements in lines 69-76 
```
WORKDIR /usr/src/app/plugins/bountyhunter
RUN pip3 install -r requirements.txt
```
- Continue the docker build as usual
- Note: When using a Caldera docker image, problems during the web ui login might occur ([see here](https://github.com/mitre/caldera/issues/3002)). To avoid problems, add the `--insecure` flag to the docker entry point (`ENTRYPOINT ["python3", "server.py", "--insecure"]`)

# Contributing
We welcome any contributions, questions and ideas.
If you have any questions or want to contact us, feel free to open an issue or a pull request.

# License
Released under Apache-2.0 license. For more information see LICENSE.