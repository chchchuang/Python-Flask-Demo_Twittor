function logout() {
    FB.getLoginStatus(function (response) {
        if (response.status === 'connected') {
            FB.logout(function (response) {});
        }
    });
    location.replace('/logout');
}
