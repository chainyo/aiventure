<script lang="ts">
    import { fly } from 'svelte/transition';
    import { spring } from 'svelte/motion';
    import { fundsAnimationStore } from "$lib/stores/animationStore";
    import { formatNumber } from "$lib/utils";
    export let value: number;
    
    let displayValue = spring(value);
    let previousValue = value;
    let showDifference = false;
    let currentDifference = 0;
    
    $: {
        displayValue.set(value);
        previousValue = value;
    }

    $: if ($fundsAnimationStore) {
        currentDifference = $fundsAnimationStore.difference;
        showDifference = true;
        setTimeout(() => {
            showDifference = false;
            fundsAnimationStore.set(null);
        }, 500);
    }
</script>

<div class="inline-flex items-center gap-2">
    <span class="bg-accent text-accent-foreground px-2 py-1 rounded-md">$ {formatNumber($displayValue, 1e6)}</span>
    
    <div class="w-[18px] relative">
        {#if showDifference && currentDifference !== 0}
            <span
                class="absolute left-0 text-xs font-bold whitespace-nowrap
                {currentDifference > 0 ? 'text-emerald-500' : 'text-red-500'}"
                in:fly={{ y: 0, duration: 100 }}
                out:fly={{ y: -40, duration: 300 }}
            >
                {currentDifference > 0 ? '+' : ''}{formatNumber(currentDifference, 1e3)}
            </span>
        {/if}
    </div>
</div>
