// Types
import type { IClusterData } from '@/types/data';

export function useClusterData(
    dataList: IClusterData[],
    formatter: (v?: IClusterData) => object = () => ({}),
) {
    const datasets = dataList.map(clusterData => {
        const regions = clusterData.data[clusterData.data.length - 1].regions;

        return {
            id: clusterData.id,
            label: clusterData.id >= 0 ? `Кластер ${clusterData.id + 1}` : 'Выбросы',
            data: Object.entries(regions).map(([regionName, regionData]) => ({
                x: regionData[0],
                y: regionData[1],
            })),
            ...formatter(clusterData),
        };
    });

    return { datasets };
}

export function useRegressionData(
    dataList: IClusterData[],
    formatter: (v?: IClusterData) => object = () => ({}),
) {
    const labels = dataList[0].regression.map(([x]) => x);

    const datasets = dataList.map(clusterData => {
        const regression = clusterData.regression;

        return {
            id: clusterData.id,
            label: clusterData.id >= 0 ? `Кластер ${clusterData.id + 1}` : 'Выбросы',
            data: regression.map(([x, y]) => y),
            ...formatter(clusterData),
        };
    });

    // const datasets2 = datasets.map(dataset => ({
    //     ...dataset,
    //     data: dataset.data.map(v => v - 40000),
    // }));

    return { labels, datasets: datasets };
}

export function useForecastData(
    dataList: IClusterData[],
    formatter: (v?: IClusterData) => object = () => ({}),
) {
    const labelsA = dataList[0].forecast.A.map(([year]) => year);
    const datasetsA = dataList.map(clusterData => {
        const forecast = clusterData.forecast.A;

        return {
            id: clusterData.id,
            label: clusterData.id >= 0 ? `Кластер ${clusterData.id + 1}` : 'Выбросы',
            data: forecast.map(([x, y]) => y),
            ...formatter(clusterData),
        };
    });

    const labelsB = dataList[0].forecast.B.map(([year]) => year);
    const datasetsB = dataList.map(clusterData => {
        const forecast = clusterData.forecast.B;

        return {
            id: clusterData.id,
            label: clusterData.id >= 0 ? `Кластер ${clusterData.id + 1}` : 'Выбросы',
            data: forecast.map(([x, y]) => y),
            ...formatter(clusterData),
        };
    });

    return {
        A: { labels: labelsA, datasets: datasetsA },
        B: { labels: labelsB, datasets: datasetsB },
    };
}
