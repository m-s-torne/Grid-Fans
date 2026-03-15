'use client'

import { supabase } from "@/lib/supabase"
import { useAuth } from "@/lib/contexts/AuthContext"
import { backendUserService } from "@/lib/services"
import { useEffect, useState } from "react"
import { useRouter, useSearchParams } from "next/navigation"

export const useEmailConfirmation = () => {
    const [status, setStatus] = useState<'loading' | 'creating-profile' | 'success' | 'error' | 'duplicate error'>('loading')
    const [message, setMessage] = useState('Confirming your email...')
    const router = useRouter()
    const searchParams = useSearchParams()
    const { isAuthenticated, user, isInitialized } = useAuth()

    const [urlParams] = useState(() => {
        const currentSearch = typeof window !== 'undefined' ? window.location.search : ''
        const currentHash = typeof window !== 'undefined' ? window.location.hash : ''
        
        const queryParams = new URLSearchParams(currentSearch)
        const hashParams = new URLSearchParams(currentHash.substring(1))
        
        const params = {
            token: queryParams.get('token') || hashParams.get('token'),
            token_hash: queryParams.get('token_hash') || hashParams.get('token_hash'),
            type: queryParams.get('type') || hashParams.get('type'),
            access_token: queryParams.get('access_token') || hashParams.get('access_token'),
            refresh_token: queryParams.get('refresh_token') || hashParams.get('refresh_token'),
            error_code: queryParams.get('error_code') || hashParams.get('error_code'),
            error_description: queryParams.get('error_description') || hashParams.get('error_description')
        }

        return params
    })

    const createBackendUser = async () => {
        try {
            const { data: { user }, error } = await supabase.auth.getUser()
            
            if (error || !user) {
                return false
            }

            const userData = {
                user_name: user.user_metadata?.username || user.email?.split('@')[0] || 'user',
                email: user.email!,
                supabase_user_id: user.id
            }

            await backendUserService.createUser(userData)
            
            return true
        } catch (error: unknown) {
            const axiosError = error as { response?: { status?: number; data?: { detail?: string } } }
            
            if (axiosError?.response?.status === 400) {
                const errorMessage = axiosError.response?.data?.detail || ''
                if (errorMessage.includes('already registered')) {
                    return true
                }
            }
            
            console.error('Error creating user in FastAPI:', error)
            return false
        }
    }

    useEffect(() => {
        const handleEmailConfirmation = async () => {
            try {
                if (!isInitialized) {
                    return
                }

                await new Promise(resolve => setTimeout(resolve, 300))
                
                const token = urlParams.token
                const tokenHash = urlParams.token_hash
                const type = urlParams.type
                const access_token = urlParams.access_token
                const refresh_token = urlParams.refresh_token
                const error_code = urlParams.error_code
                const error_description = urlParams.error_description

                if (isAuthenticated && user && !token && !tokenHash && !access_token && !error_code) {
                    setStatus('success')
                    setMessage('You are already logged in!')
                    return
                }

                if (error_code || error_description) {
                    setStatus('error')
                    setMessage(error_description || `Error code: ${error_code}`)
                    return
                }

                if (access_token && refresh_token) {
                    const { error } = await supabase.auth.setSession({
                        access_token,
                        refresh_token
                    })
                    
                    if (error) {
                        setStatus('error')
                        setMessage(error.message)
                    } else {
                        setStatus('creating-profile')
                        setMessage('Email confirmed! Setting up your profile...')
                        
                        const profileCreated = await createBackendUser()
                        
                        if (profileCreated) {
                            setTimeout(() => {
                                router.replace('/leagues')
                            }, 1000)
                            return
                        } else {
                            setTimeout(() => {
                                router.replace('/leagues')
                            }, 1000)
                            return
                        }
                    }
                } 
                else if (tokenHash && type) {
                    const { error } = await supabase.auth.verifyOtp({
                        token_hash: tokenHash,
                        type: type as any
                    })

                    if (error) {
                        setStatus('error')
                        setMessage(`OTP verification failed: ${error.message}`)
                    } else {
                        setStatus('creating-profile')
                        setMessage('Email confirmed! Setting up your profile...')
                        
                        const profileCreated = await createBackendUser()
                        
                        if (profileCreated) {
                            setStatus('success')
                            setMessage('Welcome! Your profile is ready. Click continue to start picking your drivers!')
                        } else {
                            setStatus('success')
                            setMessage('Email confirmed! You can now access your account.')
                        }
                    }
                }
                else if (token && type) {
                    const { error } = await supabase.auth.verifyOtp({
                        token_hash: token,
                        type: type as any
                    })

                    if (error) {
                        setStatus('error')
                        setMessage(`Legacy token verification failed: ${error.message}`)
                    } else {
                        setStatus('creating-profile')
                        setMessage('Email confirmed successfully! Setting up your profile...')
                        
                        const profileCreated = await createBackendUser()
                        
                        if (profileCreated) {
                            setStatus('success')
                            setMessage('Welcome! Your profile is ready. Click continue to start picking your drivers!')
                        } else {
                            setStatus('success')
                            setMessage('Email confirmed! You can now access your account.')
                        }
                    }
                }
                else if (isAuthenticated && user) {
                    setStatus('creating-profile')
                    setMessage('Setting up your profile...')
                    
                    const profileCreated = await createBackendUser()
                    
                    if (profileCreated) {
                        setStatus('success')
                        setMessage('Welcome! Your profile is ready. Click continue to start picking your drivers!')
                    } else {
                        setStatus('success')
                        setMessage('Welcome back! You can now access your account.')
                    }
                }
                else {
                    setStatus('error')
                    setMessage(`Invalid confirmation link - No valid parameters found.`)
                }
            } catch (error) {
                setStatus('error')
                setMessage(`An error occurred during confirmation: ${error}`)
            }
        }

        handleEmailConfirmation()
    }, [searchParams, router, isAuthenticated, user, isInitialized])

    const continueToApp = async () => {
        try {
            const { data: { user } } = await supabase.auth.getUser()
            if (user) {
                router.push('/leagues')
            } else {
                router.push('/')
            }
        } catch (error) {
            router.push('/')
        }
    }

    return {
        status,
        message,
        continueToApp,
    }
}
