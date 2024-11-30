<script lang="ts">
    import { onDestroy, onMount } from "svelte";
    import { goto } from "$app/navigation";
    import { toast } from "svelte-sonner";
    import { LoaderCircle } from "lucide-svelte";

    import * as Avatar from "$lib/components/ui/avatar/index.js";
    import { Button } from "$lib/components/ui/button/index.js";
    import * as Card from "$lib/components/ui/card/index.js";
    import { Label } from "$lib/components/ui/label/index.js";
    import { Input } from "$lib/components/ui/input/index.js";
    import { ScrollArea } from "$lib/components/ui/scroll-area/index.js";
    import { Skeleton } from "$lib/components/ui/skeleton/index.js";

    import GameSidebar from "$lib/components/game/GameSidebar.svelte";
    import HomeView from "$lib/components/game/HomeView.svelte";
    import InvestmentsView from "$lib/components/game/InvestmentsView.svelte";
    import LeaderboardView from "$lib/components/game/LeaderboardView.svelte";
    import MarketView from "$lib/components/game/MarketView.svelte";

    import { GameWebSocketClient } from "$lib/websocket";
    import { playerStore } from "$lib/stores/gameStore";
    import { userStore } from "$lib/stores/userStore";
    import { GameActions } from "$lib/types/websocket";
    import { GAME_CONTEXT_KEY, type GameContext } from "$lib/types/context";

    // Game context & controls
    let activeTab: string = $state("home");
    let activeLab: string | undefined = $state(undefined);
    let connectionEstablished = $state(false);
    let isLoading = $state(true);
    let needsVerification = $state(false);

    // Player creation
    let avatarImages: string[] = $state([]);
    let playerName: string = $state("");
    let labName: string = $state("");
    let location: string = $state("");
    let selectedAvatar: string = $state("");

    let gameContext: GameContext = $state({
        client: null,
        messages: [],
        sidebarOpen: false,
        toggleSidebar: () => gameContext.sidebarOpen = !gameContext.sidebarOpen,
    });

    $effect(() => {
        if (activeLab) {
            gameContext.client?.sendCommand(
                GameActions.RETRIEVE_LAB, 
                { id: $playerStore?.labs?.find((l) => l.name === activeLab)?.id }
            );
        }
    });

    $effect(() => {
        if (!activeLab && $playerStore?.labs && $playerStore?.labs?.length > 0) {
            activeLab = $playerStore.labs[0].name;
        }
    });

    function handleCreatePlayer(event: SubmitEvent) {
        event.preventDefault();
        if (!playerName.trim()) {
            toast.error("Player name is required");
            return;
        }
        if (!selectedAvatar) {
            toast.error("Please select an avatar");
        }

        gameContext.client?.sendCommand(GameActions.CREATE_PLAYER, { name: playerName.trim(), avatar: selectedAvatar });
    }

    function handleCreateLab(event: SubmitEvent) {
        event.preventDefault();
        if (!labName.trim()) {
            toast.error("Lab name is required");
            return;
        }

        gameContext.client?.sendCommand(GameActions.CREATE_LAB, { name: labName.trim(), location });
    }

    function handleCreateEmployee(event: SubmitEvent) {
        event.preventDefault();
        console.log("add employee");
    }

    function handleCreateModel(event: SubmitEvent, modelName: string, modelCategory: string) {
        event.preventDefault();
        if (!modelName.trim()) {
            toast.error("Model name is required");
            return;
        }
        if (!modelCategory.trim()) {
            toast.error("Choose a model category");
            return;
        }

        gameContext.client?.sendCommand(
            GameActions.CREATE_MODEL, 
            { name: modelName.trim(), category: modelCategory, lab_id: $playerStore?.labs?.find((l) => l.name === activeLab)?.id }
        );
    }

    async function loadAvatarImages() {
        try {
            const response = await fetch("/avatars");
            const paths = await response.json() as string[];
            avatarImages = paths.map(path => `/avatars/${path.split("/").pop()}`);
        } catch (error) {
            console.error("Failed to load avatar images", error);
            throw error;
        }
    }

    async function initializeWebSocket() {
        if (!$userStore?.access_token || connectionEstablished) {
            return;
        }

        try {
            gameContext.client = new GameWebSocketClient(undefined, gameContext);
            gameContext.client.token = $userStore.access_token;

            await gameContext.client.connectWebSocket();
            connectionEstablished = true;

            gameContext.client.sendCommand(GameActions.RETRIEVE_PLAYER_DATA);
        } catch (error) {
            throw new Error("WebSocket connection failed");
        }
    }

    onDestroy(() => {
        if (gameContext.client) {
            gameContext.client.close();
            connectionEstablished = false;
        }
    });

    onMount(async () => {
        try {
            const initialized = await userStore.initializeFromLocalStorage();

            if (!initialized) {
                throw new Error("User not initialized");
            }

            // Fetch user data first
            await userStore.fetchUser();
            
            if ($userStore?.access_token) {
                await initializeWebSocket();
            } else {
                throw new Error("User not authenticated");
            }

            gameContext.sidebarOpen = true;
            // Check if playerStore is not null else load avatars
            if (!$playerStore) {
                await loadAvatarImages();
            }
        } catch (error) {
            console.error('Failed to initialize:', error);
            await goto('/login');
        } finally {
            isLoading = false;
        }
    });
</script>

<svelte:head>
    <title>AI Venture | Play</title>
    <meta name="description" content="Play AI Venture" />
</svelte:head>

<main class="container mx-auto p-4 max-w-screen-xl">
    <GameSidebar bind:activeTab={activeTab} bind:activeLab={activeLab} {gameContext}>
        {#if isLoading}
            <div class="flex items-center justify-center h-screen mx-auto">
                <LoaderCircle class="mr-2 size-4 animate-spin" />
                <p>Loading the game state...</p>
            </div>
        {:else if needsVerification}
            <p>Please verify your email to continue. Check your inbox for a verification link.</p>
        {:else}
            {#if $userStore !== null}
                {#if $playerStore === null}
                    <form class="flex w-full max-w-sm flex-col gap-1.5" onsubmit={handleCreatePlayer}>
                        <Label for="player-name">Player name</Label>
                        <Input type="text" id="player-name" placeholder="Jane Doe" bind:value={playerName} />
                        <p class="text-muted-foreground text-sm">Enter your player name.</p>
                        <ScrollArea class="h-[400px] w-full rounded-md border p-4">
                            {#if avatarImages.length > 0}
                                <div class="grid grid-cols-4 gap-2">
                                    {#each avatarImages as imageUrl}
                                    <Avatar.Root class="relative w-12 h-12 cursor-pointer {selectedAvatar === imageUrl ? 'border-2 border-green-600' : ''}" onclick={() => selectedAvatar = imageUrl}>
                                        <Avatar.Image src={imageUrl} alt="avatar" />
                                        <Avatar.Fallback><Skeleton class="h-[20px] w-[20px] rounded-full" /></Avatar.Fallback>
                                    </Avatar.Root>
                                    {/each}
                                </div>
                            {:else}
                                <div class="text-center">
                                    <p class="text-destructive mb-2">Failed to load avatars</p>
                                    <Button 
                                        variant="outline" 
                                        onclick={() => loadAvatarImages()}
                                    >
                                        Retry
                                    </Button>
                                </div>
                            {/if}
                        </ScrollArea>
                        <Button type="submit">Submit</Button>
                    </form>
                {:else if $playerStore && ($playerStore.labs?.length === 0 || !$playerStore.labs)}
                    <form class="flex w-full max-w-lg flex-col gap-1.5" onsubmit={handleCreateLab}>
                        <Label for="lab-name">Lab name</Label>
                        <Input type="text" id="lab-name" placeholder="ClosedAI" bind:value={labName} />
                        <p class="text-muted-foreground text-sm">Enter your lab name.</p>
                        
                        <div class="grid grid-cols-3 gap-4 my-4">
                            <Card.Root 
                                class="cursor-pointer {location === 'us' ? 'border-2 border-green-600' : ''}" 
                                onclick={() => location = "us"}
                            >
                                <Card.Header>
                                    <Card.Title>US 🌎</Card.Title>
                                    <Card.Description>Silicon Valley Hub</Card.Description>
                                </Card.Header>
                                <Card.Content>
                                    <ul class="list-disc list-inside">
                                        <li class="text-sm">+5% Valuation</li>
                                        <li class="text-sm">+5% Income</li>
                                    </ul>
                                </Card.Content>
                            </Card.Root>

                            <Card.Root 
                                class="cursor-pointer {location === 'eu' ? 'border-2 border-green-600' : ''}" 
                                onclick={() => location = "eu"}
                            >
                                <Card.Header>
                                    <Card.Title>EU 🌍</Card.Title>
                                    <Card.Description>Research Focus</Card.Description>
                                </Card.Header>
                                <Card.Content>
                                    <ul class="list-disc list-inside">
                                        <li class="text-sm">+15% Research Speed</li>
                                        <li class="text-sm">-5% Valuation</li>
                                    </ul>
                                </Card.Content>
                            </Card.Root>

                            <Card.Root 
                                class="cursor-pointer {location === 'apac' ? 'border-2 border-green-600' : ''}" 
                                onclick={() => location = "apac"}
                            >
                                <Card.Header>
                                    <Card.Title>APAC 🌏</Card.Title>
                                    <Card.Description>Balanced Growth</Card.Description>
                                </Card.Header>
                                <Card.Content>
                                    <ul class="list-disc list-inside">
                                        <li class="text-sm">+5% Research Speed</li>
                                        <li class="text-sm">+5% Income</li>
                                    </ul>
                                </Card.Content>
                            </Card.Root>
                        </div>

                        <Button type="submit" disabled={!location}>Submit</Button>
                    </form>
                {/if}
            {/if}
        {/if}
        {#if activeTab === "home"}
            <HomeView activeLab={activeLab} handleCreateEmployee={handleCreateEmployee} handleCreateModel={handleCreateModel} />
        {:else if activeTab === "leaderboard"}
            <LeaderboardView />
        {:else if activeTab === "market"}
            <MarketView />
        {:else if activeTab === "investments"}
            <InvestmentsView />
        {/if}
    </GameSidebar>
</main>
