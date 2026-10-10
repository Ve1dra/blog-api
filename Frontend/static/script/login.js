const username= document.getElementById("username")
const password = document.getElementById("password")
const loginForm = document.getElementById("loginForm")
const loginBtn = document.getElementById("loginBtn")

const URL = "https://blog-api-n1d5.onrender.com/api/v1/auth/login/"

function showMessage(fieldId, message, isValid) {
    const span = document.getElementById(fieldId + "Error");
    span.textContent = message;
    span.className = isValid ? "success" : "error";
}

username.addEventListener("input", () => {
    const value = username.value.trim();
    if (/^[A-Za-z0-9\s]{3,10}$/.test(value)) {
    showMessage("username", "Username is valid.", true);
    } else {
    showMessage("username", "Enter at least 3 characters.", false);
    }
});

password.addEventListener("input", () => {
    const value = password.value;
    if (/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$/.test(value)) {
    showMessage("password", "Strong password!", true);
    } else {
    showMessage("password", "Min 8 chars, upper, lower, number, special.", false);
    }
});

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    console.log("Loading...")
    const body = {
        username: username.value,
        password: password.value
    }
    await fetch(URL, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(body)
    }).then(Response => {
        if (!Response.ok) throw new Error("API couldn't be fetched.")
            return Response.json()
    }).then(data =>{
        console.log(data)
        const payload = JSON.parse(atob(data.token.access_token.split('.')[1]));
        console.log(payload)

        localStorage.setItem('access_token', data.token.access_token)
        localStorage.setItem('refresh_token', data.token.refresh_token)
        window.location.href = '/templates/protected/market_page.html'

    })
    .catch(e => alert(e.message))
})