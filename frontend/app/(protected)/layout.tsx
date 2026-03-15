'use client';

import Link from 'next/link';
import Image from 'next/image';
import { useAuth } from '@/lib/contexts/AuthContext';
import { CustomButton } from '@/components';
import { usePathname } from 'next/navigation';
import { useState } from 'react';
import logo from '@/app/favicon.svg'

export default function ProtectedLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const { user, signOut } = useAuth();
    const pathname = usePathname();
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

    const isActiveRoute = (path: string) => {
        return pathname === path;
    };

    const leaguesActive = isActiveRoute('/leagues') ? 'text-red-500' : '';
    const teamsActive = isActiveRoute('/my-teams') ? 'text-red-500' : '';
    const calendarActive = isActiveRoute('/calendar') ? 'text-red-500' : '';

    const handleLogout = async () => {
        try {
            await signOut();
        } catch (error) {
            console.error('Error signing out:', error);
        }
    };

    const closeMobileMenu = () => {
        setIsMobileMenuOpen(false);
    };

    return (
        <>
            <header className="py-4 px-4 sm:py-5 sm:px-6 lg:px-10 flex justify-between items-center text-white relative z-50">
                <span className="hover:scale-110 transition-all ease-in-out duration-300 hover:cursor-pointer active:scale-90 z-50">
                    <Link href="/">
                        <Image 
                            className="max-w-20 sm:max-w-25"
                            src={logo}
                            alt="page_logo"
                            width={100}
                            height={40}
                        />
                    </Link>
                </span>

                {/* Desktop Navigation */}
                <nav className="hidden lg:flex items-center text-[90%] gap-6 xl:gap-10">
                    <ul className="flex gap-6 xl:gap-10">
                        <Link className={`
                            hover:text-red-600 active:backdrop-opacity-5 
                            transition-all ease-in-out
                            ${leaguesActive}
                            `
                        } href="/leagues">
                            <h2>Leagues</h2>
                        </Link>
                    </ul>
                    <div className="flex text-[80%] items-center gap-4 ml-6 pl-6 border-l border-gray-600">
                        <span className="text-sm text-gray-300 hidden xl:inline">
                            {user?.user_metadata?.username || user?.user_metadata?.full_name?.split(" ")[0] || user?.email}
                        </span>
                        <CustomButton
                            onClick={handleLogout}
                        >
                            Logout
                        </CustomButton>
                    </div>
                </nav>

                {/* Mobile Hamburger Button */}
                <button
                    onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                    className="lg:hidden z-50 p-2 text-white hover:text-red-500 transition-colors"
                    aria-label="Toggle menu"
                >
                    {isMobileMenuOpen ? (
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    ) : (
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                        </svg>
                    )}
                </button>
            </header>

            {/* Mobile Menu Overlay */}
            {isMobileMenuOpen && (
                <div 
                    className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 lg:hidden"
                    onClick={closeMobileMenu}
                />
            )}

            {/* Mobile Slide-out Menu */}
            <div className={`
                fixed top-0 right-0 h-full w-64 sm:w-80 bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 
                border-l border-gray-700 shadow-2xl z-40 lg:hidden
                transform transition-transform duration-300 ease-in-out
                ${isMobileMenuOpen ? 'translate-x-0' : 'translate-x-full'}
            `}>
                <div className="flex flex-col h-full pt-20 px-6">
                    {/* User Info */}
                    <div className="pb-6 mb-6 border-b border-gray-700">
                        <p className="text-sm text-gray-400 mb-1">Logged in as</p>
                        <p className="text-white font-semibold truncate">
                            {user?.user_metadata?.username || user?.user_metadata?.full_name || user?.email}
                        </p>
                    </div>

                    {/* Navigation Links */}
                    <nav className="flex-1">
                        <ul className="space-y-4">
                            <li>
                                <Link 
                                    className={`
                                        block py-3 px-4 rounded-lg text-lg font-medium
                                        transition-all duration-200
                                        ${leaguesActive 
                                            ? 'bg-red-600 text-white' 
                                            : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                                        }
                                    `}
                                    href="/leagues"
                                    onClick={closeMobileMenu}
                                >
                                    <div className="flex items-center">
                                        <svg className="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                                        </svg>
                                        Leagues
                                    </div>
                                </Link>
                            </li>
                            <li>
                                <Link 
                                    className={`
                                        block py-3 px-4 rounded-lg text-lg font-medium
                                        transition-all duration-200
                                        ${teamsActive 
                                            ? 'bg-red-600 text-white' 
                                            : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                                        }
                                    `}
                                    href="/my-teams"
                                    onClick={closeMobileMenu}
                                >
                                    <div className="flex items-center">
                                        <svg className="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                                        </svg>
                                        Teams
                                    </div>
                                </Link>
                            </li>
                            <li>
                                <Link 
                                    className={`
                                        block py-3 px-4 rounded-lg text-lg font-medium
                                        transition-all duration-200
                                        ${calendarActive 
                                            ? 'bg-red-600 text-white' 
                                            : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                                        }
                                    `}
                                    href="/calendar"
                                    onClick={closeMobileMenu}
                                >
                                    <div className="flex items-center">
                                        <svg className="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                        </svg>
                                        Calendar
                                    </div>
                                </Link>
                            </li>
                        </ul>
                    </nav>

                    {/* Logout Button */}
                    <div className="pt-6 pb-8 border-t border-gray-700">
                        <div className="w-full">
                            <CustomButton
                                onClick={() => {
                                    handleLogout();
                                    closeMobileMenu();
                                }}
                            >
                                <div className="flex items-center justify-center">
                                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                                    </svg>
                                    Logout
                                </div>
                            </CustomButton>
                        </div>
                    </div>
                </div>
            </div>

            {children}
        </>
    );
}
