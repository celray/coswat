
function cj_login_modal(modal_id) {
    

}

function open_cj_modal(modal_id) {
    var modal_obj = document.getElementById(modal_id);

    modal_obj.style.visibility = 'visible';

    modal_obj.classList.remove('my-awesome-modal-closed');
    modal_obj.classList.add('my-awesome-modal');
}

function close_cj_modal(modal_id) {
    var modal_obj = document.getElementById(modal_id);

    modal_obj.classList.remove('my-awesome-modal');
    modal_obj.classList.add('my-awesome-modal-closed');
    modal_obj.style.visibility = 'collapsed';
}

function show_profile_dropdown(){
    var profile_menu = document.getElementById('profile-menu');
    

    if (profile_menu.classList.contains('default-0h')){
        profile_menu.classList.remove('default-0h');
        profile_menu.classList.add('login-profile-menu-open');
    } else {
        if (profile_menu.classList.contains('login-profile-menu-closed')){
            profile_menu.classList.remove('default-0h');
            profile_menu.classList.remove('login-profile-menu-closed');
            profile_menu.classList.add('login-profile-menu-open');
        } else {

            
                profile_menu.classList.remove('login-profile-menu-open');
                profile_menu.classList.add('login-profile-menu-closed');
        }
    }
}

function signup_page(){
    window.location = "/signup";
}

/**
  * @param {String} url - address for the HTML to fetch
  * @return {String} the resulting HTML string fragment
  */
async function fetchHtmlAsText(url) {
    const response = await fetch(url);
    return await response.text();
}

// this is your `load_home() function`
async function loadHome() {
    const contentDiv = document.getElementById("content");
    contentDiv.innerHTML = await fetchHtmlAsText("home.html");
}