document.addEventListener('DOMContentLoaded', function () {
    const commentBox = document.getElementById('comments');
    const textArea = document.getElementById('comment');
    const button = document.getElementById('post-comment');
    const showComment = document.getElementById('comments-open');
    const tweet = document.getElementById('twitter-share');
    textArea.addEventListener('input', function () {
        if (textArea.value && textArea.value.trim()) {
            button.disabled = false;
        } else {
            button.disabled = true;
        }
    });

    button.addEventListener('click', async function () {
        const data = {
            comment: textArea.value?.trim(),
        }

        await postComment(data);
        textArea.value = "";
    });

    showComment.addEventListener('click', function () {
        if (commentBox.classList.contains('open')) {
            commentBox.classList.remove('open');
        } else {
            commentBox.classList.add('open');
        }
    });

    tweet.addEventListener('click', function () {
        const text = `I just published a new article. Please check it out. ${window.location.href}`;
        window.open(`https://twitter.com/intent/tweet?text=${encodeURI(text)}`, '_blank').focus();
    });
});

async function postComment(data) {
    const articleId = window.location.href.split('/story/')[1];
    await fetch(`${window.location.origin}/comment/${articleId}`, {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
}
