import type { Driver } from '@/lib/types/marketTypes'
import type { Team } from '@/lib/types'

export type F1DataService = {
    getAllDrivers(): Promise<Driver[]>,
    getAllTeams(): Promise<Team[]>
}
