window.addEventListener('scroll', function () {
    const exploreHeight = document.getElementById('explore').clientHeight;
    const button = document.getElementById('button');
    if (window.scrollY >= exploreHeight) {
        button.style.backgroundColor = 'rgba(26, 137, 23, 1)'
    } else {
        button.style.backgroundColor = 'black'
    }
});
