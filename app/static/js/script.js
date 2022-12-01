$("#add_to_library").click(function () {
    let data_word_id = $(this).attr("data-word-id");
    axios.post('/api/add-to-library', {
        'word_id': data_word_id
    })
        .then(function (response) {
            let data = response.data;
            if (data.success === true) {
                toastr.success('The word has been added to your library.', { timeOut: 1000 });
                $("#add_to_library").removeClass("btn-success").addClass("btn-info").text("The Word Is Already In The Library");
                $("#add_to_library").attr("disabled", true);
            } else {
                toastr.error('The word could not be added to your library.');
            }
        })
        .catch(function (error) {
            console.log(error);
        });
});

$(document).ready(function () {
    $(".start-practice").click(function () {
        axios.get('/api/get-question')
            .then(function (response) {
                let data = response.data;
                if (data.success === true) {
                    $("#question_text").text(data.question);
                    $("#question_area").attr("data-question-id", data.question_id);
                    $(".answer-button").each(function (index, item) {
                        $(this).text(data.answers[index]);
                        $(this).attr("disabled", false);
                        $(this).removeClass("btn-success").removeClass("btn-danger").addClass("btn-outline-secondary");
                    });
                    $("#question_area").show();
                    $("#start_practice").hide();
                } else {
                    toastr.error('The word could not be added to your library.', { timeOut: 1000 });
                }
            })
    });
});

$(document).ready(function () {
    $(".answer-button").click(function () {
        let answer = $(this);
        let question_id = $("#question_area").attr("data-question-id");
        axios.post('/api/check-answer', {
            'answer': answer.text(),
            'question_id': question_id
        })
            .then(function (response) {
                let data = response.data;
                if (data.success === true) {
                    toastr.success(data.message, { timeOut: 1000 });
                    $(answer).removeClass("btn-outline-secondary").addClass("btn-success").attr("disabled", "disabled");
                } else {
                    toastr.error(data.message, { timeOut: 1000 });
                    $(answer).removeClass("btn-outline-secondary").addClass("btn-danger").attr("disabled", "disabled");
                }
            })
    });
});


$(document).ready(function () {
    $(".accordion-wma-button").each(function (index, item) {
        let word_id = $(this).attr("data-word-id");
        console.log(word_id);
        axios.post('/api/get-point', {
            'word_id': word_id
        })
        .then(function (response) {
            let data = response.data;
            if (data.success === true) {
                $(item).html(`<span class="badge bg-success me-3">${data.point}</span> ${data.word}`);
            } else {
                toastr.error('The point could not be loaded.', { timeOut: 1000 });
            }
        })
    });
});