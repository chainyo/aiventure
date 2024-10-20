import React, { createContext, useContext, useReducer, useEffect } from 'react';

export interface UserData {
    name: string;
    pid: string;
    token: string;
    is_verified: boolean;
}

type UserState = UserData | null;

type UserAction =
    | { type: 'SET_USER'; payload: UserData }
    | { type: 'CLEAR_USER' };

const UserStateContext = createContext<UserState>(null);
const UserDispatchContext = createContext<React.Dispatch<UserAction> | null>(null);

function userReducer(state: UserState, action: UserAction): UserState {
    switch (action.type) {
        case 'SET_USER':
            localStorage.setItem('aiventureUser', JSON.stringify(action.payload));
            return action.payload;
        case 'CLEAR_USER':
            localStorage.removeItem('aiventureUser');
            return null;
        default:
            return state;
    }
}

export function UserProvider({ children }: { children: React.ReactNode }) {
    const [state, dispatch] = useReducer(userReducer, null);

    useEffect(() => {
        const storedUser = localStorage.getItem('aiventureUser');
        if (storedUser) {
            dispatch({ type: 'SET_USER', payload: JSON.parse(storedUser) });
        }
    }, []);

    return (
        <UserStateContext.Provider value={state}>
            <UserDispatchContext.Provider value={dispatch}>
                {children}
            </UserDispatchContext.Provider>
        </UserStateContext.Provider>
    );
}

export function useUserState() {
    const context = useContext(UserStateContext);
    if (context === undefined) {
        throw new Error('useUserState must be used within a UserProvider');
    }
    return context;
}

export function useUserDispatch() {
    const context = useContext(UserDispatchContext);
    if (context === undefined) {
        throw new Error('useUserDispatch must be used within a UserProvider');
    }
    return context;
}

export function useUser() {
    return [useUserState(), useUserDispatch()] as const;
}
