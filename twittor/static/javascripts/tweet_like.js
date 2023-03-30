function tweet_like(id) {
    console.log(id);
    fetch('/edit_tweet/' + id, {
        headers: {
            'Content-Type': 'application/json',
        },
        method: 'POST',
        body: JSON.stringify({
            request_button: 'Like',
        }),
    })
        .then(function (response) {
            if (response.ok) {
                console.log(response.statusText);
                response.json().then(function (data) {
                    console.log(data);
                });
                window.location.reload();
            } else {
                throw Error('Something went wrong!');
            }
        })
        .catch(function (error) {
            console.log(error);
        });
}

function tweet_unlike(id) {
    fetch('/edit_tweet/' + id, {
        headers: {
            'Content-Type': 'application/json',
        },
        method: 'POST',
        body: JSON.stringify({
            request_button: 'Unlike',
        }),
    })
        .then(function (response) {
            if (response.ok) {
                console.log(response.statusText);
                response.json().then(function (data) {
                    console.log(data);
                });
                window.location.reload();
            } else {
                throw Error('Something went wrong!');
            }
        })
        .catch(function (error) {
            console.log(error);
        });
}

function tweet_delete(id) {
    fetch('/edit_tweet/' + id, {
        headers: {
            'Content-Type': 'application/json',
        },
        method: 'POST',
        body: JSON.stringify({
            request_button: 'Delete',
        }),
    })
        .then(function (response) {
            if (response.ok) {
                console.log(response.statusText);
                response.json().then(function (data) {
                    console.log(data);
                });
                window.location.reload();
            } else {
                throw Error('Something went wrong!');
            }
        })
        .catch(function (error) {
            console.log(error);
        });
}
