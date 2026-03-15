import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useLeagues } from '@/lib/contexts/LeaguesContext';
import { formatCurrencyPrecise } from '@/lib/utils';

interface UseJoinLeagueFormProps {
    onClose: () => void;
}

export const useJoinLeagueForm = ({ onClose }: UseJoinLeagueFormProps) => {
    const { joinLeague } = useLeagues();
    const router = useRouter();
    
    const [joinCode, setJoinCode] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [successMessage, setSuccessMessage] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setError(null);
        setSuccessMessage(null);

        try {
            const result = await joinLeague({ join_code: joinCode.trim() });
            
            if (result.team_initialized) {
                const budget = result.team_details?.budget_remaining 
                    ? formatCurrencyPrecise(result.team_details.budget_remaining)
                    : '$100M';
                setSuccessMessage(`Welcome! Your starter team has been created with 3 free drivers. Full budget available: ${budget}`);
            } else {
                setSuccessMessage('Successfully joined league!');
            }
            
            setTimeout(() => {
                onClose();
                setJoinCode('');
                setSuccessMessage(null);
                router.push(`/leagues/${result.league_id}`);
            }, 2000);
        } catch (err: unknown) {
            const message = err instanceof Error ? err.message : 'Failed to join league';
            setError(message);
        } finally {
            setIsLoading(false);
        }
    };

    const handleJoinCodeChange = (value: string) => {
        setJoinCode(value.toUpperCase());
    };

    return {
        joinCode,
        isLoading,
        error,
        successMessage,
        handleSubmit,
        handleJoinCodeChange
    };
};
