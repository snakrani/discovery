// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode
'use strict';

// initializes the app
$(document).ready(function() {
    // http://thejacklawson.com/Mediator.js/
    window.Events = new Mediator() || {};

    InputHandler.init();
    ResultsManager.init();
    LayoutManager.init();
    URLManager.init();
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
