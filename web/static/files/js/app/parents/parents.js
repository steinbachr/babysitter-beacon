$(document).ready(function() {
    var BeaconsView = Backbone.View.extend({
        el: ".beacons-container",
        template: _.template($('#beacons-template').html()),
        events: {
            'click .create-beacon': 'createBeacon',
            'click .save-beacon': 'saveBeacon'
        },
        initialize: function() {
            this.model.bind('sync', this.render, this);
            this.model.bind('change:beacons', this.render, this);
        },

        createBeacon: function() {
            this.$el.find('.add-beacon-modal').modal();
        },

        saveBeacon: function() {
            this.model.addBeaconFromForm(this.$el.find('.add-beacon-modal form'));
        },

        render: function() {
            this.$el.html(this.template({beacons: this.model.get('beacons'), parent: this.model}));
            return this;
        }
    });

    var AccountView = Backbone.View.extend({
        el: '.account-container',
        template: _.template($('#account-template').html()),
        events: {
            'submit .payment-form': 'addPaymentInfo',
            'submit .location-form': 'addLocationInfo'
        },
        initialize: function() {
            this.model.bind('sync', this.render, this);
        },

        addPaymentInfo: function(evt) {
            evt.preventDefault();
            this.model.addPaymentInfoFromForm($(evt.currentTarget));
        },

        addLocationInfo: function(evt) {
            evt.preventDefault();
            this.model.addLocationFromForm($(evt.currentTarget));
        },

        render: function() {
            this.$el.html(this.template(this.model.attributes));
            return this;
        }
    });

    new NavBarView({
        model: parentModel
    });

    new BeaconsView({
        model: parentModel
    });

    new AccountView({
        model: parentModel
    });

    parentModel.fetch();
});