'use client';

import { useState } from 'react';

interface LeagueHeaderProps {
    name: string;
    description?: string | null;
    joinCode: string;
    currentParticipants: number;
    activeTab: 'lineup' | 'standings';
    onTabChange: (tab: 'lineup' | 'standings') => void;
}

export const LeagueHeader = ({
    name,
    description,
    joinCode,
    currentParticipants,
    activeTab,
    onTabChange
}: LeagueHeaderProps) => {
    const [copied, setCopied] = useState(false);

    const handleCopyJoinCode = async () => {
        try {
            await navigator.clipboard.writeText(joinCode);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        } catch (err) {
            console.error('Failed to copy: ', err);
        }
    };

    return (
        <div className="bg-gradient-to-br from-gray-800/40 to-gray-900/40 border border-gray-700/50 backdrop-blur-sm rounded-xl sm:rounded-2xl p-4 sm:p-6 lg:p-8 mb-6 sm:mb-8">
            <div className="flex flex-col lg:flex-row lg:justify-between lg:items-start gap-4 sm:gap-6 mb-4 sm:mb-6">
                <div className="flex-1 min-w-0">
                    <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-white mb-2 sm:mb-4 break-words">
                        {name}
                    </h1>
                    {description && (
                        <p className="text-gray-300 text-sm sm:text-base lg:text-lg break-words">
                            {description}
                        </p>
                    )}
                </div>
                <div className="flex flex-wrap items-center gap-2 sm:gap-3 lg:gap-4">
                    <div 
                        onClick={handleCopyJoinCode}
                        className="bg-blue-600/20 text-blue-300 px-3 sm:px-4 py-1.5 sm:py-2 rounded-full text-xs sm:text-sm font-medium border border-blue-500/30 cursor-pointer hover:bg-blue-600/30 transition-all duration-200 flex items-center gap-2"
                    >
                        <span className="font-mono">{joinCode}</span>
                        {copied ? (
                            <svg className="w-3 h-3 sm:w-4 sm:h-4 text-green-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                            </svg>
                        ) : (
                            <svg className="w-3 h-3 sm:w-4 sm:h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                            </svg>
                        )}
                    </div>
                    <div className="bg-purple-600/20 text-purple-300 px-3 sm:px-4 py-1.5 sm:py-2 rounded-full text-xs sm:text-sm font-medium border border-purple-500/30 whitespace-nowrap">
                        {currentParticipants || 0} members
                    </div>
                </div>
            </div>

            {/* Tabs */}
            <div className="flex gap-1 sm:gap-2 border-b border-gray-700/50 mt-4 sm:mt-6 overflow-hidden">
                <button
                    onClick={() => onTabChange('lineup')}
                    className={`flex-1 sm:flex-none sm:px-6 py-2 sm:py-3 text-[11px] sm:text-base font-medium transition-all duration-200 border-b-2 whitespace-nowrap ${
                        activeTab === 'lineup'
                            ? 'border-blue-500 text-blue-400'
                            : 'border-transparent text-gray-400 hover:text-gray-300'
                    }`}
                >
                    Lineup
                </button>
                <button
                    onClick={() => onTabChange('standings')}
                    className={`flex-1 sm:flex-none sm:px-6 py-2 sm:py-3 text-[11px] sm:text-base font-medium transition-all duration-200 border-b-2 whitespace-nowrap ${
                        activeTab === 'standings'
                            ? 'border-blue-500 text-blue-400'
                            : 'border-transparent text-gray-400 hover:text-gray-300'
                    }`}
                >
                    Standings
                </button>
            </div>
        </div>
    );
};
