from numpy.random import choice, seed
from yaml import safe_load

from plugins.bountyhunter.app.helper.agenda_helper import AgendaHelper


class LogicalPlanner:
    """
    The Bounty Hunter Planner is a custom Caldera Planner developed and implemented by Fraunhofer FKIE.
    The general idea behind the Bounty Hunter's implementation was to support initial access and privilege escalation methods to allow the emulation of complete, realistic attack chains.
    This kind of behavior is not supported by any other Caldera planner, at the moment.
    Furthermore, it contributes a new attack behavior for Caldera adversaries.
    It decides which ability to use next using the future_rewards() function introduced in the look ahead planner.
    Instead of choosing the 'best ability' in every step, a weighted-random decision is made.
    Furthermore, after every executed ability, rewards of other abilities are updated according to the planners configuration file and the abilities' relationship.
    This way, the planner weighted-randomly chooses which abilities to execute and pursues one procedure more likely once it has started, i.e. use following abilities more likely.
    The planner's behavior can be controlled using various parameters.
    The 'final_abilities' is the most controlling parameter since it basically 'defines' which goal the adversary should pursue (most likely).

    The initial access phase of the Bounty Hunter can be skipped by assigning the initial agent to the group `target`.
    For more information, see the planner''s README.md in `caldera/plugins/bountyhunter/`.
    """

    DEFAULT_FINAL_REWARD = 1000
    DEFAULT_REWARD = 1
    DEFAULT_REWARD_UPDATE = 200
    DEPTH = 3
    DISCOUNT = 0.9
    SEED = None

    def __init__(self, operation, planning_svc, scenario, stopping_conditions=()):
        """

        :param operation:
        :param planning_svc:
        :param scenario: Name of the scenario in bountyhunter/conf to be used
        :param stopping_conditions:
        """

        self.operation = operation
        self.planning_svc = planning_svc
        self.stopping_conditions = stopping_conditions
        self.stopping_condition_met = False
        self.next_bucket = "initial_access"
        self.state_machine = [
            "initial_access",
            "recon_ips",
            "recon_ports",
            "pick_agenda",
            "execute_agenda",
            "bounty",
            "elevate",
            "execute_elevated"
        ]

        self.scenario = scenario
        self._init_parameters()

        self.agent_waiting_for_elevation = None
        self.host_waiting_for_elevation = None
        self.ability_waiting_for_elevation = None

        self.start_agent = None

        self.agenda_helper = AgendaHelper()
        self.agendas = None
        self.picked_agenda = None

        self.after_sleep_bucket = None

        self.planning_svc.log.info("<BountyHunter> Seed: {}".format(self.seed))

    def _init_parameters(self):
        with open("plugins/bountyhunter/conf/" + self.scenario + "/scenario_params.yml") as f:
            scenario_config = safe_load(f)

        self.depth = scenario_config.get("depth", self.DEPTH)
        self.discount = scenario_config.get("discount", self.DISCOUNT)

        self.default_reward = scenario_config.get("default_reward", self.DEFAULT_REWARD)
        self.default_final_reward = scenario_config.get("default_final_reward", self.DEFAULT_FINAL_REWARD)
        self.default_reward_update = scenario_config.get("default_reward_update", self.DEFAULT_REWARD_UPDATE)

        self.final_abilities = scenario_config.get("final_abilities", {})
        self.initial_ability_rewards = scenario_config.get("ability_rewards", {})
        self.ability_rewards = None
        self.initial_locked_abilities = scenario_config.get("locked_abilities", {})
        self.locked_abilities = None
        self.reward_updates = scenario_config.get("reward_updates", {})

        self.weighted_random = scenario_config.get("weighted_random", False)
        self.seed = scenario_config.get("seed", self.SEED)

    async def execute(self):
        self.ability_rewards = self.initial_ability_rewards.copy()
        self.locked_abilities = self.initial_locked_abilities.copy()
        self.start_agent = self.operation.agents[0]

        for final_ability_id in self.final_abilities:
            if final_ability_id not in self.ability_rewards:
                self.ability_rewards[final_ability_id] = self.default_final_reward

        await self.planning_svc.execute_planner(self)

    async def initial_access(self):
        # By starting an agent with group value "target" the initial access can be skipped.
        if self.start_agent.group == "target":
            self.planning_svc.log.info("<BountyHunter> Initial Access: Skip! Start agent is in group 'target'. ")
            self.next_bucket = "bounty"
            return

        self.planning_svc.log.info("<BountyHunter> Initial Access: Enter!")

        for agent in self.operation.agents:
            if not agent.host == self.start_agent.host:
                self.planning_svc.log.info("<BountyHunter> Initial Access: Done! Got agent that is not on start host.")

                await self.start_agent.kill()
                self.operation.agents.remove(self.start_agent)
                self.next_bucket = "bounty"

                return

        self.planning_svc.log.info("<BountyHunter> Initial Access: Begin! No agent was in operation was not on start host.")

        if self.agendas:
            self.planning_svc.log.info("<BountyHunter> Initial Access: Agendas already collected - try with next agenda.")
            self.next_bucket = "pick_agenda"
        else:
            self.planning_svc.log.info("<BountyHunter> Initial Access: No agendas collected yet - enter reconnaissance!")
            self.next_bucket = "recon_ips"

    async def recon_ips(self):
        self.planning_svc.log.info("<BountyHunter> Recon IPs: Start Host Recon!")
        ability_links = await self.planning_svc.get_links(self.operation, agent=self.start_agent, buckets=["recon_ips"])

        seed(self.seed)
        shuffled_links = choice(
            ability_links, len(ability_links), replace=False
        ).tolist()

        for link in shuffled_links:
            link_id = [await self.operation.apply(link)]
            await self.operation.wait_for_links_completion(link_id)

            if link.facts:
                self.planning_svc.log.info("<BountyHunter> Recon IPs: Found Hosts. Continue with Port Discovery.")
                self.next_bucket = "recon_ports"
                return
            else:
                self.planning_svc.log.info("<BountyHunter> Recon IPs: Ability found no hosts. Continue..")

        self.planning_svc.log.warning("<BountyHunter> Recon IPs: No hosts found.. Operation done.")
        self.next_bucket = "recon_ports"

    async def recon_ports(self):
        self.planning_svc.log.info("<BountyHunter> Recon Ports: Start Port Recon!")

        ability_links = await self.planning_svc.get_links(self.operation, agent=self.start_agent, buckets=["recon_ports"])

        seed(self.seed)
        shuffled_links = choice(
            ability_links, len(ability_links), replace=False
        ).tolist()

        for link in shuffled_links:
            link_id = [await self.operation.apply(link)]
            await self.operation.wait_for_links_completion(link_id)

            if link.facts:
                self.agendas = await self.agenda_helper.get_valid_agendas(ability_links)

                if self.agendas:
                    self.next_bucket = "pick_agenda"
                    self.planning_svc.log.info("<BountyHunter> Recon Ports: Found valid agendas! Executing them.")
                    return
                else:
                    self.planning_svc.log.info("<BountyHunter> Recon Ports: No valid agendas found. Continue..")
            else:
                self.planning_svc.log.info("<BountyHunter> Recon Ports: Ability was not successful. Continue..")

        self.planning_svc.log.warning("<BountyHunter> Recon Ports: No port info or valid agenda could be gathered.. Operation done.")
        self.next_bucket = None

    async def pick_agenda(self):
        self.planning_svc.log.info("<BountyHunter> Pick Agenda: Start!")

        for agenda in self.agendas:
            self.planning_svc.log.debug("<BountyHunter> Pick Agenda: Valid Agenda: {}".format(agenda.name))

        from random import shuffle
        shuffle(self.agendas)

        try:
            self.picked_agenda = self.agendas.pop()
            self.planning_svc.log.info("<BountyHunter> Pick Agenda: Picked Agenda: {}".format(agenda.name))

            for ability_id in self.picked_agenda.ability_ids:
                self.planning_svc.log.debug("<BountyHunter> Pick Agenda: Adding ability to operation: {}".format(ability_id))
                await self._add_ability_manually_to_operation(ability_id, "execute_agenda")

            self.next_bucket = "execute_agenda"

        except IndexError:
            self.planning_svc.log.warning("<BountyHunter> Pick Agenda: No more agendas to try. Return to Recon Ports!")
            self.next_bucket = "recon_ports"

        self.planning_svc.log.info("<BountyHunter> Pick Agenda: Done!")

    async def execute_agenda(self):
        self.planning_svc.log.info("<BountyHunter> Execute Agenda: Start!")

        ability_links = await self.planning_svc.get_links(
            self.operation, agent=self.start_agent, buckets=["execute_agenda"])

        if ability_links:
            links_ids = [await self.operation.apply(l) for l in ability_links]
            await self.operation.wait_for_links_completion(links_ids)
            return
        else:
            self.planning_svc.log.info("<BountyHunter> Execute Agenda: Agenda executed. Sleep and return to Initial Access!")
            self.next_bucket = "sleep"
            self.after_sleep_bucket = "initial_access"

    async def bounty(self):
        self.planning_svc.log.info("<BountyHunter> Bounty: Start!")
        picked_links_with_reward_per_agent = []

        self.planning_svc.log.debug("<BountyHunter> Bounty: Picking abilities per agent..")

        # Pick one ability per agent and add it to list of picked abilities
        for agent in self.operation.agents:
            executable_links = await self._get_executable_links(agent)

            if executable_links:
                next_ability_link, next_ability_reward = await self._pick_next_ability_link(agent, executable_links)
                self.planning_svc.log.debug(
                    "<BountyHunter> Bounty: Picked next ability link id: {},name: {},reward: {} for agent {}."
                    .format(next_ability_link.ability.ability_id, next_ability_link.ability.name, next_ability_reward, agent.paw)
                )
                picked_links_with_reward_per_agent.append((next_ability_link, next_ability_reward, agent, ))

        # Pick and execute one of the above picked ability links
        if picked_links_with_reward_per_agent:
            if self.weighted_random:
                picked_links_with_reward_per_agent = await self._shuffle_weighted_randomly(picked_links_with_reward_per_agent)
            else:
                picked_links_with_reward_per_agent.sort(key=lambda p: p[1], reverse=True)

            chosen_link = picked_links_with_reward_per_agent[0][0]
            chosen_agent = picked_links_with_reward_per_agent[0][2]

            self.planning_svc.log.info("<BountyHunter> Bounty: Picked next ability to execute: Ability: {}, Agent: {}"
                                       .format(chosen_link.ability.name, chosen_agent.paw)
            )

            if not chosen_agent.privileged_to_run(chosen_link.ability):
                self.planning_svc.log.info("<BountyHunter> Bounty: Agent needs elevation to execute ability.")
                self.agent_waiting_for_elevation = chosen_agent
                self.host_waiting_for_elevation = chosen_agent.host
                self.ability_waiting_for_elevation = chosen_link.ability
                self.next_bucket = "elevate"
                return

            link_id = await self.operation.apply(chosen_link)
            await self.operation.wait_for_links_completion([link_id])

            await self._update_ability_rewards(chosen_link.ability, chosen_agent)

            if chosen_link.ability.ability_id in self.final_abilities:
                self.planning_svc.log.info("<BountyHunter> Bounty: Executed final ability. Ending Operation!")
                self.next_bucket = None
        else:
            self.planning_svc.log.info("<BountyHunter> Bounty: All executables links executed. Ending Operation!")
            self.next_bucket = None

    async def elevate(self):
        self.planning_svc.log.info("<BountyHunter> Elevate: Start!")

        for agent in self.operation.agents:
            if agent.privilege == "Elevated" and agent.host == self.host_waiting_for_elevation:
                self.planning_svc.log.info(
                    "<BountyHunter> Elevate: Host {} has elevated agent {}. Executing ability {} using this agent!"
                    .format(self.host_waiting_for_elevation, agent.paw, self.ability_waiting_for_elevation.name)
                )
                self.next_bucket = "execute_elevated"
                return

        privilege_escalation_links = await self.planning_svc.get_links(
            self.operation, agent=self.agent_waiting_for_elevation, buckets=["privilege-escalation"]
        )

        if not privilege_escalation_links:
            self.next_bucket = "bounty"
            return

        for link in privilege_escalation_links:
            self.planning_svc.log.debug("<BountyHunter> Elevate: Got Priv.Esc. Link with ability {}!".format(link.ability.name))

        seed(self.seed)
        chosen_link = choice(privilege_escalation_links, 1)[0]
        self.planning_svc.log.debug("<BountyHunter> Elevate: Execute Priv.Esc. Ability {}!".format(chosen_link.ability.name))

        link_ids = [await self.operation.apply(chosen_link)]
        await self.operation.wait_for_links_completion(link_ids)

        self.next_bucket = "sleep"
        self.after_sleep_bucket = "elevate"

    async def execute_elevated(self):
        self.planning_svc.log.info("<BountyHunter> Execute Elevated: Executing ability that needed elevation!")

        elevated_agent = await self._get_elevated_agent(self.host_waiting_for_elevation)
        ability_links = await self.planning_svc.get_links(self.operation, agent=elevated_agent)

        for ability_link in ability_links:
            if ability_link.ability.ability_id == self.ability_waiting_for_elevation.ability_id:
                self.planning_svc.log.debug(
                    "<BountyHunter> Execute Elevated: Found link with same ability id. Found ID: {}. Waiting for elevation ID: {}."
                    .format(ability_link.ability.ability_id, self.ability_waiting_for_elevation.ability_id)
                )
                link_ids = [await self.operation.apply(ability_link)]
                await self.operation.wait_for_links_completion(link_ids)
                await self._update_ability_rewards(self.ability_waiting_for_elevation, elevated_agent)
                break

        if self.ability_waiting_for_elevation.ability_id in self.final_abilities:
            self.next_bucket = None
        else:
            self.agent_waiting_for_elevation = None
            self.host_waiting_for_elevation = None
            self.ability_waiting_for_elevation = None
            self.next_bucket = "bounty"

    async def sleep(self):
        self.planning_svc.log.info("<BountyHunter> Sleeping... and probably waiting for initial access or privilege escalation.")

        await self._add_ability_manually_to_operation("36eecb80-ede3-442b-8774-956e906aff02", "sleep")
        sleep_link = (await self.planning_svc.get_links(
            self.operation, agent=self.agent_waiting_for_elevation, buckets=["sleep"]))[0]
        await self._remove_ability_from_operation("36eecb80-ede3-442b-8774-956e906aff02", "sleep")

        link_id = [await self.operation.apply(sleep_link)]
        await self.operation.wait_for_links_completion(link_id)

        self.next_bucket = self.after_sleep_bucket

    async def _get_elevated_agent(self, host):
        for agent in self.operation.agents:
            if agent.host == host and agent.privilege == "Elevated":
                return agent

    async def _add_ability_manually_to_operation(self, ability_id, bucket_name):
        ability = (await self.planning_svc.get_service('data_svc')
                         .locate('abilities', match=dict(ability_id=tuple([ability_id]))))[0]
        await ability.add_bucket(bucket_name)

        if not ability_id in self.operation.adversary.atomic_ordering:
            self.operation.adversary.atomic_ordering.append(ability_id)

    async def _remove_ability_from_operation(self, ability_id, bucket_name):
        ability = (await self.planning_svc.get_service('data_svc')
                   .locate('abilities', match=dict(ability_id=tuple([ability_id]))))[0]

        ability.buckets.remove(bucket_name)
        self.operation.adversary.atomic_ordering.remove(ability_id)

    async def _get_executable_links(self, agent):
        if await self._get_elevated_agent(agent.host):
            return await self.planning_svc.get_links(self.operation, agent=agent, trim=True)
        else:
            temp_agent_privilege = agent.privilege
            agent.privilege = "Elevated"
            executable_links = await self.planning_svc.get_links(self.operation, agent=agent, trim=True)
            agent.privilege = temp_agent_privilege

            return executable_links

    async def _pick_next_ability_link(self, agent, executable_links):
        supported_abilities = await self._get_supported_abilities(agent)
        ability_reward_tuples = await self._get_ability_rewards(agent, supported_abilities)

        for art in ability_reward_tuples:
            self.planning_svc.log.debug("<BountyHunter> Ability Rewards: {}".format(art))

        if self.weighted_random:
            ability_reward_tuples = await self._shuffle_weighted_randomly(ability_reward_tuples)
        else:
            ability_reward_tuples.sort(key=lambda t: t[1], reverse=True)

        for art in ability_reward_tuples:
            self.planning_svc.log.info("<BountyHunter> Shuffled/Sorted Ability Rewards: {}".format(art))

        for ability_reward_tuple in ability_reward_tuples:
            for link in executable_links:
                if link.ability.ability_id == ability_reward_tuple[0]:
                    return link, ability_reward_tuple[1]

    async def _get_supported_abilities(self, agent):
        """Return list of abilities that are supported by the given agent, i.e. which abilities are
        defined in the operation's adversary's atomic ordering and can potentially be executed by the agent.
        This list includes abilities that cannot be executed because of missing facts and privileges

        :param agent:
        :return: list of abilities that are supported by the given agent
        """

        ao = self.operation.adversary.atomic_ordering
        data_svc = self.planning_svc.get_service("data_svc")

        abilities = await data_svc.locate("abilities", match=dict(ability_id=tuple(ao)))

        # This part is an adapted version of agent.capabilities(abilities)
        # that also includes abilities that cannot be executed because of missing privileges
        supported_abilities = []

        for ability in abilities:
            if ability.find_executors(agent.executors, agent.platform):
                supported_abilities.append(ability)
        return supported_abilities

    async def _get_ability_rewards(self, agent, abilities):
        """Get list of ability reward tuples where each tuple consists of an ability ID and its future reward

        :param agent:
        :param abilities:
        :return: list of tuples (ability id, reward)
        """

        ability_rewards = []

        for ability in abilities:
            if ability.ability_id not in self.locked_abilities:
                ability_rewards.append((ability.ability_id, await self._future_reward(agent, ability, abilities, 0), ))

        return ability_rewards

    async def _future_reward(self, agent, current_ability, abilities, current_depth):
        """Calculate future reward for current ability

        :param agent:
        :param current_ability:
        :param abilities:
        :param current_depth:
        :return: reward for current ability
        """

        if current_depth > self.depth:
            return 0

        abilities = set(abilities) - set([current_ability])
        future_rewards = [0]

        following_abilities = await self._get_following_abilities(agent, current_ability, abilities)

        for following_ability in following_abilities:
            future_rewards.append(
                await self._future_reward(agent, following_ability, abilities, current_depth+1)
            )

        reward = round(
            self.ability_rewards.get(current_ability.ability_id, self.default_reward)
            * (self.discount**current_depth)
            + max(future_rewards),
            3,
        )

        return reward

    @staticmethod
    async def _get_following_abilities(agent, current_ability, abilities):
        """Get abilities that follow the current ability, i.e. abilities that use facts that are generated by
        the current ability

        :param agent:
        :param current_ability:
        :param abilities:
        :return: list of abilities that follow the given ability
        """

        current_executor = await agent.get_preferred_executor(current_ability)
        facts = [
            fact
            for parser in current_executor.parsers
            for cfg in parser.parserconfigs
            for fact in [cfg.source, cfg.target]
            if fact is not None and fact != ""
        ]

        following_abilities = []

        for ability in abilities:
            executor = await agent.get_preferred_executor(ability)

            if executor.command and any(fact in executor.command for fact in facts):
                following_abilities.append(ability)

        return following_abilities

    async def _shuffle_weighted_randomly(self, list_of_tuples):
        """Shuffle the given list of tuples weighted randomly where the first tuple element is the value and the
        second tuple element is the value's weight

        :param list_of_tuples:
        :return: Weighted-randomly shuffled list of tuples
        """

        shuffled_list = []

        values = [element[0] for element in list_of_tuples]
        weights = [element[1] for element in list_of_tuples]
        # normalizing is necessary for np.random.choice function
        normalized_weights = [float(weight)/sum(weights) for weight in weights]

        seed(self.seed)

        shuffled_values = choice(
            values, len(values), p=normalized_weights, replace=False
        ).tolist()

        for value in shuffled_values:
            for element in list_of_tuples:
                if value == element[0]:
                    shuffled_list.append(element)

        return shuffled_list

    async def _update_ability_rewards(self, executed_ability, agent):
        """Update rewards of following abilities and according to planners yml config file (reward_updates)

        :param executed_ability:
        :param agent:
        :return: None
        """
        ability_updates = self.reward_updates.get(executed_ability.ability_id, {})

        if ability_updates:
            for ability_update_id, ability_update_value in ability_updates.items():
                if ability_update_id in self.locked_abilities:
                    self.locked_abilities.remove(ability_update_id)
                if ability_update_id not in self.ability_rewards:
                    self.ability_rewards[ability_update_id] = self.default_reward + ability_update_value
                else:
                    self.ability_rewards[ability_update_id] += ability_update_value

        supported_abilities = await self._get_supported_abilities(agent)
        supported_abilities = set(supported_abilities) - set([executed_ability])
        following_abilities = await self._get_following_abilities(agent, executed_ability, supported_abilities)

        if self.default_reward_update:
            for following_ability in following_abilities:
                if following_ability.ability_id not in ability_updates:
                    if following_ability.ability_id not in self.ability_rewards:
                        self.ability_rewards[following_ability.ability_id] = \
                            self.default_reward + self.default_reward_update
                    else:
                        self.ability_rewards[following_ability.ability_id] += self.default_reward_update
