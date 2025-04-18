export interface WorkoutData {
  distance: number; // in meters
  duration: number; // in seconds
  split: number; // pace per 500m in seconds
  heartRate?: number; // optional heart rate
  timestamp: number;
}

export interface Tower {
  id: string;
  type: TowerType;
  level: number;
  position: {
    x: number;
    y: number;
  };
  upgradeRequirements: WorkoutRequirement;
}

export enum TowerType {
  SPEED_TOWER = 'SPEED_TOWER',
  ENDURANCE_TOWER = 'ENDURANCE_TOWER',
  CONSISTENCY_TOWER = 'CONSISTENCY_TOWER',
}

export interface WorkoutRequirement {
  type: 'DISTANCE' | 'TIME' | 'SPLIT' | 'HEART_RATE';
  value: number;
  comparison: 'GREATER_THAN' | 'LESS_THAN' | 'EQUAL_TO';
}

export interface UserProgress {
  totalDistance: number;
  totalWorkouts: number;
  lastWorkoutDate: number;
  towers: Tower[];
  resources: {
    gold: number;
    gems: number;
  };
} 