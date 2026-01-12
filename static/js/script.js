document.addEventListener('DOMContentLoaded', function() {
    // Track visit
    fetch('/track/visit', { method: 'POST' });

    // Track appstore click
    document.getElementById('appstore').addEventListener('click', function() {
        fetch('/track/appstore', { method: 'POST' });
    });

    // Track playmarket click
    document.getElementById('playmarket').addEventListener('click', function() {
        fetch('/track/playmarket', { method: 'POST' });
    });

    // Track email click
    document.getElementById('email').addEventListener('click', function() {
        fetch('/track/email', { method: 'POST' });
    });

    // Track telegram click
    document.getElementById('telegram').addEventListener('click', function() {
        fetch('/track/telegram', { method: 'POST' });
    });
});