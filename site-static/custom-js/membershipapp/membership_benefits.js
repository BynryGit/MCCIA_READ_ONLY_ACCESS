

    /* MCCIA Welcomes New Members Counter script */
    /* IndividualsMembers */
    var totalItems1 = $('#IndividualsMembers .item').length;
    var currentIndex = $('#IndividualsMembers div.active').index() + 1;
    $('.num').html('' + currentIndex + ' / ' + totalItems1 + '');

    $('#IndividualsMembers').bind('slide.bs.carousel', function() {
        currentIndex = $('#IndividualsMembers div.active').index() + 1;
        $('.num').html('' + currentIndex + ' / ' + totalItems1 + '');
    });
    /* OrganizationMembers */
    var totalItems = $('#OrganizationMembers .item').length;
    var currentIndex = $('#OrganizationMembers div.active').index() + 1;
    $('.number').html('' + currentIndex + ' / ' + totalItems + '');

    $('#OrganizationMembers').bind('slide.bs.carousel', function() {
        currentIndex = $('#OrganizationMembers div.active').index() + 1;
        $('.number').html('' + currentIndex + ' / ' + totalItems + '');
    });

    /* Number Counter Script */
    var a = 0;
    $(window).scroll(function() {

        var oTop = $('#counter').offset().top - window.innerHeight;
        if (a == 0 && $(window).scrollTop() > oTop) {
            $('.counter-value').each(function() {
                var $this = $(this),
                    countTo = $this.attr('data-count');
                $({
                    countNum: $this.text()
                }).animate({
                        countNum: countTo
                    },

                    {

                        duration: 5000,
                        easing: 'swing',
                        step: function() {
                            $this.text(Math.floor(this.countNum));
                        },
                        complete: function() {
                            $this.text(this.countNum);
                            //alert('finished');
                        }

                    });
            });
            a = 1;
        }

    });


    $('.carousel').carousel({
        interval: false
    });

    $(".ShowAllMembersBtn").click(function(e) {
        $(this).parents('.IndividualsMembers').find('.carousel-inner .item').show();
        $(this).parents('.IndividualsMembers').find('.ShowMember').hide();
        $(this).parents('.IndividualsMembers').find('.ShowAllMembers').hide();
        $(this).parents('.IndividualsMembers').find('.navarrowpanel').hide();
        $(this).parents('.IndividualsMembers').find('.navarrowpanel1').hide();
        $(this).parents('.IndividualsMembers').find('.num').hide();
        $(this).parents('.IndividualsMembers').find('.number').hide();
        $(this).parents('.IndividualsMembers').find('.minimizeBtn').show();
    });

    $(".minimizeBtn").click(function(e) {
        $(this).parents('.IndividualsMembers').find('.minimizeBtn').hide();
        $(this).parents('.IndividualsMembers').find('.carousel-inner .item').removeAttr("style");

        $(this).parents('.IndividualsMembers').find('.ShowMember').show();
        $(this).parents('.IndividualsMembers').find('.ShowAllMembers').show();
        $(this).parents('.IndividualsMembers').find('.navarrowpanel').show();
        $(this).parents('.IndividualsMembers').find('.navarrowpanel1').show();
        $(this).parents('.IndividualsMembers').find('.num').show();
        $(this).parents('.IndividualsMembers').find('.number').show();
    });


