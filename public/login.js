$( document ).ready(function() {
    let reponse = prompt("Enter the Token");
    $.cookie("token", reponse, {expires: 30, path: '/'});
    window.location.reload();
});