import React, { useState } from 'react';
import { View, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { Text, Button, Card } from 'react-native-paper';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../store';
import { addTower, upgradeTower } from '../store/workoutSlice';
import { Tower, TowerType, WorkoutRequirement } from '../types';

const TOWER_TYPES = [
  {
    type: TowerType.SPEED_TOWER,
    name: 'Speed Tower',
    description: 'Upgrade by achieving fast splits',
    requirement: {
      type: 'SPLIT',
      value: 120, // 2:00 split
      comparison: 'LESS_THAN',
    } as WorkoutRequirement,
    cost: 500,
  },
  {
    type: TowerType.ENDURANCE_TOWER,
    name: 'Endurance Tower',
    description: 'Upgrade by rowing long distances',
    requirement: {
      type: 'DISTANCE',
      value: 5000, // 5km
      comparison: 'GREATER_THAN',
    } as WorkoutRequirement,
    cost: 1000,
  },
  {
    type: TowerType.CONSISTENCY_TOWER,
    name: 'Consistency Tower',
    description: 'Upgrade by maintaining steady pace',
    requirement: {
      type: 'SPLIT',
      value: 10, // 10 second variance
      comparison: 'LESS_THAN',
    } as WorkoutRequirement,
    cost: 750,
  },
];

export const BaseBuilderScreen: React.FC = () => {
  const dispatch = useDispatch();
  const { userProgress } = useSelector((state: RootState) => state.workout);
  const [selectedTowerType, setSelectedTowerType] = useState<TowerType | null>(null);

  const handlePlaceTower = (type: TowerType) => {
    const towerConfig = TOWER_TYPES.find(t => t.type === type);
    if (!towerConfig) return;

    if (userProgress.resources.gold < towerConfig.cost) {
      // Show insufficient funds message
      return;
    }

    const newTower: Tower = {
      id: Date.now().toString(),
      type,
      level: 1,
      position: { x: 0, y: 0 }, // This would be determined by touch position in a real implementation
      upgradeRequirements: towerConfig.requirement,
    };

    dispatch(addTower({ tower: newTower }));
  };

  const handleUpgradeTower = (towerId: string) => {
    dispatch(upgradeTower({ towerId }));
  };

  const renderTowerCard = (tower: Tower) => {
    const towerConfig = TOWER_TYPES.find(t => t.type === tower.type);
    if (!towerConfig) return null;

    return (
      <Card key={tower.id} style={styles.towerCard}>
        <Card.Content>
          <Text style={styles.towerName}>{towerConfig.name}</Text>
          <Text>Level: {tower.level}</Text>
          <Text style={styles.requirementText}>
            Next Upgrade: {towerConfig.description}
          </Text>
        </Card.Content>
        <Card.Actions>
          <Button onPress={() => handleUpgradeTower(tower.id)}>
            Upgrade
          </Button>
        </Card.Actions>
      </Card>
    );
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Base Builder</Text>
        <View style={styles.resources}>
          <Text>Gold: {userProgress.resources.gold}</Text>
          <Text>Gems: {userProgress.resources.gems}</Text>
        </View>
      </View>

      <ScrollView style={styles.towerList}>
        {TOWER_TYPES.map(towerType => (
          <TouchableOpacity
            key={towerType.type}
            onPress={() => handlePlaceTower(towerType.type)}
            style={styles.towerOption}
          >
            <Card>
              <Card.Content>
                <Text style={styles.towerName}>{towerType.name}</Text>
                <Text>{towerType.description}</Text>
                <Text>Cost: {towerType.cost} gold</Text>
              </Card.Content>
            </Card>
          </TouchableOpacity>
        ))}
      </ScrollView>

      <View style={styles.placedTowers}>
        <Text style={styles.sectionTitle}>Placed Towers</Text>
        <ScrollView horizontal>
          {userProgress.towers.map(renderTowerCard)}
        </ScrollView>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#f5f5f5',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  resources: {
    alignItems: 'flex-end',
  },
  towerList: {
    maxHeight: 200,
  },
  towerOption: {
    marginBottom: 10,
  },
  towerCard: {
    marginRight: 10,
    width: 200,
  },
  towerName: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  requirementText: {
    color: '#666',
    fontStyle: 'italic',
  },
  placedTowers: {
    marginTop: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 10,
  },
}); 