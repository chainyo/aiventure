import { writable } from "svelte/store";

export interface Player {
    id: string;
    name: string;
    funds: number;
    user_id: string;
    labs: LabRead[];
    investments: LabRead[];
}

export interface LabRead {
    id: string;
    name: string;
    location: string;
    valuation: number;
    income: number;
    tech_tree_id: string;
    player_id: string;
    investors: Player[];
}

export interface PlayerData {
    id: string;
    name: string;
    funds: number;
    labs: LabRead[];
    investments: LabRead[];
}

export const playerStore = writable<PlayerData | null>(null);
