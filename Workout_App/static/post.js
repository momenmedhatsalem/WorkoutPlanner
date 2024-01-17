
    document.addEventListener('DOMContentLoaded', function() {
        // Like
        document.querySelectorAll('.buttons').forEach(button  => {
            var profile = button.dataset.profile;
            var button_type = button.dataset.button;
            fetch(`/edit/${button_type}/${profile}`)
                .then(response => response.json())
                .then(liked_posts => {

                    if (liked_posts['liked_posts'].includes(parseInt(post_id1))) {
                        button.classList.toggle('liked');
                    }
                });
            });
        document.querySelectorAll('.button').forEach(button  => {
        button.addEventListener('click', () => {
            var post_id1 = button.dataset.post;
            fetch(`/like/${post_id1}`)
                .then(response => response.json())
                .then(liked_posts => {
                    // check whether the user liked the post or not
                    if (liked_posts['liked_posts'].includes(parseInt(post_id1))) {
                        var likes = -1;

                    }
                    else {
                        var likes = 1;
                    }
                        fetch(`/like/${post_id1}`, {
                            method: 'PUT',
                            body: JSON.stringify({
                                likes: likes
                            })
                            });
                    
                    document.querySelector(`#z${post_id1}`).innerHTML = parseInt(document.querySelector(`#z${post_id1}`).innerHTML) + parseInt(likes);
                    
                });
            button.classList.toggle('liked');
        });
    });

        // Edit Age, Weight or Height
        document.querySelectorAll('.buttons').forEach(button  => {
            var profile = button.dataset.profile;
            var button_type = button.dataset.button;
            let save_button = document.createElement("button");
            save_button.classList.add('btn', 'btn-dark');
            button.onclick = function() {
                button.style.display = 'none';
                var post_id = this.dataset.post;

                let div = document.createElement("div");
                let text = document.createElement("textarea");
                text.classList.add('new_text');
                let heading = document.querySelector(`#${profile}`);
                div.appendChild(text);
                div.appendChild(document.createElement("br"));
                div.appendChild(save_button);
                save_button.innerHTML = "save";
                
                text.value = heading.innerHTML;
                heading.replaceWith(div);
                save_button.onclick = function() {
                
                heading.innerHTML = document.querySelector('.new_text').value;
                div.replaceWith(heading);

                fetch(`/edit/${button_type}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        new_edit: heading.innerHTML
                    })
                    });
                button.style.display = 'inline-block';
            }
            }

            
        });

        // Disable submit button till user types in
        document.querySelector('#submit').disabled = true;

        document.querySelector('#text').onkeyup = () => {
            if (document.querySelector('#text').value.length > 0) {
                document.querySelector('#submit').disabled = false;
            }
            else
            {
                document.querySelector('#submit').disabled = true;
            }
        }
    });
