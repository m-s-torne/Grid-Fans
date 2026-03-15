'use client'

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { authService } from '@/lib/services'

export const authKeys = {
    all: ['auth'] as const,
    session: () => [...authKeys.all, 'session'] as const,
    user: () => [...authKeys.all, 'user'] as const,
}

export const useSession = () => {
    return useQuery({
        queryKey: authKeys.session(),
        queryFn: authService.getSession,
        staleTime: 5 * 60 * 1000,
        gcTime: 10 * 60 * 1000,
        retry: 1,
        select: (data) => ({
            session: data.data.session,
            error: data.error
        })
    })
}

export const useCurrentUser = () => {
    return useQuery({
        queryKey: authKeys.user(),
        queryFn: authService.getCurrentUser,
        staleTime: 5 * 60 * 1000,
        gcTime: 10 * 60 * 1000,
        retry: 1,
        select: (data) => ({
            user: data.data.user,
            error: data.error
        })
    })
}

export const useSignUp = () => {
    const queryClient = useQueryClient()
    
    return useMutation({
        mutationFn: async ({ email, password, userData }: {
            email: string;
            password: string;
            userData?: any;
        }) => {
            const result = await authService.signUp(email, password, userData)
            
            if (result.error) {
                throw result.error
            }
            
            return result
        },
        onSuccess: (data) => {
            if (data.data && !data.error) {
                queryClient.invalidateQueries({ queryKey: authKeys.all })
            }
        },
        onError: (error) => {
            console.error('Sign up mutation error:', error)
        }
    })
}

export const useSignIn = () => {
    const queryClient = useQueryClient()
    
    return useMutation({
        mutationFn: async ({ email, password }: {
            email: string;
            password: string;
        }) => {
            const result = await authService.signIn(email, password)
            
            if (result.error) {
                throw result.error
            }
            
            return result
        },
        onSuccess: (data) => {
            if (data.data && !data.error) {
                queryClient.invalidateQueries({ queryKey: authKeys.all })
                queryClient.refetchQueries({ queryKey: authKeys.session() })
                queryClient.refetchQueries({ queryKey: authKeys.user() })
            }
        },
        onError: (error) => {
            console.error('Sign in mutation error:', error)
        }
    })
}

export const useSignInWithGoogle = () => {
    const queryClient = useQueryClient()
    
    return useMutation({
        mutationFn: async () => {
            const result = await authService.signInWithGoogle()
            
            if (result.error) {
                throw result.error
            }
            
            return result
        },
        onSuccess: (data) => {
            if (data.data && !data.error) {
                queryClient.invalidateQueries({ queryKey: authKeys.all })
                queryClient.refetchQueries({ queryKey: authKeys.session() })
                queryClient.refetchQueries({ queryKey: authKeys.user() })
            }
        },
        onError: (error) => {
            console.error('Google sign in mutation error:', error)
        }
    })
}

export const useSignOut = () => {
    const queryClient = useQueryClient()
    
    return useMutation({
        mutationFn: authService.signOut,
        onSuccess: (data) => {
            if (!data.error) {
                queryClient.removeQueries({ queryKey: authKeys.all })
                queryClient.clear()
            }
        },
        onError: (error) => {
            console.error('Sign out error:', error)
        }
    })
}

export const useRefreshSession = () => {
    const queryClient = useQueryClient()
    
    return useMutation({
        mutationFn: authService.refreshSession,
        onSuccess: (data) => {
            if (data.data.session && !data.error) {
                queryClient.setQueryData(authKeys.session(), data)
                queryClient.invalidateQueries({ queryKey: authKeys.user() })
            }
        },
        onError: (error) => {
            console.error('Refresh session error:', error)
        }
    })
}

export const useAuth = () => {
    const sessionQuery = useSession()
    const userQuery = useCurrentUser()
    const signInMutation = useSignIn()
    const signUpMutation = useSignUp()
    const signInWithGoogleMutation = useSignInWithGoogle()
    const signOutMutation = useSignOut()
    const refreshMutation = useRefreshSession()

    return {
        session: sessionQuery.data?.session || null,
        user: userQuery.data?.user || null,
        
        isLoading: sessionQuery.isLoading || userQuery.isLoading,
        loading: signInMutation.isPending || signInWithGoogleMutation.isPending,
        isSigningIn: signInMutation.isPending,
        isSigningInWithGoogle: signInWithGoogleMutation.isPending,
        isSigningUp: signUpMutation.isPending,
        isSigningOut: signOutMutation.isPending,
        
        sessionError: sessionQuery.data?.error || null,
        userError: userQuery.data?.error || null,
        signInError: signInMutation.error,
        signInWithGoogleError: signInWithGoogleMutation.error,
        signUpError: signUpMutation.error,
        signOutError: signOutMutation.error,
        
        signIn: signInMutation.mutateAsync,
        signInWithGoogle: signInWithGoogleMutation.mutateAsync,
        signUp: signUpMutation.mutateAsync,
        signOut: signOutMutation.mutateAsync,
        refreshSession: refreshMutation.mutateAsync,
        
        isAuthenticated: !!sessionQuery.data?.session && !!userQuery.data?.user,
        
        refetchSession: sessionQuery.refetch,
        refetchUser: userQuery.refetch,
    }
}
