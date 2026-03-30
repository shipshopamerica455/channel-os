import React, {
  createContext,
  useContext,
  useReducer,
  useEffect,
  ReactNode,
} from 'react';
import { AppState, AppAction, ChannelId } from '../types';

const STORAGE_KEY = 'channel-os-state';

const defaultState: AppState = {
  selectedChannel: 'genius-junkie',
  apiKey: '',
  analytics: {
    'genius-junkie': null,
    'shipshop-tv': null,
    'ultra-health': null,
  },
  healthSummaries: {
    'genius-junkie': null,
    'shipshop-tv': null,
    'ultra-health': null,
  },
  ideas: [],
  contentPlan: [],
  notes: [],
};

function reducer(state: AppState, action: AppAction): AppState {
  switch (action.type) {
    case 'SET_CHANNEL':
      return { ...state, selectedChannel: action.payload };

    case 'SET_API_KEY':
      return { ...state, apiKey: action.payload };

    case 'SET_ANALYTICS':
      return {
        ...state,
        analytics: {
          ...state.analytics,
          [action.payload.channelId]: action.payload,
        },
      };

    case 'SET_HEALTH_SUMMARY':
      return {
        ...state,
        healthSummaries: {
          ...state.healthSummaries,
          [action.payload.channelId]: action.payload,
        },
      };

    case 'ADD_IDEA':
      return { ...state, ideas: [action.payload, ...state.ideas] };

    case 'ADD_IDEAS':
      return { ...state, ideas: [...action.payload, ...state.ideas] };

    case 'UPDATE_IDEA':
      return {
        ...state,
        ideas: state.ideas.map((i) =>
          i.id === action.payload.id ? action.payload : i
        ),
      };

    case 'REMOVE_IDEA':
      return { ...state, ideas: state.ideas.filter((i) => i.id !== action.payload) };

    case 'ADD_PLAN_ITEM':
      return { ...state, contentPlan: [...state.contentPlan, action.payload] };

    case 'UPDATE_PLAN_ITEM':
      return {
        ...state,
        contentPlan: state.contentPlan.map((p) =>
          p.id === action.payload.id ? action.payload : p
        ),
      };

    case 'REMOVE_PLAN_ITEM':
      return {
        ...state,
        contentPlan: state.contentPlan.filter((p) => p.id !== action.payload),
      };

    case 'ADD_NOTE':
      return { ...state, notes: [action.payload, ...state.notes] };

    case 'REMOVE_NOTE':
      return { ...state, notes: state.notes.filter((n) => n.id !== action.payload) };

    case 'LOAD_STATE':
      return { ...state, ...action.payload };

    default:
      return state;
  }
}

interface AppContextValue {
  state: AppState;
  dispatch: React.Dispatch<AppAction>;
}

const AppContext = createContext<AppContextValue | null>(null);

export function AppProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(reducer, defaultState);

  // Load persisted state on mount
  useEffect(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const saved = JSON.parse(raw) as Partial<AppState>;
        // Merge saved analytics/summaries/ideas/plan/notes but reset nulls
        dispatch({ type: 'LOAD_STATE', payload: saved });
      }
    } catch {
      // ignore corrupt storage
    }
  }, []);

  // Persist state on every change (debounced)
  useEffect(() => {
    const id = setTimeout(() => {
      try {
        // Never persist the api key to storage for security
        const { apiKey: _key, ...rest } = state;
        localStorage.setItem(STORAGE_KEY, JSON.stringify(rest));
      } catch {
        // ignore quota errors
      }
    }, 300);
    return () => clearTimeout(id);
  }, [state]);

  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
}

export function useAppState() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error('useAppState must be used within AppProvider');
  return ctx.state;
}

export function useAppDispatch() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error('useAppDispatch must be used within AppProvider');
  return ctx.dispatch;
}

export function useChannel() {
  const { state } = useContext(AppContext)!;
  return state.selectedChannel as ChannelId;
}
