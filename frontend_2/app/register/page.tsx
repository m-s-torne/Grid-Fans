'use client';

import Link from 'next/link';
import { motion } from 'motion/react';
import { RegisterForm } from '@/features/Auth/components';

export default function RegisterPage() {
    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
            <motion.div 
                className="max-w-md w-full space-y-8"
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
            >
                <div>
                    <h2 className="mt-6 text-center text-3xl font-extrabold text-white">
                        Create your account
                    </h2>
                    <p className="mt-2 text-center text-sm text-gray-400">
                        Or{' '}
                        <Link
                            href="/login"
                            className="font-medium text-red-700 hover:text-red-600"
                        >
                            sign in to your existing account
                        </Link>
                    </p>
                </div>
                <RegisterForm />
            </motion.div>
        </div>
    );
}
