/**
 * WebSocket client for the game.
 */
import { toast } from "svelte-sonner";

import type { GameAction, GameMessage, GameMessageResponse } from "$lib/types/websocket";
import type { GameContext } from "$lib/types/context";
import { labStore, playerStore, type AIModel, type Lab, type Player } from "$lib/stores/gameStore";
import { GameActions } from "$lib/types/websocket";


export class GameWebSocketClient {
    private socket: WebSocket | null = null;
    public token: string | null = null;
    private baseUrl: string;
    private gameContext: GameContext;

    constructor(baseUrl: string = 'http://localhost:8000', gameContext: GameContext) {
        this.baseUrl = baseUrl;
        this.gameContext = gameContext;
    }

    async login(email: string, password: string): Promise<boolean> {
        try {
            const formData = new URLSearchParams({
                username: email,
                password: password,
                grant_type: 'password',
            });

            const response = await fetch(`${this.baseUrl}/api/auth/authenticate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                this.token = data.access_token;
                return true;
            }
            return false;
        } catch (error) {
            console.error('Login failed:', error);
            return false;
        }
    }

    async connectWebSocket(): Promise<void> {
        if (!this.token) {
            throw new Error('Must login first');
        }

        try {
            const wsUrl = this.baseUrl.replace('http://', 'ws://').replace('https://', 'wss://');
            this.socket = new WebSocket(`${wsUrl}/api/game/ws?token=${this.token}`);

            this.socket.onopen = () => {
                console.log('Connected to websocket');
            };

            this.socket.onerror = (error) => {
                console.error('WebSocket error:', error);
            };

            this.socket.onclose = (event) => {
                console.log('WebSocket connection closed:', {
                    code: event.code,
                    reason: event.reason,
                    wasClean: event.wasClean
                });
            };

            this.socket.onmessage = (event) => {
                const data: GameMessageResponse = JSON.parse(event.data);
                this.gameContext.messages = [...this.gameContext.messages, JSON.stringify(data)];

                if (data.error) {
                    toast.error(data.error);
                }

                switch (data.action) {
                    case GameActions.CREATE_LAB:
                        this.handleCreateLab(data.payload as Lab);
                        break;
                    case GameActions.CREATE_MODEL:
                        this.handleCreateModel(data.payload as AIModel);
                        break;
                    case GameActions.RETRIEVE_LAB:
                        this.handleRetrieveLab(data.payload as Lab);
                        break;
                    case GameActions.CREATE_PLAYER:
                    case GameActions.RETRIEVE_PLAYER_DATA:
                        this.handlePlayerData(data.payload as Player);
                        break;
                    case GameActions.UPDATE_FUNDS:
                        this.handleUpdateFunds(data.payload as { funds: number });
                        break;
                }
            };

            await new Promise<void>((resolve, reject) => {
                if (!this.socket) return reject(new Error('Socket not initialized'));

                const timeout = setTimeout(() => {
                    reject(new Error('WebSocket connection timeout'));
                }, 5000); // 5 second timeout

                this.socket.onopen = () => {
                    clearTimeout(timeout);
                    resolve();
                };
                this.socket.onerror = () => {
                    clearTimeout(timeout);
                    reject(new Error('WebSocket connection failed'));
                };
            });

        } catch (error) {
            console.error('Failed to connect:', error);
            throw error;
        }
    }

    sendCommand(action: GameAction, payload: Record<string, any> = {}): void {
        if (!this.socket) {
            throw new Error('WebSocket not connected');
        }

        const message: GameMessage = { action, payload };
        this.socket.send(JSON.stringify(message));
    }

    close(): void {
        if (this.socket) {
            this.socket.close();
            this.socket = null;
        }
    }

    private handleCreateLab(lab: Lab): void {
        if (lab && Object.keys(lab).length > 0) {
            playerStore.update(currentPlayer => {
                if (!currentPlayer) return currentPlayer;
                
                return {
                    ...currentPlayer,
                    labs: [...(currentPlayer.labs || []), lab]
                };
            });
        }
    }

    private handleCreateModel(model: AIModel): void {
        if (model && Object.keys(model).length > 0) {
            labStore.update(currentLab => {
                if (!currentLab) return currentLab;
                toast.success(`Created model ${model.name} in ${currentLab.name}`);

                return {
                    ...currentLab,
                    models: [...(currentLab.models || []), model]
                };
            });
        }
    }

    private handlePlayerData(player: Player): void {
        if (player && Object.keys(player).length > 0) {
            playerStore.set(player);
        }
    }

    private handleRetrieveLab(lab: Lab): void {
        if (lab && Object.keys(lab).length > 0) {
            labStore.set(lab);
        }
    }

    private handleUpdateFunds(data: { funds: number }): void {
        playerStore.update(currentPlayer => {
            if (!currentPlayer) return currentPlayer;

            return {
                ...currentPlayer,
                funds: data.funds
            };
        });
    }
}
