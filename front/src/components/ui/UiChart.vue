<script lang="ts" setup>
// Vue
import { computed, onMounted, ref } from 'vue';

// PrimeVue
import Chart from 'primevue/chart';

const textColorVar = ref<string>('');
const textColorSecondaryVar = ref<string>('');
const surfaceBorderVar = ref<string>('');

// Props
const $props = withDefaults(
    defineProps<{
        dataList?: any;
        options?: object;
        type?: string;
    }>(),
    {
        type: 'line',
        dataList: () => [],
        options: () => ({}),
    },
);

// Computed
const chartOptions = computed(() => {
    return {
        maintainAspectRatio: false,
        aspectRatio: 0.6,
        plugins: {
            legend: {
                display: false,
                position: 'left',
                labels: {
                    color: textColorVar.value,
                },
            },
        },
        scales: {
            x: {
                ticks: {
                    color: textColorSecondaryVar.value,
                },
                grid: {
                    color: surfaceBorderVar.value,
                },
            },
            y: {
                ticks: {
                    color: textColorSecondaryVar.value,
                },
                grid: {
                    color: surfaceBorderVar.value,
                },
            },
        },
        ...$props.options,
    };
});

// Lifecycle
onMounted(() => {
    const documentStyle = getComputedStyle(document.documentElement);
    textColorVar.value = documentStyle.getPropertyValue('--p-text-color');
    textColorSecondaryVar.value = documentStyle.getPropertyValue('--p-text-muted-color');
    surfaceBorderVar.value = documentStyle.getPropertyValue('--p-content-border-color');
});
</script>

<template>
    <Chart
        :type="type"
        :data="dataList"
        :options="chartOptions"
    />
</template>
