'use client';

import { motion } from 'motion/react'

type ExpandButtonProps = {
    onClick: () => void;
    className?: string;
    text?: string;
}

export const ExpandButton = ({ onClick, className = "", text="insights" }: ExpandButtonProps) => {
    return (
        <motion.button
            onClick={onClick}
            className={`
                text-lg bg-red-700 backdrop-blur-lg border-red-500 border-2
                p-2 rounded-xl hover:cursor-pointer hover:bg-red-800 shadow-lg
                ${className}
            `}
            whileHover={{ scale: 1.15 }}
            whileTap={{ scale: 0.95 }}
        >
            {text}
        </motion.button>
    );
};
