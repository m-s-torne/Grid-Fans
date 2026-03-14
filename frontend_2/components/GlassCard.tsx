'use client';

import { motion } from 'motion/react'
import type { ReactNode } from 'react'

interface GlassCardProps {
    children: ReactNode;
    color: string;
    className?: string;
    motionKey?: string | number;
    initial?: any;
    animate?: any;
    exit?: any;
    transition?: any;
}

export const GlassCard = ({ 
    children, 
    color, 
    className = "", 
    motionKey, 
    initial, 
    animate, 
    exit, 
    transition 
}: GlassCardProps) => {
    const baseStyles = {
        backgroundColor: `${color}60`,
        borderColor: `${color}60`,
        backdropFilter: 'blur(12px)',
        WebkitBackdropFilter: 'blur(12px)'
    };

    const motionProps = {
        ...(initial && { initial }),
        ...(animate && { animate }),
        ...(exit && { exit }),
        ...(transition && { transition })
    };

    return (
        <motion.div
            className={`
                flex items-center relative md:min-h-[60vh]
                min-h-[55vh] min-w-[50vw] md:min-w-[20vw]
                overflow-hidden rounded-4xl border backdrop-blur-sm p-2
                ${className}
            `}
            key={motionKey}
            style={baseStyles}
            {...motionProps}
        >
            {children}
        </motion.div>
    )
}
