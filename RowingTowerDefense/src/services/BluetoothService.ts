import { BleManager } from 'react-native-ble-plx';
import { WorkoutData } from '../types';

class BluetoothService {
  private bleManager: BleManager;
  private device: any | null = null;
  private isScanning: boolean = false;

  constructor() {
    this.bleManager = new BleManager();
  }

  async startScanning(): Promise<void> {
    if (this.isScanning) return;

    try {
      this.isScanning = true;
      await this.bleManager.startDeviceScan(
        null,
        { allowDuplicates: false },
        (error, device) => {
          if (error) {
            console.error('Scan error:', error);
            return;
          }

          if (device?.name?.includes('Concept2') || device?.name?.includes('ROW')) {
            this.device = device;
            this.stopScanning();
          }
        }
      );
    } catch (error) {
      console.error('Failed to start scanning:', error);
      this.isScanning = false;
    }
  }

  stopScanning(): void {
    if (this.isScanning) {
      this.bleManager.stopDeviceScan();
      this.isScanning = false;
    }
  }

  async connect(): Promise<boolean> {
    if (!this.device) {
      throw new Error('No device selected');
    }

    try {
      await this.device.connect();
      await this.device.discoverAllServicesAndCharacteristics();
      return true;
    } catch (error) {
      console.error('Connection error:', error);
      return false;
    }
  }

  async startWorkout(): Promise<void> {
    if (!this.device) {
      throw new Error('No device connected');
    }

    // Implementation will depend on the specific rowing machine's Bluetooth protocol
    // This is a placeholder for the actual implementation
    try {
      // Subscribe to the rowing machine's data characteristic
      // The exact characteristic UUID will depend on the machine model
      const characteristic = await this.device.monitorCharacteristicForService(
        'ROWING_SERVICE_UUID',
        'ROWING_DATA_CHARACTERISTIC_UUID',
        (error, characteristic) => {
          if (error) {
            console.error('Monitoring error:', error);
            return;
          }

          if (characteristic?.value) {
            const workoutData = this.parseWorkoutData(characteristic.value);
            // Emit workout data through an event system or callback
          }
        }
      );
    } catch (error) {
      console.error('Failed to start workout:', error);
    }
  }

  private parseWorkoutData(rawData: string): WorkoutData {
    // Implementation will depend on the specific rowing machine's data format
    // This is a placeholder for the actual implementation
    return {
      distance: 0,
      duration: 0,
      split: 0,
      timestamp: Date.now(),
    };
  }

  async disconnect(): Promise<void> {
    if (this.device) {
      try {
        await this.device.cancelConnection();
        this.device = null;
      } catch (error) {
        console.error('Disconnection error:', error);
      }
    }
  }
}

export const bluetoothService = new BluetoothService(); 