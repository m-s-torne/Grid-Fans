import { supabase } from '@/lib/supabase'
import type { User, Session, AuthError } from '@supabase/supabase-js'
import { ENV } from '@/lib/env'

export interface AuthService {
    signUp(email: string, password: string, userData?: any): Promise<{
        data: any;
        error: AuthError | null;
    }>;
    signIn(email: string, password: string): Promise<{
        data: any;
        error: AuthError | null;
    }>;
    signInWithGoogle(): Promise<{
        data: any;
        error: AuthError | null;
    }>;
    signOut(): Promise<{
        error: AuthError | null;
    }>;
    getSession(): Promise<{
        data: { session: Session | null };
        error: AuthError | null;
    }>;
    getCurrentUser(): Promise<{
        data: { user: User | null };
        error: AuthError | null;
    }>;
    refreshSession(): Promise<{
        data: { session: Session | null };
        error: AuthError | null;
    }>;
}

export const authService: AuthService = {
    async signUp(email: string, password: string, userData?: any) {
        try {
            const { data, error } = await supabase.auth.signUp({
                email,
                password,
                options: {
                    data: userData || {},
                    emailRedirectTo: `${ENV.APP_URL}/auth/confirm`
                }
            })

            return { data, error }
        } catch (error) {
            return { 
                data: null, 
                error: error as AuthError 
            }
        }
    },

    async signIn(email: string, password: string) {
        try {
            const { data, error } = await supabase.auth.signInWithPassword({
                email,
                password
            })

            return { data, error }
        } catch (error) {
            return { 
                data: null, 
                error: error as AuthError 
            }
        }
    },

    async signInWithGoogle() {
        try {
            const { data, error } = await supabase.auth.signInWithOAuth({
                provider: 'google',
                options: {
                    redirectTo: `${ENV.APP_URL}/auth/confirm`
                }
            })

            return { data, error }
        } catch (error) {
            return { 
                data: null, 
                error: error as AuthError 
            }
        }
    },

    async signOut() {
        try {
            const { error } = await supabase.auth.signOut()
            return { error }
        } catch (error) {
            return { error: error as AuthError }
        }
    },

    async getSession() {
        try {
            const result = await supabase.auth.getSession()
            return result
        } catch (error) {
            return { 
                data: { session: null }, 
                error: error as AuthError 
            }
        }
    },

    async getCurrentUser() {
        try {
            const result = await supabase.auth.getUser()
            return result
        } catch (error) {
            return { 
                data: { user: null }, 
                error: error as AuthError 
            }
        }
    },

    async refreshSession() {
        try {
            const { data, error } = await supabase.auth.refreshSession()
            return { data, error }
        } catch (error) {
            return { 
                data: { session: null }, 
                error: error as AuthError 
            }
        }
    }
}
