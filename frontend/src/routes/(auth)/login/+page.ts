import { superValidate } from "sveltekit-superforms";
import { loginFormSchema } from "$lib/schema";
import { zod } from "sveltekit-superforms/adapters";
/** @type {import('./$types').PageData} */
export const load = async () => {
    return {
        form: await superValidate(zod(loginFormSchema)),
    };
};
