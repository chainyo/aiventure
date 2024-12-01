import { writable } from "svelte/store";

interface FundsAnimation {
    difference: number;
    timestamp: number;
}

export const fundsAnimationStore = writable<FundsAnimation | null>(null);
