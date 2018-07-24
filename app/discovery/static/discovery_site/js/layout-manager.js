
var LayoutManager = {
    initializers: {},
    preprocessors: {},

    init: function() {
        // Internal event subscriptions
        EventManager.subscribe('dataInitialized', LayoutManager.route);

        for(var handler in LayoutManager.initializers){
            LayoutManager.initializers[handler].call(this);
        }
    },

    route: function() {
    },

    execPreprocessors: function() {
        for (var handler in LayoutManager.preprocessors){
            LayoutManager.preprocessors[handler].call(this);
        }
    }
};