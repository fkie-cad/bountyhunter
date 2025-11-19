# Adaptable adversarial attributes

When conducting security assessments and training, it might be beneficial to emulate adversaries that are adaptable in their attributes, such as their level of expertise.
We designed Bounty Hunter’s future reward calculation to support custom parameters that utilize specific properties of abilities.
By defining these properties (e.g., detectability of attack actions), Bounty Hunter can emulate adversaries with desired characteristics.
Additionally, the future reward calculation allows for implementing binary conditions based on these properties to facilitate the emulation of adversaries that exclusively use abilities with selected traits.
For example, Bounty Hunter can simulate adversaries with varying levels of difficulty for defenders by considering the detectability of attack actions, i.e., an indicator of how likely an ability is to be detected by security measures.
Adversaries can test their actions in controlled environments to see how detectable they are before launching an attack.
To represent this behavior, we extend Bounty Hunter’s future reward calculation by introducing a new factor, `d(a)`, which represents the detectability of ability `a`.
We also add a detectability weight parameter `w` to configure how much detectability influences the final reward.
The adjusted future reward of an ability `f∗(a)` is calculated as follows:
`f*(a)=f(a) × d(a)^w`

For more details on how Bounty Hunter uses action properties, see Example "Varying detectability".