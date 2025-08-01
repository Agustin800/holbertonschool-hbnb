/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
  if (window.location.href.includes("index.html")) {
    fetch_places("All");
    loadPriceFilter();
  }
  if (window.location.href.includes("place.html")) {
    const placeToken = JSON.parse(localStorage.getItem("place"));
    storeUserById(placeToken.owner_id);
    const ownerToken = JSON.parse(localStorage.getItem("owner"));
    displayPlaceDetails(placeToken, ownerToken);
  }


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

function loadPriceFilter() {
  const price_filter = document.querySelector("#price-filter");
  price_filter.innerHTML = "";
  price_filter.innerHTML += `
  <option value="All">All</option>
  <option value="10">$10</option>
  <option value="50">$50</option>
  <option value="100">$100</option>
  `;
}

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
    fetch_places("All");
  }
}
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

if (window.location.href.includes("index.html")) {
  const price_filter = document.querySelector("#price-filter");
  price_filter.addEventListener("change", () => {
    const selected_value = price_filter.value;
    fetch_places(selected_value);
  })
}


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

    if (value === "All") {
      places = data;
    } else {
      for (let i = 0; i < data.length; i++) {
        if (data[i].price <= Number(value)) {
          places.push(data[i]);
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
    <p>$${place.price}</p>
    <button class="details-button" onclick="fetchPlaceDetails('${place.id}')">View Details</button>
    </div>
`;
  }
}

async function fetchPlaceDetails(place_id) {
  {
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${place_id}`, {
      headers: {
        "Content-Type": "application/json",
      },
    })

    if (response.ok) {
      const place = await response.json();
      localStorage.setItem("place", JSON.stringify(place));
      window.location.href = "place.html";
    } else {
      alert(`Failed to retrieve the place with the ID: ${place_id}: ` + response.statusText);
    }
  }
}

async function storeUserById(user_id) {
  const response = await fetch(`http://127.0.0.1:5000/api/v1/users/${user_id}`, {
    headers: {
      "Content-Type": "application/json",
    },
  })

  if (response.ok) {
    const owner = await response.json();
    localStorage.setItem("owner", JSON.stringify(owner));
  } else {
    alert(`Failed to retrieve the user with the ID: ${user_id}: ` + response.statusText);
  }
}

function displayReviewLink() {
  const reviewLink = document.querySelector("#add-review-link");
  if (getCookie('token')) {
    reviewLink.style.display = "block";
  } else {
    reviewLink.style.display = "none";
  }
}

async function displayPlaceDetails(place, owner) {

  let placeContainer = document.querySelector("#place-details");
  placeContainer.innerHTML = "";
  placeContainer.innerHTML += `<div class="place-info">
                <p><strong>Host: </strong>${owner.first_name} ${owner.last_name}</p>
                <p><strong>Price per nigth: </strong>${place.price}</p>
                <p><strong>Description: </strong>${place.description}</p>
            </div>`;
  let divInfo = document.querySelector(".place-info");
  divInfo.innerHTML += `<p id="pAmenities"><strong>Amenities:</strong></p>`

  for (let i = 0; i < place.amenities.length; i++) {
    let amenity = place.amenities[i];
    if (place.amenities.length == 1) {
      document.querySelector("#pAmenities").innerHTML += `${amenity.name}`;
    } else {
      document.querySelector("#pAmenities").innerHTML += `${amenity.name}, `;
    }
  }

  let reviewsContainer = document.querySelector("#reviews");
  reviewsContainer.innerHTML = "";

  for (let i = 0; i < place.reviews.length; i++) {
    let review = place.reviews[i];
    const reviwerName = await getUserById(review.user);
    reviewsContainer.innerHTML += `
    <div class="review-card">
    <p><strong>${reviwerName}</strong></p>
    <p><strong>Rating: </strong>${review.rating}</p>
    <p><strong>Comment: </strong>${review.text}</p>
    </div>
    `;
  }
  placeContainer.innerHTML += `<a href="add_review.html" id="add-review-link">Add Reviews</a>`;
  displayReviewLink();
}

async function getUserById(user_id) {
  const response = await fetch(`http://127.0.0.1:5000/api/v1/users/${user_id}`, {
    headers: {
      "Content-Type": "application/json",
    },
  })

  if (response.ok) {
    const user = await response.json();  
    return `${user.first_name} ${user.last_name}`;  ;
  } else {
    alert(`Failed to retrieve the user with the ID: ${user_id}: ` + response.statusText);
  }
}