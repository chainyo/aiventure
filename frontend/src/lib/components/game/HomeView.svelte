<script lang="ts">
    import { 
        AudioLines,
        BrainCircuit,
        Briefcase,
        CircleDollarSign,
        CirclePlus,
        Eye,
        HandCoins,
        Landmark,
        MessageSquareText,
        Network,
        SquareStack,
        UserRoundPlus,
        type Icon as IconType
    } from "lucide-svelte";

    import { CREATE_MODEL_COST } from "$lib/constants";
    import { labStore } from "$lib/stores/gameStore";

    import * as Avatar from "$lib/components/ui/avatar/index.js";
    import { Badge } from "$lib/components/ui/badge/index.js";
    import { Button } from "$lib/components/ui/button/index.js";
    import * as Card from "$lib/components/ui/card/index.js";
    import * as Dialog from "$lib/components/ui/dialog/index.js";
    import * as HoverCard from "$lib/components/ui/hover-card/index.js";
    import { Input } from "$lib/components/ui/input/index.js";
    import { Label } from "$lib/components/ui/label/index.js";
    import { ScrollArea } from "$lib/components/ui/scroll-area/index.js";

    let { activeLab, handleCreateEmployee, handleCreateModel } = $props();
    let modelName = $state("");
    let modelCategory = $state("audio");
    const locationEmoji: Record<string, string> = {
        us: "🌎",
        eu: "🌍",
        apac: "🌏",
    };
    const modelCategories: Record<string, { title: typeof IconType, description: string }> = {
        "audio": { title: AudioLines, description: "Audio" },
        "cv": { title: Eye, description: "Vision" },
        "nlp": { title: MessageSquareText, description: "Language" },
        "multi_modal": { title: SquareStack, description: "Modal" },
    };
</script>

{#if activeLab}
    <div class="grid grid-cols-4 gap-4">
        <!-- General lab information -->
        <Card.Root class="w-full p-4 col-span-1">
            <Card.Header class="flex flex-col gap-2">
                <Card.Title>{activeLab}</Card.Title>
                <Card.Description>
                    <Badge variant="outline">
                        {locationEmoji[$labStore?.location ?? "us"]} {$labStore?.location.toUpperCase()}
                    </Badge>
                </Card.Description>
            </Card.Header>
            <Card.Content>
                <p class="flex items-center">
                    <Landmark class="w-5 h-5" />
                    <span class="text-sm pl-1">Valuation: ${$labStore?.valuation}</span>
                </p>
                <p class="flex items-center mt-2">
                    <CircleDollarSign class="w-5 h-5" />
                    <span class="text-sm pl-1">Income: ${$labStore?.income} / 5min</span>
                </p>
            </Card.Content>
            <Card.Footer class="flex justify-center mt-4">
                <Dialog.Root>
                    <Dialog.Trigger class="flex items-center gap-2 p-4 border rounded-md text-md">
                        <Network class="w-6 h-6" />
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
                    <Dialog.Root>
                        <Dialog.Trigger>
                            <CirclePlus class="w-4 h-4" />
                        </Dialog.Trigger>
                        <Dialog.Content class="w-full gap-8">
                            <Dialog.Header>
                                <Dialog.Title>New AI Model</Dialog.Title>
                                <Dialog.Description>
                                    Choose a name and pick a category 👇
                                </Dialog.Description>
                            </Dialog.Header>
                            <form onsubmit={(e) => handleCreateModel(e, modelName, modelCategory)} class="flex flex-col items-center justify-center gap-8">
                                <Label for="model-name">Model name</Label>
                                <Input type="text" id="model-name" placeholder="x-chat-v1" bind:value={modelName} />
                                <div class="grid grid-cols-4 gap-4">
                                    {#each Object.keys(modelCategories) as category}
                                        <Card.Root 
                                            class="p-4 cursor-pointer {modelCategory === category ? 'border-2 border-green-600' : ''}" 
                                            onclick={() => modelCategory = category}
                                        >
                                            <Card.Header class="flex flex-col items-center justify-center text-center">
                                                {@const Icon = modelCategories[category].title}
                                                <Card.Title><Icon class="w-4 h-4" /></Card.Title>
                                                <Card.Description class="text-xs">{modelCategories[category].description}</Card.Description>
                                            </Card.Header>
                                        </Card.Root>
                                    {/each}
                                </div>
                                <Button type="submit">$ {CREATE_MODEL_COST}</Button>
                            </form>
                        </Dialog.Content>
                    </Dialog.Root>
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
                    <Button variant="ghost" size="icon" onclick={() => handleCreateEmployee()}>
                        <UserRoundPlus class="w-4 h-4" />
                    </Button>
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