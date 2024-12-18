document.addEventListener('DOMContentLoaded', () => {
    // Follow or Unfollow user
    const followBtn = document.querySelector('#followBtn');
    const followerCount = document.querySelector('#followerCount');
    if (followBtn) {
        const profileId = followBtn.dataset.user;
        followBtn.addEventListener('click', async () => {
            const res = await fetch('/follow/' + profileId);
            const data = await res.json();
            if (data.message === 'Followed') {
                followBtn.textContent = 'Unfollow';
                followerCount.textContent = parseInt(followerCount.textContent) + 1
            } else {
                followBtn.textContent = 'Follow';
                followerCount.textContent = parseInt(followerCount.textContent) - 1
            }
        });
    }
})

function editPost(id)  {
    const postContent = document.getElementById('postContent-' + id);
    const editPostBtn = document.getElementById('editPostBtn-' + id);
    const editorForm = document.getElementById('editorForm-' + id);
    const editorTextarea = document.getElementById('editorTextarea-' + id);

    editPostBtn.classList.add('d-none');
    editorForm.classList.remove('d-none');

    editorTextarea.value = postContent.textContent;
    editorTextarea.focus();
    
    editorForm.addEventListener('submit', async (e) => {
        postContent.innerHTML = editorTextarea.value;
        editPostBtn.classList.remove('d-none');
        editorForm.classList.add('d-none');
        return false;
    });
}

