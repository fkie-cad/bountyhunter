<script setup>

import { storeToRefs } from "pinia";
import { reactive, ref, inject, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import { useCoreStore } from "@/stores/coreStore";
import { useAbilityStore } from "@/stores/abilityStore";

const coreStore = useCoreStore();
const { planners } = storeToRefs(coreStore);
const abilityStore = useAbilityStore();
const { abilities, tactics, techniques, plugins, platforms } = storeToRefs(abilityStore);

const $api = inject("$api");
const route = useRoute();

let isEditingSeed = ref(false);
let isEditingDefaultFinalReward = ref(false);
let isEditingDefaultRewardUpdate = ref(false);
let isEditingWeightedRandom = ref(false);
let isEditingDiscountFactor = ref(false);
let isEditingDepth = ref(false);

onMounted(async () => {
    await coreStore.getPlanners($api);
});

const BountyHunterInfo = computed (() => {
    return planners.value.filter((planner) => planner.name=="bountyhunter")[0];
});

async function getFinalAbilitiesInfo(final_abilities) {
    console.log("get final abilities info");
    console.log(final_abilities);
    console.log(await abilityStore.getAbilityById("267bad86-3f06-49f1-9a3e-6522f2a61e7a"));
}

async function savePlanner(info) {
    try {
        console.log(info.id);
        console.log(info.name);
        console.log(info.params);
        console.log(info.params.seed);

        const response = await $api.patch('../api/v2/planners/' + info.id, info);
        console.log(response.data);
    } catch (error) {
        console.error("Error saving planner", error);
    }
}

</script>

<template lang="pug">
.content
    h2 The Bounty Hunter
    p.
        The Bounty Hunter Plugin adds a new custom planner to Caldera.
    p.
        {{ BountyHunterInfo.description }}
    hr

    h3 Current Bounty Hunter Configuration
    p.
        The Bounty Hunter can be configured using this user interface.
        To edit a value, simply click it and press "Save" at the bottom of the page.
        Alternatively, use Caldera's API or the Bounty Hunter Planner's configuration file (plugins/bountyhunter/data/planners/e1bb9388-1845-495d-b67b-ad61a31ff6cd.yml) to change the configuration.


    // Configuration Area
    .card.block.p-4
        h3 Seed
        .content(v-if="!isEditingSeed" @click="isEditingSeed = true")
            p.pointer {{ BountyHunterInfo.params.seed }}
        form(v-else)
            .field
                .control
                    input.input(v-model="BountyHunterInfo.params.seed" type="number")
            button.button.is-primary(@click="isEditingSeed = false") Done

    .card.block.p-4
        h3 Weighted Random Attack Behavior
        .content(v-if="!isEditingWeightedRandom" @click="isEditingWeightedRandom = true")
            p.pointer {{ BountyHunterInfo.params.weighted_random }}
        form(v-else)
            .field
                .control
                    input.input(v-model="BountyHunterInfo.params.weighted_random" type="checkbox")
            button.button.is-primary(@click="isEditingWeightedRandom = false") Done

    .card.block.p-4
        h3 Ability Reward Calculation Discount Factor
        .content(v-if="!isEditingDiscountFactor" @click="isEditingDiscountFactor = true")
            p.pointer {{ BountyHunterInfo.params.discount }}
        form(v-else)
            .field
                .control
                    input.input(v-model="BountyHunterInfo.params.discount" type="number")
            button.button.is-primary(@click="isEditingDiscountFactor = false") Done

    .card.block.p-4
        h3 Ability Reward Calculation Depth
        .content(v-if="!isEditingDepth" @click="isEditingDepth = true")
            p.pointer {{ BountyHunterInfo.params.depth }}
        form(v-else)
            .field
                .control
                    input.input(v-model="BountyHunterInfo.params.depth" type="number")
            button.button.is-primary(@click="isEditingDepth = false") Done

    .card.block.p-4
        h3 Default Final Reward
        .content(v-if="!isEditingDefaultFinalReward" @click="isEditingDefaultFinalReward = true")
            p.pointer {{ BountyHunterInfo.params.default_final_reward }}
        form(v-else)
            .field
                .control
                    input.input(v-model="BountyHunterInfo.params.default_final_reward" type="number")
            button.button.is-primary(@click="isEditingDefaultFinalReward = false") Done

    .card.block.p-4
        h3 Default Reward Update
        .content(v-if="!isEditingDefaultRewardUpdate" @click="isEditingDefaultRewardUpdate = true")
            p.pointer {{ BountyHunterInfo.params.default_reward_update }}
        form(v-else)
            .field
                .control
                    input.input(v-model="BountyHunterInfo.params.default_reward_update" type="number")
            button.button.is-primary(@click="isEditingDefaultRewardUpdate = false") Done

    .card.block.p-4
        h3 Final/Goal Abilities (TODO)
        p.pointer {{ BountyHunterInfo.params.final_abilities }}

        .box.mb-2.mr-2.p-3.ability(v-for="ability in getFinalAbilitiesInfo(BountyHunterInfo.params.final_abilities)" :key="ability.ability_id")
            .is-flex.is-justify-content-space-between.is-align-items-center.mb-1
                .is-flex
                    span.tag.is-small.mr-3 {{ ability.tactic }}
                p.help.mt-0 {{ ability.technique_id }} - {{ ability.technique_name }}
            strong {{ ability.name }}
            p.help.mb-0 {{ ability.description }}

    .card.block.p-4
        h3 Ability Rewards (TODO)
        p.pointer {{ BountyHunterInfo.params.ability_rewards }}

    .card.block.p-4
        h3 Locked Abilities (TODO)
        p.pointer {{ BountyHunterInfo.params.locked_abilities }}

    .card.block.p-4
        h3 Reward Updates (TODO)
        p.pointer {{ BountyHunterInfo.params.reward_updates }}

    // Save Button
    button.button.is-primary(@click="savePlanner(BountyHunterInfo)")
        span.icon
                font-awesome-icon(icon="fas fa-save")
        span Save

// Debug Info
h3 Debug - Bounty Hunter Configuration
p {{ BountyHunterInfo }}

</template>
