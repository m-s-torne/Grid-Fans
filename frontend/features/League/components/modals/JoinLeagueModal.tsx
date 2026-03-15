'use client';

import React from 'react';
import { useJoinLeagueForm } from '@/features/League/hooks';

interface JoinLeagueModalProps {
    isOpen: boolean;
    onClose: () => void;
}

export const JoinLeagueModal: React.FC<JoinLeagueModalProps> = ({ isOpen, onClose }) => {
    const {
        joinCode,
        isLoading,
        error,
        successMessage,
        handleSubmit,
        handleJoinCodeChange
    } = useJoinLeagueForm({ onClose });

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <div className="bg-gradient-to-br from-gray-800/90 to-gray-900/90 border border-gray-700/50 backdrop-blur-sm rounded-xl sm:rounded-2xl p-5 sm:p-6 lg:p-8 max-w-md w-full">
                <div className="flex items-center justify-between mb-4 sm:mb-6">
                    <h3 className="text-xl sm:text-2xl font-bold text-white">Join League</h3>
                    <button 
                        onClick={onClose}
                        className="text-gray-400 hover:text-white transition-colors flex-shrink-0"
                    >
                        <svg className="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                <div className="text-center mb-4 sm:mb-6">
                    <svg className="w-12 h-12 sm:w-16 sm:h-16 text-blue-500 mx-auto mb-3 sm:mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                    <p className="text-gray-300 text-xs sm:text-base px-2">Enter the league code provided by the league administrator to join.</p>
                </div>

                {error && (
                    <div className="bg-red-500/20 border border-red-500/30 rounded-lg p-3 mb-4">
                        <p className="text-red-300 text-xs sm:text-sm">{error}</p>
                    </div>
                )}

                {successMessage && (
                    <div className="bg-green-500/20 border border-green-500/30 rounded-lg p-3 mb-4">
                        <p className="text-green-300 text-xs sm:text-sm">{successMessage}</p>
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-4 sm:space-y-6">
                    <div>
                        <label htmlFor="joinCode" className="block text-xs sm:text-sm font-medium text-gray-300 mb-2">
                            League Code
                        </label>
                        <input
                            type="text"
                            id="joinCode"
                            value={joinCode}
                            onChange={(e) => handleJoinCodeChange(e.target.value)}
                            required
                            className="w-full px-3 sm:px-4 py-2 sm:py-3 bg-gray-700/50 border border-gray-600/50 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all text-center text-base sm:text-lg font-mono tracking-wider"
                            placeholder="ENTER-CODE"
                            maxLength={10}
                        />
                        <p className="text-xs text-gray-500 mt-2 text-center">
                            League codes are typically 6-10 characters long
                        </p>
                    </div>

                    <div className="flex space-x-2 sm:space-x-3">
                        <button
                            type="button"
                            onClick={onClose}
                            className="flex-1 py-2 sm:py-3 px-3 sm:px-4 text-sm sm:text-base bg-gray-600/50 hover:bg-gray-600/70 text-white rounded-lg font-medium transition-all duration-200"
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            disabled={isLoading || !joinCode.trim()}
                            className="flex-1 py-2 sm:py-3 px-3 sm:px-4 text-sm sm:text-base bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 disabled:from-gray-600 disabled:to-gray-700 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-all duration-200 flex items-center justify-center"
                        >
                            {isLoading ? (
                                <>
                                    <div className="animate-spin rounded-full h-3 w-3 sm:h-4 sm:w-4 border-b-2 border-white mr-2"></div>
                                    <span className="hidden sm:inline">Joining...</span>
                                    <span className="sm:hidden">...</span>
                                </>
                            ) : (
                                <>
                                    <span className="hidden sm:inline">Join League</span>
                                    <span className="sm:hidden">Join</span>
                                </>
                            )}
                        </button>
                    </div>
                </form>

                <div className="mt-4 sm:mt-6 pt-4 sm:pt-6 border-t border-gray-700/50">
                    <p className="text-center text-gray-400 text-xs sm:text-sm px-2">
                        Don&apos;t have a league code?{' '}
                        <button 
                            onClick={() => {
                                onClose();
                            }}
                            className="text-blue-400 hover:text-blue-300 transition-colors"
                        >
                            Create your own league
                        </button>
                    </p>
                </div>
            </div>
        </div>
    );
};
