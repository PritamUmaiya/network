document.addEventListener('DOMContentLoaded', () => {
    // Follow or Unfollow user
    const followBtn = document.querySelector('#followBtn');
    const followerCount = document.querySelector('#followerCount');
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

})