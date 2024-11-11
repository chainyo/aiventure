<script lang="ts">
	import { goto } from "$app/navigation";
	import { onMount } from "svelte";
	import type { PageData } from "./$types";

    import { toast } from "svelte-sonner";
	import { zodClient } from "sveltekit-superforms/adapters";
	import { superForm } from "sveltekit-superforms";

    import * as Form from "$lib/components/ui/form";
    import { Button } from "$lib/components/ui/button";
	import { loginFormSchema } from "$lib/schema";
	import { userStore, type UserData } from "$lib/stores/userStore";

	export let data: PageData;
	let isInitialized = false;

	onMount(() => {
		if (userStore.initializeFromLocalStorage()) {
			redirectToPlay();
		}
		isInitialized = true;
	});

	function redirectToPlay() {
		setTimeout(() => {
			goto('/play');
		}, 3000);
	}

	$: if (isInitialized && $userStore) {
		redirectToPlay();
	}
 
	const form = superForm(data.form, {
		validators: zodClient(loginFormSchema),
        validationMethod: 'onsubmit',
		dataType: 'json',
		onSubmit: ({ formData, cancel }) => {
			cancel();
			submitForm(formData);
		}
	});
	const { form: formData, enhance } = form;

	async function submitForm(formData: any) {
		const params = new URLSearchParams({
			username: formData.get("email"),
			password: formData.get("password"),
			grant_type: "password",
		});
		const loginPromise = fetch('/api/auth/authenticate', {
			method: 'POST',
			headers: {
				"Content-Type": "application/x-www-form-urlencoded",
			},
			body: params.toString()
		}).then(async (response) => {
			if (!response.ok) {
				throw new Error(response.statusText);
			}
			return await response.json();
		});
		toast.promise(loginPromise, {
			loading: 'Logging in...',
			success: (data: UserData) => {
				userStore.setUser(data);
				setTimeout(() => {
					goto('/play');
				}, 3000);
				return "Logged in successfully.";
			},
			error: (error: any) => `Login failed: ${error.message}`,
		});
	}
</script>
<svelte:head>
  <title>AI Venture | Login</title>
  <meta name="description" content="Login to AI Venture" />
</svelte:head>
<main class="container mx-auto p-4 max-w-md">
    <h1 class="text-3xl font-bold mb-6">Login to AI Venture</h1>
    {#if isInitialized && !$userStore}
        <form method="POST" use:enhance>
            <Form.Field {form} name="email">
                <Form.Control let:attrs>
                    <Form.Label>Email</Form.Label>
                    <input {...attrs} type="email" bind:value={$formData.email} />
                </Form.Control>
                <Form.Description>Use an email you have access to.</Form.Description>
                <Form.FieldErrors />
            </Form.Field>
            <Form.Field {form} name="password">
                <Form.Control let:attrs>
                    <Form.Label>Password</Form.Label>
                    <input {...attrs} type="password" bind:value={$formData.password} />
                </Form.Control>
                <Form.Description>Ensure the password is at least 6 characters.</Form.Description>
                <Form.FieldErrors />
            </Form.Field>
            <Button type="submit">Log in</Button>
        </form>
    {:else if $userStore}
        <p class="text-2xl">Welcome back <span class="font-bold text-blue-500">{$userStore.email}</span></p>
		<p class="text-gray-500">Redirecting you to the game...</p>
    {:else}
		<p>Loading...</p>
	{/if}
</main>
