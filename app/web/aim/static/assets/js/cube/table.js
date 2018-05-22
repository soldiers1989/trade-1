/**
* @author polly
* version: 0.1
* 
*/
var cube = {};

cube.

function Table(head, body, form) {
	this.head = head;
	this.body = body;
	this.form = form;
};

Table.prototype = {
	constructor: Table,
	hello: function() {
		return this.head;
	}
};

var table = new Table('a', 'b', 'c');
console.log(table.hello());
	