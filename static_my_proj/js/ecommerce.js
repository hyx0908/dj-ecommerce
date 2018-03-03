$(() => {
    // Contact Form Handler
    var contactForm = $(".contact-form")
    var contactFormMethod = contactForm.attr("method")
    var contactFormEndpoint = contactForm.attr("action")
    var contactFormSubmitBtn = contactForm.find("[type='submit']")
    var contactFormSubmitBtnTxT = contactFormSubmitBtn.text()

    function displaySubmitting(doSubmit, defaultText) {
        if (doSubmit) {
            contactFormSubmitBtn.addClass("disabled")
            contactFormSubmitBtn.html("<i class='fas fa-spin fa-spinner'></i> Sending...")
        } else {
            contactFormSubmitBtn.removeClass("disabled")
            contactFormSubmitBtn.html(defaultText)
        }
    }


    contactForm.submit(function (event) {
        event.preventDefault()
        var contactFormData = contactForm.serialize()
        var thisForm = $(this)
        displaySubmitting(true, "")
        $.ajax({
            url: contactFormEndpoint,
            method: contactFormMethod,
            data: contactFormData,
            success: function (data) {
                thisForm[0].reset()
                setTimeout(function () {
                    displaySubmitting(false, contactFormSubmitBtnTxT)
                }, 500)
                $.dialog({
                    title: "<h1>Success!</h1>",
                    content: data.message,
                    theme: "modern",
                    type: "dark",
                    closeIcon: true,
                    closeIconClass: "fas fa-times"
                })
            },
            error: function (error) {
                setTimeout(function () {
                    displaySubmitting(false, contactFormSubmitBtnTxT)
                }, 500)
                $.alert({
                    title: "Ooops!",
                    content: "An error occured!",
                    theme: "modern",
                    type: "dark",
                    closeIcon: true,
                    closeIconClass: "fa fa-close"
                })
            }
        })
    })


/*    // Autocomplete Search
    var searchForm = $(".search-form")
    var searchInput = searchForm.find("[name='q']")
    var typingInterval = 500
    var typingTimer
    var searchBtn = searchForm.find("[type='submit']")
    searchInput.keyup(function (event) {
        clearTimeout(typingTimer)
        typingTimer = setTimeout(performSearch, typingInterval)
    })
    searchInput.keydown(function (event) {
        clearTimeout(typingTimer)
    })

    function doSearch() {
        searchBtn.addClass("disabled")
        searchBtn.html("<i class='fas fa-spin fa-spinner'></i> Searching...")
    }

    function performSearch() {
        doSearch()
        var query = searchInput.val()
        setTimeout(function () {
            window.location.href = '/search/?q=' + query
        }, 1000)
    }*/




    // Adding/removing product to/from cart
    var productFom = $('.form-product-ajax')
    productFom.submit(function (event) {
        event.preventDefault()
        var $thisForm = $(this)
        var actionEndpoint = $thisForm.attr('data-endpoint')
        var formMethod = $thisForm.attr('method')
        var formData = $thisForm.serialize()

        $.ajax({
            url: actionEndpoint,
            method: formMethod,
            data: formData,
            success: function (data) {
                var submitSpan = $thisForm.find('.submit-span')
                if (data.added) {
                    submitSpan.html('<button type="submit" class="btn btn-danger">Remove?</button>')
                } else {
                    submitSpan.html('<button type="submit" class="btn btn-success">Add to cart</button>')
                }

                var navbarCartCount = $('.navbar-cart-count')
                navbarCartCount.text(data.cartItemCount)
                var currentPath = window.location.href
                if (currentPath.indexOf("cart") !== -1) {
                    refreshCart()
                }
            },
            error: function (errorData) {
            }
        })

    })

    function refreshCart() {
        var cartTable = $(".cart-table")
        var cartBody = cartTable.find(".cart-body")
        var productsRow = cartBody.find(".cart-product")
        var currentUrl = window.location.href

        var refreshCartUrl = '/api/cart/'
        var refreshCartMethod = "GET"
        var data = {}
        $.ajax({
            url: refreshCartUrl,
            method: refreshCartMethod,
            data: data,
            success: function (data) {
                var hiddenCartItemRemoveForm = $(".cart-item-remove-form")

                if (data.products.length > 0) {
                    productsRow.remove()
                    i = data.products.length
                    $.each(data.products, function (index, value) {
                        var newCartItemRemove = hiddenCartItemRemoveForm.clone()
                        newCartItemRemove.removeClass("display-hidden")
                        newCartItemRemove.find(".cart-item-product-id").val(value.id)
                        cartBody.prepend("<tr class='cart-product'><th scope='row'>" + i + "</th><td><a href='" + value.url + "'>" +
                            value.title + "</a>" + newCartItemRemove.html() + "</td><td>" + value.price +
                            "</td></tr>")
                        i--
                    })
                    cartBody.find(".cart-subtotal").text(data.subtotal)
                    cartBody.find(".cart-total").text(data.total)
                } else {
                    window.location.href = currentUrl
                }
            },
            error: function (error) {
                console.log("error", error)
            }
        })

    }
})