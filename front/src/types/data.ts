export interface IClusterData {
    id: number;
    data: IRegionsData[];
    regression: number[][];
}

export interface IRegionsData {
    year: number;
    regions: Record<string, number[]>;
}
