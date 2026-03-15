'use client'

import type { ColDef, ICellRendererParams } from 'ag-grid-community'
import type { AgGridReact } from 'ag-grid-react'
import { useRef, useState, useMemo } from 'react'
import { formatCurrencyPrecise } from '@/features/Market/utils/currencyFormat'

export interface MyTeamsRow {
    team_name: string;
    league_name: string;
    drivers: string;
    constructor: string;
    total_points: number;
    budget_remaining: number;
    created_at: string;
}

export const useMyTeamsTable = () => {
    const gridRef = useRef<AgGridReact>(null);
    const [rowData, setRowData] = useState<MyTeamsRow[] | null>(null);

    const colDefs = useMemo<ColDef<MyTeamsRow>[]>(() => [
        {
            field: 'team_name',
            headerName: 'Team Name',
            flex: 1.5,
            headerComponent: () => (
                <div className="flex items-center h-full">
                    <p className="font-bold text-[170%]">Team Name</p>
                </div>
            ),
            cellRenderer: (params: ICellRendererParams) => (
                <div className="flex items-center h-full p-2">
                    <div className="bg-white/5 backdrop-blur-sm px-3 py-2 rounded-lg border border-white/10">
                        <span className="font-bold text-white text-[13px]">{params.value}</span>
                    </div>
                </div>
            ),
            filter: true,
            floatingFilter: true,
            sortable: true,
        },
        {
            field: 'league_name',
            headerName: 'League',
            flex: 1,
            headerComponent: () => (
                <div className="flex items-center h-full">
                    <p className="font-bold text-[170%]">League</p>
                </div>
            ),
            cellRenderer: (params: ICellRendererParams) => (
                <div className="flex items-center h-full p-2">
                    <div className="bg-white/5 backdrop-blur-sm px-3 py-2 rounded-lg border border-white/10">
                        <span className="text-blue-300 font-semibold">{params.value}</span>
                    </div>
                </div>
            ),
            filter: true,
            floatingFilter: true,
            sortable: true,
        },
        {
            field: 'drivers',
            headerName: 'Drivers',
            flex: 2.5,
            headerComponent: () => (
                <div className="flex items-center h-full">
                    <p className="font-bold text-[170%]">Drivers</p>
                </div>
            ),
            cellRenderer: (params: ICellRendererParams) => (
                <div className="flex items-center h-full p-2">
                    <span className="text-white">{params.value}</span>
                </div>
            ),
            filter: true,
            floatingFilter: true,
            sortable: false,
        },
        {
            field: 'constructor',
            headerName: 'Constructor',
            flex: 1.2,
            headerComponent: () => (
                <div className="flex items-center h-full">
                    <p className="font-bold text-[170%]">Constructor</p>
                </div>
            ),
            cellRenderer: (params: ICellRendererParams) => (
                <div className="flex items-center h-full p-2">
                    <div className="bg-white/5 backdrop-blur-sm px-3 py-2 rounded-lg border border-white/10">
                        <span className="text-orange-300 font-semibold">{params.value}</span>
                    </div>
                </div>
            ),
            filter: true,
            floatingFilter: true,
            sortable: true,
        },
        {
            field: 'total_points',
            headerName: 'Points',
            flex: 0.8,
            headerComponent: () => (
                <div className="flex items-center h-full">
                    <p className="font-bold text-[170%]">Points</p>
                </div>
            ),
            cellRenderer: (params: ICellRendererParams) => (
                <div className="flex items-center justify-center h-full p-2">
                    <div className="bg-white/5 backdrop-blur-sm px-3 py-2 rounded-lg border border-white/10 text-center">
                        <span className="font-bold text-yellow-400 text-lg">{params.value.toLocaleString()}</span>
                    </div>
                </div>
            ),
            filter: 'agNumberColumnFilter',
            floatingFilter: true,
            sortable: true,
        },
        {
            field: 'budget_remaining',
            headerName: 'Budget',
            flex: 1,
            headerComponent: () => (
                <div className="flex items-center h-full">
                    <p className="font-bold text-[170%]">Budget</p>
                </div>
            ),
            cellRenderer: (params: ICellRendererParams) => (
                <div className="flex items-center justify-center h-full p-2">
                    <div className="bg-white/5 backdrop-blur-sm px-3 py-2 rounded-lg border border-white/10 text-center">
                        <span className="text-green-400 font-bold text-lg">
                            {formatCurrencyPrecise(params.value)}
                        </span>
                    </div>
                </div>
            ),
            filter: 'agNumberColumnFilter',
            floatingFilter: true,
            sortable: true,
        },
        {
            field: 'created_at',
            headerName: 'Created',
            flex: 1,
            headerComponent: () => (
                <div className="flex items-center h-full">
                    <p className="font-bold text-[170%]">Created</p>
                </div>
            ),
            cellRenderer: (params: ICellRendererParams) => (
                <div className="flex items-center h-full p-2">
                    <span className="text-gray-400">
                        {new Date(params.value).toLocaleDateString()}
                    </span>
                </div>
            ),
            filter: 'agDateColumnFilter',
            floatingFilter: true,
            sortable: true,
        },
    ], []);

    return {
        gridRef,
        rowData,
        setRowData,
        colDefs,
    };
};
