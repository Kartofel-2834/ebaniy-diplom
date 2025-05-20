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

    return { labels, datasets };
}
