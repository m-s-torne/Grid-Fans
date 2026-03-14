interface LoadingErrorProps {
    error?: string;
    errorMessage?: string;
}

export const LoadingError = ({ error="Loading error", errorMessage="There has been an error" }: LoadingErrorProps) => {
    return (
        <div className="text-center py-12">
            <svg className="w-16 h-16 text-red-500 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p className="text-red-400 text-lg">{error}</p>
            <p className="text-gray-500 mt-2">{errorMessage}</p>
        </div>
    )
}
