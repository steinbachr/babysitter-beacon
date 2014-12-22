$(document).ready(function() {
    new NavBarView({
        model: sitterModel
    });

    sitterModel.fetch();
});