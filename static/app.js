const navLogout = $('#navLogout');
const navRegister = $('#navRegister');
const navLogin = $('#navLogin');

// navbar link redirects
navLogin.click(() => (window.location.href = '/login'));
navLogout.click(() => (window.location.href = '/logout'));
navRegister.click(() => (window.location.href = '/register'));
