import { http } from '@/core/services'

export interface League {
    id: number
    name: string
    description: string | null
    admin_user_id: number
    is_active: boolean
    join_code: string
    current_participants: number
    created_at: string
}

export interface CreateLeagueRequest {
    name: string
    description?: string
}

export interface JoinLeagueRequest {
    join_code: string
}

export interface LeagueParticipant {
    user_id: number
    user_name: string
    email: string
    is_admin: boolean
    joined_at: string
}

export interface LeagueParticipantsResponse {
    league_id: number
    league_name: string
    participants: LeagueParticipant[]
    total_participants: number
}

export interface JoinLeagueResponse {
    message: string
    league_id: number
    team_initialized?: boolean
    team_details?: {
        team_id: number
        assigned_drivers: number[]
        constructor_id: number
        total_cost: number
        budget_remaining: number
        error?: string
    }
}

export interface LeagueServiceType {
    createLeague(leagueData: CreateLeagueRequest, adminUserId: string): Promise<League>
    getUserLeagues(userId: string): Promise<League[]>
    getLeagueById(leagueId: number, userId: string): Promise<League>
    joinLeague(joinData: JoinLeagueRequest, userId: string): Promise<JoinLeagueResponse>
    leaveLeague(leagueId: number, userId: string): Promise<{ message: string; league_id: number }>
    getLeagueParticipants(leagueId: number): Promise<LeagueParticipantsResponse>
}

export const leagueService: LeagueServiceType = {
    async createLeague(leagueData: CreateLeagueRequest, adminUserId: string): Promise<League> {
        const { data } = await http.post(`/leagues/?admin_user_id=${adminUserId}`, leagueData)
        return data
    },

    async getUserLeagues(userId: string): Promise<League[]> {
        const { data } = await http.get(`/leagues/user/${userId}`)
        return data
    },

    async getLeagueById(leagueId: number, userId: string): Promise<League> {
        const { data } = await http.get(`/leagues/${leagueId}?user_id=${userId}`)
        return data
    },

    async joinLeague(joinData: JoinLeagueRequest, userId: string): Promise<JoinLeagueResponse> {
        const { data } = await http.post(`/leagues/join/?user_id=${userId}`, joinData)
        return data
    },

    async leaveLeague(leagueId: number, userId: string): Promise<{ message: string; league_id: number }> {
        const { data } = await http.delete(`/leagues/${leagueId}/leave?user_id=${userId}`)
        return data
    },

    async getLeagueParticipants(leagueId: number): Promise<LeagueParticipantsResponse> {
        const { data } = await http.get(`/leagues/${leagueId}/participants`)
        return data
    }
}