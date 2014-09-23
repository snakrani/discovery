// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode
'use strict';

// initializes the app
$(document).ready(function() {
    // http://thejacklawson.com/Mediator.js/
    window.Events = new Mediator() || {};

    InputHandler.init();
    RequestsManager.init();
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

// .bind() polyfill
// https://gist.github.com/dsingleton/1312328
Function.prototype.bind=Function.prototype.bind||function(b){if(typeof this!=="function"){throw new TypeError("Function.prototype.bind - what is trying to be bound is not callable");}var a=Array.prototype.slice,f=a.call(arguments,1),e=this,c=function(){},d=function(){return e.apply(this instanceof c?this:b||window,f.concat(a.call(arguments)));};c.prototype=this.prototype;d.prototype=new c();return d;};
