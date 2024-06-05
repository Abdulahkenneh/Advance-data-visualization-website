document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('.post-link').forEach(function(postLink) {
        postLink.addEventListener('click', function(event) {
            event.preventDefault();
            const postId = this.getAttribute('data-post-id');
            fetch(`/blogs/home/?post_id=${postId}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                document.querySelector('.post-title').textContent = data.title;
                document.querySelector('.post-content').innerHTML = `<p>${data.content}</p>`;
            })
            .catch(error => console.error('Error fetching post:', error));
        });
    });
});