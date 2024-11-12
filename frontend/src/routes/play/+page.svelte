<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import { userStore } from "$lib/stores/userStore";
    import { GameWebSocketClient } from "$lib/websocket";

    let client: GameWebSocketClient;
    let messages: string[] = [];

    async function initializeWebSocket() {
        if (!$userStore?.access_token) {
            return;
        }

        try {
            client = new GameWebSocketClient();
            client.token = $userStore.access_token;

            console.log("Connecting to WebSocket");
            await client.connectWebSocket();

            client.onMessage((data) => {
                messages = [...messages, JSON.stringify(data)];
                console.log("Received message:", data);
            });

            client.sendCommand("test", { message: "Hello from client!" });

            client.sendCommand("retrieve-player-data");

        } catch (error) {
            console.error("WebSocket connection failed:", error);
            setTimeout(initializeWebSocket, 5000);
        }
    }

    onMount(async () => {
        console.log("Mounting Play page");
        if ($userStore?.access_token) {
            console.log("User token found, initializing WebSocket");
            await initializeWebSocket();
            console.log("WebSocket initialized");
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
    {/if}
</main>
