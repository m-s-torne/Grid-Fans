'use client';

import ReactCountryFlag from "react-country-flag"

interface DriverInfoProps {
    name: string;
    country:string;
    team:string;
    points:number;
    expanded?: boolean;
}

export const DriverInfo = ({ name, country, team, points, expanded = false }: DriverInfoProps) => {
    const nameParts = name.split(" ");
    const firstName = nameParts.slice(0, -1).join(" ");
    const lastName = nameParts[nameParts.length - 1];

    const isSmallLogo = ["Ferrari", "Mercedes", "Racing Bulls", "Williams", "Kick Sauber"]
        .includes(team);
    const logoSize = expanded 
        ? (isSmallLogo ? "max-w-[30px] sm:max-w-[40px] md:max-w-[5%]" : "max-w-[50px] sm:max-w-[60px] md:max-w-[10%]")
        : (isSmallLogo ? "md:max-w-[5%]" : "md:max-w-[10%]");
    const logoSrc = `/teams/${(team || "").replace(/\s+/g, "").toLowerCase()}.svg`;

    const isExpanded = expanded ? "md:min-w-[40px]" : "md:text-[35px]";
    
    return (
        <div className={`${expanded ? 'text-base sm:text-xl md:text-3xl' : 'md:text-3xl text-[170%]'} flex flex-col gap-2 sm:gap-3 text-white`}>
            <div className="flex gap-2 sm:gap-3 md:gap-5 items-center flex-wrap">
                <div className="flex flex-col gap-0.5 sm:gap-1 md:gap-3">
                    <span className="font-light text-gray-200">{firstName}</span>
                    <span className="font-bold text-white">{lastName}</span>
                </div>
                <span className="text-gray-400">
                    <ReactCountryFlag 
                        countryCode={country}
                        svg
                        className={`${isExpanded}`}
                    />
                </span>
                <span className="text-gray-400">|</span>
                <img
                    className={logoSize}
                    src={logoSrc} 
                    alt={team}
                />
                <span className="text-gray-400">|</span>
                <div className="text-[11px] sm:text-[13px] md:text-[15px] space-y-1 sm:space-y-2 text-gray-300">
                    <p className="text-gray-100">CHAMPIONSHIP</p>
                    <p className="font-bold text-white">{points} pts.</p>
                </div>
            </div>
        </div>
    )
}
