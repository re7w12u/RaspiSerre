$(()=>{

    var nav = '<div class="row"> \
                <div class="col-sm">\
                 <div class="card">\
                  <div class="card-body">\
                   <ul class="nav nav-pills">\
                    <li class="nav-item"><a class="nav-link" href="/">Home</a></li>\
                    <li class="nav-item"><a class="nav-link" href="/param">Param</a></li>\
                    <li class="nav-item"><a class="nav-link" href="https://github.com/re7w12u/RaspiSerre" target="_blank"> Git</a></li>\
                   </ul>\
                  </div>\
                 </div>\
                </div>\
                </div>';

    $("#menuPlaceHolder").html(nav);


    $('.nav-link').each(function (i) {        
        var currentLink = $(this);
        var hrefValue = currentLink.attr('href');
        var page = location.pathname;
        if (page == hrefValue) currentLink.addClass('active');
        else if (this.className.includes('active')) currentLink.removeClass('active');
    });

});