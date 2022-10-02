$(document).ready(function() {

    // Language / Translation / i18n

    // Show/hide popup
    var languageVisible = false;
    $('#language-show').on('click', function() {
        // Hide language popup
        if (languageVisible) {
            $('#language-popup').animate({left: '-15em'});
            $(this).animate({left: '0em'});
            languageVisible = false;
        }
        // Show language popup
        else {
            $('#language-popup').animate({left: '0'});
            $(this).animate({left: '6em'});
            languageVisible = true;
        }
    });

    // Add link to current page in specified language
    // The a tag must have a data-langcode="(code)" attribute
    $('a[data-langcode]').each(function(){
        var urlCurrent = window.location.pathname.split('/');
        langCode = $(this).attr('data-langcode');
        // Add 'active' class if this is the current language
        if(urlCurrent[1] === langCode) $(this).addClass('active');
        // Set href for this language code
        urlCurrent[1] = langCode;
        $(this).attr('href', urlCurrent.join('/') + window.location.search);
    });

});