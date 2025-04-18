# Rowing Tower Defense

A mobile fitness game that combines rowing workouts with tower defense mechanics. Players build and upgrade towers by completing real-world rowing workouts on a Concept2 or Bluetooth-enabled rowing machine.

## Features

- Real-time rowing machine integration via Bluetooth
- Track workout metrics:
  - Distance
  - Time
  - Split (pace per 500m)
  - Heart rate (if supported by device)
- Three tower types:
  - Speed Tower: Upgrade by achieving fast splits
  - Endurance Tower: Upgrade by rowing long distances
  - Consistency Tower: Upgrade by maintaining steady pace
- Resource system:
  - Gold: Earned based on distance rowed
  - Gems: Earned for milestone achievements
- Base builder interface for placing and upgrading towers

## Technical Stack

- React Native
- TypeScript
- Redux Toolkit for state management
- React Navigation for routing
- React Native Paper for UI components
- React Native BLE PLX for Bluetooth connectivity

## Setup

1. Install dependencies:
```bash
npm install
```

2. For iOS, install pods:
```bash
cd ios && pod install && cd ..
```

3. Start the development server:
```bash
npm start
```

4. Run on your device:
```bash
# For iOS
npm run ios

# For Android
npm run android
```

## Bluetooth Requirements

The app requires Bluetooth Low Energy (BLE) support and the following permissions:

### Android
- BLUETOOTH
- BLUETOOTH_ADMIN
- ACCESS_FINE_LOCATION

### iOS
- NSBluetoothAlwaysUsageDescription
- NSBluetoothPeripheralUsageDescription

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 