function FBlogin() {
    FB.login(
        function (response) {
            var obj = {
                userID: response.authResponse.userID,
                accessToken: response.authResponse.accessToken,
            };
            var data_json = JSON.stringify(obj);
            $.ajax({
                url: '/API_FB_login',
                type: 'POST',
                data: data_json,
                dataType: 'json',
                async: false,
                contentType: 'application/json',
                success: function (data, textStatus, jqXHR) {
                    if (data == 'FB_login_OK') {
                        location.replace('/index');
                    }
                },
                error: function () {
                    document.getElementById('population').innerHTML = 'Error Login.';
                },
            });
        },
        {
            scope: 'publish_actions, email, user_friends',
            return_scope: true,
        }
    );
}

function fetchUserDetail() {
    FB.api('/me', function (response) {
        console.log('Successful login for: ' + response.name);
    });
    location.replace('/index');
}

function checkFBlogin() {
    // Called when a person is finished with the Login Button.
    FB.getLoginStatus(function (response) {
        // See the onlogin handler
        console.log('statusChangeCallback' + response); // The current login status of the person.
        if (response.status === 'connected') {
            // Logged into your webpage and Facebook.
            fetchUserDetail();
        } else {
            // Not logged into your webpage or we are unable to tell.
            FBlogin();
            console.log('please log into this Facebook.');
            // document.getElementById('status').innerHTML = 'Please log ' + 'into this webpage.';
        }
    });
}
