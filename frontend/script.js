// --- CONFIGURATION ---
// !!! IMPORTANT: This is the local test URL. REPLACE this with your public Render URL before deploying.
const API_URL = "https://recycarm-api.onrender.com/get_count";
const FETCH_INTERVAL = 4000; // Fetch data every 4 seconds
// --- END CONFIGURATION ---

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

  // Set fetching status
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
      document.getElementById("organic").textContent =
        data.organic_trash_count.toFixed(1) + " kg";
      document.getElementById("anorganic").textContent =
        data.anorganic_trash_count.toFixed(1) + " kg";

      // 3. Update Status Bar
      statusElement.textContent = "ONLINE";
      statusElement.classList.add("online");
      statusElement.classList.remove("offline", "fetching");
      lastUpdatedElement.textContent = data.last_updated;

      console.log("Dashboard updated with live data.");
    })
    .catch((error) => {
      // 4. Handle errors (e.g., if the server is offline)
      console.error("Failed to connect to the server:", error);

      // Set cards to display error/offline status
      document.getElementById("organic").textContent = "N/A";
      document.getElementById("anorganic").textContent = "N/A";

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
