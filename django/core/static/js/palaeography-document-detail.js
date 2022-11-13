$(document).ready(function(){

    var lastActiveDocumentImagePartId = $('.transcription-exercise-line-part-input').first().attr('id').split('-').slice('-1')[0];
    var showCorrectAnswerInlineCurrent = false;
    var showCorrectAnswerInlineAll = false;

    $('.detail-controls div').attr('data-placement', 'bottom').tooltip();

    // Ensure transcription inputs are cleared on page load (stops browser caching on page refresh)
    $('.transcription-exercise-line-part-input').each(function(){$(this).val('').removeClass('correct').removeClass('wrong');});

    // Transcription Controls functionality
    // Reset the exercise fully by refreshing the page
    $('#transcription-exercise-controls-reset').on('click', function(){
        window.location.replace(window.location.href);
    });
    // Controls dropdown content toggle
    function controlsDropdownContentToggle(button){
        // Get the final word in id of button, e.g. get 'information' in id="...-...-information"
        var thisId = $(button).attr('id').split('-').slice(-1)[0];
        // Hide all controldropdown instances and remove active from all buttons
        $('.transcription-exercise-controlsdropdown').not('#transcription-exercise-' + thisId).hide();
        $('.detail-controls-item.active').not(button).removeClass('active');
        // Show this controldropdown instance and mark this button as active
        $(button).toggleClass('active');
        $('#transcription-exercise-' + thisId).toggle();
    }
    // Information
    $('#transcription-exercise-controls-information').on('click', function(){ controlsDropdownContentToggle(this); });
    // Instructions
    $('#transcription-exercise-controls-instructions').on('click', function(){ controlsDropdownContentToggle(this); });
    // Full solutions
    $('#transcription-exercise-controls-fullsolution').on('click', function(){ controlsDropdownContentToggle(this); });
    // Scores details
    $('#transcription-exercise-controls-scores').on('click', function(){
        // Set score text
        setTranscriptionScoresText();
        controlsDropdownContentToggle(this);
    });
    // All correct answers
    $('#transcription-exercise-controls-correctall').on('click', function(){
        // Toggle global var
        showCorrectAnswerInlineAll = !showCorrectAnswerInlineAll;
        // Toggle elements
        var element_beforepart = '.transcription-exercise-line-beforepart-answer';
        var element_text = '.transcription-exercise-line-part-answer';
        var element_afterpart = '.transcription-exercise-line-afterpart-answer';
        var elements = $([element_beforepart, element_text, element_afterpart].join(', '));
        if (showCorrectAnswerInlineAll) elements.addClass('active');
        else elements.removeClass('active');
    });
    // Current correct answer
    $('#transcription-exercise-controls-correctcurrent').on('click', function(){
        // Toggle global var
        showCorrectAnswerInlineCurrent = !showCorrectAnswerInlineCurrent;
        // Set image part Id to the last active (if exists) or 1 by default, to show the first image part
        if (!showCorrectAnswerInlineAll){
            var element_beforepart = '#transcription-exercise-line-beforepart-answer-' + lastActiveDocumentImagePartId;
            var element_text = '#transcription-exercise-line-part-answer-' + lastActiveDocumentImagePartId;
            var element_afterpart = '#transcription-exercise-line-afterpart-answer-' + lastActiveDocumentImagePartId;

            var elements = $([element_beforepart, element_text, element_afterpart].join(', '));
            // Toggle elements
            if (showCorrectAnswerInlineCurrent) elements.addClass('active');
            else elements.removeClass('active');
        }
    });
    // Position Details
    $('#transcription-exercise-controls-positiondetails').on('click', function(){
        $('.transcription-exercise-linecount, .transcription-exercise-line-part-count').toggleClass('active');
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
    $('.transcription-exercise-line-part-input').on('focusout', function(){
        scoreTranscriptionAttempt($(this));
    });
    // Score transcription attempt as correct whilst user types
    $('.transcription-exercise-line-part-input').on('input', function(){
        scoreTranscriptionAttempt($(this), true);
    });
    // Set the score text for transcriptions
    function setTranscriptionScoresText(){
        // Get counts
        var count_available = $('.transcription-exercise-line-part-input').length;
        var count_wrong = $('.transcription-exercise-line-part-input.wrong').length;
        var count_correct = $('.transcription-exercise-line-part-input.correct').length;
        var count_answered = count_wrong + count_correct;
        var count_unanswered = count_available - count_answered;
        var percentage = Math.round((count_correct / count_available) * 100);
        
        // Set text
        // Core info
        $('#transcription-exercise-coreinfo-scoresummary').text(count_correct + '/' + count_available + ' (' + percentage + '%)');
        // Score details
        $('#transcription-exercise-scores-percentage').text(percentage + '%');
        $('#transcription-exercise-scores-available').text(count_available);
        $('#transcription-exercise-scores-unanswered').text(count_unanswered);
        $('#transcription-exercise-scores-answered').text(count_answered);
        $('#transcription-exercise-scores-wrong').text(count_wrong);
        $('#transcription-exercise-scores-correct').text(count_correct);
    }
    // Run on page load
    setTranscriptionScoresText();

    // Click 'enter' to move focus to next transcription input
    $('.transcription-exercise-line-part-input').keydown(function(e){
        var key = e.charCode ? e.charCode : e.keyCode ? e.keyCode : 0;
        if (key == 13) {
            e.preventDefault();
            var inputs = $(this).closest('.transcription-exercise').find('.transcription-exercise-line-part-input');
            inputs.eq( inputs.index(this)+ 1 ).focus();
        }
    });

    // Set a 'reveal' class to document image parts that overlay image when user hovers over them
    $('.detail-images-image-parts-part, .transcription-exercise-line-part-input').hover(
        // Hover starts
        function(){
            var documentImagePartId = $(this).attr('id').split('-').slice('-1')[0];
            $('#detail-images-image-parts-part-' + documentImagePartId + ', #transcription-exercise-line-part-' + documentImagePartId).addClass('reveal');
        },
        // Hover ends
        function(){
            var documentImagePartId = $(this).attr('id').split('-').slice('-1')[0];
            $('#detail-images-image-parts-part-' + documentImagePartId + ', #transcription-exercise-line-part-' + documentImagePartId).removeClass('reveal');
        }
    );

    // Connect document image part occurences: image overlays and transcription inputs
    $('.transcription-exercise-line-part-input').on('focus', function(){
        var documentImagePartId = $(this).attr('id').split('-').slice('-1')[0];
        $('.detail-images-image-parts-part').removeClass('active');
        $('#detail-images-image-parts-part-' + documentImagePartId).addClass('active');
        // Hide the active correct answer inline (current) if focussing on a different part
        if (showCorrectAnswerInlineCurrent && lastActiveDocumentImagePartId !== documentImagePartId){
            $('#transcription-exercise-controls-correctcurrent').first().trigger('click');
        }
        lastActiveDocumentImagePartId = documentImagePartId;  // Update last active global var
    }).on('focusout', function(){
        $('.detail-images-image-parts-part').removeClass('active');
        $('#transcription-exercise-part-popup').hide()
    });
    $('.detail-images-image-parts-part').on('click', function(){
        var documentImagePartId = $(this).attr('id').split('-').slice('-1')[0];
        $('#transcription-exercise-line-part-' + documentImagePartId).focus();
    });

    // Document Image Part Popup
    function setDocumentImagePartPopupStyle(inputElement){
        var inputElement = $('#transcription-exercise-line-part-' + lastActiveDocumentImagePartId);
        var unit = 'px';
        $('#transcription-exercise-part-popup').show().width($(inputElement).attr('data-width') + unit);
        var popupWidth = $('#transcription-exercise-part-popup').outerWidth();
        var popupHeight = $('#transcription-exercise-part-popup').outerHeight();
        var inputElementPosition = $(inputElement).position();
        var inputElementWidth = $(inputElement).outerWidth();
        var balance = (inputElementWidth > 89 ? 40 : 15);  // Make wider parts go further right to make feel more balanced
        $('#transcription-exercise-part-popup').css({
            'top': (inputElementPosition.top - popupHeight) + unit,
            // Right align popup relative to input, so it never goes off the screen to right
            'left': (inputElementPosition.left - popupWidth + $(inputElement).outerWidth() + balance) + unit
        });
    }
    // Update popup when scrolled, so it moves with the scroll (if already currently visible)
    $('.transcription-exercise').on('scroll', function(){
        if ($('#transcription-exercise-part-popup').is(":visible")){
            setDocumentImagePartPopupStyle();
        }
    });
    // When focusing on a part, load the popup with that part's content and style/position it for the part
    $('.transcription-exercise-line-part-input').on('focus', function(){

        var unit = 'px';

        // Set the position details (i.e. line count and part count in line)
        var positiontext = 'Line: ' + $(this).attr('data-linecount') + ', Part: ' + $(this).attr('data-partcountinline');
        $('#transcription-exercise-part-popup-position').text(positiontext);

        // Set the image in the preview as the current image part's cropped image
        var img = $('.detail-images-image.active').first().find('img');
        var imagePartWidth = $(this).attr('data-width');
        var imagePartHeight = $(this).attr('data-height');
        $('#transcription-exercise-part-popup-image').css({
            'background-repeat': 'no-repeat',
            'background-image': 'url("' + img.attr('src') + '")',
            'background-position': '-' + $(this).attr('data-left') + unit + ' -' + $(this).attr('data-top') + unit,
            'width': imagePartWidth + unit,
            'height': imagePartHeight + unit,
            'display': 'block'
        });

        // Set the help text for this document image part in the popup
        var helptext = $(this).attr('data-helptext');
        if (!helptext) helptext = '';  // Set as an empty string to clear parts with no help text
        $('#transcription-exercise-part-popup-helptext').text(helptext);

        // Set the style of the popup
        setDocumentImagePartPopupStyle(this);
    });

    // Choose/show an image and accompanying transcription
    $('#detail-images-controls-chooseimage').on('change', function(){
        // Go to the correct tab
        $('li#transcription').trigger('click');
        // Hide any existing dropdown content
        $('.transcription-exercise-controlsdropdown').hide();

        var imageId = $(this).find(":selected").val();
        // Remove 'active' from existing image (and related content)
        $('.detail-images-image.active, .detail-controls-item.active, .transcription-exercise.active, .transcription-exercise-coreinfo-difficulty.active, .transcription-exercise-fullsolution-instance.active, .transcription-exercise-instructions-instruction.active').removeClass('active');
        // Mark this image (and related content) as 'active'
        $('#detail-images-image-' + imageId + ', #transcription-exercise-' + imageId + ', #transcription-exercise-coreinfo-difficulty-' + imageId + ', #transcription-exercise-fullsolution-instance-' + imageId + ', #transcription-exercise-instructions-instruction-' + imageId).addClass('active');
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