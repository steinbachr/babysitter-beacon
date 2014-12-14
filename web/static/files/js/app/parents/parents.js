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

        _selectTab: function($clickedTab) {
            var PADDING = 2;
            var clickedTabWidth = $clickedTab.width(),
                newLeft = $clickedTab.offset().left + (clickedTabWidth / 2) + PADDING;
            var $arrow = $clickedTab.parent().find('span');

            $arrow.animate({
                left: newLeft
            }, 500);
        },

        selectTab: function(evt) {
            this._selectTab($(evt.currentTarget));
        },

        render: function() {
            this.$el.html(this.template(this.model.attributes));
            this._selectTab(this.$el.find('.nav-bar a').first());
        }
    });

    new NavBarView({
        model: parentModel
    });

    parentModel.fetch();
});