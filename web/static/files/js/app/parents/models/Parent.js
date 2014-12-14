var ParentModel = Backbone.Model.extend({
    urlRoot: '/api/parents',
    parse: function(resp) {
        resp.children = new ChildCollection(resp.children);
        return resp;
    },

    addChildFromForm: function($form) {
        var childObject = _.object(_.map($form.serializeArray(), function(obj) { return [obj.name, obj.value] }));
        this.get('children').create(childObject, {
            error: function(collection, response, options) {
                debugger;
            }
        });
        this.trigger('change:children');
    }
});