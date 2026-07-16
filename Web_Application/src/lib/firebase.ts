import { initializeApp } from 'firebase/app';
import { getDatabase } from 'firebase/database';
import { getAnalytics } from 'firebase/analytics';

// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDbi8r5PT1V91oiGvTjjniZkoalYbGGTAA",
  authDomain: "cowfit-demo-d2364.firebaseapp.com",
  databaseURL: "https://cowfit-demo-d2364-default-rtdb.firebaseio.com",
  projectId: "cowfit-demo-d2364",
  storageBucket: "cowfit-demo-d2364.firebasestorage.app",
  messagingSenderId: "724557214275",
  appId: "1:724557214275:web:769100f5a4087de0d6daf6",
  measurementId: "G-G8X98B0FCE"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const database = getDatabase(app);
export const analytics = getAnalytics(app);

export default app;
