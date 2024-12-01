import { writable, get } from "svelte/store";

export interface Player {
    id: string;
    name: string;
    avatar: string;
    funds: number;
    user_id: string;
    labs: Lab[];
    investments: Investment[];
}

export interface Employee {
    id: string;
    name: string;
    salary: number;
    image_url: string;
    role_id: number;
    quality_id: number;
    lab_id: string;
    // modifiers: Modifier[];
    lab: Lab;
}

export interface AIModel {
    id: string;
    name: string;
    ai_model_type_id: number;
    tech_tree_id: string;
    lab_id: string;
}

export interface Investor {
    player: Player;
    part: number;
}

export interface Investment {
    lab: Lab;
    part: number;
}

export interface UpdateFunds {
    funds: number;
    update_type: "increment" | "decrement";
}

export interface Lab {
    id: string;
    name: string;
    location: string;
    valuation: number;
    income: number;
    tech_tree_id: string;
    player_id: string;
    employees: Employee[];
    models: AIModel[];
    investors: Investor[];
    player: Player | null;
}

function createPlayerStore() {
    const { subscribe, set, update } = writable<Player | null>(null);

    return {
        subscribe,
        set,
        update,
        reset: () => set(null),
        initialize: async (data: Player) => {
            set(data);
        },
        getCurrentPlayer: () => get({ subscribe }),
    };
}

export const playerStore = createPlayerStore();

function createLabStore() {
    const { subscribe, set, update } = writable<Lab | null>(null);

    return {
        subscribe,
        set,
        update,
        reset: () => set(null),
        initialize: async (data: Lab) => {
            set(data);
        },
        getCurrentLab: () => get({ subscribe }),
    };
}

export const labStore = createLabStore();
