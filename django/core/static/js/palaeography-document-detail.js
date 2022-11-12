$(document).ready(function(){

    var lastActiveDocumentImagePartId;
    var showCorrectAnswerInlineIndividual = false;
    var showCorrectAnswerInlineAll = false;

    $('.detail-controls div').attr('data-placement', 'bottom').tooltip();

    // Transcription Controls functionality
    // Clear transcription attempts
    $('#transcription-exercise-controls-reset').on('click', function(){
        $('.transcription-exercise-input-line-word').each(function(){$(this).val('').removeClass('correct').removeClass('wrong');});
    }).trigger('click');  // Execute on page load (stops browser caching them on page refresh)
    // Information
    $('#transcription-exercise-controls-information').on('click', function(){
        $('#transcription-exercise-information').toggle();
        // Hide other controldropdown instances
        $('.transcription-exercise-controlsdropdown').not('#transcription-exercise-information').hide();
    });
    // Instructions
    $('#transcription-exercise-controls-instructions').on('click', function(){
        $('#transcription-exercise-instructions').toggle();
        // Hide other controldropdown instances
        $('.transcription-exercise-controlsdropdown').not('#transcription-exercise-instructions').hide();
    });
    // Full solutions
    $('#transcription-exercise-controls-fullsolution').on('click', function(){
        $('#transcription-exercise-solutions').toggle();
        // Hide other controldropdown instances
        $('.transcription-exercise-controlsdropdown').not('#transcription-exercise-solutions').hide();
    });
    // All correct answers
    $('#transcription-exercise-controls-correctall').on('click', function(){
        // Toggle global var
        showCorrectAnswerInlineAll = !showCorrectAnswerInlineAll;
        // Toggle elements
        var element_beforepart = '.transcription-exercise-input-line-word-answer-beforepart';
        var element_text = '.transcription-exercise-input-line-word-answer';
        var element_afterpart = '.transcription-exercise-input-line-word-answer-afterpart';
        var elements = $([element_beforepart, element_text, element_afterpart].join(', '));
        if (showCorrectAnswerInlineAll) elements.addClass('active');
        else elements.removeClass('active');
    });
    // Current correct answer
    $('#transcription-exercise-controls-correctcurrent').on('click', function(){
        // Toggle global var
        showCorrectAnswerInlineIndividual = !showCorrectAnswerInlineIndividual;
        // Only continue if there's an active image part and not all are active
        if (lastActiveDocumentImagePartId && !showCorrectAnswerInlineAll){
            var element_beforepart = '#transcription-exercise-input-line-word-answer-beforepart-' + lastActiveDocumentImagePartId;
            var element_text = '#transcription-exercise-input-line-word-answer-' + lastActiveDocumentImagePartId;
            var element_afterpart = '#transcription-exercise-input-line-word-answer-afterpart-' + lastActiveDocumentImagePartId;

            var elements = $([element_beforepart, element_text, element_afterpart].join(', '));
            // Toggle elements
            if (showCorrectAnswerInlineIndividual) elements.addClass('active');
            else elements.removeClass('active');
        }
    });
    // Scores details
    $('#transcription-exercise-controls-scores').on('click', function(){
        // Set score text
        setTranscriptionScoresText();
        // Show/hide scores
        $('#transcription-exercise-scores').toggle();
        // Hide other controldropdown instances
        $('.transcription-exercise-controlsdropdown').not('#transcription-exercise-scores').hide();
    });
    // Position Details
    $('#transcription-exercise-controls-positiondetails').on('click', function(){
        $('.transcription-exercise-input-linecount, .transcription-exercise-input-line-word-count').toggleClass('active');
    });

    // Score transcription attempts
    function scoreTranscriptionAttempt(inputField, ignoreWrongAnswers=false){
        // Class names
        var classCorrect = 'correct';
        var classWrong = 'wrong';
        // Answers
        var answerAttempt = inputField.val();
        var answerCorrectList = inputField.attr('data-correctanswer').split("|");
        // Only score answer if a value provided
        if (answerAttempt !== ''){
            // Correct - if the answer attempt is in list of correct answers
            if (answerCorrectList.indexOf(answerAttempt) > -1){
                inputField.addClass(classCorrect).removeClass(classWrong);
                setTranscriptionScoresText();
                return;  // End function here
            }
            // Wrong
            else if (!ignoreWrongAnswers){
                inputField.addClass(classWrong).removeClass(classCorrect);
                setTranscriptionScoresText();
                return;  // End function here
            }
        }
        // Remove correct/wrong score, if not marked as correct/wrong by this point
        inputField.removeClass(classWrong).removeClass(classCorrect);
        setTranscriptionScoresText();
    }
    // Score transcription attempt as correct/incorrect when focus out of an input
    $('.transcription-exercise-input-line-word').on('focusout', function(){
        scoreTranscriptionAttempt($(this));
    });
    // Score transcription attempt as correct whilst user types
    $('.transcription-exercise-input-line-word').on('input', function(){
        scoreTranscriptionAttempt($(this), true);
    });
    // Set the score text for transcriptions
    function setTranscriptionScoresText(){
        // Get counts
        var count_available = $('.transcription-exercise-input-line-word').length;
        var count_wrong = $('.transcription-exercise-input-line-word.wrong').length;
        var count_correct = $('.transcription-exercise-input-line-word.correct').length;
        var count_answered = count_wrong + count_correct;
        var count_unanswered = count_available - count_answered;
        var percentage = Math.round((count_correct / count_available) * 100);
        // Set scores text
        $('#transcription-exercise-scores-percentage').text(percentage + '%');
        $('#transcription-exercise-scores-available').text(count_available);
        $('#transcription-exercise-scores-unanswered').text(count_unanswered);
        $('#transcription-exercise-scores-answered').text(count_answered);
        $('#transcription-exercise-scores-wrong').text(count_wrong);
        $('#transcription-exercise-scores-correct').text(count_correct);
    }

    // Click 'enter' to move focus to next transcription input
    $('.transcription-exercise-input-line-word').keydown(function(e){
        var key = e.charCode ? e.charCode : e.keyCode ? e.keyCode : 0;
        if (key == 13) {
            e.preventDefault();
            var inputs = $(this).closest('.transcription-exercise-input').find('.transcription-exercise-input-line-word');
            inputs.eq( inputs.index(this)+ 1 ).focus();
        }
    });

    // Set a 'reveal' class to document image parts that overlay image when user hovers over them
    $('.detail-images-image-parts-part, .transcription-exercise-input-line-word').hover(
        // Hover starts
        function(){
            var documentImagePartId = $(this).attr('id').split('-').slice('-1')[0];
            $('#detail-images-image-parts-part-' + documentImagePartId + ', #transcription-exercise-input-line-word-' + documentImagePartId).addClass('reveal');
        },
        // Hover ends
        function(){
            var documentImagePartId = $(this).attr('id').split('-').slice('-1')[0];
            $('#detail-images-image-parts-part-' + documentImagePartId + ', #transcription-exercise-input-line-word-' + documentImagePartId).removeClass('reveal');
        }
    );

    // Connect document image part occurences: image overlays and transcription inputs
    $('.transcription-exercise-input-line-word').on('focus', function(){
        var documentImagePartId = $(this).attr('id').split('-').slice('-1')[0];
        $('.detail-images-image-parts-part').removeClass('active');
        $('#detail-images-image-parts-part-' + documentImagePartId).addClass('active');
        // Hide the active correct answer inline (individual) if focussing on a different part
        if (showCorrectAnswerInlineIndividual && lastActiveDocumentImagePartId !== documentImagePartId){
            $('#transcription-exercise-controls-correctcurrent').first().trigger('click');  // TODO update this with the correct button when it's been created
        }
        lastActiveDocumentImagePartId = documentImagePartId;  // Update last active global var
    }).on('focusout', function(){
        // When an input is no longer focussed on, ensure image overlay isn't left active
        $('.detail-images-image-parts-part').removeClass('active');
    });
    $('.detail-images-image-parts-part').on('click', function(){
        var documentImagePartId = $(this).attr('id').split('-').slice('-1')[0];
        $('#transcription-exercise-input-line-word-' + documentImagePartId).focus();
    });

    // Document Image Part Popup
    $('.transcription-exercise-input-line-word').on('focus', function(){
        // Move the preview above the current image part
        var posX = 400;
        var posY = 400;

        // Set the image in the preview as the current image part's cropped image
        var img = $('.detail-images-image.active').first().find('img');
        $('#transcription-exercise-part-popup-image').attr('src', img.attr('src'));

        // Set the help text for this document image part in the popup
        var helptext = $('#transcription-exercise-input-line-word-' + lastActiveDocumentImagePartId).attr('data-helptext');
        if (!helptext) helptext = '';  // Set as an empty string to clear parts with no help text
        $('#transcription-exercise-part-popup-helptext').text(helptext);
    });

    // Choose/show an image and accompanying transcription
    $('#detail-images-controls-chooseimage').on('change', function(){
        // Go to the correct tab
        $('li#transcription').trigger('click');
        // Hide any existing dropdown content
        $('.transcription-exercise-controlsdropdown').hide();

        var imageId = $(this).find(":selected").val();
        // Remove 'active' from existing image (and related content)
        $('.detail-images-image.active, .transcription-exercise.active, .transcription-exercise-coreinfo-difficulty.active, .transcription-exercise-solutions-solution.active').removeClass('active');
        // Mark this image (and related content) as 'active'
        $('#detail-images-image-' + imageId + ', #transcription-exercise-' + imageId + ', #transcription-exercise-coreinfo-difficulty-' + imageId + ', #transcription-exercise-solutions-solution-' + imageId).addClass('active');
        // Set the 'Download image' link location
        var imageUrl = $('#detail-images-image-' + imageId).find('img').attr('src');
        $('#detail-images-controls-downloadimage a').attr('href', imageUrl);
    }).trigger('change');  // Show the first image by default on page load


    // Image Controls

    // Zoom
    function zoomInOrOut(zoomOut=false){
        let slider = $('#detail-images-controls-zoom-range-slider');
        let currentVal = slider.val();
        let changeVal = (zoomOut ? 0.7 : 1.3);
        slider.val(currentVal * changeVal).trigger('input');
    }
    // Zoom: Out
    $('#detail-images-controls-zoom-out').on('click', function(){
        zoomInOrOut(true);
    });
    // Zoom: In
    $('#detail-images-controls-zoom-in').on('click', function(){
        zoomInOrOut();
    });
    // Zoom: Slider
    function zoomItemImage(zoomLevel){
        $('.detail-images-image').css({'transform': 'scale(' + zoomLevel + ', ' + zoomLevel + ')', 'transform-origin': '0% 0%'});
    }
    // Set zoom via slider
    $('#detail-images-controls-zoom-range-slider').on('input', function(){
        let zoomLevel = $(this).val() / 100;
        zoomItemImage(zoomLevel);
    }).on('change', function(){$(this).blur();});  // Stops the tooltip from remaining visible when focus stays on range slider
    // Set zoom/scale for 100% width of the image in the container
    function zoomFullWidth(){
        var imageWidth = $('.detail-images-image.active').first().find('img').width();
        var imageContainerWidth = $('#detail-images-container').width();
        var scale = (imageContainerWidth / imageWidth) * 100;
        $('#detail-images-controls-zoom-range-slider').val(scale).trigger('input');
    }

    // Reset image viewer to default
    $('#detail-images-controls-reset').on('click', function(){
        zoomFullWidth();
        $('#detail-images-container').scrollTop(0).scrollLeft(0);
    }).trigger('click'); // Reset the image viewer on page load

});