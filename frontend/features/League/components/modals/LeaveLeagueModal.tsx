interface LeaveLeagueModalProps {
    leagueName: string;
    isLeaving: boolean;
    onConfirm: () => void;
    onCancel: () => void;
}

export const LeaveLeagueModal = ({
    leagueName,
    isLeaving,
    onConfirm,
    onCancel
}: LeaveLeagueModalProps) => {
    return (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            <div className="bg-gradient-to-br from-gray-800 to-gray-900 border border-gray-700 rounded-xl sm:rounded-2xl p-5 sm:p-6 lg:p-8 max-w-md w-full">
                <div className="text-center">
                    <div className="w-12 h-12 sm:w-16 sm:h-16 mx-auto mb-3 sm:mb-4 bg-red-600/20 rounded-full flex items-center justify-center">
                        <svg className="w-6 h-6 sm:w-8 sm:h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
                        </svg>
                    </div>
                    <h3 className="text-lg sm:text-xl font-bold text-white mb-3 sm:mb-4">
                        Leave League
                    </h3>
                    <p className="text-gray-300 text-sm sm:text-base mb-6 sm:mb-8 px-2">
                        Are you sure you want to leave <strong className="text-white">{leagueName}</strong>? 
                        This action cannot be undone and you&apos;ll need the join code to rejoin.
                    </p>
                    <div className="flex flex-col sm:flex-row gap-3 sm:gap-4">
                        <button
                            onClick={onCancel}
                            disabled={isLeaving}
                            className="flex-1 bg-gray-600 hover:bg-gray-700 disabled:bg-gray-800 text-white px-4 py-2.5 sm:py-3 text-sm sm:text-base rounded-lg font-medium transition-all duration-200"
                        >
                            Cancel
                        </button>
                        <button
                            onClick={onConfirm}
                            disabled={isLeaving}
                            className="flex-1 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 disabled:from-red-400 disabled:to-red-500 text-white px-4 py-2.5 sm:py-3 text-sm sm:text-base rounded-lg font-medium transition-all duration-200"
                        >
                            {isLeaving ? 'Leaving...' : 'Leave League'}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};
