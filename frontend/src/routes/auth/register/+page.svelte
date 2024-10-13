<script lang="ts">
    import { toast } from "svelte-sonner";
    import * as Form from "$lib/components/ui/form";
	import { signupFormSchema } from "$lib/schema";
	import { zodClient } from "sveltekit-superforms/adapters";
	import { superForm } from "sveltekit-superforms";
    import { Button } from "$lib/components/ui/button";

	import type { PageData } from "./$types";
	export let data: PageData;

    let registrationSuccess: boolean = false;
 
	const form = superForm(data.form, {
		validators: zodClient(signupFormSchema),
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
			name: formData.get("name"),
			email: formData.get("email"),
			password: formData.get("password"),
		}

		const registerPromise = fetch('/api/auth/register', {
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
			loading: 'Registering...',
			success: (data) => {
				registrationSuccess = true;
				return "Registration successful. Please check your email for verification.";
			},
			error: (error: any) => `Registration failed: ${error.message}`,
		});
	}
</script>

<main class="container mx-auto p-4 max-w-md">
    <h1 class="text-3xl font-bold mb-6">Welcome to Aiventure</h1>
    {#if !registrationSuccess}
        <form method="POST" use:enhance>
            <Form.Field {form} name="name">
                <Form.Control let:attrs>
                    <Form.Label>Username</Form.Label>
                    <input {...attrs} bind:value={$formData.name} />
                </Form.Control>
                <Form.Description>This will be your display name.</Form.Description>
                <Form.FieldErrors />
            </Form.Field>
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
            <Button type="submit">Register</Button>
        </form>
    {:else}
        <p>Registration successful. You can now <a href="/auth/login">login</a>.</p>
    {/if}
</main>
