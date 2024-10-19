<script lang="ts">
    import { Button } from "$lib/components/ui/button";
</script>

<div class="flex flex-col items-center justify-center h-screen">
    <div class="flex flex-col items-center justify-center m-8">
        <h1 class="text-4xl font-bold">AI Venture</h1>
        <p class="text-lg text-gray-600">
        A strategy game where you build and lead AI labs to dominate the tech industry through smart investments and innovation.
        </p>
    </div>
    <div class="flex flex-row gap-4 items-center justify-center">
        <Button href="/login">Login</Button>
        <Button href="/register">Register</Button>
    </div>
</div>
