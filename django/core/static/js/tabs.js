// JS for tabbed content on pages, e.g. About page, detail pages, etc.

$(document).ready(function() {

    // Functions for simplifying interacting with URL parameters
    function getUrlParameter(parameter) {
        return new URLSearchParams(window.location.search).get(parameter);
    }
    function setUrlParameter(parameter, value) {
        let urlParams = new URLSearchParams(window.location.search);
        urlParams.set(parameter, value);
        history.replaceState(null, null, "?" + urlParams.toString());
    }

    // Tabbed sections
    $('.tabs li').on('click', function(){
        // Show/hide the appropriate sections
        var active_tab_id = $(this).attr('id');
        $('section.tabbed#tabbed-' + active_tab_id).show();
        $('section.tabbed:not(#tabbed-' + active_tab_id + ')').hide();
        // Alter active state of tab button
        $('.tabs li').removeClass('active');
        $(this).addClass('active');
        // Set URL parameter
        setUrlParameter('tab', active_tab_id);
        // Scroll to top
        window.scrollTo(0, 0);
    });

    // Get tab from url params and initiate above click event function
    function setTabFromUrl(){
        var tab_value = getUrlParameter('tab');
        var valid_tab_values = []
        $(".tabs li").each(function(){ valid_tab_values.push($(this).attr('id')); })
        var tab = (!valid_tab_values.includes(tab_value) ? valid_tab_values[0] : tab_value);
        $('.tabs li#' + tab).trigger('click');
    }
    setTabFromUrl();  // Set initial tab on page load

    // On print show all tabs
    $(window).bind("beforeprint", function(){
        $('section.tabbed').show();
    });

    // On print show all tabs
    $(window).bind("afterprint", function(){
        setTabFromUrl();
    });

});