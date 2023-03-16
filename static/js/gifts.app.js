$(function () {
// related to index.template
    let is_side_opened = false;
    function openNav() {
        $("#mySidebar").css("width", "250px");
        //$("#main, #icons-section").css("marginLeft", "250px");
        //$(".card-holder").removeClass('col-lg-4').addClass('col-lg-6')
        $("#openNavbtn").css('display', 'none');
        is_side_opened = true;
    }

    function closeNav() {
        $("#mySidebar").css("width", "0px");
        //$("#main, #icons-section").css("marginLeft", "0px");
        $("#openNavbtn").show()
        //$(".card-holder").removeClass('col-lg-6').addClass('col-lg-4')
        is_side_opened = false;
    }

    $("#openNavbtn").click(function () {
        openNav();
    })

    $("#closeNavBtn").click(function () {
        closeNav();
    })

    $(document).on("mousemove", function (event) {
        if (event.pageX == 0) {
            openNav()
        }
    });

// related to index.template
    $(document).mouseup(function (e) {
        if (is_side_opened) {
            var container = $("#mySidebar");
            // if the target of the click isn't the container nor a descendant of the container
            if (!container.is(e.target) && container.has(e.target).length === 0) {
                closeNav();
            }
        }
    });
})