// CONFIGURATION
const API_URL = "https://recycarm-api.onrender.com/get_fullness";
const FETCH_INTERVAL = 2000; // Fetch data every 2 seconds

// Portfolio Utility Function (Hamburger Menu)
function toggleMenu() {
  const menu = document.querySelector(".menu-links");
  const icon = document.querySelector(".hamburger-icon");
  menu.classList.toggle("open");
  icon.classList.toggle("open");
}

// Dashboard Live Data Function
function fetchAndDisplayData() {
  const statusElement = document.getElementById("robot-status");
  const lastUpdatedElement = document.getElementById("last-updated");
  const cameraFeedElement = document.getElementById("camera-feed-img");

  statusElement.textContent = "FETCHING...";
  statusElement.classList.remove("online", "offline");
  statusElement.classList.add("fetching");

  // 1. Fetch data from the Flask Server
  fetch(API_URL)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      // 2. Update the HTML elements (Organic/Anorganic cards)
      // Display the state string directly (data is guaranteed to be ALL CAPS by app.py)
      document.getElementById("organic").textContent =
        data.organic_fullness_percent;
      document.getElementById("anorganic").textContent =
        data.anorganic_fullness_percent;

      // 3. Camera Feed Logic
      const base64String = data.camera_feed_base64;

      if (base64String && base64String !== "None") {
        cameraFeedElement.src = `data:image/jpeg;base64,${base64String}`;
        cameraFeedElement.alt = "Live Camera Feed";
      } else {
        cameraFeedElement.src = "";
        cameraFeedElement.alt = "No Camera Feed Available";
      }

      // 4. Update Status Bar
      statusElement.textContent = "ONLINE";
      statusElement.classList.add("online");
      statusElement.classList.remove("offline", "fetching");
      lastUpdatedElement.textContent = data.last_updated;

      console.log("Dashboard updated with live data and camera feed.");
    })
    .catch((error) => {
      // 5. Handle errors (e.g., if the server is offline)
      console.error("Failed to connect to the server:", error);

      // Set cards to display error/offline status
      document.getElementById("organic").textContent = "N/A";
      document.getElementById("anorganic").textContent = "N/A";

      // Also clear the camera feed on error
      cameraFeedElement.src = "";
      cameraFeedElement.alt = "Server Offline";

      // Update Status Bar
      statusElement.textContent = "OFFLINE";
      statusElement.classList.add("offline");
      statusElement.classList.remove("online", "fetching");
      lastUpdatedElement.textContent = "N/A";
    });
}

// Start the fetch loop
fetchAndDisplayData();
setInterval(fetchAndDisplayData, FETCH_INTERVAL);
