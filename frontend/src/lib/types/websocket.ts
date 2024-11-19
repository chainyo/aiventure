/**
 * Game actions
 */

export const GameActions = {
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
