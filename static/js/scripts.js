document.querySelectorAll('.question-like-btn').forEach(button => {
    button.addEventListener('click', function () {
        const questionId = this.dataset.id;
        const isLike = this.dataset.like === 'true';
        const csrfToken = '{{ csrf_token }}';

        fetch("{% url 'like_question_ajax' %}", {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: questionId, is_like: isLike }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.total_likes !== undefined) {
                document.getElementById(`question-like-count-${questionId}`).textContent = data.total_likes;
            }
        })
        .catch(error => console.error('Error:', error));
    });
});




document.querySelectorAll('.comment-like-btn').forEach(button => {
    button.addEventListener('click', function () {
        const commentId = this.dataset.id;
        const isLike = this.dataset.like === 'true';
        const csrfToken = '{{ csrf_token }}';

        fetch("{% url 'like_comment_ajax' %}", {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: commentId, is_like: isLike }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.total_likes !== undefined) {
                document.getElementById(`comment-like-count-${commentId}`).textContent = data.total_likes;
            }
        })
        .catch(error => console.error('Error:', error));
    });
});

    document.querySelectorAll('.mark-correct').forEach(checkbox => {
    checkbox.addEventListener('change', function () {
        const commentId = this.dataset.id;
        const csrfToken = '{{ csrf_token }}';

        fetch("{% url 'mark_correct_answer' %}", {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ comment_id: commentId }),
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                alert(data.error);
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
