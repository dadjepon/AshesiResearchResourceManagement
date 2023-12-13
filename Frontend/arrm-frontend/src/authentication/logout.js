import { customFetch, handleUnauthorizedError } from "./token_middleware";

const logout_button = document.getElementById("logout");

async function logout() {
    try {
        const response = await customFetch("http://127.0.0.1:8000/api/account/logout/", {
            method: "POST",
            body: {}
        });

        if (response.ok) {
            // remove stored access and refresh tokens
            document.cookie = "access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
            document.cookie = "refresh_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";

            // redirect to login page
            handleUnauthorizedError();
        } else if (response.status === 401) {
            handleUnauthorizedError();
        } else {
            console.log("ERROR");
        }
    } catch (error) {
        console.log(error);
    }
};

logout_button.addEventListener("click", () => {
    setTimeout(logout, 1000);
});