'use client'

import { useQuery } from '@tanstack/react-query'
import { useCurrentUser } from '../auth/useAuth'
import { backendUserService } from '@/lib/services'

export const useBackendUser = () => {
    const { data } = useCurrentUser()
    const supabaseUser = data?.user

    return useQuery({
        queryKey: ['backend-user', supabaseUser?.id],
        queryFn: () => backendUserService.getUserBySupabaseId(supabaseUser?.id || ''),
        enabled: !!supabaseUser?.id,
        select: (data) => data
    })
}
