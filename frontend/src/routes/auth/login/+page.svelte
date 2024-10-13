<script lang="ts">
    import { toast } from "svelte-sonner";
    import * as Form from "$lib/components/ui/form";
	import { loginFormSchema } from "$lib/schema";
	import { zodClient } from "sveltekit-superforms/adapters";
	import { superForm, type SuperValidated, type Infer } from "sveltekit-superforms";
    import { Button } from "$lib/components/ui/button";

    /** @type {import('./$types').PageData} */
	export let data: SuperValidated<Infer<typeof loginFormSchema>>;

    let userData: any = null;
 
	const form = superForm(data, {
		validators: zodClient(loginFormSchema),
        validationMethod: 'onsubmit',
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

		const registerPromise = fetch('/api/auth/login', {
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

		toast.promise(registerPromise, {
			loading: 'Logging in...',
			success: (data) => {
				console.log(data);
                userData = data;
				return "Logged in successfully.";
			},
			error: (error: any) => `Login failed: ${error.message}`,
		});
	}
</script>

<main class="container mx-auto p-4 max-w-md">
    <h1 class="text-3xl font-bold mb-6">Welcome to Aiventure</h1>
    {#if !userData}
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
    {:else}
        <p>Logged in as {userData.user.name}</p>
        <p>Email: {userData.user.email}</p>
        <Button on:click={() => (userData = null)}>Log out</Button>
    {/if}
</main>
