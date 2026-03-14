interface EmptyStateProps {
    title: string;
    description: string;
    className?: string;
}

export const EmptyState = ({ 
    title, 
    description,
    className = ""
}: EmptyStateProps) => {
    return (
        <div className={`flex flex-col items-center justify-center w-full py-16 ${className}`}>
            <h3 className="text-white text-xl font-bold mb-2">{title}</h3>
            <p className="text-gray-300 text-center">
                {description}
            </p>
        </div>
    );
};
