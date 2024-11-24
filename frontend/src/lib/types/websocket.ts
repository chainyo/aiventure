/**
 * Game actions
 */

export const GameActions = {
    CREATE_LAB: "create-lab",
    CREATE_PLAYER: "create-player",
    RETRIEVE_LAB: "retrieve-lab",
    RETRIEVE_PLAYER_DATA: "retrieve-player-data",
} as const;

export type GameAction = typeof GameActions[keyof typeof GameActions];

export interface GameMessage {
    action: GameAction;
    payload: Record<string, any>;
}

export interface GameMessageResponse {
    action: GameAction;
    payload: Record<string, any>;
    error?: string;
}
