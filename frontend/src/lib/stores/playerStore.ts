import { writable, get } from "svelte/store";

export interface Player {
    id: string;
    name: string;
    funds: number;
    user_id: string;
    labs: Lab[];
    investments: Lab[];
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
    lab: Lab;
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
    investors: Player[];
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
