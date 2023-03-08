$(document).keypress(function (e) {
    if (e.which == 13) {
            document.getElementById("authBtn").click();
    }
});

function auth() {
    let username = document.getElementById("username").value
    let password = document.getElementById("password").value

    var formData = {"username": username, "password": password};
    $.ajax({
        url: "/auth/jwt/login",
        type: "POST",
        data: formData,
        success: function (data, textStatus, jqXHR) {
            window.location.href = '/home';
        },
        error: function (jqXHR, textStatus, errorThrown) {
            alert("Ошибочка вышла((");
            console.log(textStatus);
            console.log(errorThrown);
        }
    });
}