const redirectUrl = document;
const urlInput = document.querySelector("#url");
const pwInput = document.querySelector("#password");

function validateInput(input) {
    let inputText = input.value;
    return inputText.trim() != "";
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
    if (!validateInput(urlInput)) {
        console.error("error: url input is empty");
        return;
    }
    const url = urlInput.value;
    let password = null;

    if (pwInput.value.trim() != "") password = pwInput.value;

    const res = await shortenUrlRequest(url, password);

    if (!res.success) {
        console.error("error: something unexpected happened");
        return;
    }

    console.log("Success", res);
});
