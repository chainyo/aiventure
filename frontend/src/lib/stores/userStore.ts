import { writable } from "svelte/store";

export interface UserData {
    email: string | null
    id: string | null;
    is_admin: boolean | null;
    is_verified: boolean | null;
    access_token: string | null;
    token_type: string | null;
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
            if (!storedUser?.access_token) return false;

            try {
                const response = await fetch('/api/auth/me', {
                    headers: {
                        'Authorization': `Bearer ${storedUser.access_token}`
                    }
                });

                if (response.ok) {
                    const userData = await response.json();
                    const updatedUserData: UserData = {
                        email: userData.email,
                        id: userData.id,
                        is_admin: userData.is_admin,
                        is_verified: userData.is_verified,
                        access_token: storedUser.access_token,
                        token_type: storedUser.token_type
                    };
                    set(updatedUserData);
                    localStorage.setItem('aiventureUser', JSON.stringify(updatedUserData));
                    return true;
                } else {
                    set(null);
                    localStorage.removeItem('aiventureUser');
                    return false;
                }
            } catch (error) {
                console.error('Error fetching user data:', error);
                set(null);
                localStorage.removeItem('aiventureUser');
                return false;
            }
        }
    };
}

export const userStore = createUserStore();
