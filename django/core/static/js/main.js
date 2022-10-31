$(document).ready(function() {

    // Language / Translation / i18n
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