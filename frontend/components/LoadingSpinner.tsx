type LoadingSpinnerProps = {
    message?: string;
    className?: string;
}

export const LoadingSpinner = ({ 
    message = "Loading...", 
    className = "" 
}: LoadingSpinnerProps) => {
    return (
        <div className="text-center py-12">
            <div className={`animate-spin rounded-full h-16 w-16 border-b-2 border-red-500 mx-auto mb-4 ${className}`}></div>
            <p className="text-gray-400 text-lg">{message}</p>
        </div>
    );
};
