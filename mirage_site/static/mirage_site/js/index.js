
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode
'use strict';

// add support for cross-domain requests
$.support.cors = true;

// initializes the app
$(document).ready(function() {
    // http://thejacklawson.com/Mediator.js/
    window.Events = new Mediator() || {};

    InputHandler.init();
    RequestsManager.init();
    LayoutManager.init();
    URLManager.init();

    //fix for select2 IE disable bug
    $('#naics-code').fireOnDisable().select2();
    $('#placeholder').select2({ 
        'placeholder': 'Select a vehicle', 
        minimumResultsForSearch: -1,
        width: "170px"
    });
});

// removes empty strings
Array.prototype.removeEmpties = function() {
  for (var i = 0; i < this.length; i++) {
    if (this[i].length === 0) {         
      this.splice(i, 1);
      i--;
    }
  }
  return this;
};

// .bind() polyfill
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/bind#Compatibility
if (!Function.prototype.bind) {
Function.prototype.bind = function (oThis) {
    if (typeof this !== "function") {
        // closest thing possible to the ECMAScript 5
        // internal IsCallable function
        throw new TypeError("Function.prototype.bind - what is trying to be bound is not callable");
    }

    var aArgs = Array.prototype.slice.call(arguments, 1), 
        fToBind = this, 
        fNOP = function () {},
        fBound = function () {
          return fToBind.apply(this instanceof fNOP && oThis
                 ? this
                 : oThis,
                 aArgs.concat(Array.prototype.slice.call(arguments)));
        };

    fNOP.prototype = this.prototype;
    fBound.prototype = new fNOP();

    return fBound;
  };
}

// .trim() polyfill
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/Trim#Compatibility
if (!String.prototype.trim) {
  String.prototype.trim = function () {
    return this.replace(/^[\s\xA0]+|[\s\xA0]+$/g, '');
  };
}
