'use client';

import { useEmailConfirmation } from '@/lib/hooks/auth';
import { motion } from 'motion/react';
import { useRouter } from 'next/navigation';

export default function EmailConfirmationPage() {
    const router = useRouter();
    const {
        status,
        message,
        continueToApp,
    } = useEmailConfirmation();

    const getIcon = () => {
        switch (status) {
            case 'loading':
                return (
                    <div className="mb-6">
                        <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-red-700 border-solid mx-auto"></div>
                    </div>
                );
            case 'creating-profile':
                return (
                    <div className="mb-6">
                        <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-blue-500 border-solid mx-auto"></div>
                    </div>
                );
            case 'success':
                return <div className="text-green-500 text-6xl mb-6">&#x2705;</div>;
            case 'error':
                return <div className="text-red-500 text-6xl mb-6">&#x274C;</div>;
        }
    };

    const getTitle = () => {
        switch (status) {
            case 'loading':
                return 'Confirming your email...';
            case 'creating-profile':
                return 'Setting up your profile...';
            case 'success':
                return 'Welcome to Grid Fans!';
            case 'error':
                return 'Confirmation Failed';
        }
    };

    const getDescription = () => {
        switch (status) {
            case 'loading':
                return 'Please wait while we verify your email address.';
            case 'creating-profile':
                return 'We are setting up your account and preparing everything for you.';
            case 'success':
                return 'Your email has been confirmed and your account is ready!';
            case 'error':
                return 'Something went wrong during the confirmation process.';
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-900 px-4">
            <motion.div 
                className="text-center max-w-md"
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
            >
                {getIcon()}
                <h2 className="text-3xl font-bold text-white mb-4">{getTitle()}</h2>
                <p className="text-gray-300 mb-2">{getDescription()}</p>
                {message && (
                    <p className="text-gray-400 text-sm mb-6">{message}</p>
                )}
                
                {status === 'success' && (
                    <button
                        onClick={continueToApp}
                        className="hover:cursor-pointer w-full py-3 px-4 text-center font-medium text-white bg-red-700 hover:bg-red-800 rounded-md transition-colors duration-200"
                    >
                        Continue to Grid Fans
                    </button>
                )}
                
                {status === 'error' && (
                    <div className="space-y-4">
                        <button
                            onClick={() => router.push('/login')}
                            className="hover:cursor-pointer block w-full py-3 px-4 text-center font-medium text-white bg-red-700 hover:bg-red-800 rounded-md transition-colors duration-200"
                        >
                            Go to Login
                        </button>
                        <button
                            onClick={() => router.push('/register')}
                            className="hover:cursor-pointer block w-full py-3 px-4 text-center font-medium text-gray-400 hover:text-white transition-colors duration-200"
                        >
                            Register Again
                        </button>
                    </div>
                )}
            </motion.div>
        </div>
    );
}
