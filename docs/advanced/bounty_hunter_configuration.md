# Bounty Hunter configuration

Bounty Hunter can be configured in many ways to further customize the emulated attack behavior.
Its parameters can be configured using scenario configuration files (`bountyhunter/conf/<scenario_name>/scenario_params.yml`).
Which scenario Bounty Hunter should use can be configured in its configuration file (`bountyhunter/data/planners/e1bb9388-1845-495d-b67b-ad61a31ff6cd.yml`) using the name of the scenario directory (e.g. `demo_initial_access`).

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

## Example scenario

The following scenarion configuration shows how the various parameters can be configured.

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