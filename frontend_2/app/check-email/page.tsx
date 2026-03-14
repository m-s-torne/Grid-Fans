'use client';

import { motion } from 'motion/react';
import Link from 'next/link';
import { useAuth } from '@/lib/contexts/AuthContext';

export default function CheckEmailPage() {
    const { user } = useAuth();
    
    return (
        <div className="min-h-screen bg-linear-to-br from-gray-900 via-gray-800 to-black flex items-center justify-center p-4">
            <motion.div
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="w-full max-w-md"
            >
                <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 shadow-2xl border border-white/20">
                    <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
                        className="w-16 h-16 bg-linear-to-r from-red-600 to-red-700 rounded-full flex items-center justify-center mx-auto mb-6"
                    >
                        <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                        </svg>
                    </motion.div>
                    
                    <h1 className="text-2xl font-bold text-center text-white mb-4">
                        ¡Revisa tu correo!
                    </h1>
                    
                    <p className="text-gray-300 text-center mb-6">
                        {user?.email ? (
                            <>
                                Te hemos enviado un enlace de confirmación a <strong className="text-white">{user.email}</strong>.
                                <br />
                                Haz clic en el enlace para activar tu cuenta.
                            </>
                        ) : (
                            <>
                                Te hemos enviado un enlace de confirmación a tu correo electrónico.
                                <br />
                                Haz clic en el enlace para activar tu cuenta.
                            </>
                        )}
                    </p>
                    
                    <Link
                        href="/login"
                        className="w-full hover:scale-[1.05] active:scale-[0.95] bg-linear-to-r from-red-700 to-red-800 hover:from-red-800 hover:to-red-900 text-white font-semibold py-3 px-4 rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl block text-center"
                    >
                        Volver al login
                    </Link>
                    
                    <p className="text-sm text-gray-400 text-center mt-4">
                        ¿No recibiste el correo? Revisa tu carpeta de spam.
                    </p>
                </div>
            </motion.div>
        </div>
    );
}
