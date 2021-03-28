window.addEventListener('DOMContentLoaded', function () {
    hideLoader();
    window.addEventListener('scroll', function () {
        const exploreHeight = document.getElementById('explore').clientHeight;
        const button = document.getElementById('button');
        if (window.scrollY >= exploreHeight) {
            button.style.backgroundColor = 'rgba(26, 137, 23, 1)';
        } else {
            button.style.backgroundColor = 'black';
        }

        const {
            scrollTop,
            scrollHeight,
            clientHeight
        } = document.documentElement;

        if (scrollTop + clientHeight >= scrollHeight - 5) {
            fetchPosts();
        }
    });
});

function hideLoader() {
    const loader = document.getElementById('loader');
    loader.style.display = 'none';
}

function showLoader() {
    const loader = document.getElementById('loader');
    loader.style.display = 'block';
}

async function fetchPosts() {
    showLoader();

    setTimeout(async () => {
        try {
            const API_URL = `https://localhost:5000/posts`;
            const response = await fetch(API_URL);
            if (!response.ok) {
                throw new Error(`An error occurred: ${response.status}`);
            }

            const responseJson = await response.json();
            showPosts(responseJson);
        } catch (error) {
            console.log(error.message);
        } finally {
            hideLoader();
        }
    }, 500);
}

function showPosts(posts) {
    const postsEl =  document.getElementById('posts');
    posts.forEach(post => {
        const postEl = document.createElement('div');
        postEl.classList.add('post');

        const content = document.createElement('div');
        content.classList.add('content');

        const author = document.createElement('div');
        author.classList.add('author');

        postEl.innerHTML = `
            <div class="content">
                <div class="author">
                    <img src="${post.author_img}" alt="author-image" />
                    <span>${post.author_name}</span>
                </div>
                <a href="${post.url}">
                    <h3 class="blog-title">${post.title}</h3>
                    <p class="short-description">${post.short_description}</p>
                </a>
                <div class="bottom">
                    <p class="date">${post.date} · ${post.time} min read</p>
                    <svg width="25" height="25" viewBox="0 0 25 25" class="ln">
                        <path d="M19 6a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v14.66h.01c.01.1.05.2.12.28a.5.5 0 0 0 .7.03l5.67-4.12 5.66 4.13a.5.5 0 0 0 .71-.03.5.5 0 0 0 .12-.29H19V6zm-6.84 9.97L7 19.64V6a1 1 0 0 1 1-1h9a1 1 0 0 1 1 1v13.64l-5.16-3.67a.49.49 0 0 0-.68 0z" fill-rule="evenodd"></path>
                    </svg>
                </div>
            </div>
            <a href="${post.url}">
                <img src="${post.post_image}" alt="post-image" />
            </a>
        `;

        postsEl.appendChild(postEl);
    });
};
