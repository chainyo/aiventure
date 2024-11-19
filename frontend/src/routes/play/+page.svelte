<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import { userStore } from "$lib/stores/userStore";
    import { playerStore, type PlayerData } from "$lib/stores/playerStore";
    import { GameWebSocketClient } from "$lib/websocket";
    import { GameActions, type GameMessageResponse } from "$lib/types/websocket";

    let client: GameWebSocketClient;
    let messages: string[] = [];

    async function initializeWebSocket() {
        if (!$userStore?.access_token) {
            return;
        }

        try {
            client = new GameWebSocketClient();
            client.token = $userStore.access_token;

            await client.connectWebSocket();

            client.onMessage((data: GameMessageResponse) => {
                messages = [...messages, JSON.stringify(data)];

                if (data.action === GameActions.RETRIEVE_PLAYER_DATA) {
                    playerStore.set(data.payload as PlayerData);
                }
            });

            client.sendCommand(GameActions.RETRIEVE_PLAYER_DATA);

        } catch (error) {
            console.error("WebSocket connection failed:", error);
            setTimeout(initializeWebSocket, 5000);
        }
    }

    onMount(async () => {
        if ($userStore?.access_token) {
            await initializeWebSocket();
        }
    });

    onDestroy(() => {
        if (client) {
            client.close();
        }
    });
</script>

<svelte:head>
    <title>AI Venture | Play</title>
    <meta name="description" content="Play AI Venture" />
</svelte:head>

<main class="container mx-auto p-4 max-w-md">
    {#if $userStore}
        <h1 class="text-3xl font-bold mb-6">Welcome to AI Venture</h1>
        {#if $playerStore}
            <p>Player name: {$playerStore.name}</p>
            <p>Player funds: {$playerStore.funds}</p>
        {/if}
    {/if}
</main>
