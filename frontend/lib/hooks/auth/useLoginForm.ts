'use client'

import { useAuth } from "@/lib/contexts/AuthContext"
import { mapAuthError } from "@/lib/utils/authErrors"
import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"

export const useLoginForm = () => {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')
    
    const { 
        signIn, 
        signInWithGoogle, 
        loading, 
        isSigningInWithGoogle,
        signInError, 
        signInWithGoogleError 
    } = useAuth()
    const router = useRouter()

    useEffect(() => {
        if (signInError) {
            setError(mapAuthError(signInError))
        } else if (signInWithGoogleError) {
            setError(mapAuthError(signInWithGoogleError))
        }
    }, [signInError, signInWithGoogleError])

    useEffect(() => {
        if (error) {
            setError('')
        }
    }, [email, password])

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError('')

        try {
            await signIn(email, password)
            router.push('/leagues')
        } catch (err: any) {
            setError(mapAuthError(err))
        }
    }

    const handleGoogleSignIn = async () => {
        setError('')
        try {
            await signInWithGoogle()
        } catch (err: any) {
            setError(mapAuthError(err))
        }
    }

    return {
        handleSubmit,
        email,
        setEmail,
        password,
        setPassword,
        error,
        loading,
        isSigningInWithGoogle,
        handleGoogleSignIn,
    }
}
