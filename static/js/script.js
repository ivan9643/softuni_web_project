$(document).ready(function () {
    $('.like-form').submit(function (e) {
        e.preventDefault()
        const post_id = $(this).attr('id')
        const buttonText = $.trim($(`.like-button-${post_id}`).text())

        const url = $(this).attr('action')

        let res;
        let likes = $(`.like-count-${post_id}`).text()
        likes = parseInt(likes)
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'post_id': post_id,
            },
            success: function (response) {
                if (buttonText === 'Unlike') {
                    $(`.like-button-${post_id}`).text('Like')
                    res = likes - 1
                } else {
                    $(`.like-button-${post_id}`).text('Unlike')
                    res = likes + 1
                }
                $(`.like-count-${post_id}`).text(res)
            },
            error: function (response) {
                console.log('error', response)
            }

        })

    })
    $('.follow-form').submit(function (e) {
        e.preventDefault()
        const user_id = $(this).attr('id')
        const buttonText = $.trim($(`.follow-button-${user_id}`).text())
        const url = $(this).attr('action')

        let res;
        let followers = $(`.follower-count-${user_id}`).text()
        followers = parseInt(followers)
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'user_id': user_id,
            },
            success: function (response) {
                if (buttonText === 'Unfollow') {
                    $(`.follow-button-${user_id}`).text('Follow')
                    res = followers - 1
                } else {
                    $(`.follow-button-${user_id}`).text('Unfollow')
                    res = followers + 1
                }
                $(`.follower-count-${user_id}`).text(res)
            },
            error: function (response) {
                console.log('error', response)
            }

        })

    })
})