    $(document).ready(function () {

        $('.rightclickarea').bind('contextmenu', function (e) {
            var $cmenu = $('.vmenu');
            $('<div class="overlay"></div>').css({
                left: '0px',
                top: '0px',
                position: 'absolute',
                width: '100%',
                height: '100%',
                zIndex: '100'
            }).click(function () {
                $(this).remove();
                $cmenu.hide();
            }).bind('contextmenu', function () {
                return false;
            }).appendTo(document.body);
            $('.vmenu').css({
                left: e.pageX,
                top: e.pageY,
                zIndex: '101'
            }).show();

            return false;
        });

        $('.vmenu .first_li').live('click', function () {
            if ($(this).children().size() == 1) {
                $('.vmenu').hide();
                $('.overlay').hide();
            }
        });


        $(".first_li").hover(function () {
                $(this).css({
                    backgroundColor: '#E0EDFE',
                    cursor: 'pointer'
                });
                $(this).css({
                    cursor: 'default'
                });
            },
            function () {
                $(this).css('background-color', '#fff');
            });


    });