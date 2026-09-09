
---

### Step-by-Step Setup Guide

#### 1. Set Up Firebase Console

1. Go to the [Firebase Console](https://console.firebase.google.com/) and click **Add Project** to create a new project.
2. In the left navigation menu, go to **Build > Authentication**.
* Click **Get Started**.
* Under the **Sign-in method** tab, select **Google**, enable it, choose your support email, and click **Save**.


3. In the left menu, go to **Build > Firestore Database**.
* Click **Create Database**.
* Choose **Start in production mode** (or test mode for quick setup) and select a location close to you.
* Under the **Rules** tab in Firestore, allow logged-in users to read and write their own data:
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}

```





---

#### 2. Get Your Firebase Configuration Credentials

1. Click the **Gear icon (Project settings)** at the top left of the Firebase Console.
2. Scroll down to the **Your apps** section, click the **Web icon (`</>`)**, and register your app name.
3. Firebase will generate a code block containing your `firebaseConfig` object (includes your `apiKey`, `authDomain`, `projectId`, etc.).
4. Copy these key details into your project's frontend code.

---

#### 3. Connect Firebase in Frontend JavaScript

1. Import the Firebase Web SDK modules at the bottom of your HTML file inside a `<script type="module">` tag:
```javascript
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getAuth, signInWithPopup, GoogleAuthProvider, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";
import { getFirestore, doc, setDoc, getDoc } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";

```


2. Initialize Firebase with your config details:
```javascript
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);
const provider = new GoogleAuthProvider();

```


3. Use `signInWithPopup(auth, provider)` to open the Google Sign-In window when a user logs in.

---

#### 4. Save and Restore Expense Data in Firestore

1. **Listen to Login State:** Use `onAuthStateChanged(auth, async (user) => ...)` so when a user signs in, the app automatically fetches their unique User ID (`user.uid`).
2. **Retrieve Data on Login:** Fetch existing expense records stored under the user's document using `getDoc(doc(db, "users", user.uid))`.
3. **Save/Sync Data on Update:** Whenever an expense is added or modified, update the user's document using `setDoc(doc(db, "users", user.uid), { expenses: data, income: value })`.

---

#### 5. Add Your Live Website Domain to Firebase

1. In the Firebase Console, go to **Authentication > Settings > Authorized domains**.
2. Click **Add domain** and enter your deployed app domain (e.g., `your-app-name.onrender.com`).
3. Click **Save** so Google allows authentication popups directly from your live deployed website.
