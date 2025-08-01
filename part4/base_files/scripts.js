document.addEventListener('DOMContentLoaded', () => {
  if (window.location.href.includes("index.html")) {
    checkAuthentication();
    fetch_places("All");
    loadPriceFilter();
  }
  if (window.location.href.includes("place.html")) {
    const params = new URLSearchParams(window.location.search);
    const placeId = params.get("place_id");

    if (placeId) {
      fetchPlaceAndOwner(placeId);
    } else {
      alert("No place_id found in URL");
    }
  }
  if (window.location.href.includes("add_review.html")) {
    const token = getCookie('token');
    if (!token) {
      window.location.href = 'index.html';
    }

    loadSelectOptions();

    const reviewForm = document.getElementById('review-form');
    const place_id = getPlaceIdFromURL();

    if (reviewForm) {
      reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        let rating = Number(document.querySelector("#slcRating").value);
        let text = document.querySelector("#review").value;

         addReview(text, rating, place_id, token);
      });
    }
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
      window.location.href = `place.html?place_id=${place_id}`;
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
    let rating = review.rating
    const reviwerName = await getUserById(review.user);
    reviewsContainer.innerHTML += `
    <div class="review-card">
    <p><strong>${reviwerName}</strong></p>
    <p><strong>Rating: </strong>${'✡'.repeat(rating)}</p>
    <p><strong>Comment: </strong>${review.text}</p>
    </div>
    `;
  }

  placeContainer.innerHTML += `<a href="add_review.html?place_id=${getPlaceIdFromURL()}" id="add-review-link">Add Reviews</a>`;
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
    return `${user.first_name} ${user.last_name}`;;
  } else {
    alert(`Failed to retrieve the user with the ID: ${user_id}: ` + response.statusText);
  }
}

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get("place_id");
}

async function fetchPlaceAndOwner(placeId) {
  const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
    headers: {
      "Content-Type": "application/json"
    }
  });

  if (response.ok) {
    const place = await response.json();
    const ownerResponse = await fetch(`http://127.0.0.1:5000/api/v1/users/${place.owner_id}`, {
      headers: {
        "Content-Type": "application/json"
      }
    });

    if (ownerResponse.ok) {
      const owner = await ownerResponse.json();
      displayPlaceDetails(place, owner);
    } else {
      alert("Failed to load owner info");
    }
  } else {
    alert("Failed to load place details");
  }
}

function loadSelectOptions() {
  let selectContainer = document.querySelector("#slcRating");
  selectContainer.innerHTML = "";
  selectContainer.innerHTML += `<option value="1">✡</option>
  <option value="2">✡✡</option>
  <option value="3">✡✡✡</option>
  <option value="4">✡✡✡✡</option>
  <option value="5">✡✡✡✡✡</option>`
}

 async function addReview(text, rating, place_id, token) {
  let response = await fetch("http://127.0.0.1:5000/api/v1/reviews/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify({ text, rating, place_id })
  })

  if (response.ok) {
    alert('Review added successfully');
    document.querySelector("#review").value = "";
  } else {
    alert('Could not add review : ' + response.statusText);

  }
}
