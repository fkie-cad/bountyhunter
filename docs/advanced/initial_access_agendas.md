# Initial Access Agendas

Initial Access Agendas are predefined ability chains that Bounty Hunter uses during the initial access phase.
After scanning the potential targets, the agendas help the planner decide how to continue the operation.
Defining the agendas as ability chains allows more sophisticated scenarios than using the "classic" Caldera approach of using facts and requirements.
Also, during the initial access phase, the attacker's behavior should be more straight-forward instead of simply adding all abilities to the current adversary and letting the planner decide which ability to execute based on facts and requirements.
Each agenda should have the goal to start a new Caldera agent on the target machine.

## Agenda configuration
Agendas are defined for each scenario in `bountyhunter/conf/<scenario_name>/agenda_mapping.json`.
Each agenda has a name, requirements and a list of ability IDs.
An agenda is considered "valid" if all its requirements are met.
At the moment, options for requirements are `port`, `service_info` and `version_info`, i.e., the facts gathered during the port scanning phase and parsed by the nmap parser.

The following example agenda implements an SSH Brute Force Attack using Hydra.
As requirements, the target host must have an open port 22.
Three abilities are added to the running operation and executed:
1. `Get SSH credentials using Hydra brute force`: Uses Hydra and custom wordlists containing usernames and passwords to use.
2. `Copy start agent via scp over ssh`: Copies the `start_agent` script to the target machine using the gathered SSH credentials.
3. `Run start_agent script using known SSH credentials`: Executes the copied script in order to start a new Caldera agent.

```yaml
{
  "agendas": [
    {
      "name": "ssh bruteforce linux/windows",
      "requirements": {
        "port": "22"
      },
      "ability_ids": [
        "85d6ce79-07ea-4ed4-b763-8a6f7d5591d7",
        "6a49e8f3-0c00-436e-a848-06de496a942f",
        "099ea47f-fa4d-4c2e-a089-601eefecb962"
      ],
      "reward": 100,
      "detectability": 2.0,
      "success_rate": 2.0
    }
  ]
}
```

To add a new agenda, implement the respective abilities, e.g., for exploiting a known vulnerability, and create a new entry in the `agendas` list.
Then, add the ability IDs, a name, and the requirements.
Bounty Hunter will autonomously decide if an agenda is valid and will consider executing it during the Initial Access phase.

Optionally, agendas can also be assigned a reward, a detectability, and a success rate.
These values are used to calculate the anticipated reward for all valid agendas in a similar manner as for the future reward calculation of abilities.