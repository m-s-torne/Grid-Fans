import { http } from '@/core/services'

export interface CreateBackendUserRequest {
    user_name: string;
    email: string;
    supabase_user_id: string;
}

export interface BackendUserResponse {
    id: number;
    user_name: string;
    email: string;
    is_verified: boolean;
    created_at: string;
}

export interface CreateBackendUserTeam {
    user_id: number;
    league_id: number | null;
    team_name: string | null;
    driver_1_id: number;
    driver_2_id: number;
    driver_3_id: number;
    constructor_id: number | undefined;
}

export interface BackendUser {
    id: number;
    user_name: string;
    email: string;
    supabase_user_id: string;
    is_verified: boolean;
    created_at: string;
}

export const backendUserService = {
    async createUser(userData: CreateBackendUserRequest): Promise<BackendUserResponse> {
        const { data } = await http.post("/users/", userData)
        return data
    },

    async getUserBySupabaseId(supabaseUserId: string): Promise<BackendUser> {
        const { data } = await http.get(`/users/by-id/${supabaseUserId}`)
        return data
    },

    async createUserTeam(userTeam: CreateBackendUserTeam) {
        const { data } = await http.post("/user-team/", userTeam)
        return data
    }
}