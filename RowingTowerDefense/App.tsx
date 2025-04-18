import React from 'react';
import { Provider as PaperProvider } from 'react-native-paper';
import { Provider as StoreProvider } from 'react-redux';
import { store } from './src/store';
import { AppNavigator } from './src/navigation/AppNavigator';

const App: React.FC = () => {
  return (
    <StoreProvider store={store}>
      <PaperProvider>
        <AppNavigator />
      </PaperProvider>
    </StoreProvider>
  );
};

export default App; 