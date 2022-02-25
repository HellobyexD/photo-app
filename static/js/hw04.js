const story2Html = story => {
    return `
        <div>
            <img src="${ story.user.thumb_url }" class="pic" alt="profile pic for ${ story.user.username }" />
            <p>${ story.user.username }</p>
        </div>
    `;
};

const user2Html = user => {
    return `
    <section>
        <img src="${user.thumb_url }" class="pic" alt="Profile pic for ${ user.username }" />
        <div>
            <p class="username">${user.username}</p>
            <p>suggested for you</p>
        </div>
        <div>
            <button 
                class="follow" 
                aria-label="Follow"
                aria-checked="false"
                data-user-id="${user.id}" 
                onclick="toggleFollow(event);">follow</button>
        </div>
    </section>
    `;
};

const caption2Html = post => {
    return `
    <section>
        <img src="${post.user.thumb_url}" alt="Profile pic for ${ post.user.username }" />
        <div>
            <p>
                <strong>${post.user.username}</strong>
                ${ post.caption }
            </p>
            <div>
                <strong>${post.display_time}</strong>
            </div>
        </div>
        <button>
            <i class="far fa-heart"></i>
        </button>
    </section>
    `
};

// modal representation only
const comment2Html = comment => {
    return `
    <section>
        <img src="${comment.user.thumb_url}" alt="Profile pic for ${ comment.user.username }" />
        <div>
            <p>
                <strong>${comment.user.username}</strong>
                ${ comment.text }
            </p>
            <div>
                <strong>${comment.display_time}</strong>
            </div>
        </div>
        <button>
            <i class="far fa-heart"></i>
        </button>
    </section>
    `
};

const post2Html = post => {
    return `
    <section class="card">
        <div class="header">
            <h3>${ post.user.username }</h3>
            <i class="fa fa-dots"></i>
        </div>
        <img src="${ post.image_url }" alt="Image posted by ${ post.user.username }" width="300" height="300">
        <div class="info">
            <div class="buttons">
                <div>
                    <button 
                        onclick="likeUnlike(event, ${ post.id })" 
                        aria-label="Like"
                        aria-checked="${ post.current_user_like_id ? 'true' : 'false' }">
                        <i class="fa${ post.current_user_like_id ? 's' : 'r' } fa-heart" data-like-id="${ post.current_user_like_id ? post.current_user_like_id : "" }"></i>
                    </button>
                    <i class="far fa-comment"></i>
                    <i class="far fa-paper-plane"></i>
                </div>
                <div>
                    <button 
                        onclick="bookmarkUnbookmark(event, ${ post.id })"
                        aria-label="Bookmark"
                        aria-checked="${ post.current_user_bookmark_id ? 'true' : 'false' }">
                        <i class="fa${ post.current_user_bookmark_id ? 's' : 'r' } fa-bookmark" data-bookmark-id="${ post.current_user_bookmark_id ? post.current_user_bookmark_id : "" }"></i>
                    </button>
                </div>
            </div>
            <p class="likes">
                <strong>${ post.likes.length } like${post.likes.length != 1 ? 's' : ''}</strong>
            </p>
            <div class="caption">
                <p>
                    <strong>${ post.user.username }</strong> 
                    ${ post.caption }
                </p>
                <div class="timestamp">
                    ${ post.display_time }
                </div>
            </div>
        </div>
        <div class="comments">
            ${ displayComments(post.comments, post.id) }
        </div>
    </section>
    `
};

const toggleFollow = ev => {
    const elem = ev.currentTarget;

    if (elem.getAttribute('aria-checked') == 'false') {
        // issue post request:
        followUser(elem.dataset.userId, elem);
    } else {
        // issue delete request:
        unfollowUser(elem.dataset.followingId, elem);
    }
}

const followUser = (userId, elem) => {
    const postData = {
        "user_id": userId
    };
    
    fetch("/api/following/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': getCookie('csrf_access_token')
            },
            body: JSON.stringify(postData)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            elem.innerHTML = 'unfollow'


            elem.setAttribute('aria-checked', 'true');

            elem.classList.add('unfollow');
            elem.classList.remove('follow');
            // in the event that we want to unfollow this user:
            elem.setAttribute('data-following-id', data.id);
        });
};

const unfollowUser = (followingId, elem) => {
    // issue a delete request:
    const deleteURL = `/api/following/${followingId}`;
    fetch(deleteURL, {
        method: "DELETE", 
        headers: {
            'X-CSRF-TOKEN': getCookie('csrf_access_token')
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        elem.innerHTML = 'follow'
        elem.setAttribute('aria-checked', 'false');
        elem.classList.add('follow');
        elem.classList.remove('unfollow');
        elem.removeAttribute('data-following-id');
    });
};

const destroyModal = ev => {
    document.querySelector('#modal-container').innerHTML = "";
    const button = document.getElementById('last');
    button.id = "";
    button.focus();
};

const showPostDetail = ev => {
    const button = ev.currentTarget
    button.id = "last";
    const postId = button.dataset.postId;
    fetch(`/api/posts/${postId}`)
        .then(response => response.json())
        .then(post => {
            const html = `
                <div class="modal-bg">
                    <button onclick="destroyModal(event)" aria-label="Close" aria-checked="false">
                        <i class="fas fa-times"></i>
                    </button>
                    <div class="modal">
                        <img src="${post.image_url}" />
                        <div class="modal-text">
                            <header>
                                <img src="${ post.user.thumb_url }" alt="Profile pic for ${ post.user.username }" />
                                <h3>${ post.user.username }</h3>
                            </header>
                            <div class="modal-comments">
                                ${ caption2Html(post) }
                                ${ post.comments.map(comment2Html).join('\n') }
                            </div>
                        </div>
                    </div>
                </div>`;
            document.querySelector('#modal-container').innerHTML = html;
            let closeButton = document.querySelector('.modal-bg').querySelector('button')
            closeButton.addEventListener("keydown", event => {
                if (event.code == "Escape") {
                    destroyModal(event);
                }
            })
            closeButton.focus();
        })
    
};

const updateLikeCount = (likeCount, postId) => {
    const postURL = `/api/posts/${postId}`
    fetch(postURL, {
    })
    .then(response => response.json())
    .then(data => {
        const html = `<strong>${ data.likes.length } like${data.likes.length != 1 ? 's' : ''}</strong>`
        likeCount.innerHTML = html;
    });
};


const likeUnlike = (ev, postId) => {
    const elem = ev.currentTarget;
    const icon = elem.querySelector('i');

    if (elem.getAttribute('aria-checked') == 'false') {
        likePost(elem, postId);
    } else {
        unlikePost(elem, postId, icon.dataset.likeId);
    }
    const likeCount = elem.parentNode.parentNode.parentNode.querySelector('.likes');
    updateLikeCount(likeCount, postId);
};

const likePost = (button, postId) => {
    const postData = {};

    const likeURL = `/api/posts/${ postId }/likes/`
    fetch(likeURL, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': getCookie('csrf_access_token')
        },
        body: JSON.stringify(postData)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        button.setAttribute('aria-checked', 'true');
        const elem = button.querySelector('i');
        elem.classList.remove("far");
        elem.classList.add("fas");
        elem.setAttribute('data-like-id', data.id);
    });
};

const unlikePost = (button, postId, likeId) => {
    const unlikeURL = `/api/posts/${ postId }/likes/${ likeId }`
    fetch(unlikeURL, {
        method: "DELETE",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': getCookie('csrf_access_token')
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        button.setAttribute('aria-checked', 'false');
        const elem = button.querySelector('i');
        elem.classList.add("far");
        elem.classList.remove("fas");
        elem.removeAttribute('data-like-id');
    });
};

const bookmarkUnbookmark = (ev, postId) => {
    const elem = ev.currentTarget;
    const icon = elem.querySelector('i');
    
    if (elem.getAttribute('aria-checked') == 'false') {
        bookmarkPost(elem, postId);
    } else {
        unbookmarkPost(elem, icon.dataset.bookmarkId);
    }
};

const bookmarkPost = (button, postId) => {
    const postData = {
        "post_id": postId
    };
    
    fetch("/api/bookmarks/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': getCookie('csrf_access_token')
            },
            body: JSON.stringify(postData)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            button.setAttribute('aria-checked', 'true');
            const elem = button.querySelector('i');
            elem.classList.remove("far");
            elem.classList.add("fas");
            elem.setAttribute('data-bookmark-id', data.id);
        });
};

const unbookmarkPost = (button, bookmarkId) => {
    const bookmarkURL = `/api/bookmarks/${bookmarkId}`
    fetch(bookmarkURL, {
        method: "DELETE",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': getCookie('csrf_access_token')
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        button.setAttribute('aria-checked', 'false');
        const elem = button.querySelector('i');
        elem.classList.add("far");
        elem.classList.remove("fas");
        elem.removeAttribute('data-bookmark-id');
    });
};

const postComment = (ev, postId) => {
    const elem = ev.currentTarget;
    const text = elem.parentNode.querySelector('input');
    let textVal = text.value;
    const postData = {
        "post_id": postId,
        "text": textVal
    };
    
    fetch("/api/comments", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': getCookie('csrf_access_token')
            },
            body: JSON.stringify(postData)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            const postURL = `/api/posts/${postId}`
            fetch(postURL, {
            })
            .then(response => response.json())
            .then(data => {
                const newComments = displayComments(data.comments, postId);
                const commentsElement = elem.parentNode.parentNode;
                commentsElement.innerHTML = newComments;
                commentsElement.querySelector('input').focus();
            });
        });

};

// fetch data from your API endpoint:
const displayPosts = () => {
    fetch('/api/posts')
        .then(response => response.json())
        .then(posts => {
            const html = posts.map(post2Html).join('\n');
            document.querySelector('#posts').innerHTML = html;
        })
};

const displayComments = (comments, postID) => {
    let html = '';
    if (comments.length > 1) {
        html += `
            <button class="link" data-post-id="${postID}" onclick="showPostDetail(event);">
                view all ${comments.length} comments
            </button>
        `;
    }
    if (comments && comments.length > 0) {
        const lastComment = comments[comments.length - 1];
        html += `
            <p>
                <strong>${lastComment.user.username}</strong> 
                ${lastComment.text}
            </p>
            <div class="timestamp">${lastComment.display_time}</div>
        `
    }
    html += `
        <div class="add-comment">
            <div class="input-holder">
                <input type="text" aria-label="Add a comment" placeholder="Add a comment...">
            </div>
            <button class="link" onclick="postComment(event, ${postID})">Post</button>
        </div>
    `;
    return html;
};

// fetch data from your API endpoint:
const displayStories = () => {
    fetch('/api/stories')
        .then(response => response.json())
        .then(stories => {
            const html = stories.map(story2Html).join('\n');
            document.querySelector('.stories').innerHTML = html;
        })
};

const displayProfile = () => {
    fetch('/api/profile')
        .then(response => response.json())
        .then(user => {
            const html = `
            <img src="${user.image_url}" class="pic" alt="Profile pic for ${ user.username }"/>
            <h2>${ user.username }</h2>
            `
            document.querySelector('header').innerHTML = html;
        })
};

const displaySuggestions = () => {
    fetch('/api/suggestions')
        .then(response => response.json())
        .then(users => {
            let html = `
            <p class="suggestion-text">Suggestions for you</p>`
            html += users.map(user2Html).join('\n'); 
            document.querySelector('.suggestions').innerHTML = html;
        });
};

const getCookie = key => {
    let name = key + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
};

const initPage = () => {
    displayProfile();
    displaySuggestions();
    displayStories();
    displayPosts();
};

// invoke init page to display stories:
initPage();