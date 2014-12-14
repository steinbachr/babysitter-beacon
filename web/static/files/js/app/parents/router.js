var ParentsRouter = Backbone.Router.extend({
    routes: {
        "dashboard": "dashboard",
        "account": "account",
        "*actions": "defaultRoute" // matches http://example.com/#anything-here
    }
});

// Initiate the router
var parentsRouter = new ParentsRouter;

parentsRouter.on('route:dashboard', function(actions) {
    ParentsPage.dashboard();
});
parentsRouter.on('route:account', function(actions) {
    ParentsPage.account();
});

// Start Backbone history a necessary step for bookmarkable URL's
Backbone.history.start();