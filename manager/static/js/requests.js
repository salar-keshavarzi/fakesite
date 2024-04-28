const getReq = async (uri, type = 1) => {
    let url = uri;
    if (type !== 1) {
        url = baseUrl + uri;
    }
    return await fetch(url).then(response => {
        return response.json();
    }).catch(err => {
        console.error(err);
        throw err;
    })
}
const postReq = async (uri, data = null, csrf = null, type = 1) => {
    let url = uri;
    if (type !== 1) {
        url = baseUrl + uri;
    }
    return await fetch(url, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": csrf
        },
    }).then(response => {
        if (response.status === 429) {
            const retryAfter = response.headers.get('Retry-After');
            return {statusCode: response.status, data: {'retryAfter': retryAfter}};
        }
        return response.json().then(data => ({statusCode: response.status, data: data}));
    }).catch(err => {
        console.error(err);
        throw err;
    })
}

const deleteReq = async (uri, csrf = null, type = 1) => {
    let url = uri;
    if (type !== 1) {
        url = baseUrl + uri;
    }
    return await fetch(url, {
        method: "DELETE",
        body: null,
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": csrf
        }
    }).then(response => {
        return true;
    }).catch(err => {
        throw err;
    })
}
const putReq = async (uri, data = null, csrf = null, type = 1) => {
    let url = uri;
    if (type !== 1) {
        url = baseUrl + uri
    }
    return await fetch(url, {
        method: "PUT",
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": csrf
        },
    }).then(response => {
        return response.json().then(data => ({statusCode: response.status, data: data}));
    }).catch(err => {
        console.error(err);
        throw err;
    })
}