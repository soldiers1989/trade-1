/**
* @author polly
* version: 0.1
* 
*/
var cube = {};

/////////////time///////////////
cube.time = new function() {
	var self = this;

	//timestamp to local date time string
	self.localstr = function(tm) {
    	var date = new Date();
    	date.setTime(tm*1000);
    	return date.toLocaleString();
 	};
 };

/////////////page///////////////

