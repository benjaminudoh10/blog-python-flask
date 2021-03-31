document.addEventListener('DOMContentLoaded', () => {
    const deleteButtons = document.querySelectorAll('.delete');
    for (const button of deleteButtons) {
        button.addEventListener('click', async () => {
            const storyId = button.attributes['data-id'].nodeValue;
            const confirmDelete = confirm('Are you sure you want to delete this article?');
            if (!confirmDelete) return;
            const response = await fetch(`${window.location.origin}/story/${storyId}`, {
                method: 'DELETE',
                mode: 'cors',
                headers: {
                  'Content-Type': 'application/json'
                },
            });

            if (!response.ok) {
                alert('Error occured while trying to delete article. Try again later.');
                throw new Error(`An error occurred: ${response.status}`);
            }

            const responseJson = await response.json();
            if (responseJson.status === 200) {
                alert(responseJson.message);
                setTimeout(() => {
                    window.location.reload();
                }, 2000);
            }
        });
    }
});
