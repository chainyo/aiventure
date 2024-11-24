<script lang="ts">
    import { onMount, onDestroy, setContext } from 'svelte';
    import { goto } from "$app/navigation";
    import { LoaderCircle, Moon, Sun } from "lucide-svelte";
    import { toast } from "svelte-sonner";
    import { toggleMode } from "mode-watcher";

    import { GameWebSocketClient } from "$lib/websocket";
    import { GAME_CONTEXT_KEY, type GameContext } from "$lib/types/context";
    import { GameActions } from "$lib/types/websocket";
    import { playerStore } from "$lib/stores/gameStore";
    import { userStore } from "$lib/stores/userStore";
    import * as Avatar from "$lib/components/ui/avatar/index.js";
    import { Badge } from "$lib/components/ui/badge/index.js";
    import { Button } from "$lib/components/ui/button/index.js";
    import * as Card from "$lib/components/ui/card/index.js";
    import { Label } from "$lib/components/ui/label/index.js";
    import { Input } from "$lib/components/ui/input/index.js";
    import { ScrollArea } from "$lib/components/ui/scroll-area/index.js";
    import * as Select from "$lib/components/ui/select/index.js";
    import * as Sidebar from "$lib/components/ui/sidebar/index.js";
    import { Skeleton } from "$lib/components/ui/skeleton/index.js";

    let { children } = $props();
    let isLoading = $state(true);
    let connectionEstablished = $state(false);
    let needsVerification = $state(false);
    let avatarImages: string[] = $state([]);
    let selectedAvatar: string = $state("");
    let playerAvatar: string = $state("");
    let avatarLoadingPromise: Promise<void> | null = $state(null);
    let playerName: string = $state("");
    let labName: string = $state("");
    let location: string = $state("");

    let gameContext: GameContext = $state({
        client: null,
        messages: [],
        activeLab: undefined,
        sidebarOpen: false,
        toggleSidebar: () => gameContext.sidebarOpen = !gameContext.sidebarOpen,
    });
    setContext(GAME_CONTEXT_KEY, gameContext);

    const triggerActiveLab = $derived(
        $playerStore?.labs?.find((l) => l.name === gameContext.activeLab)?.name ?? "Select a lab"
    );

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
            console.log($playerStore?.avatar);
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
        } catch (error) {
            console.error('Failed to initialize:', error);
            await goto('/login');
        } finally {
            isLoading = false;
        }
    });
</script>

<Sidebar.Provider open={gameContext.sidebarOpen}>
    <Sidebar.Root>
        <Sidebar.Header>
            <Sidebar.Menu>
                <Sidebar.MenuItem class="w-full flex justify-center">
                    <Select.Root type="single" name="activeLab" bind:value={gameContext.activeLab}>
                        <Select.Trigger class="w-full max-w-[calc(100%-1rem)]">{triggerActiveLab}</Select.Trigger>
                        <Select.Content>
                          <Select.Group>
                            <Select.GroupHeading>🧪 Your Labs</Select.GroupHeading>
                            {#each $playerStore?.labs ?? [] as lab}
                              <Select.Item value={lab.name} label={lab.name}
                                >{lab.name}</Select.Item
                              >
                            {/each}
                          </Select.Group>
                        </Select.Content>
                    </Select.Root>
                </Sidebar.MenuItem>
            </Sidebar.Menu>
        </Sidebar.Header>
        <Sidebar.Content>
            <Sidebar.Group />

            <Sidebar.Group />
        </Sidebar.Content>
        <Sidebar.Footer class="pb-8">
            <Sidebar.Menu class="flex flex-row items-center mx-auto justify-center gap-4">
                {#if $playerStore}
                    <Sidebar.MenuItem>
                        <Avatar.Root class="relative w-12 h-12 ">
                            <Avatar.Image src={playerAvatar} alt="avatar" />
                            <Avatar.Fallback>{$playerStore.name.slice(0, 2)}</Avatar.Fallback>
                        </Avatar.Root>
                    </Sidebar.MenuItem>
                    <div class="flex flex-col gap-2">
                        <Sidebar.MenuItem>
                            <Badge class="max-w-full" variant="outline">{$playerStore.name}</Badge>
                        </Sidebar.MenuItem>
                        <Sidebar.MenuItem>
                            <Badge class="max-w-full">$ {$playerStore.funds}</Badge>
                        </Sidebar.MenuItem>
                    </div>
                {:else}
                    <Sidebar.MenuItem>
                        <Skeleton class="size-8 rounded-full" />
                    </Sidebar.MenuItem>
                    <div class="flex flex-col gap-2">
                        <Sidebar.MenuItem>
                            <Skeleton class="h-4 w-[125px]" />
                        </Sidebar.MenuItem>
                        <Sidebar.MenuItem>
                            <Skeleton class="h-4 w-[125px]" />
                        </Sidebar.MenuItem>
                    </div>
                {/if}
            </Sidebar.Menu>
            <Sidebar.Menu class="flex flex-row justify-center gap-2 mt-8">
                <Button onclick={toggleMode} variant="outline" size="icon">
                    <Sun
                    class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0"
                    />
                    <Moon
                    class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100"
                    />
                    <span class="sr-only">Toggle theme</span>
                </Button>
                <Button onclick={() => { window.open('https://github.com/chainyo/aiventure', '_blank'); }} variant="outline" size="icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-github"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/><path d="M9 18c-4.51 2-5-2-7-2"/></svg>
                </Button>
                <Button onclick={() => { userStore.clearUser(); goto('/login'); }} variant="outline" size="icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-log-out"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" x2="9" y1="12" y2="12"/></svg>
                </Button>
            </Sidebar.Menu>
        </Sidebar.Footer>
    </Sidebar.Root>
    <main class="container mx-auto p-4 w-full">
        <Sidebar.Trigger class="absolute top-0 right-0"/>
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
                            {#if !avatarLoadingPromise}
                                <Button variant="outline" onclick={() => avatarLoadingPromise = loadAvatarImages()} class="w-full">Load Avatars</Button>
                            {:else}
                                {#await avatarLoadingPromise}
                                    <Skeleton class="h-[20px] w-[20px] rounded-full" />
                                {:then}
                                    <div class="grid grid-cols-4 gap-2">
                                        {#each avatarImages as imageUrl}
                                        <Avatar.Root class="relative w-12 h-12 cursor-pointer {selectedAvatar === imageUrl ? 'border-2 border-green-600' : ''}" onclick={() => selectedAvatar = imageUrl}>
                                            <Avatar.Image src={imageUrl} alt="avatar" />
                                            <Avatar.Fallback><Skeleton class="h-[20px] w-[20px] rounded-full" /></Avatar.Fallback>
                                        </Avatar.Root>
                                        {/each}
                                    </div>
                                {:catch error}
                                    <div class="text-center">
                                        <p class="text-destructive mb-2">Failed to load avatars: {error.message}</p>
                                        <Button 
                                            variant="outline" 
                                            onclick={() => avatarLoadingPromise = loadAvatarImages()}
                                        >
                                            Retry
                                        </Button>
                                    </div>
                                {/await}
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
                {:else}
                    {@render children?.()}
                {/if}
            {/if}
        {/if}
    </main>
</Sidebar.Provider>
