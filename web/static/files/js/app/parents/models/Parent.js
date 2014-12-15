var ParentModel = Backbone.Model.extend({
    urlRoot: '/api/parents',
    parse: function(resp) {
        resp.children = new ChildCollection(resp.children);
        resp.beacons = new BeaconCollection(resp.beacons);
        return resp;
    },

    /**
     * convert a form into it's equivalent objectified representation. For example, given a form having inputs name="bob"
     * and age=10, should return an object like {name: "bob", age: 10}
     * @param $form
     * @returns {*}
     * @private
     */
    _objFromForm: function($form) {
        return _.object(_.map($form.serializeArray(), function(obj) { return [obj.name, obj.value] }));
    },

    /**
     * create a new object in the given collection using the given form
     * @param $form the form to use for creating a  new object in the collection
     * @param collection a string representing the key for this parent to use to get a collection (for example, "children" or "beacons")
     * @private
     */
    _createFromForm: function($form, collection) {
        var childObject = this._objFromForm($form);
        this.get(collection).create(childObject, {
            error: function(collection, response, options) {
                console.log(response);
                debugger;
            }
        });

        this.trigger('change:' + collection);
    },

    /**
     * augment this Parent's fields with the data in the form
     * @param $form the form whose values to augment this Parent with
     * @private
     */
    _augmentFromForm: function($form) {
        var _this = this;
        var formObj = this._objFromForm($form);
        this.save(formObj, {
            error: function(model, resp, options) {
                console.log(resp);
                debugger;
            }
        });
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
            $.post(_this.url() + "/payment", $form.serialize(), function() {
                _this.fetch();
            });
        });
    },

    addLocationFromForm: function($form) {
        this._augmentFromForm($form);
    }
});