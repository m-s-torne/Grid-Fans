'use client';

import { useState, useEffect } from 'react';
import { motion } from 'motion/react';

const teamLogos = [
  'alpine.svg',
  'astonmartin.svg',
  'ferrari.svg',
  'haasf1team.svg',
  'kicksauber.svg',
  'mclaren.svg',
  'mercedes.svg',
  'racingbulls.svg',
  'redbullracing.svg',
  'williams.svg'
];

export const RandomTeamLogo = () => {
  const [selectedLogo, setSelectedLogo] = useState<string>('');

  useEffect(() => {
    const randomIndex = Math.floor(Math.random() * teamLogos.length);
    setSelectedLogo(teamLogos[randomIndex]);
  }, []);

  if (!selectedLogo) return null;

  return (
    <motion.div
      className="w-full h-full flex items-center justify-center p-12 md:p-14"
      initial={{ opacity: 0, scale: 0.8, rotate: -10 }}
      animate={{ opacity: 1, scale: 1, rotate: 0 }}
      transition={{ duration: 1.2, delay: 0.6, ease: "easeOut" }}
    >
      <motion.img
        src={`/teams/${selectedLogo}`}
        alt="F1 Team Logo"
        className="w-full h-full object-contain drop-shadow-2xl"
        initial={{ y: 20 }}
        animate={{ y: 0 }}
        transition={{
          duration: 2,
          repeat: Infinity,
          repeatType: "reverse",
          ease: "easeInOut"
        }}
      />
    </motion.div>
  );
};
