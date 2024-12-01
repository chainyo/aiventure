<script lang="ts">
    import { onMount } from "svelte";
    import { BrainCircuit, BriefcaseBusiness, HandCoins } from "lucide-svelte";

    import * as Avatar from "$lib/components/ui/avatar/index.js";
    import * as Table from "$lib/components/ui/table/index.js";

    import { LOCATIONS } from "$lib/constants.js";
    import type { Lab } from "$lib/stores/gameStore";
    import { formatNumber } from "$lib/utils.js";

    let labs: Lab[] = $state([]);

    async function fetchLeaderboard() {
        const response = await fetch("/api/game/leaderboard");
        const data = (await response.json()) as Lab[];
        labs = data;
    }

    onMount(async () => {
        await fetchLeaderboard();
    });
</script>


<Table.Root>
    <Table.Caption>AI Venture Leaderboard - Top 100</Table.Caption>
    <Table.Header>
        <Table.Row>
            <Table.Head>#</Table.Head>
            <Table.Head class="w-[100px]">Lab</Table.Head>
            <Table.Head>Location</Table.Head>
            <Table.Head>Owner</Table.Head>
            <Table.Head>Models</Table.Head>
            <Table.Head>Employees</Table.Head>
            <Table.Head>Investors</Table.Head>
            <Table.Head>Income</Table.Head>
            <Table.Head class="text-right">Valuation</Table.Head>
        </Table.Row>
    </Table.Header>
    <Table.Body>
        <Table.Row>
            {#each labs as lab, index}
                {@const loc = LOCATIONS[lab.location]}
                <Table.Cell>{index + 1}</Table.Cell>
                <Table.Cell class="font-medium">{lab.name}</Table.Cell>
                <Table.Cell>
                    <span class="flex items-center gap-2">
                        {loc.emoji} {loc.title}
                    </span>
                </Table.Cell>
                <Table.Cell>
                    <Avatar.Root class="relative w-6 h-6">
                        <Avatar.Image src={lab.player?.avatar} alt="avatar" />
                        <Avatar.Fallback>{lab.player?.name.slice(0, 2)}</Avatar.Fallback>
                    </Avatar.Root>
                </Table.Cell>
                <Table.Cell>
                    <span class="flex items-center gap-2">
                        <BrainCircuit class="w-4 h-4" /> {lab.models.length}
                    </span>
                </Table.Cell>
                <Table.Cell>
                    <span class="flex items-center gap-2">
                        <BriefcaseBusiness class="w-4 h-4" /> {lab.employees.length}
                    </span>
                </Table.Cell>
                <Table.Cell>
                    <span class="flex items-center gap-2">
                        <HandCoins class="w-4 h-4" /> {lab.investors.length}
                    </span>
                </Table.Cell>
                <Table.Cell>${formatNumber(lab.income, 1e6)}/min</Table.Cell>
                <Table.Cell class="text-right">${formatNumber(lab.valuation, 1e6)}</Table.Cell>
            {/each}
        </Table.Row>
    </Table.Body>
</Table.Root>
