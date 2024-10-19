import { writable } from "svelte/store";
import type { Writable } from "svelte/store";

export interface UserData {
    name: string;
    pid: string;
    token: string;
    is_verified: boolean;
}

function createUserStore() {
    const { subscribe, set } = writable<UserData | null>(null);

    return {
        subscribe,
        setUser: (userData: UserData) => {
            set(userData);
            localStorage.setItem('aiventureUser', JSON.stringify(userData));
        },
        clearUser: () => {
            set(null);
            localStorage.removeItem('aiventureUser');
        },
        initializeFromLocalStorage: () => {
            const storedUser = localStorage.getItem('aiventureUser');
            if (storedUser) {
                set(JSON.parse(storedUser) as UserData);
                return true;
            }
            return false;
        },
        fetchUser: async () => {
            const storedUser: UserData | null = JSON.parse(localStorage.getItem('aiventureUser') || 'null');
            if (!storedUser) return false;

            try {
                const response = await fetch('/api/user/current', {
                    headers: {
                        'Authorization': `Bearer ${storedUser.token}`
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    console.log(data);
                    set(data as UserData);
                    return true;
                } else {
                    throw new Error('Failed to fetch user data');
                }
            } catch (error) {
                console.error('Error fetching user data:', error);
                return false;
            }
        }
    };
}

export const userStore = createUserStore();
