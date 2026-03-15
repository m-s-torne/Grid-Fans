import { useState } from 'react';

export const useLeagueModals = () => {
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showJoinModal, setShowJoinModal] = useState(false);

  const openCreateModal = () => setShowCreateModal(true);
  const closeCreateModal = () => setShowCreateModal(false);
  
  const openJoinModal = () => setShowJoinModal(true);
  const closeJoinModal = () => setShowJoinModal(false);

  return {
    showCreateModal,
    showJoinModal,
    openCreateModal,
    closeCreateModal,
    openJoinModal,
    closeJoinModal,
  };
};
