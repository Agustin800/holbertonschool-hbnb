/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
  fetch_places("All");
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      let email = document.querySelector("#email").value;
      let password = document.querySelector("#password").value;

      await loginUser(email, password);
    });
  }
});

async function loginUser(email, password) {
  let response = await fetch("http://127.0.0.1:5000/api/v1/auth/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password })
  })

  if (response.ok) {
    const data = await response.json();
    document.cookie = `token=${data.access_token}; path=/`;
    window.location.href = 'index.html';
  } else {
    alert('Login failed: ' + response.statusText);

  }
}

function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!token) {
    loginLink.style.display = 'block';
  } else {
    loginLink.style.display = 'none';
    // Fetch places data if the user is authenticated
    fetchPlaces(token);
  }
}
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

const price_filter = document.getElementById("#price-filter");
price_filter.addEventListener("change", () => {
  const selected_value = price_filter.value;
  fetch_places(selected_value);
})

async function fetch_places(value) {
  const token = getCookie('token');
  let places = [];
  const response = await fetch("http://127.0.0.1:5000/api/v1/places/", {
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    }
  });

  if (response.ok) {
    const data = await response.json();

    if (value == "All") {
      places = data;
    } else {
      for (let i = 0; i < data.length; i++) {
        if (data[i].price <= value) {
          places.push(data);
        }
      }
    }
    displayPlaces(places);

  } else {
    alert('Failed to fetch places: ' + response.statusText);
  }

}

function displayPlaces(places) {
  let placesContainer = document.querySelector("#places-list");
  placesContainer.innerHTML = "";

  for (let i = 0; i < places.length; i++) {
    let place = places[i];
    placesContainer.innerHTML += `
    <div class="place-card">
    <h3>${place.title}</h3>
    <p>${place.price}</p>
    <input class="details-button">View Details</input>
    </div>
`
  }
}