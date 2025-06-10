<script setup>
// Vue
import { ref } from 'vue';

// Components
import UploadPart from '@/components/UploadPart.vue';
import ChartPart from '@/components/ChartPart.vue';

const mode = ref('upload');
</script>

<template>
    <main>
        <div class="wrapper">
            <Transition name="fade">
                <UploadPart
                    v-if="mode === 'upload'"
                    class="upload-part"
                    @start="mode = 'chart'"
                />
            </Transition>

            <Transition name="fade">
                <ChartPart
                    v-if="mode === 'chart'"
                    class="chart-wrapper"
                />
            </Transition>
        </div>
    </main>
</template>

<style scoped>
.wrapper {
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 1fr;
    width: 100%;
    padding: 4rem;
}

.wrapper > * {
    grid-column: 1 / 2;
    grid-row: 1 / 2;
}

.chart-wrapper,
.upload-part {
    width: 100%;
    height: calc(100vh - 12rem);
}

.chart {
    width: 100%;
    height: 100vh;
}
</style>
