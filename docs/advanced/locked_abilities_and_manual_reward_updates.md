# Locked abilities and manual reward updates

Locking abilities and performing manual reward updates enables Bounty Hunter to perform more realistic, more sophisticated and customized attacks.
Consider the scenario `demo_locked_abilities` and the example adversary _Bounty Hunter - Locked Abilities Demonstrator_ with the following abilities: _Find files_, _Stage sensitive files_, _Create staging directory_, _Compress staged directory_, and _Exfil staged directory_.
The ability _Exfil staged directory_ has a high reward value, e.g., `1000`.
When using Caldera's Look-Ahead Planner, the agent will execute the following attack chain:
- Create staging directory
- Compress staged directory
- Exfil staged directory
- Find files (x3)
- Stage sensitive files (for each found file)
- (...)

This results in an empty directory being exfiltrated because it is the "shortest path to the goal" since it follows the highest future reward values.
Now, Bounty Hunter can be configured to "lock" the _Compress staged directory_ ability and only "unlock" it by executing the ability _Stage sensitive files_.
This means, it will only compress the staged directory after files have been staged. See example configuration below.

```
final_abilities:
- ea713bc4-63f0-491c-9a6f-0b01d560b87e        # exfiltrate staged directory
locked_abilities:
- 300157e5-f4ad-4569-b533-9d1fa0e74d74        # compress staged directory
reward_updates:
4e97e699-93d7-4040-b5a3-2e906a58199e:         # stage sensitive files
  300157e5-f4ad-4569-b533-9d1fa0e74d74: 1     # compress staged directory
```

Now, when running an operation using Bounty Hunter and the above configuration, the following attack chain is generated and executed:
- Create staging directory
- Find files (3x)
- Stage sensitive files (3x)
- Compress staged directory
- Exfil staged directory

As we can see, the resulting attack chain is more sophisticated and more realistic because the exfiltrated directory is not empty.
Furthermore, the planner automatically stops the operation after executing the goal ability, compared to the Look-Ahead Planner that continued with collecting and staging files after already exfiltrating.
