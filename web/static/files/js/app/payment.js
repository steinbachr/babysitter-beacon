var Payment = function() {
    Stripe.setPublishableKey(window.stripePublishableKey);
};

Payment.prototype.createToken = function($form) {
    var _this = this;
    var deferred = $.Deferred();

    Stripe.card.createToken({
        number: $form.find('input[name="card_number"]').val(),
        cvc: $form.find('input[name="cvc"]').val(),
        exp_month: $form.find('input[name="expiration_month"]').val(),
        exp_year: $form.find('input[name="expiration_year"]').val()
    }, function(status, response) {
        deferred.resolveWith(_this, [status, response, $form]);
    });

    $.when(deferred).then(this.responseHandler);
    return deferred.promise();
};

Payment.prototype.responseHandler = function(status, response, $form) {
    if (response.error) {
        // Show the errors on the form
        $form.find('.payment-errors').text(response.error.message);
        $form.find('button').prop('disabled', false);
    } else {
        var token = response.id;
        $form.find('input[name="stripe_token"]').val(token);
    }
};