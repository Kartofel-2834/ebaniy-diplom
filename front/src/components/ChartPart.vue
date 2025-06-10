<script setup>
import BEZRAB_ZP from '@/data/bezrab__zp.json';
import INVEST_VRP from '@/data/invest__vrp.json';
import ZANYAT_VRP from '@/data/zanyat__vrp.json';
import OSN_FOND_VRP from '@/data/osn-fond__vrp.json';

import {
    Accordion,
    AccordionContent,
    AccordionHeader,
    AccordionPanel,
    Button,
    ButtonGroup,
} from 'primevue';
import { computed, ref } from 'vue';
import IconRegression from './icons/IconRegression.vue';
import IconCluster from './icons/IconCluster.vue';
import { useClusterData, useForecastData, useRegressionData } from '@/composables/data';
import UiChart from './ui/UiChart.vue';
import IconMadeInHeaven from './icons/IconMadeInHeaven.vue';

const DATA = OSN_FOND_VRP

const mode = ref('cluster');
const selectedCluster = ref(null);
const selectedCharacteristic = ref('A');

const clusters = computed(() => {
    const clusters = DATA.map((cluster, index) => {
        const label = cluster.id >= 0 ? `Кластер ${cluster.id + 1}` : 'Выбросы';
        const data = cluster.data[cluster.data.length - 1];
        const regions = Object.entries(data.regions).map(([regionName, regionData]) => ({
            label: regionName,
            id: regionName,
            data: regionData,
        }));

        return {
            id: cluster.id,
            value: String(index),
            label,
            regions,
        };
    });

    return clusters.filter(cluster => cluster.regions.length > 0);
});

const clusterChartData = computed(() => {
    const result = useClusterData(DATA, () => ({
        tension: 0.4,
        fill: false,
    }));

    result.datasets = result.datasets.map(dataset => {
        return {
            ...dataset,
            hidden: selectedCluster.value !== null && dataset.id !== selectedCluster.value,
        };
    });

    return result;
});

const regressionChartData = computed(() => {
    const result = useRegressionData(DATA, () => ({
        tension: 0.4,
        fill: false,
    }));

    result.datasets = result.datasets.map(dataset => {
        return {
            ...dataset,
            hidden: checkIsDatasetHidden(dataset),
        };
    });

    return result;
});

const forecastChartData = computed(() => {
    const { A, B } = useForecastData(DATA, () => ({
        tension: 0.4,
        fill: false,
    }));

    A.datasets = A.datasets.map(dataset => {
        return {
            ...dataset,
            hidden: checkIsDatasetHidden(dataset),
        };
    });

    B.datasets = B.datasets.map(dataset => {
        return {
            ...dataset,
            hidden: checkIsDatasetHidden(dataset),
        };
    });

    return selectedCharacteristic.value === 'A' ? A : B;
});

function onClusterSelect(event) {
    selectedCluster.value = event;
}

function checkIsDatasetHidden(dataset) {
    return selectedCluster.value !== null && dataset.id !== selectedCluster.value;
}
</script>

<template>
    <div class="chart-part">
        <div class="bar">
            <ButtonGroup class="characteristics">
                <Button
                    class="characteristic-button"
                    size="large"
                    :disabled="mode !== 'forecast'"
                    :style="{ pointerEvents: selectedCharacteristic === 'A' ? 'none' : 'auto' }"
                    :severity="selectedCharacteristic === 'A' ? 'success' : 'secondary'"
                    @click="selectedCharacteristic = 'A'"
                >
                    A
                </Button>
                <Button
                    class="characteristic-button"
                    size="large"
                    :disabled="mode !== 'forecast'"
                    :style="{ pointerEvents: selectedCharacteristic === 'B' ? 'none' : 'auto' }"
                    :severity="selectedCharacteristic === 'B' ? 'success' : 'secondary'"
                    @click="selectedCharacteristic = 'B'"
                >
                    B
                </Button>
            </ButtonGroup>

            <Button
                class="select-all"
                size="large"
                :style="{ pointerEvents: selectedCluster === null ? 'none' : 'auto' }"
                :severity="selectedCluster === null ? 'success' : 'secondary'"
                @click="selectedCluster = null"
            >
                Все кластеры
            </Button>

            <div class="menu">
                <Accordion
                    :value="selectedCluster"
                    @update:value="onClusterSelect"
                >
                    <AccordionPanel
                        v-for="cluster of clusters"
                        :key="cluster.id"
                        :value="cluster.id"
                    >
                        <AccordionHeader
                            :pt="{
                                root: `accordion-header ${cluster.id === selectedCluster ? '_selected' : ''}`,
                            }"
                            >{{ cluster.label }}</AccordionHeader
                        >
                        <AccordionContent>
                            <div
                                v-for="region of cluster.regions"
                                :key="region.id"
                                class="region"
                            >
                                {{ region.label }}
                                <span class="region-data">({{ region.data.join(';') }})</span>
                            </div>
                        </AccordionContent>
                    </AccordionPanel>
                </Accordion>
            </div>
        </div>

        <div class="chart">
            <ButtonGroup class="controls">
                <Button
                    class="control-button"
                    :style="{ pointerEvents: mode === 'cluster' ? 'none' : 'auto' }"
                    :severity="mode === 'cluster' ? 'success' : 'secondary'"
                    @click="mode = 'cluster'"
                >
                    <IconCluster class="control-button-icon" />

                    Кластеризация
                </Button>

                <Button
                    class="control-button"
                    :style="{ pointerEvents: mode === 'regression' ? 'none' : 'auto' }"
                    :severity="mode === 'regression' ? 'success' : 'secondary'"
                    @click="mode = 'regression'"
                >
                    <IconRegression class="control-button-icon" />

                    Регрессия
                </Button>

                <Button
                    class="control-button"
                    :style="{ pointerEvents: mode === 'forecast' ? 'none' : 'auto' }"
                    :severity="mode === 'forecast' ? 'success' : 'secondary'"
                    @click="mode = 'forecast'"
                >
                    <IconMadeInHeaven class="control-button-icon forecast-icon" />

                    Прогнозирование
                </Button>
            </ButtonGroup>

            <div class="canvas-wrapper">
                <Transition name="fade">
                    <UiChart
                        v-show="mode === 'cluster'"
                        class="canvas"
                        :data-list="clusterChartData"
                        type="scatter"
                    />
                </Transition>

                <Transition name="fade">
                    <UiChart
                        v-show="mode === 'regression'"
                        class="canvas"
                        :data-list="regressionChartData"
                        type="line"
                    />
                </Transition>

                <Transition name="fade">
                    <UiChart
                        v-show="mode === 'forecast'"
                        class="canvas"
                        :data-list="forecastChartData"
                        type="line"
                    />
                </Transition>
            </div>
        </div>
    </div>
</template>

<style scoped>
.chart-part {
    display: flex;
    gap: 2rem;
}

.bar {
    overflow: hidden;
    width: 40rem;
    display: flex;
    flex-direction: column;
    flex-shrink: 0;
    background-color: var(--p-content-background);
    border-radius: 0.6rem;
}

.select-all {
    width: calc(100% - 2rem);
    font-size: 1.8rem;
    margin: 1rem;
}

.menu {
    overflow: auto;
    width: 100%;
    height: 100%;
}

.chart {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    gap: 2rem;
}

.canvas-wrapper {
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 1fr;
    width: 100%;
    height: 100%;
}

.canvas {
    grid-column: 1 / 2;
    grid-row: 1 / 2;
    height: 100%;
}

.controls {
    display: grid;
    grid-auto-flow: column;
    grid-auto-columns: 1fr;
    width: 100%;
}

.control-button {
    font-size: 1.8rem;
}

.control-button-icon {
    width: 1.6em;
    height: auto;
}

.forecast-icon {
    width: 1.4em;
}

.region {
    margin: 2rem 0;
    pointer-events: none;
}

.region:first-child {
    margin-top: 1rem;
}

.region-data {
    font-size: 0.8em;
    color: var(--p-text-muted-color);
}

.characteristics {
    display: grid;
    grid-auto-flow: column;
    width: calc(100% - 2rem);
    margin: 1rem;
}

.characteristic-button {
    font-size: 1.6rem;
    font-weight: 600;
}
</style>

<style>
.accordion-header._selected {
    color: var(--p-primary-color) !important;
}

.accordion-header._selected .p-accordionheader-toggle-icon {
    color: var(--p-primary-color) !important;
}
</style>
