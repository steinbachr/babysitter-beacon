var ParentModel = Backbone.Model.extend({
    urlRoot: '/api/parents',
    paymentUrl: this.urlRoot + "/payment",
    parse: function(resp) {
        resp.children = new ChildCollection(resp.children);
        resp.beacons = new BeaconCollection(resp.beacons);
        return resp;
    },

    /**
     * create a new object in the given collection using the given form
     * @param $form the form to use for creating a  new object in the collection
     * @param collection a string representing the key for this parent to use to get a collection (for example, "children" or "beacons")
     * @private
     */
    _createFromForm: function($form, collection) {
        var childObject = _.object(_.map($form.serializeArray(), function(obj) { return [obj.name, obj.value] }));
        this.get(collection).create(childObject, {
            error: function(collection, response, options) {
                debugger;
            }
        });

        this.trigger('change:' + collection);
    },

    addChildFromForm: function($form) {
        this._createFromForm($form, "children");
    },

    addBeaconFromForm: function($form) {
        this._createFromForm($form, "beacons");
    },

    addPaymentInfoFromForm: function($form) {
        var _this = this;
        var paymentObj = new Payment();
        var deferred = paymentObj.createToken($form);

        $.when(deferred).then(function() {
            $.post(_this.paymentUrl, $form.serialize(), function() {
                _this.fetch();
            });
        });
    }
});