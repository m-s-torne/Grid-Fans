import { supabase } from '@/lib/supabase'
import type { PostgrestError } from '@supabase/supabase-js'

export interface CreateUserData {
    username: string;
    email: string;
    full_name?: string;
    avatar_url?: string;
}

export interface UpdateUserData {
    username?: string;
    full_name?: string;
    avatar_url?: string;
}

export interface UserService {
    createUserProfile(userData: CreateUserData): Promise<{
        data: any;
        error: PostgrestError | null;
    }>;
    getUserProfile(userId: string): Promise<{
        data: any;
        error: PostgrestError | null;
    }>;
    updateUserProfile(userId: string, userData: UpdateUserData): Promise<{
        data: any;
        error: PostgrestError | null;
    }>;
    getUserByUsername(username: string): Promise<{
        data: any;
        error: PostgrestError | null;
    }>;
}

export const userService: UserService = {
    async createUserProfile(userData: CreateUserData) {
        try {
            const { data, error } = await supabase
                .from('users')
                .insert([userData])
                .select()
                .single()

            return { data, error }
        } catch (error) {
            console.error('Error in userService.createUserProfile:', error)
            return { 
                data: null, 
                error: error as PostgrestError 
            }
        }
    },

    async getUserProfile(userId: string) {
        try {
            const { data, error } = await supabase
                .from('users')
                .select('*')
                .eq('id', userId)
                .single()

            return { data, error }
        } catch (error) {
            console.error('Error in userService.getUserProfile:', error)
            return { 
                data: null, 
                error: error as PostgrestError 
            }
        }
    },

    async updateUserProfile(userId: string, userData: UpdateUserData) {
        try {
            const { data, error } = await supabase
                .from('users')
                .update(userData)
                .eq('id', userId)
                .select()
                .single()

            return { data, error }
        } catch (error) {
            console.error('Error in userService.updateUserProfile:', error)
            return { 
                data: null, 
                error: error as PostgrestError 
            }
        }
    },

    async getUserByUsername(username: string) {
        try {
            const { data, error } = await supabase
                .from('users')
                .select('*')
                .eq('username', username)
                .single()

            return { data, error }
        } catch (error) {
            console.error('Error in userService.getUserByUsername:', error)
            return { 
                data: null, 
                error: error as PostgrestError 
            }
        }
    }
}
