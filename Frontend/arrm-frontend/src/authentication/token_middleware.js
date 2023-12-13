import React from "react";
import { useNavigate } from "react-router-dom";
import AuthenticationError from "./errors.js";

const navigate = useNavigate();

function getRefreshToken() {
    const cookies = document.cookie.split('; ');

    for (const cookie of cookies) {
        const [name, value] = cookie.split('=');
        if (name === 'refresh_token') {
            console.log(value);
            return value;
        }
    }
    return null;
}

function updateAccessToken(newAccessToken) {
    document.cookie = `access_token=${newAccessToken}`; // update the 'access_token' cookie
}

function handleRefreshTokenError() {
    // redirect to the login page
    navigate('/loginpage', { replace: true });
}

function getAccessToken() {
    const cookies = document.cookie.split('; ');
    for (const cookie of cookies) {
        const [name, value] = cookie.split('=');
        if (name === 'access_token') {
            return value;
        }
    }
    return null;
}

function handleUnauthorizedError() {
    // redirect to the login page
    navigate('/loginpage', { replace: true });
}

const refreshAccessToken = async () => {
    const refreshToken = getRefreshToken();
    if (!refreshToken) {
        handleRefreshTokenError();
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/api/account/token/refresh/access/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ refresh: refreshToken }),
        });

        if (response.ok) {
            const responseData = await response.json();
            const newAccessToken = responseData.access;
            updateAccessToken(newAccessToken);
            return newAccessToken;
        } else {
            handleRefreshTokenError();
        }
    } catch (error) {
        handleRefreshTokenError();
    }
};

const customFetch = async (url, options) => {
    const accessToken = getAccessToken();

    if (!accessToken) {
        accessToken = await refreshAccessToken();
    } 
    
    if (!accessToken) {
        handleUnauthorizedError();
        return;
    }

    try {
        return await fetch(url, {
            ...options,
            headers: {
                ...options.headers,
                Authorization: `Bearer ${accessToken}`,
            },
        });
    } catch (error) {
        if (error instanceof AuthenticationError) {
            const newAccessToken = await refreshAccessToken();
            if (newAccessToken) {
                return await fetch(url, {
                    ...options,
                    headers: {
                        ...options.headers,
                        Authorization: `Bearer ${newAccessToken}`,
                    },
                });
            } else {
                handleUnauthorizedError();
            }
        }
    }
};

export { customFetch, handleUnauthorizedError };