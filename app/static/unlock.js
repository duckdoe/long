const code = window.location.pathname.split("/").pop();
const pwInput = document.querySelector("#password");

async function unlockRedirectUrl(password) {
    let success = false;

    let res = await fetch(`/api/unlock/${code}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            password,
        }),
    });

    let data = await res.json();

    return data;
}

const submitButton = document.querySelector(".js-button");

submitButton.addEventListener("click", async function () {
    if (pwInput.value.trim == "") return;

    const res = await unlockRedirectUrl(pwInput.value);

    if (res.status_code > 299 || res.status_code < 200) {
        console.error("Something uexpected happened");
        return;
    }

    window.location.assign(res.url);
});
