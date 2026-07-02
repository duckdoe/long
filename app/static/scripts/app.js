const redirectUrl = document;
const urlInput = document.querySelector("#url");
const pwInput = document.querySelector("#password");

const pwErrorMessage = document.querySelector(".password-message");
const urlErrorMessage = document.querySelector(".url-message");

function validateInput(input) {
    let inputText = input.value;

    return (
        inputText.trim() != "" &&
        (inputText.startsWith("http://") || inputText.startsWith("https://"))
    );
}

async function shortenUrlRequest(url, password = null) {
    let success = false;

    let res = await fetch("/api/shorten", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            url,
            password,
        }),
    });

    let data = await res.json();

    if (data.status_code >= 200 && data.status_code <= 300) success = true;
    console.log(res, data);
    return { success, data };
}

const shortenUrlButton = document.querySelector(".js-button");

shortenUrlButton.addEventListener("click", async function () {
    let error = false; // tracks if there is an error

    if (!validateInput(urlInput)) {
        urlInput.style.borderColor = "red"; // Turns input field red

        urlErrorMessage.style.color = "red";
        urlErrorMessage.textContent =
            "Invalid url: urls should start with http:// or https://";

        error = true;
    }
    const url = urlInput.value;
    let password = null;

    if (pwInput.value.trim() != "") password = pwInput.value;

    if (password && password.length < 8) {
        pwInput.style.borderColor = "red";

        pwErrorMessage.style.color = "red"; // Tuen message color red
        pwErrorMessage.textContent =
            "Password must contain atleast 8 characters";

        error = true;
    }

    if (error) return;

    const res = await shortenUrlRequest(url, password);

    if (!res.success) {
        console.error("error: something unexpected happened");
        return;
    }
});
