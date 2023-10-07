// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.4.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.4.0/firebase-analytics.js";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAeZMFo-poxJbPVMIHc8UNoqJS6UR0ZbZI",
  authDomain: "fir-aab7d.firebaseapp.com",
  projectId: "fir-aab7d",
  storageBucket: "fir-aab7d.appspot.com",
  messagingSenderId: "615101886112",
  appId: "1:615101886112:web:60b79f8aa38ca0cc65e3c5",
  measurementId: "G-DYTKLTWG2Z"
};

// Initialize Firebase
export const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);