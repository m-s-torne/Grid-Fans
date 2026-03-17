'use client'

import { useRouter, useParams } from 'next/navigation'
import { useLeagueDetail } from '@/features/League/hooks'
import { useCreateOrUpdateTeam, useUserTeam } from '@/lib/hooks/userTeams'
import { useEffect, useState } from 'react'
import type { Driver } from '@/features/Market/types/marketTypes'
import type { Team } from '@/lib/types'
import { useQuery } from '@tanstack/react-query'
import { f1DataService } from '@/lib/services'
import { useAuth } from '@/lib/contexts/AuthContext'

export const useTeamBuilder = () => {
    const { leagueId } = useParams<{ leagueId: string }>();
    const router = useRouter();
    const { isInitialized } = useAuth();
    
    const { league, isLoading: leagueLoading, error: leagueError } = useLeagueDetail(leagueId!);
    
    const { data: existingTeam, isLoading: teamLoading } = useUserTeam(parseInt(leagueId!));
    const createOrUpdateTeamMutation = useCreateOrUpdateTeam();
    
    const [selectedDrivers, setSelectedDrivers] = useState<Driver[]>([]);
    const [selectedConstructor, setSelectedConstructor] = useState<Team | null>(null);
    const [expandedDriver, setExpandedDriver] = useState<Driver | null>(null);
    const [searchFilter, setSearchFilter] = useState<string>('');
    const [teamName, setTeamName] = useState<string>('');
    
    const { data: drivers, isLoading: driversLoading } = useQuery({
        queryKey: ['drivers'],
        queryFn: f1DataService.getAllDrivers,
        enabled: isInitialized,
    });
    
    const { data: teams, isLoading: constructorsLoading } = useQuery({
        queryKey: ['teams'],
        queryFn: f1DataService.getAllTeams,
        enabled: isInitialized,
    });

    useEffect(() => {
        if (existingTeam && drivers && teams) {
            setTeamName(existingTeam.team_name);
            
            const driver1 = drivers.find((d: Driver) => d.id === existingTeam.driver_1_id);
            const driver2 = drivers.find((d: Driver) => d.id === existingTeam.driver_2_id);
            const driver3 = drivers.find((d: Driver) => d.id === existingTeam.driver_3_id);
            
            if (driver1 && driver2 && driver3) {
                setSelectedDrivers([driver1, driver2, driver3]);
            }
            
            const team = teams.find((t: Team) => t.id === existingTeam.constructor_id);
            if (team) {
                setSelectedConstructor(team);
            }
        }
    }, [existingTeam, drivers, teams]);

    const handleDriverSelect = (driver: Driver) => {
        if (selectedDrivers.find(d => d.id === driver.id)) {
            setSelectedDrivers(prev => prev.filter(d => d.id !== driver.id));
        } else if (selectedDrivers.length < 3) {
            setSelectedDrivers(prev => [...prev, driver]);
        }
    };

    const handleConstructorSelect = (team: Team) => {
        if (selectedConstructor?.id === team.id) {
            setSelectedConstructor(null);
        } else {
            setSelectedConstructor(team);
        }
    };

    const handleSaveTeam = async () => {
        if (!isTeamComplete) return;
        
        try {
            await createOrUpdateTeamMutation.mutateAsync({
                leagueId: parseInt(leagueId!),
                teamData: {
                    team_name: teamName,
                    driver_1_id: selectedDrivers[0].id,
                    driver_2_id: selectedDrivers[1].id,
                    driver_3_id: selectedDrivers[2].id,
                    constructor_id: selectedConstructor!.id
                }
            });
            
            router.push(`/leagues/${leagueId}`);
        } catch (error) {
            console.error('Error saving team:', error);
            alert('Failed to save team. Please try again.');
        }
    };

    const isTeamComplete = selectedDrivers.length === 3 && selectedConstructor !== null && teamName.length >= 4;

    const getButtonText = () => {
        const driversNeeded = 3 - selectedDrivers.length;
        const constructorNeeded = selectedConstructor ? 0 : 1;
        
        if (isTeamComplete) {
            return 'Save Team';
        }
        
        if (driversNeeded > 0 && constructorNeeded > 0) {
            return `Select ${driversNeeded} more driver(s) and ${constructorNeeded} constructor`;
        }
        
        if (driversNeeded > 0) {
            return `Select ${driversNeeded} more driver(s)`;
        }
        
        if (constructorNeeded > 0) {
            return 'Select a constructor';
        }

        if (teamName.trim().length === 0) {
            return 'Enter a team name to continue';
        }
        
        if (teamName.trim().length < 4) {
            return 'Team name must be at least 4 characters';
        }
        
        return 'Complete your team selection';
    };

    const filteredDrivers = drivers?.filter((driver: Driver) => {
        if (!searchFilter.trim()) return true;
        const searchTerm = searchFilter.toLowerCase();
        return (
            driver.full_name.toLowerCase().includes(searchTerm) ||
            driver.team_name?.toLowerCase().includes(searchTerm)
        );
    });

    const filteredTeams = teams?.filter((team: Team) => {
        if (!searchFilter.trim()) return true;
        const searchTerm = searchFilter.toLowerCase();
        return team.team_name.toLowerCase().includes(searchTerm);
    });

    const budgetBarWidth = Math.min((selectedDrivers.reduce((acc, driver) => acc + (driver.fantasy_stats?.price || 0), 0) / 1_000_000) / 100 * 100, 100);
    
    return {
        leagueLoading, driversLoading, 
        constructorsLoading, teamLoading,
        leagueError, league, router,
        leagueId, teamName, setTeamName,
        selectedDrivers, selectedConstructor,
        handleDriverSelect, handleConstructorSelect,
        budgetBarWidth, handleSaveTeam, isTeamComplete,
        getButtonText, searchFilter, setSearchFilter,
        filteredDrivers, setExpandedDriver, filteredTeams,
        expandedDriver
    }
}
