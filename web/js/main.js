/*
------------------------------------------------------------------------------
* Template Name    : Halman | Personal Portfolio Html5 One Page Template     *
* Author           : ParExcellence                                           *
* Version          : 1.0.0                                                   *
* Created          : Mar 2020                                                *
*-----------------------------------------------------------------------------
*/
$(document).ready(function () {
    "use strict";


    /*=========================================================================
      Typed JS
    =========================================================================*/
    (function ($) {
        $(".typed").typed({
            strings: ["Donna Walker.", "A Photographer.", "A Photo Editor."],
            stringsElement: null,
            typeSpeed: 60,
            startDelay: 1000,
            backSpeed: 20,
            backDelay: 1000,
            loop: true,
            loopCount: 5,
            showCursor: true,
            cursorChar: "|",
            attr: null,
            contentType: 'html',
            callback: function () { },
            preStringTyped: function () { },
            onStringTyped: function () { },
            resetCallback: function () { }
        });
    })(jQuery);

    /*=========================================================================
     Counter JS
   =========================================================================*/
    $('.count').counterUp({
        delay: 10,
        time: 5000
    });


    /*=========================================================================
      Tetstimonial JS
    =========================================================================*/
    (function ($) {
        var ClientCarousel = $('.client-slider');
        if (ClientCarousel.length > 0) {
            ClientCarousel.owlCarousel({
                margin: 0,
                loop: false,
                nav: true,
                center: false,
                dots: false,
                autoplay: true,
                autoplayTimeout: 5000,
                items: 2,
                responsiveClass: true,
                navText: ['<span class="mdi mdi-arrow-left"></span>', '<span class="mdi mdi-arrow-right"></span>'],
                responsive: {
                    0: {
                        items: 1,
                        nav: false,
                    },
                    600: {
                        items: 1,
                        nav: false,
                    },
                    1000: {
                        items: 2,
                        nav: false,
                    },
                    1200: {
                        items: 2,
                        nav: true,
                    }
                }
            });
        }
    })(jQuery);

    /*=========================================================================
      Menu JS
    =========================================================================*/
    (function ($) {
        $("#menu > li a").on('click', function () {
            $("#main-wrapper > section.active, #menu > li a").removeClass("active");
            $(this).addClass('active');
            var SectionId = $(this).attr('href');
            $('#main-wrapper').children(SectionId).addClass('active');

   /*=========================================================================
    Isotop JS
   =========================================================================*/
            var $container = $('.portfolio-items');
            var $filter = $('#portfolio-filter');
            $container.isotope({
                filter: '*',
                layoutMode: 'masonry',
                animationOptions: {
                    duration: 750,
                    easing: 'linear'
                }
            });
            $filter.find('a').on("click", function () {
                var selector = $(this).attr('data-filter');
                $filter.find('a').removeClass('active');
                $(this).addClass('active');
                $container.isotope({
                    filter: selector,
                    animationOptions: {
                        animationDuration: 750,
                        easing: 'linear',
                        queue: false,
                        touchSensitivity: 2,
                    }
                });
                return false;
            });
        });
    })(jQuery);
    /*=========================================================================
     Mobile Menu Toggle JS
   =========================================================================*/
    (function ($) {
        var $menuToggler = $(".menu-toggler");
        var $window = $(window);
        var $header = $('header');
        $menuToggler.click(function () {
            $(this).toggleClass('open').find('i').toggleClass('mdi-menu mdi-close ');
            $header.toggleClass('open');
        });
        if ($window.width() < 992) {
            $('.menu-list li a').click(function () {
                $header.removeClass('open');
                $menuToggler.removeClass('open').find('i').removeClass('mdi-close').addClass('mdi-menu');
            })
        }
    })(jQuery);

    /*=========================================================================
         Magnific Popup JS
        =========================================================================*/
    if (('.portfolio-items').length > 0) {
        $('.portfolio-items').each(function () {
            $(this).magnificPopup({
                delegate: '.js-zoom-gallery',
                type: 'image',
                gallery: {
                    enabled: true
                }
            });
        });
    }
  

});

(function ($) {
    "use strict";
    /*=========================================================================
    Preloader JS
    =========================================================================*/
    $(window).on('load', function () {
        var preloaderFadeOutTime = 500;
        function hidePreloader() {
            var preloader = $('.spinner-wrapper');
            setTimeout(function () {
                preloader.fadeOut(preloaderFadeOutTime);
            }, 500);
        }
        hidePreloader();
    });
})(jQuery);

/*=========================================================================
  MENU CLOSE JS
=========================================================================*/
$(".menu-close-btn").on('click', function () {
    $('.navbar-collapse').removeClass('show');
}),

    /*=========================================================================
      Particles JS
    =========================================================================*/
    (function ($) {
        "use strict";
        var ViewportWidth = jQuery(window).width();
        if ((ViewportWidth) > '992') {
            particlesJS.load('particles-js', 'particles.json', function () { });
            particlesJS.load('particles-js1', 'particles.json', function () { });
        }
     
    })(jQuery);
