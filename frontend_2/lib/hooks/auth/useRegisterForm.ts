'use client'

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { mapAuthError } from "@/lib/utils/authErrors"
import { useAuth } from "@/lib/contexts/AuthContext"

export const useRegisterForm = () => {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')
    const [fullName, setFullName] = useState('')
    const [username, setUsername] = useState('')
    const [error, setError] = useState('')
    
    const { signUp, loading, signUpError } = useAuth()
    const router = useRouter()

    useEffect(() => {
        if (signUpError) {
            setError(mapAuthError(signUpError))
        }
    }, [signUpError])

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError('')

        if (password !== confirmPassword) {
            setError('Las contraseñas no coinciden')
            return
        }

        if (password.length < 6) {
            setError('La contraseña debe tener al menos 6 caracteres')
            return
        }

        try {
            await signUp(email, password, {
                full_name: fullName,
                username: username
            })
            
            router.push('/check-email')
        } catch (err: any) {
            setError(mapAuthError(err))
        }
    }

    return {
        handleSubmit,
        fullName, setFullName,
        username, setUsername,
        email, setEmail,
        password, setPassword,
        confirmPassword, 
        setConfirmPassword,
        error, loading,
    }
}
