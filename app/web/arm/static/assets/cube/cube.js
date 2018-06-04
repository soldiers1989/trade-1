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

cube.format = new function() {
	var self = this;

	//format boolean
	self.boolean = function(b) {
		if(b)
			return '是';
		else
			return '否';
	}

	//format timestamp to date
	self.date = function(tm) {
		var date = new Date();
		date.setTime(tm*1000);
		return date.toLocaleDateString();
	}

	//form timestamp to datetime
	self.datetime = function(tm) {
		var date = new Date();
		date.setTime(tm);
		return date.toLocaleString();
	}
}