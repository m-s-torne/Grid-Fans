export const mapAuthError = (error: any): string => {
    if (!error?.message) {
        return 'Unexpected error'
    }

    const message = error.message.toLowerCase()

    if (message.includes('invalid login credentials')) {
        return 'Invalid email or password'
    }
    
    if (message.includes('email not confirmed')) {
        return 'Please confirm your email before signing in'
    }
    
    if (message.includes('too many requests')) {
        return 'Too many attempts. Please try again later'
    }
    
    if (message.includes('invalid email')) {
        return 'Invalid email address'
    }
    
    if (message.includes('user not found')) {
        return 'User not found'
    }

    if (message.includes('already registered')) {
        return 'This email is already registered'
    }
    
    if (message.includes('password should be')) {
        return 'Password does not meet requirements'
    }

    if (message.includes('session not found')) {
        return 'Session expired. Please sign in again'
    }

    return error.message
}
