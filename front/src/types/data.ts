export interface IClusterData {
    id: number;
    data: IRegionsData[];
    regression: number[][];
    forecast: {
        A: number[][];
        B: number[][];
    };
}

export interface IRegionsData {
    year: number;
    regions: Record<string, number[]>;
}
