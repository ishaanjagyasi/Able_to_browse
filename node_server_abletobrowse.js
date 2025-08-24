const Max = require('max-api');

Max.post('🚀 Starting Firebase Realtime Device Loader...');

const { initializeApp } = require('firebase/app');
const { getDatabase, ref, onValue, off, remove } = require('firebase/database');
const os = require('os');

// Firebase configuration
const FIREBASE_CONFIG = {
    projectId: "ableton-device-loader",
    databaseURL: "https://ableton-device-loader-default-rtdb.firebaseio.com",
    apiKey: "AIzaSyB0_6KxIa40hjrMBXIAFSmq-DbM0n3dV4c"
};

// Initialize Firebase
const app = initializeApp(FIREBASE_CONFIG);
const database = getDatabase(app);

// Session ID that's unique per computer but persistent
let sessionId = "session_default";
let isListening = false;
let deviceRequestsRef = null;
let unsubscribe = null;
let lastProcessedRequests = new Set(); // Track processed requests

// Generate a unique session ID based on computer info
function generateComputerSessionId() {
    const computerName = os.hostname();
    const userInfo = os.userInfo();
    
    // Create a consistent ID based on computer + user
    const baseId = computerName + '_' + userInfo.username;
    // Clean it up for Firebase
    const cleanId = baseId.toLowerCase().replace(/[^a-z0-9]/g, '_').substring(0, 20);
    
    return 'ableton_' + cleanId;
}

function startListening() {
    if (isListening) return;
    
    isListening = true;
    Max.post('👂 Starting real-time listener for device requests...');
    Max.post('💡 Session ID: ' + sessionId);
    Max.post('🔄 Listening for real-time changes (no polling!)'); 
    
    Max.post('🔄 Session ID: ' + sessionId);
    // Create reference to device requests for this session
    deviceRequestsRef = ref(database, `device_requests/${sessionId}`);
    Max.post('📍 Created Firebase reference for path: device_requests/' + sessionId);
    
    // Set up real-time listener
    Max.post('🎯 Setting up Firebase real-time listener...');
    unsubscribe = onValue(deviceRequestsRef, (snapshot) => {
        Max.post('📡 Firebase listener triggered!');
        if (snapshot.exists()) {
            Max.post('📊 Device requests found - processing...');
            const data = snapshot.val();
            if (data && typeof data === 'object') {
            Object.keys(data).forEach(requestId => {
                const deviceName = data[requestId];
                
                // Only process if we haven't seen this request before
                if (deviceName && !lastProcessedRequests.has(requestId)) {
                    Max.post('🎵 LOADING DEVICE: ' + deviceName + ' (ID: ' + requestId + ')');
                    
                    // Send device name to Max patch output
                    Max.outlet(deviceName);
                    
                    // Remember we processed this request
                    lastProcessedRequests.add(requestId);
                    
                    // Clean up the processed request
                    cleanupProcessedRequest(requestId);
                }
            });
            }
        } else {
            Max.post('📭 No device requests pending (snapshot empty)');
        }
    }, (error) => {
        Max.post('❌ Firebase listener error: ' + error.message);
    });
    
    Max.post('✅ Firebase real-time listener successfully attached!');
    Max.post('👂 Now listening for changes on: device_requests/' + sessionId);
}

function stopListening() {
    if (unsubscribe) {
        unsubscribe();
        unsubscribe = null;
    }
    if (deviceRequestsRef) {
        off(deviceRequestsRef);
        deviceRequestsRef = null;
    }
    isListening = false;
    Max.post('⏹️ Stopped listening for device requests');
}

// This function is no longer needed - real-time listeners handle everything
// function checkForDeviceRequests() is replaced by the onValue listener in startListening()

function cleanupProcessedRequest(requestId) {
    // Remove the processed request from Firebase using the SDK
    const requestRef = ref(database, `device_requests/${sessionId}/${requestId}`);
    remove(requestRef).catch((error) => {
        Max.post('⚠️ Error cleaning up request: ' + error.message);
    });
}

// makeSimpleRequest function no longer needed - using Firebase SDK directly

function setSessionId(newSessionId) {
    const wasListening = isListening;
    
    // Stop current listener if running
    if (wasListening) {
        stopListening();
    }
    
    sessionId = newSessionId;
    Max.post('📱 Session ID updated to: ' + sessionId);
    Max.post('✅ Ready to receive device requests for session: ' + sessionId);
    
    // Clear processed requests when session changes
    lastProcessedRequests.clear();
    
    // Restart listener with new session ID if it was running
    if (wasListening) {
        Max.post('🔄 Restarting listener with new session ID...');
        startListening();
    }
}

function testConnection() {
    Max.post('🔍 Testing Firebase Realtime Database connection...');
    
    const { set } = require('firebase/database');
    const testRef = ref(database, 'test');
    const testData = {
        timestamp: new Date().toISOString(),
        test: 'connection'
    };
    
    set(testRef, testData)
        .then(() => {
            Max.post('✅ Firebase Realtime Database connection successful!');
        })
        .catch((error) => {
            Max.post('❌ Firebase connection test failed: ' + error.message);
        });
}

function forceCheck() {
    Max.post('🔍 Force check not needed with real-time listeners!');
    Max.post('📡 Real-time listeners are always active when started');
}

function clearProcessedCache() {
    lastProcessedRequests.clear();
    Max.post('🗑️ Cleared processed requests cache');
}

// Max message handlers
Max.addHandler('setSession', (id) => {
    setSessionId(id);
});

Max.addHandler('start', () => {
    startListening();
});

Max.addHandler('stop', () => {
    stopListening();
});

Max.addHandler('test', () => {
    testConnection();
});

Max.addHandler('check', () => {
    forceCheck();
});

Max.addHandler('clear', () => {
    clearProcessedCache();
});

Max.addHandler('status', () => {
    Max.post('📊 FIREBASE REALTIME STATUS:');
    Max.post('   Session ID: ' + sessionId);
    Max.post('   Listening: ' + (isListening ? 'ON' : 'OFF'));
    Max.post('   Mode: Real-time Firebase listeners (no polling!)');
    Max.post('   Connection: ' + (unsubscribe ? 'Active' : 'Inactive'));
    Max.post('   Processed Requests: ' + lastProcessedRequests.size);
});

// Auto-start when script loads
// setTimeout(() => {
//     sessionId = generateComputerSessionId();
//     testConnection();
//     startListening();
    
//     Max.post('');
//     Max.post('🖥️  COMPUTER SESSION ID: ' + sessionId);
//     Max.post('');
//     Max.post('📱 TO CONNECT FROM PHONE/TABLET:');
//     Max.post('   1. Open: https://ishaanjagyasi.github.io/ableton-device-loader-website/');
//     Max.post('   2. Enter this Session ID: ' + sessionId);
//     Max.post('   3. Start loading devices!');
//     Max.post('');
// }, 1000);

Max.post('✅ Firebase Realtime Device Loader initialized!');
Max.post('📡 Using Firebase real-time listeners (efficient, no polling!)');
Max.post('');