function clearEditView(postId) {

    // Remove textarea, save button and cancel button
    document.getElementById(`textarea_${postId}`).remove()
    document.getElementById(`save_${postId}`).remove()
    document.getElementById(`cancel_${postId}`).remove()

    // Show content, edit button and no of likes
    document.getElementById(`post_content_${postId}`).style.display = 'block';
    document.getElementById(`edit_${postId}`).style.display = 'inline-block';
    document.getElementById(`post_likes_${postId}`).style.display = 'block';
}

// Adds validation message within parentDiv
function addValidationMessage(message, parentDiv) {
    // Add validation message
    const warningMessage = document.createElement('p');
    warningMessage.innerHTML = message;
    warningMessage.className = 'text-danger';

    document.getElementById(parentDiv).append(warningMessage);
}

// Updates no of likes for a given ID
function updateLikes(id, likes) {
    const likesCount = document.querySelector(`#post_likecount_${id}`);
    likesCount.innerHTML = likes;
}

document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', event => {
        const element = event.target;

        // 첫번쨰, If the user clicked on a like icon
        if (element.id.startsWith('post_likeicon_')) {
            let id = element.dataset.id;

            fetch(`/updatelike/${id}`, {
                method: 'POST'
            })
            .then((response) => response.json())
            .then((data) => {
                const likes = data.likesCount;
                const likesPost = data.likesPost;

                let likeIcon = document.querySelector(`#post_likeicon_${id}`);

                updateLikes(id, likes);

                if (likePost) {
                    likeIcon.className = 'likeicon fa-heart fas';
                } else {
                    likeIcon.className = 'likeicon fa-heart far';
                }
            }).catch((ex) => {
                console.log("parsing failed", ex);
            });
        }

        // 2번쨰, If the thing the user clicked is the edit button
        if (element.id.startsWith('edit_')) {

            const editButton = element;
            const postId = editButton.dataset.id;
            const postText = document.getElementById(`post_content_${postId}`);

            let textArea = document.createElement('textarea');
            textArea.innerHTML = postText.innerHTML;
            textArea.className = 'form-control';
            textArea.id = `textarea_${postId}`;
            document.querySelector(`#post_contentgroup_${postId}`).append(textArea);

            // Hide textArea of content before u click editbutton, hide editbutton, hide likes
            postText.style.display = 'none';
            editButton.style.display = 'none';
            document.getElementById(`post_likes_${postId}`).style.display = 'none';

            // Add 'cancel' button
            const cancelButton = document.createElement('button');
            cancelButton.className = 'btn btn-outline-danger cancel-badge badge ml-1 text-right btn-sm';
            cancelButton.innerHTML = 'Cancel';
            cancelButton.id = `cancel_${postId}`;

            // Add 'save' button
            const saveButton = document.createElement('button');
            saveButton.className = 'btn green-button btn-sm mt-2 px-2';
            saveButton.innerHTML = 'Save';
            saveButton.id = `save_${postId}`;

            // Append each button into DOM
            document.getElementById(`save_buttons_${postId}`).append(saveButton);
            document.getElementById(`post_headline_${postId}`).append(cancelButton);

            // Make eventlistener when u click buttons
            cancelButton.addEventListener('click', function() {
                clearEditView(postId);
            });
            // Fetch request when the user clicks 'save' button
            saveButton.addEventListener('click', function() {

                textArea = document.getElementById(`textarea_${postId}`);

                fetch(`/editpost/${postId}`, {
                    method: 'POST',
                    body: JSON.stringify({
                        content: textArea.value,
                    })
                })
                .then(response => response.json())
                .then((result) => {
                    console.log(result)

                    if (!result.error) {
                        postText.innerHTML = result.content;
                        clearEditView(postId);
                    } else {
                        clearEditView(postId);
                        editButton.sytle.display = 'none';
                        addValidationMessage(result.error, `post_contentgroup_${postId}`);
                    }
                })
                .catch(error => {
                    console.error(error);
                })
            })

        }

    })
})

