
window.CacheService = {
    inProgress: {},

    get: function(ajaxOptions) {
        var url = ajaxOptions.url;

        if (! $.isEmptyObject(ajaxOptions.data)) {
            url += '?' + $.param(ajaxOptions.data);
        }
        if (this.inProgress[url]) {
            console.log("Cached: %s", url);
            return this.inProgress[url];
        }
        else {
            console.log("New: %s", url);
            this.inProgress[url] = $.ajax(ajaxOptions);
            return this.inProgress[url];
        }
    }
};

window.EventManager = {

    publish: function(name, arg1 = null, arg2 = null, arg3 = null, arg4 = null) {
        console.log("Publishing %s", name);

        if (arg1) {
            //console.log("1> %o", arg1);
        }
        if (arg2) {
            //console.log("2> %o", arg2);
        }
        if (arg3) {
            //console.log("3> %o", arg3);
        }
        if (arg4) {
            //console.log("4> %o", arg4);
        }
        Events.publish(name, arg1, arg2, arg3, arg4);
    },

    subscribe: function(name, func) {
        console.log("Subscribing to %s from %s", name, arguments.callee.caller.name);
        Events.subscribe(name, func);
    }
};
