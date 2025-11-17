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
const scenarios = ref([])

onMounted(async () => {
    await coreStore.getPlanners($api);

    scenarios.value = await getScenarios()
});

const BountyHunterInfo = computed(() => {
    return planners.value.filter((planner) => planner.name == "bountyhunter")[0];
});

async function getScenarios() {
    console.log("get all available scenarios")
    const scenarios = await $api.get('../plugin/bountyhunter/scenarios');
    console.log("scenarios:", scenarios.data)

    return scenarios.data;
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

<style scoped>
.content .pointer {
    display: block;
    width: 100%;
    min-height: 2.5rem;
    cursor: pointer;
}
</style>

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
        To configure the currently used Bounty Hunter scenario, click the name of the current scenario below, select the scenario to use and click "Save".
        Alternatively, use the Bounty Hunter Planner's configuration file (plugins/bountyhunter/data/planners/e1bb9388-1845-495d-b67b-ad61a31ff6cd.yml) to change the scenario.


    // Configuration Area
    .card.block.p-4
        h3 Scenario
        .content
            .field
                .control
                    .select.w-full
                        select(
                            v-model="BountyHunterInfo.params.scenario"
                        )
                            option(
                                v-for="(scenario, idx) in scenarios"
                                :key="idx"
                                :value="scenario"
                            ) {{ scenario }}

    // Save Button
    button.button.is-primary(@click="savePlanner(BountyHunterInfo)")
        span.icon
                font-awesome-icon(icon="fas fa-save")
        span Save

// Debug Info
.content
    h3 Current Bounty Hunter Scenario Configuration
    p Viewing and editing the currently used scenario configuration via the UI is not supported, yet. Please use the respective scenario's configuration file (plugins/bountyhunter/conf/scenario_name/scenario_params.yml).
    h3 Debug - Bounty Hunter Configuration Info
    p {{ BountyHunterInfo }}

</template>