<script lang="ts">
	import { goto } from "$app/navigation";
	import { onMount } from "svelte";

    import { toast } from "svelte-sonner";
    import * as Form from "$lib/components/ui/form";
	import { loginFormSchema } from "$lib/schema";
	import { zodClient } from "sveltekit-superforms/adapters";
	import { superForm } from "sveltekit-superforms";
    import { Button } from "$lib/components/ui/button";

	import { userStore, type UserData } from "$lib/stores/userStore";

	import type { PageData } from "./$types";
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
		const jsonData = {
			email: formData.get("email"),
			password: formData.get("password"),
		}

		const loginPromise = fetch('/api/auth/login', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(jsonData)
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
        <p class="text-2xl">Welcome back <span class="font-bold text-blue-500">{$userStore.name}</span></p>
		<p class="text-gray-500">Redirecting you to the game...</p>
    {:else}
		<p>Loading...</p>
	{/if}
</main>
