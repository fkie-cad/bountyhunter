# Bounty Hunter configuration

Bounty Hunter can be configured in many ways to further customize the emulated attack behavior.
Its parameters can be configured using scenario configuration files (`bountyhunter/conf/<scenario_name>/scenario_params.yml`).
Which scenario Bounty Hunter should use can be configured on its UI page or in its configuration file (`bountyhunter/data/planners/e1bb9388-1845-495d-b67b-ad61a31ff6cd.yml`) using the name of the scenario directory (e.g. `demo_initial_access`).

## Basic parameters
The following lists shows the basic parameters used by Bounty Hunter including a short description and the default values.

- `weighted_random`: `False` - Toggles weighted random attack behavior. If enabled, the next ability to execute is picked weighted-randomly depending on the abilities' reward values. If disabled, the ability with the highest reward is picked.
- `seed`: `None` - Seed value to use for random decisions during the weighted-random attack behavior as well as the initial access and privilege escalation phases. Allows reproduction.
- `final_abilities`: `None` - List of final ability IDs. Final abilities are automatically assigned a high reward value by default. Operation stops when one of those abilities is executed.

## More optional parameters
The following parameters are purely optional and do not need to be configured for a basic emulation.
However, they allow further customization for more complex behaviors.

- `discount`: `0.9` - Discount factor for the future reward calculation.
- `depth`: `3` - Recursive depth for the future reward calculation.
- `default_reward`: `1` - Default reward value for all abilities.
- `default_final_reward`: `1000` - Default reward value for all final abilities. Should be larger than the default_reward, so that the planner tries to pursuit them (more likely).
- `default_reward_update`: `200` - Default reward update value. After executing an ability all "following" abilities' (i.e., abilities that require facts that are collected by the executed ability) reward values are increased by this value.
- `locked_abilities`: `None` - List of locked ability IDs. These abilities will not be executed until they are "unlocked" by increasing their ability reward (manually or automatically).
- `ability_rewards`: `None` - List of ability IDs and corresponding reward values. Allows further attack behavior customization.
- `reward_updates`: `None` - List of custom reward update values per ability ID. Allows further attack behavior customization and "unlocking" abilities that are not logically (i.e., by facts) connected.

## Detectability of abilities
To allow for selective loud vs. silent adversaries, the detectabilities of abilities can be configured in a scenario's `detectability_data.yml`.

```yaml
9c109820-6c4d-4378-9a82-00a75323bfda: 2.0     # Nmap host scan (T5)
cb53b600-783b-4cb3-92de-c58a7f563ce8: 1.0     # Nmap host scan (T2)
```

The weight of the detectabilities of actions determines their influence on the final reward and whether the adversary should be loud (e.g., 1) or silent (e.g., -1).
The weight and a default detectability can be configured in the scenario's `scenario_params.yml`:

- `detectability_weight`: `0` - Exponential weight of abilities' detectability.
- `default_detectability_factor`: `1` - Default detectability for abilities that have no detectability configured.

The adjusted future reward of an ability `f∗(a)` using the detectability of an ability `d(a)` and the detectability weight `w` is calculated as follows:
`f*(a)=f(a) × d(a)^w`

## Success of abilities
Bounty Hunter also integrates a success factor of abilities into its reward calculation, that depends on the outcome of past ability execution.
The success data of abilities can be configured in the scenario's `success_data.yml`:

```yaml
9c109820-6c4d-4378-9a82-00a75323bfda: 1.0     # Nmap host scan (T5)
cb53b600-783b-4cb3-92de-c58a7f563ce8: 2.0     # Nmap host scan (T2)
```

Bounty Hunter allows to automatically update the success data of abilities, depending on the success of their last execution.
By default, Bounty Hunter counts an execution as _successful_ if the ability link was executed without an error
The success condition of an ability can be configured in its `additional_info` field to check whether the ability was executed without an error (`no-error`) or the ability gathered at least one fact (`facts-collected`):

```yaml
additional_info:
  success_condition: facts-collected
```

Bounty Hunter can automatically update the success factors of abilities (using `update_success_factors`) utilizing exponential smoothing.
For example, after successful execution of _Nmap host scan (T5)_ its success factor would be increased to `0.3 * 2 + 0.7 * 1 = 1.3`.
If the execution had failed, the updates factor would be decreased to `0.3 * 0.5 + 0.7 * 1 = 0.85`.
The utilized alpha, minimum, and maximum values can also be configured, if necessary.

Similar to the detectability, a success weight determines the influence and "direction" of the success factors.

- `success_weight`: `0` - Exponential weight of abilities' success factors.
- `default_success_factor`: `1` - Default success factor for abilities that have no success factor configured.
- `default_success_condition`: `no-error` - Can be configured in an ability's `additional_info` field (see above). Options are: `no-error` and `facts-collected`.
- `update_success_factors`: `False` - Determines whether the configured success factors should be updated and overwritten.
- `success_alpha`: `0.3` - Alpha value used by exponential smoothing during success factor updates.
- `success_max_value`: `2` - Maximum success factor value used by exponential smoothing during success factor updates.
- `sucess_min_value`: `0.5` - Minimum success factor value used by exponential smoothing during success factor updates.

The adjusted future reward of an ability `f∗(a)` using the success factor of an ability `s(a)` and the success weight `w` is calculated as follows:
`f*(a)=f(a) × s(a)^w`

## Example scenario configuration with all possible parameters

The following scenario configuration shows how the various parameters can be configured.

```yaml
name: Default scenario
description: Default scenario configuration showing all possible parameters.
seed: 4711
weighted_random: True
depth: 3
discount: 0.9
default_final_reward: 1000
default_reward: 1
default_reward_update: 200
detectability_weight: 0
default_detectability_factor: 1
success_weight: 0
default_success_factor: 1
default_success_condition: no-error
update_success_factors: False
success_alpha: 0.3
success_max_value: 2
sucess_min_value: 0.5
final_abilities:
  - ea713bc4-63f0-491c-9a6f-0b01d560b87e             # exfiltrate staged directory
ability_rewards:
  4e97e699-93d7-4040-b5a3-2e906a58199e: 1000         # stage sensitive files
locked_abilities:
  - 300157e5-f4ad-4569-b533-9d1fa0e74d74             # compress staged directory
reward_updates:
  6469befa-748a-4b9c-a96d-f191fde47d89:              # create staging directory
    4e97e699-93d7-4040-b5a3-2e906a58199e: 10000      # stage sensitive files
  4e97e699-93d7-4040-b5a3-2e906a58199e:              # stage sensitive files
    300157e5-f4ad-4569-b533-9d1fa0e74d74: 1          # compress staged directory
  300157e5-f4ad-4569-b533-9d1fa0e74d74:              # compress staged directory
    4e97e699-93d7-4040-b5a3-2e906a58199e: -10000     # stage sensitive files
    90c2efaa-8205-480d-8bb6-61d90dbaf81b: -10000     # find files
```