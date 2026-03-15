'use client';

import React from 'react';
import { useCreateLeagueForm } from '@/features/League/hooks';

interface CreateLeagueModalProps {
    isOpen: boolean;
    onClose: () => void;
}

export const CreateLeagueModal: React.FC<CreateLeagueModalProps> = ({ isOpen, onClose }) => {
    const {
        formData,
        isLoading,
        error,
        handleSubmit,
        handleInputChange
    } = useCreateLeagueForm({ onClose });

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <div className="bg-gradient-to-br from-gray-800/90 to-gray-900/90 border border-gray-700/50 backdrop-blur-sm rounded-xl sm:rounded-2xl p-5 sm:p-6 lg:p-8 max-w-md w-full">
                <div className="flex items-center justify-between mb-4 sm:mb-6">
                    <h3 className="text-xl sm:text-2xl font-bold text-white">Create New League</h3>
                    <button 
                        onClick={onClose}
                        className="text-gray-400 hover:text-white transition-colors flex-shrink-0"
                    >
                        <svg className="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                {error && (
                    <div className="bg-red-500/20 border border-red-500/30 rounded-lg p-3 mb-4">
                        <p className="text-red-300 text-xs sm:text-sm">{error}</p>
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-3 sm:space-y-4">
                    <div>
                        <label htmlFor="name" className="block text-xs sm:text-sm font-medium text-gray-300 mb-2">
                            League Name *
                        </label>
                        <input
                            type="text"
                            id="name"
                            name="name"
                            value={formData.name}
                            onChange={handleInputChange}
                            required
                            className="w-full px-3 sm:px-4 py-2 sm:py-3 text-sm sm:text-base bg-gray-700/50 border border-gray-600/50 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500/50 focus:border-red-500/50 transition-all"
                            placeholder="Enter league name"
                        />
                    </div>

                    <div>
                        <label htmlFor="description" className="block text-xs sm:text-sm font-medium text-gray-300 mb-2">
                            Description
                        </label>
                        <textarea
                            id="description"
                            name="description"
                            value={formData.description}
                            onChange={handleInputChange}
                            rows={3}
                            className="w-full px-3 sm:px-4 py-2 sm:py-3 text-sm sm:text-base bg-gray-700/50 border border-gray-600/50 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500/50 focus:border-red-500/50 transition-all resize-none"
                            placeholder="Optional description for your league"
                        />
                    </div>

                    <div className="flex space-x-2 sm:space-x-3 pt-2 sm:pt-4">
                        <button
                            type="button"
                            onClick={onClose}
                            className="flex-1 py-2 sm:py-3 px-3 sm:px-4 text-sm sm:text-base bg-gray-600/50 hover:bg-gray-600/70 text-white rounded-lg font-medium transition-all duration-200"
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            disabled={isLoading || !formData.name.trim()}
                            className="flex-1 py-2 sm:py-3 px-3 sm:px-4 text-sm sm:text-base bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 disabled:from-gray-600 disabled:to-gray-700 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-all duration-200 flex items-center justify-center"
                        >
                            {isLoading ? (
                                <>
                                    <div className="animate-spin rounded-full h-3 w-3 sm:h-4 sm:w-4 border-b-2 border-white mr-2"></div>
                                    <span className="hidden sm:inline">Creating...</span>
                                    <span className="sm:hidden">...</span>
                                </>
                            ) : (
                                <>
                                    <span className="hidden sm:inline">Create League</span>
                                    <span className="sm:hidden">Create</span>
                                </>
                            )}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};
