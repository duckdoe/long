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

function popUp(
    success /*decides whether to show error or success popup*/,
    details /* object determines what gets embedded in the body*/,
) {
    const messagePopUp = document.querySelector(".message-popup");
    const overlay = document.querySelector(".overlay");

    const errorHtml = `<h2 class="title" style="color: red;">Error:</h2>
            <div class="body">
                <p>${details.detail}</p>
            </div>`;

    const successHtml = `<h2 class="title" style="color: green;">Success:</h2>
            <div class="body">
                <p class="detail">Yay, your link is shorter now!</p>
                <div class="url-container">
                    <p class="url">${window.origin}/u/${details.id}</p>
                </div>
                <button class="copy-btn">Copy Link</button>
            </div>`;

    if (success) {
        messagePopUp.innerHTML = successHtml;
    } else {
        messagePopUp.innerHTML = errorHtml;
    }

    overlay.classList.add("overlay-active");
    messagePopUp.classList.add("active");
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

    if (
        (data.status_code >= 200 && data.status_code <= 300) ||
        data.visits == 0
    )
        success = true;
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

        pwErrorMessage.style.color = "red"; // Turn message color red
        pwErrorMessage.textContent =
            "Password must contain atleast 8 characters";

        error = true;
    }

    if (error) return;

    pwInput.value = "";
    urlInput.value = "";

    const res = await shortenUrlRequest(url, password);
    popUp(res.success, res.data);
});
