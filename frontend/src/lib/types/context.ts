import type { GameWebSocketClient } from "$lib/websocket";

export type GameContext = {
    client: GameWebSocketClient | null;
    messages: string[];
    activeLab: string | undefined;
    sidebarOpen: boolean;
    toggleSidebar: () => void;
};

export const GAME_CONTEXT_KEY = "gameContext";