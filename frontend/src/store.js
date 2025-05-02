import create from 'zustand';

const useStore = create((set) => ({
    // Search state
    searchQuery: '',
    setSearchQuery: (query) => set({ searchQuery: query }),

    // Properties state
    properties: [],
    setProperties: (properties) => set({ properties }),

    // Workflow state
    workflowStep: 0,
    setWorkflowStep: (step) => set({ workflowStep: step }),

    // Loading state
    isLoading: false,
    setIsLoading: (loading) => set({ isLoading: loading }),

    // UI state
    showConfetti: false,
    setShowConfetti: (show) => set({ showConfetti: show }),

    // Theme state
    themeMode: 'dark',
    toggleTheme: () => set((state) => ({
        themeMode: state.themeMode === 'dark' ? 'light' : 'dark',
    })),

    // Animation state
    animationSpeed: 1,
    setAnimationSpeed: (speed) => set({ animationSpeed: speed }),
}));

export default useStore; 