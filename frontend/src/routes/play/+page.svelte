<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import { Button } from "$lib/components/ui/button/index.js";
    import { Input } from "$lib/components/ui/input/index.js";
    import { Label } from "$lib/components/ui/label/index.js";
    import { userStore } from "$lib/stores/userStore";
    import { playerStore, type PlayerData } from "$lib/stores/playerStore";
    import { GameWebSocketClient } from "$lib/websocket";
    import { GameActions, type GameMessageResponse } from "$lib/types/websocket";

    let client: GameWebSocketClient;
    let messages: string[] = [];
    let playerName: string = "";
    let labName: string = "";

    function handleCreatePlayer(event: SubmitEvent) {
        event.preventDefault();
        if (!playerName.trim()) return;

        client.sendCommand(GameActions.CREATE_PLAYER, { name: playerName.trim() });
    }

    function handleCreateLab(event: SubmitEvent) {
        event.preventDefault();
        if (!labName.trim()) return;

        client.sendCommand(GameActions.CREATE_LAB, { name: labName.trim() });
    }

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

                switch (data.action) {
                    case GameActions.CREATE_PLAYER:
                    case GameActions.RETRIEVE_PLAYER_DATA:
                        const playerData = data.payload as PlayerData;
                        if (playerData && Object.keys(playerData).length > 0) {
                            playerStore.set(playerData);
                        }
                        break;
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
    {#if $userStore !== null}
        {#if $playerStore !== null}
            <p>Play...</p>
        {:else}
            <form class="flex w-full max-w-sm flex-col gap-1.5" on:submit={handleCreatePlayer}>
                <Label for="player-name">Player name</Label>
                <Input type="text" id="player-name" placeholder="Jane Doe" bind:value={playerName} />
                <p class="text-muted-foreground text-sm">Enter your player name.</p>
                <Button type="submit">Submit</Button>
            </form>
        {/if}
        {#if $playerStore && $playerStore.labs.length === 0}
            <form class="flex w-full max-w-sm flex-col gap-1.5" on:submit={handleCreateLab}>
                <Label for="lab-name">Lab name</Label>
                <Input type="text" id="lab-name" placeholder="Jane Doe" bind:value={labName} />
                <p class="text-muted-foreground text-sm">Enter your lab name.</p>
                <Button type="submit">Submit</Button>
            </form>
        {:else}
            <p>Play...</p>
        {/if}
    {/if}
</main>
