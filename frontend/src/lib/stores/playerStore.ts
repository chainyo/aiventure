import { writable, get } from "svelte/store";

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

function createPlayerStore() {
    const { subscribe, set, update } = writable<PlayerData | null>(null);

    return {
        subscribe,
        set,
        update,
        reset: () => set(null),
        initialize: async (data: PlayerData) => {
            set(data);
        },
        getCurrentPlayer: () => get({ subscribe }),
    };
}

export const playerStore = createPlayerStore();
