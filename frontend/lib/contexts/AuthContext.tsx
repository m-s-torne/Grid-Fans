'use client'

import { createContext, useContext, useEffect, useState } from 'react'
import type { ReactNode } from 'react'
import { useAuth as useAuthHooks, authKeys } from '@/lib/hooks/auth'
import { supabase } from '@/lib/supabase'
import { useQueryClient } from '@tanstack/react-query'

type AuthContextType = {
    user: any | null
    session: any | null
    signUp: (email: string, password: string, userData?: any) => Promise<any>
    signIn: (email: string, password: string) => Promise<any>
    signInWithGoogle: () => Promise<any>
    signOut: () => Promise<void>
    loading: boolean
    isAuthenticated: boolean
    isSigningIn: boolean
    isSigningInWithGoogle: boolean
    isSigningUp: boolean
    isSigningOut: boolean
    signInError: any
    signInWithGoogleError: any
    signUpError: any
    signOutError: any
    isInitialized: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

interface AuthProviderProps {
    children: ReactNode
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
    const queryClient = useQueryClient()
    const auth = useAuthHooks()
    const [isInitialized, setIsInitialized] = useState(false)

    useEffect(() => {
        const checkInitialSession = async () => {
            try {
                await supabase.auth.getSession()
                setIsInitialized(true)
            } catch (error) {
                setIsInitialized(true)
            }
        }

        checkInitialSession()

        const { data: { subscription } } = supabase.auth.onAuthStateChange(
            async (event, session) => {
                if (!isInitialized) {
                    setIsInitialized(true)
                }
                
                if (event === 'SIGNED_IN' || event === 'TOKEN_REFRESHED') {
                    queryClient.setQueryData(authKeys.session(), {
                        data: { session },
                        error: null
                    })
                    if (session?.user) {
                        queryClient.setQueryData(authKeys.user(), {
                            data: { user: session.user },
                            error: null
                        })
                    }
                } else if (event === 'SIGNED_OUT') {
                    queryClient.removeQueries({ queryKey: authKeys.all })
                }
            }
        )

        return () => subscription.unsubscribe()
    }, [queryClient, isInitialized])

    const signUpWrapper = async (email: string, password: string, userData?: any) => {
        try {
            const result = await auth.signUp({ email, password, userData })
            return result
        } catch (error) {
            throw error
        }
    }

    const signInWrapper = async (email: string, password: string) => {
        try {
            const result = await auth.signIn({ email, password })
            return result
        } catch (error) {
            throw error
        }
    }

    const signInWithGoogleWrapper = async () => {
        try {
            const result = await auth.signInWithGoogle()
            return result
        } catch (error) {
            throw error
        }
    }

    const signOutWrapper = async () => {
        try {
            await auth.signOut()
        } catch (error) {
            throw error
        }
    }

    const value: AuthContextType = {
        user: auth.user,
        session: auth.session,
        signUp: signUpWrapper,
        signIn: signInWrapper,
        signInWithGoogle: signInWithGoogleWrapper,
        signOut: signOutWrapper,
        loading: auth.isLoading || auth.isSigningIn || auth.isSigningUp || auth.isSigningOut || auth.isSigningInWithGoogle,
        isAuthenticated: auth.isAuthenticated,
        isSigningIn: auth.isSigningIn,
        isSigningInWithGoogle: auth.isSigningInWithGoogle,
        isSigningUp: auth.isSigningUp,
        isSigningOut: auth.isSigningOut,
        signInError: auth.signInError,
        signInWithGoogleError: auth.signInWithGoogleError,
        signUpError: auth.signUpError,
        signOutError: auth.signOutError,
        isInitialized,
    }

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    )
}

export const useAuth = (): AuthContextType => {
    const context = useContext(AuthContext)
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider')
    }
    return context
}
