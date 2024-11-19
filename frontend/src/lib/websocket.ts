/**
 * WebSocket client for the game.
 */

import type { GameAction, GameMessage, GameMessageResponse } from "./types/websocket";

export class GameWebSocketClient {
    private socket: WebSocket | null = null;
    public token: string | null = null;
    private baseUrl: string;

    constructor(baseUrl: string = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
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

    onMessage(callback: (data: GameMessageResponse) => void): void {
        if (!this.socket) {
            throw new Error('WebSocket not connected');
        }

        this.socket.onmessage = (event) => {
            const data: GameMessageResponse = JSON.parse(event.data);
            callback(data);
        };
    }

    close(): void {
        if (this.socket) {
            this.socket.close();
            this.socket = null;
        }
    }
}
