var BeaconModel = Backbone.Model.extend({
});


var BeaconCollection = Backbone.Collection.extend({
    model: BeaconModel,
    url: '/api/beacons'
});