'use client';

import { useMediaQuery } from "react-responsive";

interface DriverImageProps {
    url: string;
    name: string;
    color: string;
    expanded?: boolean;
}

export const DriverImage = ({ url, name, color, expanded=false }: DriverImageProps) => {
    const isDesktop = useMediaQuery({ minWidth: 768 });
    const maskSize = expanded ? "100% 35%" : isDesktop ? "100% 48%" : "100% 41%";
    const width = expanded ? "w-[100px] sm:w-[120px] md:w-[130px]" : "md:w-[17vw]"
    
    return (
        <img
            className={`${width} w-[35vw]`}
            src={`${url}`}
            alt={`${name} headshot`}
            style={{
                WebkitMaskImage: `linear-gradient(to bottom, ${color} 60%, transparent 83%)`,
                WebkitMaskRepeat: "no-repeat",
                WebkitMaskSize: `${maskSize}`,
                maskImage: `linear-gradient(to bottom, ${color} 60%, transparent 80%)`,
                maskRepeat: "no-repeat",
                maskSize: `${maskSize}`,
            }}
        />
    )
}
