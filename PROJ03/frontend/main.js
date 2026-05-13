// Loads all the tables and dropdowns upon opening the page
displayArtist();
displayConcert("concert-table");
displayCustomer();
displayTicket();

displayCityDropdown();
displayConcert("concert-city-table");

displayArtistDropdown();
displayConcertByArtist();

displayCustomerDropdown();
displayCustomerSpending();

displayTopArtists();

function showSection(sectionName, clickedItem) {
    // Hide sections except selected one
    const sections = document.querySelectorAll(".content-section");
    sections.forEach(section => {section.classList.add("hidden");});
    document.getElementById(sectionName).classList.remove("hidden");

    // Update active navigation item
    const navItems = document.querySelectorAll(".nav-item");
    navItems.forEach(item => {item.classList.remove("active");});
    clickedItem.classList.add("active");
}

// Displays and hides the different subsections for the Queries tab
function showSubSection(subName, clickedItem) {
    const subSections = document.querySelectorAll(".sub-content");
    subSections.forEach(section => {section.classList.add("hidden");});
    document.getElementById(subName).classList.remove("hidden");

    const subItems = document.querySelectorAll(".sub-item");
    subItems.forEach(item => {item.classList.remove("active");});
    clickedItem.classList.add("active");
}


/* ---------- Functions to Add Records ---------- */

function addArtist() {
    // Retrieve values from the form
    const artistName = document.getElementById("artist-name");
    const genre = document.getElementById("genre");

    // Run php file and pass in values as JSON object
    fetch("../backend/addArtist.php", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            artistName: artistName.value,
            genre: genre.value
        })
    })
    // Print out appropriate message
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            alert(artistName.value + " was successfully added to the database.");

            // Clear form
            artistName.value = "";
            genre.value = "";

            // Update displays
            displayArtist();
            displayArtistDropdown();
        } else
            alert("ERROR: " + data.error);
    });
}

function addConcert() {
    const venueName = document.getElementById("venue-name");
    const city = document.getElementById("city");
    const concertDate = document.getElementById("concert-date");
    const artistId = document.getElementById("artist-id");

    fetch("../backend/addConcert.php", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify ({
            venueName: venueName.value,
            city: city.value,
            concertDate: concertDate.value,
            artistId: artistId.value
        })
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            alert("Concert was successfully added to the database.");

            venueName.value = "";
            city.value = "";
            concertDate.value = "";
            artistId.value = "";

            displayConcert("concert-table");
            displayConcert("concert-city-table");
            displayCityDropdown();
            displayConcertByArtist();
        } else
            alert("ERROR: " + data.error);
    });
}

function addCustomer() {
    const customerName = document.getElementById("customer-name");

    fetch("../backend/addCustomer.php", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({customerName: customerName.value})
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            alert(customerName.value + " was successfully added to the database.");

            customerName.value = "";

            displayCustomer();
            displayCustomerDropdown();
        } else
            alert("ERROR: " + data.error);
    });
}

function addTicket() {
    const concertId = document.getElementById("concert-id");
    const customerId = document.getElementById("customer-id");
    const seatNumber = document.getElementById("seat-number");
    const price = document.getElementById("price");

    fetch("../backend/addTicket.php", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify ({
            concertId: concertId.value,
            customerId: customerId.value,
            seatNumber: seatNumber.value,
            price: price.value
        })
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            alert("Ticket was successfully added to the database.");

            concertId.value = "";
            customerId.value = "";
            seatNumber.value = "";
            price.value = "";

            displayTicket();
            displayCustomerSpending();
            displayTopArtists();
        } else
            alert("ERROR: " + data.error);
    });
}


/* ---------- Functions to Display Database Tables ---------- */

function displayArtist() {
    // Run php file to retrieve table records
    fetch("../backend/getTable.php", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({tableName: "Artist"})
    })
    .then(response => response.json())
    .then(data => {
        // Modify HTML of table element to display records
        const tableRecords = document.getElementById("artist-table");
        tableRecords.innerHTML = data.map(artist => `
            <tr>
                <td>${artist.artist_id}</td>
                <td>${artist.artist_name}</td>
                <td>${artist.genre}</td>
            </tr>
        `).join("")
    });
}

function displayConcert(elementName) {
    fetch("../backend/getTable.php", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({tableName: "Concert"})
    })
    .then(response => response.json())
    .then(data => {
        const tableRecords = document.getElementById(elementName);
        tableRecords.innerHTML = data.map(concert => `
            <tr>
                <td>${concert.concert_id}</td>
                <td>${concert.venue_name}</td>
                <td>${concert.city}</td>
                <td>${concert.concert_date}</td>
                <td>${concert.artist_id}</td>
            </tr>
        `).join("")
    });
}

function displayCustomer() {
    fetch("../backend/getTable.php", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({tableName: "Customer"})
    })
    .then(response => response.json())
    .then(data => {
        const tableRecords = document.getElementById("customer-table");
        tableRecords.innerHTML = data.map(customer => `
            <tr>
                <td>${customer.customer_id}</td>
                <td>${customer.customer_name}</td>
            </tr>
        `).join("")
    });
}

function displayTicket() {
    fetch("../backend/getTable.php", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({tableName: "Ticket"})
    })
    .then(response => response.json())
    .then(data => {
        const tableRecords = document.getElementById("ticket-table");
        tableRecords.innerHTML = data.map(ticket => `
            <tr>
                <td>${ticket.ticket_id}</td>
                <td>${ticket.concert_id}</td>
                <td>${ticket.customer_id}</td>
                <td>${ticket.seat_number}</td>
                <td>${ticket.price}</td>
            </tr>
        `).join("")
    });
}


/* ---------- Functions to Filter Concert by City ---------- */

function displayCityDropdown() {
    // Retrieves all the cities from the Concert table
    fetch("../backend/getCities.php")
    .then(response => response.json())
    .then(data => {
        // Populates dropdown with the cities
        const dropdown = document.getElementById("city-filter");
        dropdown.innerHTML = '<option value="all">Filter by City</option>' +
            data.map(city => `<option value="${city}">${city}</option>`).join("");
    });
}

function filterByCity() {
    const city = document.getElementById("city-filter").value;

    // If 'Filter by City' is selected, show all records from Concert
    if(city == "all") {
        displayConcert("concert-city-table");
        return;
    }

    // Retrieve all the concerts based on the selected city
    fetch("../backend/filterConcertByCity.php", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({city: city})
    })
    .then(response => response.json())
    .then(data => {
        // Modify table to display them
        const tableRecords = document.getElementById("concert-city-table");
        tableRecords.innerHTML = data.map(concert => `
            <tr>
                <td>${concert.concert_id}</td>
                <td>${concert.venue_name}</td>
                <td>${concert.city}</td>
                <td>${concert.concert_date}</td>
                <td>${concert.artist_id}</td>
            </tr>
        `).join("")
    });
}


/* ---------- Functions to Filter Concert by Artist ---------- */

function displayConcertByArtist() {
    fetch("../backend/getConcertByArtist.php")
    .then(response => response.json())
    .then(data => {
        const tableRecords = document.getElementById("concert-artist-table")
        tableRecords.innerHTML = data.map(concert => `
            <tr>
                <td>${concert.artist_name}</td>
                <td>${concert.venue_name}</td>
                <td>${concert.city}</td>
                <td>${concert.concert_date}</td>
            </tr>
        `).join("")
    })
}

function displayArtistDropdown() {
    fetch("../backend/getTable.php", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({tableName: "Artist"})
    })
    .then(response => response.json())
    .then(data => {
        const dropdown = document.getElementById("artist-filter");
        dropdown.innerHTML = '<option value="all">Filter by Artist</option>' +
            data.map(artist => `<option value="${artist.artist_name}">${artist.artist_name}</option>`).join("");
    });
}

function filterByArtist() {
    const artist = document.getElementById("artist-filter").value;

    if(artist == "all") {
        displayConcertByArtist();
        return;
    }

    fetch("../backend/filterConcertByArtist.php", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({artist: artist})
    })
    .then(response => response.json())
    .then(data => {
        const tableRecords = document.getElementById("concert-artist-table");
        tableRecords.innerHTML = data.map(concert => `
            <tr>
                <td>${concert.artist_name}</td>
                <td>${concert.venue_name}</td>
                <td>${concert.city}</td>
                <td>${concert.concert_date}</td>
            </tr>
        `).join("")
    });
}


/* ---------- Functions to View Customer Spending ---------- */

function displayCustomerSpending() {
    fetch("../backend/getCustomerSpending.php")
    .then(response => response.json())
    .then(data => {
        const tableRecords = document.getElementById("customer-spending-table")
        tableRecords.innerHTML = data.map(customer => `
            <tr>
                <td>${customer.customer_id}</td>
                <td>${customer.customer_name}</td>
                <td>${customer.total_spending}</td>
            </tr>
        `).join("")
    })
}

function displayCustomerDropdown() {
    fetch("../backend/getTable.php", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({tableName: "Customer"})
    })
    .then(response => response.json())
    .then(data => {
        const dropdown = document.getElementById("customer-filter");
        dropdown.innerHTML = '<option value="all">Filter by Customer</option>' +
            data.map(customer => `<option value="${customer.customer_name}">${customer.customer_name}</option>`).join("");
    });
}

function filterByCustomer() {
    const customer = document.getElementById("customer-filter").value;

    if(customer == "all") {
        displayCustomerSpending();
        return;
    }

    fetch("../backend/filterByCustomer.php", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({customer: customer})
    })
    .then(response => response.json())
    .then(data => {
        const tableRecords = document.getElementById("customer-spending-table");
        tableRecords.innerHTML = data.map(customer => `
            <tr>
                <td>${customer.customer_id}</td>
                <td>${customer.customer_name}</td>
                <td>${customer.total_spending}</td>
            </tr>
        `).join("")
    });
}


/* ---------- Functions to View Customer Spending ---------- */

function displayTopArtists() {
    fetch("../backend/getTopArtists.php")
    .then(response => response.json())
    .then(data => {
        const tableRecords = document.getElementById("top-artists-table");
        tableRecords.innerHTML = data.map(artist => `
            <tr>
                <td>${artist.artist_name}</td>
                <td>${artist.total_revenue}</td>
            </tr>
        `).join("")
    })
}