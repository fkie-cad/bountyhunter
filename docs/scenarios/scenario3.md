# Varying detectability

This example shows how Bounty Hunter facilitates the emulation of adversaries with varying detectability of its Nmap host scan during initial access as an example for adaptable attributes.

We configure two scenarios: (1) _Demo Scenario - Detectability (loud)_ with a detectability weight of 1 and (2) _Demo Scenario - Detectability (silent)_ with a detectability weight of -1, configured in the respective `scenario_params.yml`.
Both scenarios have the goal of gathering information about the current user on a target machine to allow the investigation of Bounty Hunter's actions during initial access.

```yaml
name: Demo Scenario - Detectability (loud)
description: Use with adversary profile "Bounty Hunter - Demo Adversary Profile" 
  or "Bounty Hunter - Initial Access Tester" and elevated agent running on host machine.
final_abilities:
  - bd527b63-9f9e-46e0-9816-b8434d2b8989           # Current User
detectability_weight: 1
```

Next, we define the detectability of two Nmap host scan abilities: _Nmap host scan (T5)_ uses the "insane" timing setting with an assigned detectability of 2 while _Nmap host scan (T2)_ uses the "polite" timing setting with an assigned detectability of 1.
The detectabilities of both abilities are configured in the scenarios' `detectability_data.yml`:

```yaml
9c109820-6c4d-4378-9a82-00a75323bfda: 2.0     # Nmap host scan (T5)
cb53b600-783b-4cb3-92de-c58a7f563ce8: 1.0     # Nmap host scan (T2)
```

When using the scenario _Demo Scenario - Detectability (loud)_ and the adversary profile _Bounty Hunter - Initial Access Tester_, the rewards of the two Nmap scan abilities (with a default base reward of 1) are:

```yaml
Nmap host scan (T5): 1 * 2^(1) = 2
Nmap host scan (T2): 1 * 1^(1) = 1
```

Bounty Hunter chooses to execute _Nmap host scan (T5)_ - motivated by its high reward, due to its high detectability and the detectability weight of 1.
Rerunning the operation using the scenario _Demo Scenario - Detectability (silent)_, it starts the operation with _Nmap host scan (T2)_ instead, because of the negative detectability weight and its influence on the reward values:

```yaml
Nmap host scan (T5): 1 * 2^(-1) = 0.5
Nmap host scan (T2): 1 * 1^(-1) = 1
```