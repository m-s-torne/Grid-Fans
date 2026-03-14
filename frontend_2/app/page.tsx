'use client';

import { motion } from 'motion/react';
import Link from 'next/link';
import { RandomTeamLogo } from '@/components';

export default function Home() {
    return (
        <main className="h-screen bg-linear-to-br from-gray-900 via-gray-800 to-gray-900 relative overflow-hidden">
            {/* Background decorative elements */}
            <div className="absolute inset-0 bg-linear-to-br from-amber-600/5 to-red-600/5" />
            <div className="absolute top-0 left-0 w-full h-full">
                <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-amber-500/10 rounded-full blur-3xl" />
                <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-red-500/10 rounded-full blur-3xl" />
            </div>

            <motion.div
                className="relative z-10 h-full flex flex-col"
                initial={{ opacity: 0, y: 100 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -100 }}
                transition={{ duration: 1, ease: "easeOut" }}
            >
                {/* Header Section - Compact top */}
                <div className="flex-none pt-8 pb-4 px-6">
                    <motion.div 
                        className="text-center max-w-4xl mx-auto"
                        initial={{ opacity: 0, y: 50 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 1, delay: 0.3 }}
                    >
                        <h1 className="font-black text-3xl md:text-5xl lg:text-6xl text-transparent bg-clip-text bg-linear-to-r from-amber-400 via-red-500 to-amber-400 mb-3 tracking-tight">
                            WELCOME TO
                        </h1>
                        <h1 className="font-black text-2xl md:text-4xl lg:text-5xl text-white mb-4 tracking-wide">
                            GRIDFANS CLUB
                        </h1>
                        <p className="text-gray-300 text-base md:text-lg max-w-2xl mx-auto leading-relaxed">
                            Join the ultimate Formula 1 fantasy experience and compete with fans worldwide
                        </p>
                    </motion.div>
                </div>

                {/* Team Logo Section */}
                <div className="flex-1 flex items-center justify-center px-6 min-h-0">
                    <motion.div 
                        className="w-full max-w-2xl mx-auto h-full max-h-80"
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ duration: 1.2, delay: 0.6 }}
                    >
                        <div className="relative w-full h-full rounded-3xl overflow-hidden flex items-center justify-center">
                            <RandomTeamLogo />

                            <div className="absolute -top-6 -left-6 w-4 h-4 bg-amber-500/40 rounded-full blur-sm animate-pulse" />
                            <div className="absolute -top-4 -right-8 w-3 h-3 bg-red-500/40 rounded-full blur-sm animate-pulse" style={{ animationDelay: '0.5s' }} />
                            <div className="absolute -bottom-6 -left-4 w-5 h-5 bg-amber-500/30 rounded-full blur-sm animate-pulse" style={{ animationDelay: '1s' }} />
                            <div className="absolute -bottom-8 -right-6 w-4 h-4 bg-red-500/35 rounded-full blur-sm animate-pulse" style={{ animationDelay: '1.5s' }} />
                        </div>
                    </motion.div>
                </div>

                {/* CTA Section */}
                <div className="flex-none pb-8 px-6">
                    <motion.div 
                        className="text-center max-w-xl mx-auto"
                        initial={{ opacity: 0, y: 50 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 1, delay: 1 }}
                    >
                        <div className="relative inline-block">
                            <div className="absolute inset-0 bg-linear-to-r from-amber-600/20 to-red-600/20 rounded-2xl blur-xl scale-110" />
                            
                            <div className="relative bg-black/30 backdrop-blur-sm border border-white/20 rounded-2xl p-6">
                                <h2 className="text-xl md:text-2xl font-bold text-white mb-3">
                                    READY TO RACE?
                                </h2>
                                <p className="text-gray-300 mb-4 text-base leading-relaxed">
                                    Create leagues, pick your drivers, and dominate the championship
                                </p>
                                
                                <Link href="/leagues" className="inline-block group">
                                    <div className="relative transform transition-all duration-300 group-hover:scale-105">
                                        <div className="absolute -inset-1 bg-linear-to-r from-amber-600 to-red-600 rounded-xl blur opacity-75 group-hover:opacity-100 transition-all duration-300" />
                                        
                                        <div className="relative bg-linear-to-r from-amber-600 to-red-600 rounded-xl p-0.5">
                                            <div className="bg-gray-900/90 backdrop-blur-sm rounded-xl px-6 py-3 group-hover:bg-gray-900/80 transition-all duration-300">
                                                <span className="flex items-center font-bold text-base text-white">
                                                    COMPETE
                                                    <svg className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                                                    </svg>
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                </Link>
                            </div>
                        </div>
                    </motion.div>
                </div>
            </motion.div>
        </main>
    );
}
