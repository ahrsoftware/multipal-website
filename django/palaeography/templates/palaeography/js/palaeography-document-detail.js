$(document).ready(function(){

    // Panzoom
    var panzoom;
    var panzoomParent;
    var panzoomElement;
    var panzoomImageId;
    var panzoomOptions = {
        cursor: 'move',
        maxScale: 13,
        minScale: 0.13,
        disablePan: false,
        disableZoom: false,
        step: 0.13,
        handleStartEvent: function(e) {
            // The following 2 lines were default but stopped drawing new parts from working
            // e.preventDefault();
            // e.stopPropagation();
        }
    };
    // Calculate the start scale (e.g. so image width matches container width by default)
    function setPanzoomStartScale(){
        var imageWidth = $('#detail-images-image-' + panzoomImageId).find('img').width();
        var imageContainerWidth = $('#detail-images-container').width();
        var startScale = (imageContainerWidth / imageWidth);
        panzoomOptions.startScale = startScale;
    }
    // Activate Panzoom on the current panzoomImageId image
    function setPanzoomOnImage(){
        if (panzoom !== undefined) panzoom.destroy();
        panzoomElement = document.getElementById('detail-images-image-' + panzoomImageId);
        panzoom = Panzoom(panzoomElement, panzoomOptions);
        panzoomParent = panzoomElement.parentElement
        panzoomParent.addEventListener('wheel', panzoom.zoomWithWheel);
    }

    // Functions for simplifying interacting with URL parameters
    function getUrlParameter(parameter) {
        return new URLSearchParams(window.location.search).get(parameter);
    }
    function setUrlParameter(parameter, value) {
        let urlParams = new URLSearchParams(window.location.search);
        urlParams.set(parameter, value);
        history.replaceState(null, null, "?" + urlParams.toString());
    }

    var lastActiveDocumentImagePartId;
    // Set the default to the first input if there is one
    if ($('.transcription-exercise-line-part-input').length) {
        lastActiveDocumentImagePartId = $('.transcription-exercise-line-part-input').first().attr('id').split('-').slice('-1')[0];
    }

    var showCorrectAnswerInlineCurrent = false;
    var showCorrectAnswerInlineAll = false;

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
    // Controls dropdown close button
    $('.transcription-exercise-controlsdropdown-close').on('click', function(){
        // Get the final word in id of this section, e.g. get 'information' in id="...-...-information"
        var thisId = $(this).closest('.transcription-exercise-controlsdropdown').attr('id').split('-').slice(-1)[0];
        $('#transcription-exercise-controls-' + thisId).trigger('click');
    });
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
        if (isNaN(percentage)) percentage = 0;  // prevent it from showing NaN as the score

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
        // Set the relevant form field values
        $('.deletedocumentimagepart-form-deleteimagepartid.active select').val(documentImagePartId);
        // Update last active global var
        lastActiveDocumentImagePartId = documentImagePartId;
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
        $('#transcription-exercise-part-popup').show();
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
    // When focusing on a part, load the popup with that part's content, style, position
    $('.transcription-exercise-line-part-input').on('focus', function(){

        // Set the position details (i.e. line count and part count in line)
        $('#transcription-exercise-part-popup-position').text($(this).attr('data-position'));

        // Set the help text for this document image part in the popup
        var helptext = $(this).attr('data-helptext');
        if (!helptext) helptext = '';  // Set as an empty string to clear parts with no help text
        $('#transcription-exercise-part-popup-helptext').text(helptext);

        // Set the style of the popup
        setDocumentImagePartPopupStyle(this);
    });

    // Document Image Controls

    // Choose image select list (set default value, change event, trigger on load)
    $('#detail-images-controls-chooseimage select').val(
        getUrlParameter('image') ? getUrlParameter('image') : $('#detail-images-controls-chooseimage select').val()
    ).on('change', function(){
        // Go to the correct tab
        $('li#transcription').trigger('click');
        // Reset toggle for allowing to drawer new parts (if it's active)
        if(canDrawNewDocumentImagePart) $('#transcription-exercise-controls-newdocumentimagepart').trigger('click');
        // Hide any existing dropdown content
        $('.transcription-exercise-controlsdropdown').hide();

        var imageId = $(this).find(":selected").val();
        panzoomImageId = imageId;
        // Update URL
        setUrlParameter('image', imageId);
        // Remove 'active' from existing image (and related content)
        $('.detail-images-image.active, .detail-controls-item.active, .transcription-exercise.active, .transcription-exercise-coreinfo-difficulty.active, .transcription-exercise-fullsolution-instance.active, .transcription-exercise-instructions-instruction.active, .newdocumentimagepart-form-addafterimagepartid.active, .newdocumentimagepart-form-newline.active, .deletedocumentimagepart-form-deleteimagepartid.active').removeClass('active');
        // Mark this image (and related content) as 'active'
        $('#detail-images-image-' + imageId + ', #transcription-exercise-' + imageId + ', #transcription-exercise-coreinfo-difficulty-' + imageId + ', #transcription-exercise-fullsolution-instance-' + imageId + ', #transcription-exercise-instructions-instruction-' + imageId + ', #newdocumentimagepart-form-addafterimagepartid-' + imageId + ', #newdocumentimagepart-form-newline-' + imageId + ', #deletedocumentimagepart-form-deleteimagepartid-' + imageId).addClass('active');
        // Set the 'Download image' link location
        var imageUrl = $('#detail-images-image-' + imageId).find('img').attr('src');
        $('#detail-images-controls-downloadimage a').attr('href', imageUrl);
        // Set Panzoom
        setPanzoomStartScale();
        setPanzoomOnImage();
    }).trigger('change');  // Show the first image by default on page load

    // Reveal All Parts
    $('#detail-images-controls-revealallparts').on('click', function(){
        $('.detail-images-image-parts-part').toggleClass('revealall');
    });

    // Reset image viewer to default
    $('#detail-images-controls-reset').on('click', function(){
        setPanzoomStartScale();
        panzoom.reset();
    });

    //
    // Document Image Part controls (e.g. add, delete)
    //
    var canDrawNewDocumentImagePart = false;
    var isDrawingNewDocumentImagePart = false;  // User is in the process of drawing (mousedown starts, mouseup ends)
    var newDocumentImagePartPosition;  // Top, left, width, height values of the new part
    // Can start drawing rectangle
    $('#transcription-exercise-controls-newdocumentimagepart').on('click', function(){
        controlsDropdownContentToggle(this);
        $('.detail-images-image-parts-part.new').remove();
        // If can draw state is active, deactivate it
        if(canDrawNewDocumentImagePart){
            $(this).removeClass('active');
            canDrawNewDocumentImagePart = false;
            $('.detail-images-image').removeClass('drawable');
            // Change panzoom options
            panzoomOptions.disablePan = false;
            panzoomOptions.cursor = 'move';
            panzoom.setOptions(panzoomOptions);
        }
        // If can draw state is deactive, activate it
        else {
            $(this).addClass('active');
            canDrawNewDocumentImagePart = true;
            $('.detail-images-image').addClass('drawable');
            // Change panzoom options
            panzoomOptions.disablePan = true;
            panzoomOptions.cursor = 'crosshair';
            panzoom.setOptions(panzoomOptions);
            // Show/hide steps information
            $('.newdocumentimagepart-step, #newdocumentimagepart-submit').hide();
            $('.newdocumentimagepart-step[data-step="1"]').show();
        }
    });
    // Start drawing rectangle
    $('.detail-images-image').on('mousedown', function(e){
        // Only allow to draw a rectangle if a current annotation isn't already happening
        if(canDrawNewDocumentImagePart){
            // Remove existing new parts, if any exist
            $('.detail-images-image-parts-part.new').remove();

            // Reset position values
            newDocumentImagePartPosition = {left: 0, top: 0, width: 0, height: 0}
            // Set new position values
            newDocumentImagePartPosition.left = (e.pageX - $(this).offset().left) / panzoom.getScale();
            newDocumentImagePartPosition.top = (e.pageY - $(this).offset().top) / panzoom.getScale();

            // Create and append the new rectangle
            let newDocumentImagePartHtml = `<div class="detail-images-image-parts-part new" style="height: 2px; width: 2px; left: ` + newDocumentImagePartPosition.left + `px; top: ` + newDocumentImagePartPosition.top + `px;"></div>`;
            $(this).append(newDocumentImagePartHtml);

            // Activate drawing boolean
            isDrawingNewDocumentImagePart = true;
        }
    });
    // Drawing size of rectangle
    $('.detail-images-image').on('mousemove', function(e){
        if (isDrawingNewDocumentImagePart){
            newDocumentImagePartPosition.width = ((e.pageX - $(this).offset().left) / panzoom.getScale()) - newDocumentImagePartPosition.left;
            newDocumentImagePartPosition.height = ((e.pageY - $(this).offset().top) / panzoom.getScale()) - newDocumentImagePartPosition.top;

            $('.detail-images-image-parts-part.new').first().css({'height': newDocumentImagePartPosition.height + 'px', 'width': newDocumentImagePartPosition.width + 'px'})
        }
    });
    // Finish drawing rectangle
    $('.detail-images-image').on('mouseup', function(){
        if (isDrawingNewDocumentImagePart){
            isDrawingNewDocumentImagePart = false;

            // Show content in the new part form
            $('.newdocumentimagepart-step, #newdocumentimagepart-submit').show();

            // Fill in hidden field values:
            // Document Image
            var document_image_id = $('.detail-images-image.active').first().attr('id').split('-').slice(-1)[0];
            $('#transcription-exercise-newdocumentimagepart-form input[name="document_image_id"]').val(document_image_id);
            // Positions
            $('#transcription-exercise-newdocumentimagepart-form input[name="image_cropped_left"]').val(newDocumentImagePartPosition.left);
            $('#transcription-exercise-newdocumentimagepart-form input[name="image_cropped_top"]').val(newDocumentImagePartPosition.top);
            $('#transcription-exercise-newdocumentimagepart-form input[name="image_cropped_width"]').val(newDocumentImagePartPosition.width);
            $('#transcription-exercise-newdocumentimagepart-form input[name="image_cropped_height"]').val(newDocumentImagePartPosition.height);
        }
    });
    // Stop the document image img object from dragging/selecting when trying to draw a rectangle
    $('.detail-images-image').bind('dragstart', function(){ return false; });

    // As submitting 'add new part' form
    $('#transcription-exercise-newdocumentimagepart-form').on('submit', function(){

        // Ensure rectangle has been drawn
        var partPositionData = [
            $('input[type="hidden"][name="image_cropped_left"]').val(),
            $('input[type="hidden"][name="image_cropped_top"]').val(),
            $('input[type="hidden"][name="image_cropped_width"]').val(),
            $('input[type="hidden"][name="image_cropped_height"]').val(),
        ]
        if (partPositionData.includes('')) {
            alert('Please draw a part. See Step 1 for more information');
            return false;
        }

        // Delete inactive form fields (e.g. if multiple images, remove inactive image related fields from form)
        $('.newdocumentimagepart-form-addafterimagepartid:not(.active), .newdocumentimagepart-form-newline:not(.active)').remove();
    });

    // Delete a Document Image Part
    // Toggle form
    $('#transcription-exercise-controls-deletedocumentimagepart').on('click', function(){
        controlsDropdownContentToggle(this);
    });
    // As submitting 'delete existing part' form
    $('#transcription-exercise-deletedocumentimagepart-form').on('submit', function(){
        $('.deletedocumentimagepart-form-deleteimagepartid:not(.active)').remove();
    });

    // jQuery UI
    $('.detail-controls div').attr('data-placement', 'bottom').tooltip();

});
