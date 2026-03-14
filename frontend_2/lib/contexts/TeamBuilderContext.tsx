'use client'

import React, { createContext, useContext } from 'react';
import type { ReactNode } from 'react';
import { useTeamBuilder } from '@/lib/hooks/userTeams';

type TeamBuilderContextType = ReturnType<typeof useTeamBuilder>;

const TeamBuilderContext = createContext<TeamBuilderContextType | undefined>(undefined);

interface TeamBuilderProviderProps {
    children: ReactNode;
}

export const TeamBuilderProvider: React.FC<TeamBuilderProviderProps> = ({ children }) => {
    const teamBuilderState = useTeamBuilder();

    return (
        <TeamBuilderContext.Provider value={teamBuilderState}>
            {children}
        </TeamBuilderContext.Provider>
    );
};

export const useTeamBuilderContext = (): TeamBuilderContextType => {
    const context = useContext(TeamBuilderContext);
    
    if (context === undefined) {
        throw new Error('useTeamBuilderContext must be used within a TeamBuilderProvider');
    }
    
    return context;
};

export { TeamBuilderContext };
