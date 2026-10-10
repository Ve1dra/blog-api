const usernameField = document.getElementById("username");
const emailField = document.getElementById("email");
const phoneField = document.getElementById("number");
const dobField = document.getElementById("dob");
const passwordField = document.getElementById("password");
const confirmPasswordField = document.getElementById("c_password");
const button = document.getElementById("button")

// Helper function to show error or success
function showMessage(fieldId, message, isValid) {
    const span = document.getElementById(fieldId + "Error");
    span.textContent = message;
    span.className = isValid ? "success" : "error";
}

// Name validation
usernameField.addEventListener("input", () => {
    const value = usernameField.value.trim();
    if (/^[A-Za-z0-9\s]{3,10}$/.test(value)) {
    showMessage("username", "Username is valid.", true);
    } else {
    showMessage("username", "Enter not more than 10 and not less than 3 characters.", false);
    }
});

// Email validation
emailField.addEventListener("input", () => {
    const value = emailField.value.trim();
    if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
    showMessage("email", "Valid email!", true);
    } else {
    showMessage("email", "Invalid email format/email.", false);
    }
});

// Nigerian phone validation
phoneField.addEventListener("input", () => {
    const value = phoneField.value.trim().replace(/[\s-]/g, "");
    if (/^(\+234|0)[789][01]\d{8}$/.test(value)) {
    showMessage("number", "Valid Nigerian number!", true);
    } else {
    showMessage("number", "Must start with +234 and be valid.", false);
    }
});

// DOB validation (18+ years)
dobField.addEventListener("change", () => {
    const birthDate = new Date(dobField.value);
    const today = new Date();
    const age = today.getFullYear() - birthDate.getFullYear();
    const cutoff = new Date(today.setFullYear(today.getFullYear() - 18));
    if (!dobField.value) {
    showMessage("dob", "Please enter your date of birth.", false);
    } else if (birthDate > cutoff) {
    showMessage("dob", "You must be at least 18.", false);
    } else {
    showMessage("dob", "Valid age!", true);
    }
});

// Password validation
passwordField.addEventListener("input", () => {
    const value = passwordField.value;
    if (/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$/.test(value)) {
    showMessage("password", "Strong password!", true);
    } else {
    showMessage("password", "Min 8 chars, upper, lower, number, special.", false);
    }
});

// Confirm password validation
confirmPasswordField.addEventListener("input", () => {
if (confirmPasswordField.value === passwordField.value) {
    showMessage("c_password", "Passwords match!", true);
    button.disabled = false
} else {
    button.disabled = true
    showMessage("c_password", "Password mismatch!", false)
}
});

// Final check on submit
//     e.preventDefault();
//     if (nameField.value === ""){
    //         showMessage("usename", "Please input a username", false)
    //     }
    
    // });
    
    
const url = "https://blog-api-n1d5.onrender.com/api/v1/auth/signup/"

const btn = document.getElementById("registerForm")
btn.addEventListener('submit', async (e)=>{
    e.preventDefault();
    const body = {
        username: usernameField.value,
        email: emailField.value,
        phone: phoneField.value,
        dob: dobField.value,
        password: passwordField.value,
    }
    await fetch(url, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(body)
    })
    .then(Response => {
        if (!Response.ok) throw new Error(alert("API could not be fetched"))
            return Response.json()
    })
    .then(data => {
        window.location.href = '/templates/accounts/login.html'
    })
    .catch(e => alert(e.message))
})