<script lang="ts">
    import { getContext } from "svelte";
    import { BrainCircuit, Briefcase, CircleDollarSign, HandCoins, Landmark, Network } from "lucide-svelte";

    import { type GameContext, GAME_CONTEXT_KEY } from "$lib/types/context";
    import { labStore } from "$lib/stores/gameStore";

    import * as Avatar from "$lib/components/ui/avatar/index.js";
    import { Badge } from "$lib/components/ui/badge/index.js";
    import * as Card from "$lib/components/ui/card/index.js";
    import * as Dialog from "$lib/components/ui/dialog/index.js";
    import * as HoverCard from "$lib/components/ui/hover-card/index.js";
    import { ScrollArea } from "$lib/components/ui/scroll-area/index.js";

    let gameContext = getContext<GameContext>(GAME_CONTEXT_KEY);
    const locationEmoji: Record<string, string> = {
        us: "🌎",
        eu: "🌍",
        apac: "🌏",
    };
</script>

<svelte:head>
    <title>AI Venture | Play</title>
    <meta name="description" content="Play AI Venture" />
</svelte:head>

<main class="container mx-auto p-4 max-w-screen-xl">
    {#if gameContext.activeLab}
        <div class="grid grid-cols-4 gap-4">
            <!-- General lab information -->
            <Card.Root class="w-full p-4 col-span-1">
                <Card.Header class="flex flex-col gap-2">
                    <Card.Title>{gameContext.activeLab}</Card.Title>
                    <Card.Description>
                        <Badge variant="outline">
                            {locationEmoji[$labStore?.location ?? "us"]} {$labStore?.location.toUpperCase()}
                        </Badge>
                    </Card.Description>
                </Card.Header>
                <Card.Content>
                    <p class="flex items-center">
                        <Landmark class="w-5 h-5" />
                        <span class="text-md pl-1">Valuation: ${$labStore?.valuation}</span>
                    </p>
                    <p class="flex items-center mt-2">
                        <CircleDollarSign class="w-5 h-5" />
                        <span class="text-md pl-1">Income: ${$labStore?.income} / 5min</span>
                    </p>
                </Card.Content>
                <Card.Footer class="flex justify-center mt-4">
                    <Dialog.Root>
                        <Dialog.Trigger class="flex items-center gap-2 p-4 border rounded-md text-lg">
                            <Network class="w-8 h-8" />
                            Tech Tree
                        </Dialog.Trigger>
                        <Dialog.Content>
                          <Dialog.Header>
                            <Dialog.Title>{$labStore?.tech_tree_id}</Dialog.Title>
                            <Dialog.Description>
                                Here you can see the tech tree for your lab.
                            </Dialog.Description>
                          </Dialog.Header>
                        </Dialog.Content>
                    </Dialog.Root>
                </Card.Footer>
            </Card.Root>

            <!-- Models -->
            <Card.Root class="w-full p-4 col-span-3">
                <Card.Header>
                    <Card.Title class="flex gap-2 items-center">
                        <BrainCircuit class="w-5 h-5" />
                        Models
                    </Card.Title>
                </Card.Header>
                <Card.Content>
                    <ScrollArea class="h-[200px] w-full p-4">
                        {#each $labStore?.models ?? [] as model}
                            <p>{model.name}</p>
                        {/each}
                    </ScrollArea>
                </Card.Content>
            </Card.Root>

            <!-- Employees -->
            <Card.Root class="w-full p-4 col-span-3">
                <Card.Header>
                    <Card.Title class="flex gap-2 items-center">
                        <Briefcase class="w-5 h-5" />
                        Employees
                    </Card.Title>
                </Card.Header>
                <Card.Content>
                    <ScrollArea class="h-[200px] w-full p-4">
                        {#each $labStore?.employees ?? [] as employee}
                            <p>{employee.name}</p>
                        {/each}
                    </ScrollArea>
                </Card.Content>
            </Card.Root>

            <!-- Investors -->
            <Card.Root class="w-full p-4 col-span-1">
                <Card.Header>
                    <Card.Title class="flex gap-2 items-center">
                        <HandCoins class="w-5 h-5" />
                        Investors
                    </Card.Title>
                </Card.Header>
                <Card.Content>
                    <ScrollArea class="h-[200px] w-full p-4">
                        {#each $labStore?.investors ?? [] as investor}
                            <HoverCard.Root>
                                <HoverCard.Trigger>
                                    <Avatar.Root class="relative w-8 h-8">
                                        <Avatar.Image src={investor.player.avatar} alt="avatar" />
                                        <Avatar.Fallback>{investor.player.name.slice(0, 2).toUpperCase()}</Avatar.Fallback>
                                    </Avatar.Root>
                                </HoverCard.Trigger>
                                <HoverCard.Content class="w-full items-center">
                                    <div class="flex flex-row gap-2">
                                        <Avatar.Root class="relative w-8 h-8">
                                            <Avatar.Image src={investor.player.avatar} alt="avatar" />
                                            <Avatar.Fallback>{investor.player.name.slice(0, 2).toUpperCase()}</Avatar.Fallback>
                                        </Avatar.Root>
                                        <div class="flex flex-col">
                                            <p class="text-lg">{investor.player.name}</p>
                                            <p class="text-sm text-gray-500">{investor.part * 100}%</p>
                                        </div>
                                    </div>
                                </HoverCard.Content>
                            </HoverCard.Root>
                        {/each}
                    </ScrollArea>
                </Card.Content>
            </Card.Root>
        </div>
    {:else}
        <p>No lab selected. Please select a lab from the sidebar.</p>
    {/if}
</main>
