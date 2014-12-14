var ChildModel = Backbone.Model.extend({
});


var ChildCollection = Backbone.Collection.extend({
    model: ChildModel,
    url: '/api/children'
});