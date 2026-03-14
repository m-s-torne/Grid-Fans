import { useState } from 'react';

export const useLeagueUI = () => {
    const [activeTab, setActiveTab] = useState<'lineup' | 'standings'>('lineup');
    const [showLeaveModal, setShowLeaveModal] = useState(false);
    
    return {
        activeTab,
        setActiveTab,
        showLeaveModal,
        setShowLeaveModal,
    };
};
