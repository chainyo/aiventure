<script lang="ts">
    import { PawPrint } from 'lucide-svelte';
    import { Button } from "$lib/components/ui/button";
</script>


<div class="flex flex-col justify-center items-center h-screen">
    <div class="grid grid-cols-2 gap-4 items-center">
        <div class="flex justify-end">
            <img src="/not-found.png" alt="404-not-found-doge" class="max-w-xs" />
        </div>
        <div class="flex flex-col items-start text-left gap-2">
            <p>such missing link</p>
            <p>so 404</p>
            <p>wow</p>
        </div>
    </div>
    <Button variant="outline" href="/" class="mt-8 gap-2 bg-amber-300 dark:bg-amber-500 dark:hover:bg-zinc-500">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-arrow-up-right"><path d="M7 7h10v10"/><path d="M7 17 17 7"/></svg>
        back home
    </Button>
</div>
