$(document).ready(function () {
    $('.like-form').submit(function (e) {
        e.preventDefault()
        const post_id = $(this).attr('id')
        const buttonText = $.trim($(`.like-button-${post_id}`).text())

        const url = $(this).attr('action')
        let change;
        let current_post_likes = $(`.like-count-${post_id}`).text()
        current_post_likes = parseInt(current_post_likes)
        let total_likes = $('.like-count-total').text()
        total_likes = parseInt(total_likes)
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
                    change = -1
                } else {
                    $(`.like-button-${post_id}`).text('Unlike')
                    change = 1
                }
                $(`.like-count-${post_id}`).text(current_post_likes + change)
                $('.like-count-total').text(total_likes + change)
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

        let change;
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
                    change = -1
                } else {
                    $(`.follow-button-${user_id}`).text('Unfollow')
                    change = 1
                }
                $(`.follower-count-${user_id}`).text(followers + change)
            },
            error: function (response) {
                console.log('error', response)
            }

        })

    })
})