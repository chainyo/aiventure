<script lang="ts">
    import * as Form from "$lib/components/ui/form";
	import type { PageData } from "./$types";
	import { signupFormSchema } from "$lib/schema";
	import { zodClient } from "sveltekit-superforms/adapters";
	import { superForm } from "sveltekit-superforms";
    import { Button } from "$lib/components/ui/button";
	export let data: PageData;
 
	const form = superForm(data.form, {
		validators: zodClient(signupFormSchema),
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
        console.log(jsonData);

		try {
			const response = await fetch('/api/auth/register', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify(jsonData)
			});
			if (response.ok) {
				// Handle successful registration
				console.log('Registration successful');
			} else {
				// Handle errors
				console.error('Registration failed');
			}
		} catch (error) {
			console.error('Error submitting form:', error);
		}
	}
</script>

<main class="container mx-auto p-4 max-w-md">
    <h1 class="text-3xl font-bold mb-6">Welcome to Aiventure</h1>
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
</main>
