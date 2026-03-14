export type Team = {
    id: number;
    team_name: string;
    team_color: string;
    team_url: string;
    season_results: {
        points: number;
        driver_count: number;
    }
}
