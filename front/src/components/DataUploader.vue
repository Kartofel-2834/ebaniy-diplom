<script setup>
import { FileUpload, Button, ProgressBar, Badge } from 'primevue';

import { ref } from 'vue';
import { usePrimeVue } from 'primevue/config';
import IconCloud from './icons/IconCloud.vue';
import IconFolder from './icons/IconFolder.vue';
import IconDelete from './icons/IconDelete.vue';
import IconExcel from './icons/IconExcel.vue';

const $primevue = usePrimeVue();

const $emit = defineEmits(['change']);

const uploader = ref(null);

const totalSize = ref(0);
const files = ref([]);

const onSelectedFiles = event => {
    files.value = event.files;
    files.value.forEach(file => {
        totalSize.value += parseInt(formatSize(file.size));
    });
    $emit('change', event.files[0]);
};

function onClear() {
    files.value = [];
    $emit('change', null);
}

const formatSize = bytes => {
    const k = 1024;
    const dm = 3;
    const sizes = $primevue.config.locale.fileSizeTypes;

    if (bytes === 0) {
        return `0 ${sizes[0]}`;
    }

    const i = Math.floor(Math.log(bytes) / Math.log(k));
    const formattedSize = parseFloat((bytes / Math.pow(k, i)).toFixed(dm));

    return `${formattedSize} ${sizes[i]}`;
};
</script>

<template>
    <FileUpload
        class="file-uploader"
        ref="uploader"
        name="data[]"
        accept=".xlsx"
        :pt="{ root: 'file-uploader', content: 'content', empty: 'empty' }"
        :multiple="false"
        :maxFileSize="1000000"
        @select="onSelectedFiles"
        @clear="onClear"
    >
        <template #header="{ chooseCallback, uploadCallback, clearCallback, files }">
            <Button
                :disabled="files.length"
                severity="success"
                aria-label="Upload"
                @click="chooseCallback"
            >
                <IconFolder />
            </Button>

            <Button
                :disabled="!files.length"
                severity="danger"
                aria-label="Clear"
                @click="clearCallback"
            >
                <IconDelete />
            </Button>
        </template>
        <template #content="{ files }">
            <div
                v-if="files.length"
                class="file"
            >
                <IconExcel class="excel" />

                <div class="label">{{ files[0].name }} ({{ formatSize(files[0].size) }})</div>
            </div>
        </template>

        <template #empty>
            <div class="nodata">
                <IconCloud class="cloud" />

                <div class="label">Перенесите сюда файл c характеристиками регионов</div>
            </div>
        </template>
    </FileUpload>
</template>

<style scoped>
.file,
.nodata {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 2rem;
    width: 100%;
    height: 100%;
    font-size: 2rem;
    padding: 2rem;
}

.excel,
.cloud {
    width: 10rem;
    height: auto;
    aspect-ratio: 1 / 1;
}

.label {
    user-select: none;
    text-align: center;
}
</style>

<style>
.file-uploader {
    display: flex;
    flex-direction: column;
}

.empty,
.content {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
}
</style>
