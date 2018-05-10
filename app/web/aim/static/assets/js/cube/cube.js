/**
* @author polly
* version: 0.1
* 
*/
var cube = window.NameSpace || {}

//time relate functions
cube.time = new function() {
	var self = this;

	self.localstr = function(tm) {
    	var date = new Date();
    	date.setTime(tm*1000);
    	return date.toLocaleString();
 	};
 };
