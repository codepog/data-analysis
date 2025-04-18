import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { WorkoutData, UserProgress } from '../types';

interface WorkoutState {
  currentWorkout: WorkoutData | null;
  isWorkoutActive: boolean;
  userProgress: UserProgress;
  lastWorkoutDate: number | null;
}

const initialState: WorkoutState = {
  currentWorkout: null,
  isWorkoutActive: false,
  userProgress: {
    totalDistance: 0,
    totalWorkouts: 0,
    lastWorkoutDate: 0,
    towers: [],
    resources: {
      gold: 1000,
      gems: 100,
    },
  },
  lastWorkoutDate: null,
};

const workoutSlice = createSlice({
  name: 'workout',
  initialState,
  reducers: {
    startWorkout: (state) => {
      state.isWorkoutActive = true;
      state.currentWorkout = {
        distance: 0,
        duration: 0,
        split: 0,
        timestamp: Date.now(),
      };
    },
    updateWorkoutData: (state, action: PayloadAction<Partial<WorkoutData>>) => {
      if (state.currentWorkout) {
        state.currentWorkout = { ...state.currentWorkout, ...action.payload };
      }
    },
    endWorkout: (state) => {
      if (state.currentWorkout) {
        state.userProgress.totalDistance += state.currentWorkout.distance;
        state.userProgress.totalWorkouts += 1;
        state.userProgress.lastWorkoutDate = Date.now();
        state.lastWorkoutDate = Date.now();
        
        // Award resources based on workout performance
        const goldEarned = Math.floor(state.currentWorkout.distance / 100); // 1 gold per 100m
        const gemsEarned = Math.floor(state.currentWorkout.distance / 1000); // 1 gem per 1000m
        
        state.userProgress.resources.gold += goldEarned;
        state.userProgress.resources.gems += gemsEarned;
      }
      state.isWorkoutActive = false;
      state.currentWorkout = null;
    },
    addTower: (state, action: PayloadAction<{ tower: any }>) => {
      state.userProgress.towers.push(action.payload.tower);
    },
    upgradeTower: (state, action: PayloadAction<{ towerId: string }>) => {
      const tower = state.userProgress.towers.find(t => t.id === action.payload.towerId);
      if (tower) {
        tower.level += 1;
      }
    },
  },
});

export const { startWorkout, updateWorkoutData, endWorkout, addTower, upgradeTower } = workoutSlice.actions;
export default workoutSlice.reducer; 