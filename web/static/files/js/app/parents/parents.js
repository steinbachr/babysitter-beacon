$(document).ready(function() {
    var NavBarView = Backbone.View.extend({
        el: '.header-container',
        template: _.template($('#parent-nav-template').html()),
        initialize: function() {
            var _this = this;

            this.model.bind('sync', this.render, this);
            this.model.bind('change:children', this.render, this);
        },
        events: {
            'click .new-child': 'addChild',
            'click .save-child': 'saveChild',
            'click .nav-bar a': 'selectTab'
        },

        addChild: function() {
            this.$el.find('.add-child-modal').modal();
        },

        saveChild: function() {
            this.model.addChildFromForm(this.$el.find('.add-child-modal form'));
        },

        _containerForTab: function($clickedTab) {
            var tabIndex = $clickedTab.index();
            return $($('.container').children()[tabIndex]);
        },

        _selectTab: function($clickedTab) {
            var PADDING = 2;
            var clickedTabWidth = $clickedTab.width(),
                newLeft = $clickedTab.offset().left + (clickedTabWidth / 2) + PADDING;
            var $arrow = $clickedTab.parent().find('span');

            $arrow.animate({
                left: newLeft
            }, 500);

            var $newContainer = this._containerForTab($clickedTab);
            $newContainer.siblings().hide();
            $newContainer.show();
        },

        selectTab: function(evt) {
            this._selectTab($(evt.currentTarget));
        },

        render: function() {
            this.$el.html(this.template(this.model.attributes));
            this._selectTab(this.$el.find('.nav-bar a').first());
        }
    });

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
            this.$el.html(this.template({beacons: this.model.get('beacons')}));
            return this;
        }
    });

    var AccountView = Backbone.View.extend({
        el: '.account-container',
        template: _.template($('#account-template').html()),
        events: {
            'submit .payment-form': 'addPaymentInfo'
        },
        initialize: function() {

        },

        addPaymentInfo: function() {

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