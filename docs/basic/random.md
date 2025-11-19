# Weighted-random attack behavior

When running emulation scenarios multiple times, the emulated adversary should be able to create different attack paths across runs to improve the training experience for security personnel.
To enable varying attack paths that use different abilities to reach a defined goal, Bounty Hunter can be set up to use a probabilistic decision-making method with weighted randomness.
This means that Bounty Hunter can make different choices from the same input by randomly selecting abilities based on their assigned probabilities.
Instead of always picking the ability with the highest reward, Bounty Hunter can choose the next ability based on future rewards in a weighted-random manner.
This results in varied attack paths where both the chosen abilities and their execution order can change.
Additionally, Bounty Hunter can select and execute abilities unrelated to the defined goal (e.g., to obfuscate its intentions), and users can configure it to have multiple goals, ensuring that the assessment outcome isn’t predetermined.
For reproducibility, Bounty Hunter’s random selection algorithm can be seeded.