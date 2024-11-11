<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import { goto } from "$app/navigation";
    import { userStore } from "$lib/stores/userStore";
    import { Button } from "$lib/components/ui/button";
    import { GameWebSocketClient } from "$lib/websocket";
  
    let client: GameWebSocketClient;
    let messages: string[] = [];
    let connectionStatus = "Disconnected";

    function handleLogout() {
        if (client) {
            client.close();
        }
        userStore.clearUser();
        goto('/');
    }

    async function initializeWebSocket() {
        console.log("Initializing WebSocket");
        if (!$userStore?.access_token) {
            console.log("No token found");
            connectionStatus = "Not authenticated";
            return;
        }

        try {
            console.log("Initializing client");
            connectionStatus = "Connecting...";
            client = new GameWebSocketClient();
            console.log("Setting token");
            client.token = $userStore.access_token;
            console.log("Setting onMessage handler");
            client.onMessage((data) => {
                messages = [...messages, JSON.stringify(data)];
                console.log("Received message:", data);
            });
            console.log("Connecting to WebSocket");
            await client.connectWebSocket();
            connectionStatus = "Connected";

            client.sendCommand("test", { message: "Hello from client!" });

        } catch (error) {
            console.error("WebSocket connection failed:", error);
            connectionStatus = "Connection failed";
            setTimeout(initializeWebSocket, 5000);
        }
    }

    $: if ($userStore?.access_token) {
        (async () => {
            await initializeWebSocket();
        })();
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
    <h1 class="text-3xl font-bold mb-6">Welcome to AI Venture</h1>
    
    {#if $userStore}
        <div class="space-y-4">
            <div class="bg-gray-800 p-4 rounded-lg">
                <p>Logged in as {$userStore.email}</p>
                <p>User ID: {$userStore.id}</p>
                <p>Connection status: {connectionStatus}</p>
            </div>

            <!-- WebSocket Messages -->
            <div class="bg-gray-800 p-4 rounded-lg max-h-60 overflow-y-auto">
                <h2 class="text-xl font-semibold mb-2">Messages</h2>
                {#if messages.length === 0}
                    <p class="text-gray-500">No messages yet</p>
                {:else}
                    {#each messages as message}
                        <div class="bg-white p-2 rounded mb-2">
                            {message}
                        </div>
                    {/each}
                {/if}
            </div>

            <!-- Test Commands -->
            <div class="space-x-2">
                <Button 
                    on:click={() => client?.sendCommand("test", { action: "ping" })}
                    disabled={connectionStatus !== "Connected"}
                >
                    Send Test Message
                </Button>
                <Button variant="destructive" on:click={handleLogout}>
                    Log out
                </Button>
            </div>
        </div>
    {:else}
        <p>You are not logged in</p>
    {/if}
</main>
