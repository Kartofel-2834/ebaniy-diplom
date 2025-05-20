<script setup>
import { Button } from 'primevue';
import DataUploader from './DataUploader.vue';
import { ref } from 'vue';

const $emit = defineEmits(['start']);

const firstFile = ref(null);
const secondFile = ref(null);

function onSubmit() {
    console.log('A', firstFile.value);
    console.log('B', secondFile.value);

    $emit('start');
}
</script>

<template>
    <div class="upload-part">
        <DataUploader
            class="uploader"
            @change="firstFile = $event"
        />

        <DataUploader
            class="uploader"
            @change="secondFile = $event"
        />

        <Button
            class="submit"
            :disabled="!firstFile || !secondFile"
            severity="success"
            size="large"
            @click="onSubmit"
        >
            Начать кластерный анализ
        </Button>
    </div>
</template>

<style scoped>
.upload-part {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr;
    grid-auto-flow: row;
    grid-auto-rows: min-content;
    gap: 2rem;
    width: 100%;
    height: 100%;
}

.uploader {
    width: 100%;
    height: 100%;
}

.submit {
    font-size: 2rem;
    grid-column: 1 / 3;
    height: 5.6rem;
    font-weight: 500;
}
</style>
