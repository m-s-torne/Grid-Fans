'use client';

import { useState, useEffect } from 'react';

export type EventType = 'practice' | 'qualifying' | 'race' | 'sprint' | 'shootout';
export type EventModalMode = 'create' | 'edit' | 'view';

export interface CalendarEvent {
  id: string;
  title: string;
  start: Date;
  end: Date;
  resource?: {
    description?: string;
    type?: EventType;
    color?: string;
  };
}

interface EventModalProps {
  isOpen: boolean;
  mode: EventModalMode;
  event?: CalendarEvent | null;
  onClose: () => void;
  onCreate: (eventData: Omit<CalendarEvent, 'id'>) => void;
  onUpdate: (id: string, eventData: Partial<CalendarEvent>) => void;
  onDelete: (id: string) => void;
  onEdit: () => void;
}

export const EventModal = ({ 
  isOpen, mode, 
  event, onClose, 
  onCreate, onUpdate, 
  onDelete, onEdit
}: EventModalProps) => {
  const [formData, setFormData] = useState({
    title: '',
    start: new Date(),
    end: new Date(),
    description: '',
    type: 'practice' as EventType,
    color: '#3174ad'
  });

  useEffect(() => {
    if (event) {
      setFormData({
        title: event.title || '',
        start: event.start || new Date(),
        end: event.end || new Date(),
        description: event.resource?.description || '',
        type: event.resource?.type || 'practice',
        color: event.resource?.color || '#3174ad'
      });
    }
  }, [event]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const eventData = {
      title: formData.title,
      start: formData.start,
      end: formData.end,
      resource: {
        description: formData.description,
        type: formData.type,
        color: formData.color
      }
    };

    if (mode === 'edit' && event) {
      onUpdate(event.id, eventData);
    } else {
      onCreate(eventData);
    }
  };

  const handleDelete = () => {
    if (event && confirm('Are you sure you want to delete this event?')) {
      onDelete(event.id);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-black/30 backdrop-blur-sm border border-white/20 rounded-2xl p-6 w-full max-w-md shadow-2xl">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold text-white">
            {mode === 'create' && 'Create Event'}
            {mode === 'edit' && 'Edit Event'}
            {mode === 'view' && event?.title}
          </h2>
          <button 
            onClick={onClose} 
            className="text-gray-400 hover:text-white transition-colors text-2xl"
          >
            ✕
          </button>
        </div>

        {mode === 'view' ? (
          <div className="space-y-4 text-white">
            <div className="bg-white/10 rounded-lg p-4 border border-white/20">
              <p className="text-gray-300"><strong className="text-white">Start:</strong> {event?.start.toLocaleString()}</p>
            </div>
            <div className="bg-white/10 rounded-lg p-4 border border-white/20">
              <p className="text-gray-300"><strong className="text-white">End:</strong> {event?.end.toLocaleString()}</p>
            </div>
            {event?.resource?.description && (
              <div className="bg-white/10 rounded-lg p-4 border border-white/20">
                <p className="text-gray-300"><strong className="text-white">Description:</strong> {event.resource.description}</p>
              </div>
            )}
            {event?.resource?.type && (
              <div className="bg-white/10 rounded-lg p-4 border border-white/20">
                <p className="text-gray-300"><strong className="text-white">Type:</strong> {event.resource.type}</p>
              </div>
            )}
            <div className="flex gap-3 mt-6">
              <button
                onClick={onEdit}
                className="flex-1 px-4 py-3 bg-blue-600/80 backdrop-blur-sm text-white rounded-xl hover:bg-blue-700/80 transition-all duration-300 border border-blue-500/30 shadow-lg"
              >
                Edit
              </button>
              <button
                onClick={handleDelete}
                className="flex-1 px-4 py-3 bg-red-600/80 backdrop-blur-sm text-white rounded-xl hover:bg-red-700/80 transition-all duration-300 border border-red-500/30 shadow-lg"
              >
                Delete
              </button>
            </div>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-sm font-medium mb-2 text-white">Title</label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => setFormData({...formData, title: e.target.value})}
                className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-transparent backdrop-blur-sm"
                placeholder="Event title"
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2 text-white">Beginning</label>
                <input
                  type="datetime-local"
                  value={formData.start.toISOString().slice(0, 16)}
                  onChange={(e) => setFormData({
                    ...formData, 
                    start: new Date(e.target.value)
                  })}
                  className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-transparent backdrop-blur-sm"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2 text-white">Ending</label>
                <input
                  type="datetime-local"
                  value={formData.end.toISOString().slice(0, 16)}
                  onChange={(e) => setFormData({
                    ...formData, 
                    end: new Date(e.target.value)
                  })}
                  className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-transparent backdrop-blur-sm"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2 text-white">Description</label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({...formData, description: e.target.value})}
                rows={3}
                className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-transparent backdrop-blur-sm resize-none"
                placeholder="Describe the event (optional)"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2 text-white">Type</label>
              <select
                value={formData.type}
                onChange={(e) => setFormData({
                  ...formData, 
                  type: e.target.value as EventType
                })}
                className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-transparent backdrop-blur-sm"
              >
                <option value="practice" className="bg-gray-800">Free Practice</option>
                <option value="qualifying" className="bg-gray-800">Qualifying</option>
                <option value="race" className="bg-gray-800">Race</option>
                <option value="sprint" className="bg-gray-800">Sprint Race</option>
                <option value="shootout" className="bg-gray-800">Sprint Quali</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2 text-white">Color</label>
              <input
                type="color"
                value={formData.color}
                onChange={(e) => setFormData({...formData, color: e.target.value})}
                className="w-full h-12 bg-white/10 border border-white/20 rounded-xl cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500/50"
              />
            </div>

            <div className="flex gap-3 pt-4">
              <button
                type="submit"
                className="flex-1 px-4 py-3 bg-blue-600/80 backdrop-blur-sm text-white rounded-xl hover:bg-blue-700/80 transition-all duration-300 border border-blue-500/30 shadow-lg"
              >
                {mode === 'edit' ? 'Update' : 'Create'}
              </button>
              <button
                type="button"
                onClick={onClose}
                className="flex-1 px-4 py-3 bg-gray-600/80 backdrop-blur-sm text-white rounded-xl hover:bg-gray-700/80 transition-all duration-300 border border-gray-500/30 shadow-lg"
              >
                Cancel
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};
