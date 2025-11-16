# Part 13: Expo React Native Mobile App Development with the Air Framework

Welcome back to our series on the Air web framework! I'm Winston Mhango, and in this thirteenth installment, we're exploring one of the most exciting aspects of modern application development: **Expo React Native Mobile App Development**.

In our previous posts, we've covered [the basics of Air](01-introduction-to-air-framework.md), [mastered Air Tags](02-mastering-air-tags.md), learned about [routing and HTTP methods](03-routing-and-http-methods.md), explored [forms and validation](04-forms-and-validation.md), understood [templates and Jinja integration](05-templates-and-jinja-integration.md), enhanced our applications with [Tailwind CSS styling](06-styling-with-tailwind-css.md), made our apps more interactive with [HTMX integration](07-htmx-integration.md), implemented [database integration](08-database-integration.md), secured our applications with [authentication and security](09-authentication-and-security.md), ensured quality through [testing and debugging](10-testing-and-debugging.md), prepared our applications for production with [deployment and performance optimization](11-deployment-and-performance.md), and integrated with modern [React frontend applications](12-react-frontend-integration.md). Now it's time to extend our Air applications to mobile platforms using Expo and React Native.

## Introduction to Expo

Expo is a powerful framework and platform for building universal React Native applications that run on both iOS and Android. It provides a comprehensive set of tools and services that make mobile development more accessible and efficient.

### What is Expo?

Expo is an open-source platform for making universal native apps for Android, iOS, and the web with JavaScript and React. It provides a rich set of pre-built components and APIs that work across all platforms, eliminating the need to configure native projects manually.

### Benefits of Expo over Vanilla React Native

1. **Simplified Setup**: No need to install Xcode or Android Studio initially
2. **Rich Ecosystem**: Access to hundreds of pre-built native modules
3. **Over-the-Air Updates**: Update your app without going through app store review
4. **Unified Development**: Single codebase for iOS, Android, and web
5. **Managed Workflow**: Expo handles native dependencies and configurations
6. **Developer Tools**: Excellent tooling including Expo Dev Tools and Expo Go

### Expo Development Workflow

The Expo development workflow is designed to be fast and efficient:

1. **Create Project**: Initialize a new Expo project with a single command
2. **Develop**: Use Expo Go app to preview changes instantly on your device
3. **Test**: Run on simulators, emulators, or physical devices
4. **Build**: Generate standalone app binaries for distribution
5. **Deploy**: Publish updates over-the-air or submit to app stores

## Creating a Mobile App

Let's start by creating a new Expo project and setting up the basic structure.

### Initializing an Expo Project

```
# Install Expo CLI globally (if not already installed)
npm install -g @expo/cli

# Create a new Expo project
npx create-expo-app air-mobile-app --template

# Navigate to the project directory
cd air-mobile-app

# Install additional dependencies we'll need
npm install nativewind react-native-safe-area-context react-native-screens react-native-gesture-handler react-native-reanimated
npm install react-navigation @react-navigation/native-stack
npm install expo-camera expo-media-library expo-location expo-notifications
```

### Project Structure

A typical Expo project follows this structure:

```
air-mobile-app/
├── app/
│   ├── (tabs)/
│   │   ├── _layout.jsx
│   │   ├── index.jsx
│   │   ├── posts.jsx
│   │   └── profile.jsx
│   ├── post/
│   │   └── [id].jsx
│   ├── _layout.jsx
│   └── index.jsx
├── components/
│   ├── PostItem.jsx
│   ├── PostList.jsx
│   └── Header.jsx
├── services/
│   ├── api.js
│   └── authService.js
├── hooks/
│   └── usePosts.js
├── utils/
│   └── helpers.js
├── app.json
├── babel.config.js
├── package.json
└── tailwind.config.js
```

### Navigation Setup

Expo Router provides file-based routing for React Native apps:

```jsx
// app/_layout.jsx
import React from 'react'
import { Stack } from 'expo-router'
import { SafeAreaProvider } from 'react-native-safe-area-context'

export default function RootLayout() {
  return (
    <SafeAreaProvider>
      <Stack>
        <Stack.Screen name="index" options={{ title: 'Home' }} />
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        <Stack.Screen name="post/[id]" options={{ title: 'Post Details' }} />
      </Stack>
    </SafeAreaProvider>
  )
}
```

```jsx
// app/(tabs)/_layout.jsx
import React from 'react'
import { Tabs } from 'expo-router'
import { MaterialIcons } from '@expo/vector-icons'

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: '#2563eb',
        headerShown: false,
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          tabBarIcon: ({ color }) => <MaterialIcons name="home" size={24} color={color} />,
        }}
      />
      <Tabs.Screen
        name="posts"
        options={{
          title: 'Posts',
          tabBarIcon: ({ color }) => <MaterialIcons name="article" size={24} color={color} />,
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: 'Profile',
          tabBarIcon: ({ color }) => <MaterialIcons name="person" size={24} color={color} />,
        }}
      />
    </Tabs>
  )
}
```

### Platform-Specific Code

Expo makes it easy to write platform-specific code when needed:

```jsx
// components/PlatformButton.jsx
import React from 'react'
import { Platform, TouchableOpacity, Text, StyleSheet } from 'react-native'

const PlatformButton = ({ title, onPress }) => {
  if (Platform.OS === 'ios') {
    return (
      <TouchableOpacity style={[styles.button, styles.iosButton]} onPress={onPress}>
        <Text style={[styles.buttonText, styles.iosButtonText]}>{title}</Text>
      </TouchableOpacity>
    )
  } else {
    return (
      <TouchableOpacity style={[styles.button, styles.androidButton]} onPress={onPress}>
        <Text style={[styles.buttonText, styles.androidButtonText]}>{title}</Text>
      </TouchableOpacity>
    )
  }
}

const styles = StyleSheet.create({
  button: {
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  iosButton: {
    backgroundColor: '#007AFF',
  },
  androidButton: {
    backgroundColor: '#2196F3',
  },
  buttonText: {
    fontWeight: '600',
  },
  iosButtonText: {
    color: 'white',
  },
  androidButtonText: {
    color: 'white',
  },
})

export default PlatformButton
```

## Connecting to Air Backend

Now let's connect our mobile app to the Air backend API.

### Network Configuration

Configure your app to communicate with your Air backend:

```javascript
// services/api.js
import Constants from 'expo-constants'

// Determine API URL based on environment
const API_BASE_URL = Constants.expoConfig?.extra?.apiUrl || 'http://localhost:8000'

class ApiService {
  constructor() {
    this.baseUrl = API_BASE_URL
    this.token = null
  }

  setToken(token) {
    this.token = token
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    }

    if (this.token) {
      config.headers.Authorization = `Bearer ${this.token}`
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }

  async get(endpoint) {
    return this.request(endpoint, { method: 'GET' })
  }

  async post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async put(endpoint, data) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  }

  async delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' })
  }
}

export default new ApiService()
```

### API Service Layer

Create a service layer for your API endpoints:

```javascript
// services/postService.js
import api from './api'

class PostService {
  async getAllPosts() {
    return api.get('/api/posts')
  }

  async getPostById(id) {
    return api.get(`/api/posts/${id}`)
  }

  async createPost(postData) {
    return api.post('/api/posts', postData)
  }

  async updatePost(id, postData) {
    return api.put(`/api/posts/${id}`, postData)
  }

  async deletePost(id) {
    return api.delete(`/api/posts/${id}`)
  }
}

export default new PostService()
```

### Authentication Flow

Implement authentication in your mobile app:

```javascript
// services/authService.js
import api from './api'
import * as SecureStore from 'expo-secure-store'

class AuthService {
  async login(credentials) {
    try {
      const response = await api.post('/api/login', credentials)
      
      // Store token securely
      await SecureStore.setItemAsync('userToken', response.token)
      api.setToken(response.token)
      
      return { success: true, user: response.user }
    } catch (error) {
      return { success: false, error: error.message }
    }
  }

  async logout() {
    try {
      await SecureStore.deleteItemAsync('userToken')
      api.setToken(null)
      return { success: true }
    } catch (error) {
      return { success: false, error: error.message }
    }
  }

  async getCurrentUser() {
    try {
      const token = await SecureStore.getItemAsync('userToken')
      if (token) {
        api.setToken(token)
        const user = await api.get('/api/me')
        return { user, token }
      }
      return null
    } catch (error) {
      await SecureStore.deleteItemAsync('userToken')
      api.setToken(null)
      return null
    }
  }

  async register(userData) {
    try {
      const response = await api.post('/api/register', userData)
      return { success: true, user: response.user }
    } catch (error) {
      return { success: false, error: error.message }
    }
  }
}

export default new AuthService()
```

### Offline Support

Implement offline support for better user experience:

```javascript
// utils/offlineManager.js
import AsyncStorage from '@react-native-async-storage/async-storage'

class OfflineManager {
  static async savePendingRequest(request) {
    try {
      const pendingRequests = await this.getPendingRequests()
      pendingRequests.push({ ...request, timestamp: Date.now() })
      await AsyncStorage.setItem('pendingRequests', JSON.stringify(pendingRequests))
      return true
    } catch (error) {
      console.error('Failed to save pending request:', error)
      return false
    }
  }

  static async getPendingRequests() {
    try {
      const requests = await AsyncStorage.getItem('pendingRequests')
      return requests ? JSON.parse(requests) : []
    } catch (error) {
      console.error('Failed to get pending requests:', error)
      return []
    }
  }

  static async clearPendingRequests() {
    try {
      await AsyncStorage.removeItem('pendingRequests')
      return true
    } catch (error) {
      console.error('Failed to clear pending requests:', error)
      return false
    }
  }

  static async processPendingRequests() {
    const requests = await this.getPendingRequests()
    const processedRequests = []
    
    for (const request of requests) {
      try {
        // Attempt to process the request
        const response = await fetch(request.url, {
          method: request.method,
          headers: request.headers,
          body: request.body
        })
        
        if (response.ok) {
          processedRequests.push(request)
        }
      } catch (error) {
        console.error('Failed to process request:', error)
        // Keep failed requests for retry
      }
    }
    
    // Remove processed requests
    const remainingRequests = requests.filter(
      req => !processedRequests.includes(req)
    )
    
    await AsyncStorage.setItem('pendingRequests', JSON.stringify(remainingRequests))
    
    return {
      processed: processedRequests.length,
      remaining: remainingRequests.length
    }
  }
}

export default OfflineManager
```

## Mobile UI with Tailwind

Let's implement mobile UI using NativeWind, which brings Tailwind CSS to React Native.

### NativeWind for Tailwind in React Native

Install and configure NativeWind:

```
# Install NativeWind
npm install nativewind
npm install --save-dev tailwindcss

# Initialize Tailwind CSS
npx tailwindcss init
```

```javascript
// tailwind.config.js
module.exports = {
  content: [
    "./app/**/*.{js,jsx,ts,tsx}",
    "./components/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

```javascript
// babel.config.js
module.exports = function (api) {
  api.cache(true)
  return {
    presets: [
      ['babel-preset-expo', { jsxImportSource: 'nativewind' }],
      'nativewind/babel',
    ],
  }
}
```

```javascript
// metro.config.js
const { getDefaultConfig } = require('expo/metro-config')
const { withNativeWind } = require('nativewind/metro')

const config = getDefaultConfig(__dirname)

module.exports = withNativeWind(config, { input: './global.css' })
```

```css
/* global.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Responsive Design for Mobile

Create responsive components for mobile devices:

``jsx
// components/ResponsiveCard.jsx
import React from 'react'
import { View, Text, TouchableOpacity } from 'react-native'
import { styled } from 'nativewind'

const StyledView = styled(View)
const StyledText = styled(Text)
const StyledTouchableOpacity = styled(TouchableOpacity)

const ResponsiveCard = ({ title, content, onPress, className = '' }) => {
  return (
    <StyledTouchableOpacity 
      className={`bg-white rounded-lg shadow-md p-4 mb-4 ${className}`}
      onPress={onPress}
    >
      <StyledText className="text-lg font-bold text-gray-800 mb-2">
        {title}
      </StyledText>
      <StyledText className="text-gray-600" numberOfLines={3}>
        {content}
      </StyledText>
      <StyledView className="flex-row justify-between items-center mt-3">
        <StyledText className="text-blue-600 text-sm font-medium">
          Read more
        </StyledText>
        <StyledView className="w-6 h-6 rounded-full bg-blue-100 items-center justify-center">
          <StyledText className="text-blue-600 text-xs">→</StyledText>
        </StyledView>
      </StyledView>
    </StyledTouchableOpacity>
  )
}

export default ResponsiveCard
```

### Platform-Specific Styling

Apply platform-specific styling with NativeWind:

``jsx
// components/PlatformButton.jsx
import React from 'react'
import { TouchableOpacity, Text } from 'react-native'
import { styled } from 'nativewind'

const StyledTouchableOpacity = styled(TouchableOpacity)
const StyledText = styled(Text)

const PlatformButton = ({ title, onPress, variant = 'primary' }) => {
  const baseClasses = "py-3 px-6 rounded-lg items-center justify-center"
  
  const variantClasses = {
    primary: "bg-blue-600",
    secondary: "bg-gray-200",
    danger: "bg-red-600",
  }
  
  const textVariantClasses = {
    primary: "text-white",
    secondary: "text-gray-800",
    danger: "text-white",
  }
  
  // Platform-specific styling
  const platformClasses = {
    ios: "shadow-sm",
    android: "elevation-2",
  }
  
  const platform = Platform.OS
  
  return (
    <StyledTouchableOpacity
      className={`${baseClasses} ${variantClasses[variant]} ${platformClasses[platform]}`}
      onPress={onPress}
    >
      <StyledText className={`font-semibold ${textVariantClasses[variant]}`}>
        {title}
      </StyledText>
    </StyledTouchableOpacity>
  )
}

export default PlatformButton
```

### Performance Considerations

Optimize mobile UI performance:

``jsx
// components/OptimizedFlatList.jsx
import React, { memo } from 'react'
import { FlatList } from 'react-native'
import { styled } from 'nativewind'

const StyledFlatList = styled(FlatList)

const OptimizedFlatList = memo(({ data, renderItem, keyExtractor, ...props }) => {
  return (
    <StyledFlatList
      data={data}
      renderItem={renderItem}
      keyExtractor={keyExtractor}
      showsVerticalScrollIndicator={false}
      initialNumToRender={10}
      maxToRenderPerBatch={10}
      windowSize={10}
      removeClippedSubviews={true}
      {...props}
    />
  )
})

export default OptimizedFlatList
```

## Mobile Features Integration

Let's integrate native mobile features into our app.

### Camera and Image Upload

Implement camera functionality and image upload:

``javascript
// services/cameraService.js
import * as ImagePicker from 'expo-image-picker'
import * as MediaLibrary from 'expo-media-library'
import * as FileSystem from 'expo-file-system'

class CameraService {
  async requestCameraPermissions() {
    const { status } = await ImagePicker.requestCameraPermissionsAsync()
    return status === 'granted'
  }

  async requestMediaLibraryPermissions() {
    const { status } = await MediaLibrary.requestPermissionsAsync()
    return status === 'granted'
  }

  async takePhoto() {
    const hasPermission = await this.requestCameraPermissions()
    if (!hasPermission) {
      throw new Error('Camera permission not granted')
    }

    const result = await ImagePicker.launchCameraAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 0.8,
    })

    if (!result.canceled) {
      return result.assets[0]
    }
    
    return null
  }

  async pickImage() {
    const hasPermission = await this.requestMediaLibraryPermissions()
    if (!hasPermission) {
      throw new Error('Media library permission not granted')
    }

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 0.8,
    })

    if (!result.canceled) {
      return result.assets[0]
    }
    
    return null
  }

  async uploadImage(imageUri, endpoint) {
    try {
      const formData = new FormData()
      formData.append('image', {
        uri: imageUri,
        type: 'image/jpeg',
        name: 'photo.jpg',
      })

      const response = await fetch(endpoint, {
        method: 'POST',
        body: formData,
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      if (!response.ok) {
        throw new Error('Upload failed')
      }

      return await response.json()
    } catch (error) {
      console.error('Image upload failed:', error)
      throw error
    }
  }
}

export default new CameraService()
```

``jsx
// components/ImagePicker.jsx
import React, { useState } from 'react'
import { View, TouchableOpacity, Text, Image, Alert } from 'react-native'
import { styled } from 'nativewind'
import * as ImagePicker from 'expo-image-picker'
import cameraService from '../services/cameraService'

const StyledView = styled(View)
const StyledTouchableOpacity = styled(TouchableOpacity)
const StyledText = styled(Text)
const StyledImage = styled(Image)

const ImagePickerComponent = ({ onImageSelected }) => {
  const [selectedImage, setSelectedImage] = useState(null)

  const takePhoto = async () => {
    try {
      const image = await cameraService.takePhoto()
      if (image) {
        setSelectedImage(image.uri)
        onImageSelected(image.uri)
      }
    } catch (error) {
      Alert.alert('Error', error.message)
    }
  }

  const pickImage = async () => {
    try {
      const image = await cameraService.pickImage()
      if (image) {
        setSelectedImage(image.uri)
        onImageSelected(image.uri)
      }
    } catch (error) {
      Alert.alert('Error', error.message)
    }
  }

  return (
    <StyledView className="mb-4">
      {selectedImage ? (
        <StyledView className="items-center">
          <StyledImage
            source={{ uri: selectedImage }}
            className="w-64 h-64 rounded-lg mb-4"
            resizeMode="cover"
          />
          <StyledTouchableOpacity
            className="bg-red-500 py-2 px-4 rounded-lg mb-2"
            onPress={() => {
              setSelectedImage(null)
              onImageSelected(null)
            }}
          >
            <StyledText className="text-white font-medium">Remove Image</StyledText>
          </StyledTouchableOpacity>
        </StyledView>
      ) : (
        <StyledView className="items-center">
          <StyledTouchableOpacity
            className="bg-blue-500 py-3 px-6 rounded-lg mb-2 w-full items-center"
            onPress={takePhoto}
          >
            <StyledText className="text-white font-medium">Take Photo</StyledText>
          </StyledTouchableOpacity>
          <StyledTouchableOpacity
            className="bg-gray-500 py-3 px-6 rounded-lg w-full items-center"
            onPress={pickImage}
          >
            <StyledText className="text-white font-medium">Choose from Library</StyledText>
          </StyledTouchableOpacity>
        </StyledView>
      )}
    </StyledView>
  )
}

export default ImagePickerComponent
```

### Push Notifications

Implement push notifications:

``javascript
// services/notificationService.js
import * as Notifications from 'expo-notifications'
import * as Device from 'expo-device'
import Constants from 'expo-constants'

class NotificationService {
  async registerForPushNotificationsAsync() {
    if (!Device.isDevice) {
      alert('Must use physical device for Push Notifications')
      return
    }

    const { status: existingStatus } = await Notifications.getPermissionsAsync()
    let finalStatus = existingStatus
    
    if (existingStatus !== 'granted') {
      const { status } = await Notifications.requestPermissionsAsync()
      finalStatus = status
    }
    
    if (finalStatus !== 'granted') {
      alert('Failed to get push token for push notification!')
      return
    }

    try {
      const projectId = Constants.expoConfig?.extra?.eas?.projectId ?? Constants.expoConfig?.extra?.projectId
      if (!projectId) {
        throw new Error('Project ID not found')
      }
      
      const pushTokenString = (
        await Notifications.getExpoPushTokenAsync({
          projectId,
        })
      ).data
      
      return pushTokenString
    } catch (error) {
      console.error('Error getting push token:', error)
      return null
    }
  }

  async scheduleNotification(title, body, trigger = null) {
    return await Notifications.scheduleNotificationAsync({
      content: {
        title,
        body,
        sound: 'default',
      },
      trigger: trigger || {
        seconds: 2,
      },
    })
  }

  async cancelNotification(notificationId) {
    await Notifications.cancelScheduledNotificationAsync(notificationId)
  }

  async getAllScheduledNotifications() {
    return await Notifications.getAllScheduledNotificationsAsync()
  }

  setupNotificationHandler() {
    Notifications.setNotificationHandler({
      handleNotification: async () => ({
        shouldShowAlert: true,
        shouldPlaySound: true,
        shouldSetBadge: true,
      }),
    })
  }
}

export default new NotificationService()
```

### Geolocation

Implement geolocation features:

```
// services/locationService.js
import * as Location from 'expo-location'

class LocationService {
  async requestLocationPermissions() {
    const { status } = await Location.requestForegroundPermissionsAsync()
    return status === 'granted'
  }

  async getCurrentLocation() {
    const hasPermission = await this.requestLocationPermissions()
    if (!hasPermission) {
      throw new Error('Location permission not granted')
    }

    const location = await Location.getCurrentPositionAsync({
      accuracy: Location.Accuracy.High,
    })

    return {
      latitude: location.coords.latitude,
      longitude: location.coords.longitude,
      altitude: location.coords.altitude,
      accuracy: location.coords.accuracy,
      timestamp: location.timestamp,
    }
  }

  async watchLocation(callback) {
    const hasPermission = await this.requestLocationPermissions()
    if (!hasPermission) {
      throw new Error('Location permission not granted')
    }

    return await Location.watchPositionAsync(
      {
        accuracy: Location.Accuracy.High,
        timeInterval: 5000,
        distanceInterval: 10,
      },
      callback
    )
  }

  async reverseGeocode(latitude, longitude) {
    try {
      const locations = await Location.reverseGeocodeAsync({
        latitude,
        longitude,
      })

      if (locations.length > 0) {
        const location = locations[0]
        return {
          city: location.city,
          region: location.region,
          country: location.country,
          street: location.street,
          name: location.name,
        }
      }
      
      return null
    } catch (error) {
      console.error('Reverse geocoding failed:', error)
      return null
    }
  }

  async calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371 // Earth radius in kilometers
    const dLat = (lat2 - lat1) * Math.PI / 180
    const dLon = (lon2 - lon1) * Math.PI / 180
    const a = 
      Math.sin(dLat/2) * Math.sin(dLat/2) +
      Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
      Math.sin(dLon/2) * Math.sin(dLon/2)
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))
    return R * c // Distance in kilometers
  }
}

export default new LocationService()
```

### Device Sensors

Access device sensors:

```
// services/sensorService.js
import { Accelerometer, Gyroscope, Magnetometer } from 'expo-sensors'

class SensorService {
  constructor() {
    this.accelerometerSubscription = null
    this.gyroscopeSubscription = null
    this.magnetometerSubscription = null
  }

  async requestSensorPermissions() {
    // Permissions are typically granted automatically for sensors
    return true
  }

  startAccelerometer(callback, interval = 1000) {
    this.accelerometerSubscription = Accelerometer.addListener(callback)
    Accelerometer.setUpdateInterval(interval)
  }

  stopAccelerometer() {
    if (this.accelerometerSubscription) {
      this.accelerometerSubscription.remove()
      this.accelerometerSubscription = null
    }
  }

  startGyroscope(callback, interval = 1000) {
    this.gyroscopeSubscription = Gyroscope.addListener(callback)
    Gyroscope.setUpdateInterval(interval)
  }

  stopGyroscope() {
    if (this.gyroscopeSubscription) {
      this.gyroscopeSubscription.remove()
      this.gyroscopeSubscription = null
    }
  }

  startMagnetometer(callback, interval = 1000) {
    this.magnetometerSubscription = Magnetometer.addListener(callback)
    Magnetometer.setUpdateInterval(interval)
  }

  stopMagnetometer() {
    if (this.magnetometerSubscription) {
      this.magnetometerSubscription.remove()
      this.magnetometerSubscription = null
    }
  }

  async isAvailableAsync(sensor) {
    switch (sensor) {
      case 'accelerometer':
        return await Accelerometer.isAvailableAsync()
      case 'gyroscope':
        return await Gyroscope.isAvailableAsync()
      case 'magnetometer':
        return await Magnetometer.isAvailableAsync()
      default:
        return false
    }
  }
}

export default new SensorService()
```

## Publishing and Distribution

Finally, let's prepare our app for publishing and distribution.

### App Store Preparation

Prepare your app for app store submission:

```json
// app.json
{
  "expo": {
    "name": "Air Mobile App",
    "slug": "air-mobile-app",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "userInterfaceStyle": "light",
    "splash": {
      "image": "./assets/splash.png",
      "resizeMode": "contain",
      "backgroundColor": "#ffffff"
    },
    "ios": {
      "supportsTablet": true,
      "bundleIdentifier": "com.yourcompany.airmobileapp"
    },
    "android": {
      "adaptiveIcon": {
        "foregroundImage": "./assets/adaptive-icon.png",
        "backgroundColor": "#ffffff"
      },
      "package": "com.yourcompany.airmobileapp"
    },
    "web": {
      "favicon": "./assets/favicon.png"
    },
    "extra": {
      "eas": {
        "projectId": "your-project-id"
      },
      "apiUrl": "https://your-production-api.com"
    }
  }
}
```

### OTA Updates

Implement over-the-air updates:

```javascript
// services/updateService.js
import * as Updates from 'expo-updates'

class UpdateService {
  async checkForUpdates() {
    try {
      const update = await Updates.checkForUpdateAsync()
      
      if (update.isAvailable) {
        await Updates.fetchUpdateAsync()
        return true
      }
      
      return false
    } catch (error) {
      console.error('Failed to check for updates:', error)
      return false
    }
  }

  async reloadApp() {
    try {
      await Updates.reloadAsync()
    } catch (error) {
      console.error('Failed to reload app:', error)
    }
  }

  async getUpdateInfo() {
    try {
      const update = await Updates.checkForUpdateAsync()
      return {
        isAvailable: update.isAvailable,
        manifest: update.manifest,
      }
    } catch (error) {
      console.error('Failed to get update info:', error)
      return null
    }
  }
}

export default new UpdateService()
```

### Analytics Integration

Add analytics to track user behavior:

```javascript
// services/analyticsService.js
import { Platform } from 'react-native'

class AnalyticsService {
  constructor() {
    this.isEnabled = true
  }

  enable() {
    this.isEnabled = true
  }

  disable() {
    this.isEnabled = false
  }

  async trackEvent(eventName, properties = {}) {
    if (!this.isEnabled) return

    try {
      const eventData = {
        event: eventName,
        timestamp: new Date().toISOString(),
        platform: Platform.OS,
        ...properties,
      }

      // In a real app, you would send this to your analytics service
      console.log('Analytics Event:', eventData)
      
      // Example: Send to your backend
      // await fetch('/api/analytics', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify(eventData),
      // })
    } catch (error) {
      console.error('Failed to track event:', error)
    }
  }

  async trackScreenView(screenName) {
    await this.trackEvent('screen_view', { screen_name: screenName })
  }

  async trackUserAction(action, target) {
    await this.trackEvent('user_action', { action, target })
  }
}

export default new AnalyticsService()
```

### Performance Monitoring

Implement performance monitoring:

```javascript
// services/performanceService.js
import { Platform } from 'react-native'

class PerformanceService {
  constructor() {
    this.metrics = []
  }

  startMeasurement(name) {
    const startTime = performance.now()
    return { name, startTime }
  }

  endMeasurement(measurement) {
    const endTime = performance.now()
    const duration = endTime - measurement.startTime
    
    const metric = {
      name: measurement.name,
      duration: duration,
      timestamp: new Date().toISOString(),
      platform: Platform.OS,
    }
    
    this.metrics.push(metric)
    
    // Log slow operations
    if (duration > 1000) {
      console.warn(`Slow operation detected: ${measurement.name} took ${duration.toFixed(2)}ms`)
    }
    
    return metric
  }

  async sendMetrics() {
    if (this.metrics.length === 0) return

    try {
      // Send metrics to your backend
      // await fetch('/api/performance', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify(this.metrics),
      // })
      
      // Clear sent metrics
      this.metrics = []
    } catch (error) {
      console.error('Failed to send performance metrics:', error)
    }
  }

  getAverageDuration(metricName) {
    const metrics = this.metrics.filter(m => m.name === metricName)
    if (metrics.length === 0) return 0
    
    const total = metrics.reduce((sum, m) => sum + m.duration, 0)
    return total / metrics.length
  }
}

export default new PerformanceService()
```

## What's Coming Next

In our next post, we'll explore real-world project development, covering:

1. Project planning and requirements gathering
2. Architecture design for full-stack applications
3. Implementation of backend with Air and frontend with React
4. Advanced features like real-time updates and admin dashboards

## Conclusion

Expo React Native mobile app development with the Air framework creates a powerful full-stack development experience. By leveraging Expo's rich ecosystem and the Air backend, you can build universal mobile applications that run on both iOS and Android while maintaining a clean, scalable architecture.

Key takeaways from this post:

1. **Expo Framework**: Understand the benefits of Expo over vanilla React Native
2. **Project Setup**: Create and configure Expo projects with proper navigation
3. **Backend Integration**: Connect mobile apps to Air backend APIs with authentication
4. **Mobile UI**: Implement responsive design with NativeWind and Tailwind CSS
5. **Native Features**: Integrate camera, geolocation, notifications, and sensors
6. **Publishing**: Prepare apps for distribution with OTA updates and analytics

With Expo React Native mobile app development mastered, you can now build modern, feature-rich mobile applications that communicate seamlessly with your Air backend. The combination of Air's Python-based approach and Expo's cross-platform capabilities provides an efficient workflow for building full-stack applications that run on web and mobile platforms.

Ready to continue your journey with Air? Make sure to follow this series on [codetips.blog](https://codetips.blog/series) for weekly updates. You can also connect with me through [LinkedIn](https://www.linkedin.com/in/winston-mhango-401980ab/), [GitHub](https://github.com/winstonmhango23/), or by email at winstonmhango23@gmail.com.

See you in the next post where we'll dive into real-world project development!

---

*This post is part of the "Mastering the Air Framework" series. Stay tuned for more deep dives into this exciting new Python web framework!*
*Previous: [React Frontend Integration](12-react-frontend-integration.md)*

## Quiz: Test Your Knowledge

1. What is the primary advantage of using Expo over vanilla React Native?
   a) Better performance
   b) Rich pre-configured ecosystem with built-in APIs
   c) Smaller bundle sizes
   d) Faster rendering

2. Which command is used to start an Expo development server?
   a) npm start
   b) expo start
   c) react-native start
   d) yarn dev

3. What is the correct way to access device location in an Expo app?
   a) navigator.geolocation.getCurrentPosition()
   b) import { Location } from 'expo-location'
   c) import { Geolocation } from 'react-native'
   d) expo.location.getCurrentPosition()

4. True or False: Expo apps can only run on mobile devices and cannot be deployed to the web.

5. True or False: You can use NativeWind (Tailwind CSS for React Native) to style components in Expo applications.

6. Explain how Expo's over-the-air (OTA) updates work and what benefits they provide for mobile app development.

### Answers:
1. b) Rich pre-configured ecosystem with built-in APIs
2. b) expo start
3. b) import { Location } from 'expo-location'
4. False - Expo apps can be deployed to iOS, Android, and web platforms
5. True
6. Expo's OTA updates allow developers to push code updates to users without going through the app store review process. When you publish an update, Expo builds and hosts the new JavaScript bundle. The app checks for updates when it starts or when triggered programmatically, downloads the new bundle, and reloads with the updated code. This provides benefits like faster iteration cycles, immediate bug fixes, and the ability to roll back problematic updates without app store delays.
