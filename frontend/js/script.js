// ------------------ Login Form Submission ------------------ //
document.getElementById('loginForm')?.addEventListener('submit', function(e) {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    fetch('/api/users/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Login Response:', data);
        if (data.token) {
            alert(data.message || 'Login successful!');
            // Optional: Store token in localStorage
            // localStorage.setItem("token", data.token);
            window.location.href = 'dashboard.html';
        } else {
            alert(data.error || 'Invalid login credentials');
        }
    })
    .catch(error => {
        console.error('Login Error:', error);
        alert('An error occurred during login.');
    });
});

// ------------------ Logout ------------------ //
document.getElementById('logoutBtn')?.addEventListener('click', function() {
    fetch('/api/users/logout', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            console.log('Logout Response:', data);
            alert(data.message || 'Logged out');
            window.location.href = 'http://192.168.0.105:5000/';
        })
        .catch(error => {
            console.error('Logout Error:', error);
            alert('An error occurred during logout.');
        });
});

// ------------------ Register Form Submission ------------------ //
document.getElementById('registerForm')?.addEventListener('submit', function(e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    console.log("Register form submitted");
    console.log("Username:", username, "Email:", email, "Password:", password);

    fetch('/api/users/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Register Response:', data);
        if (data.message) {
            alert(data.message);
            window.location.href = 'index.html'; // Redirect to login or welcome page
        } else {
            alert(data.error || 'Registration failed');
        }
    })
    .catch(error => {
        console.error('Registration Error:', error);
        alert('An error occurred during registration.');
    });
});
