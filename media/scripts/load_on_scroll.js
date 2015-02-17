$(function(){
    var App = {
        nextStartItem: 0,
        scrollThreshold: 100,
        loading: false,
        setStartItem: function(){
            var app = this;
            app.nextStartItem = parseInt($('#load_next_page').data('start_item'));
            return app.nextStartItem;
        },
        LoadPage: function() {
            var app = this;
            if(!app.loading) {
                app.loading = true;
                app.nextStartItem = app.setStartItem();
                $.get(
                    '/',
                    {
                        'start_from': app.nextStartItem,
                        'ajax': 'Y'
                    },
                    function (data) {
                        $('#place_for_next_page').replaceWith($(data));
                        app.loading = false;
                    }
                )
            }
        },
        Init: function(){
            var app = this;
            app.nextStartItem = parseInt($('#load_next_page').data('start_item'));
            $('#content').on('click', '#load_next_page', function() {
                 app.LoadPage();
            });
            $(window).scroll(function(){
                var documentHeight = $(document).height(),
                    windowHeight = $(window).height(),
                    scrollTop = $(window).scrollTop(),
                    n = documentHeight - windowHeight - scrollTop;
                if(n <= app.scrollThreshold) {
                    app.LoadPage();
                }
            })
        }
    };
    App.Init();
});