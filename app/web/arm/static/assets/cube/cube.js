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

    //format none
    self.none = function(v) {
        if(v == null)
            return '-';
        else
            return v;
    }

	//format timestamp to date
	self.date = function(tm) {
        if(tm == null)
            return '-';

		var date = new Date();
		date.setTime(tm*1000);
		return date.toLocaleDateString();
	}

	//form timestamp to datetime
	self.datetime = function(tm) {
        if(tm == null)
            return '-';

		var date = new Date();
		date.setTime(tm);
		return date.toLocaleString();
	}
}

//////////////validatebox extension//////////////
$.extend($.fn.validatebox.defaults.rules, {
    /*10:05:02*/
    time: {
        validator: function (value) {
            var a = value.match(/^(\d{1,2})(:)?(\d{1,2})\2(\d{1,2})$/);
            if (a == null) {
                return false;
            } else if (a[1] > 24 || a[3] > 60 || a[4] > 60) {
                return false;
            }
            return true;
        },
        message: '时间格式不正确，请重新输入。'
    },

    /*2017-02-01*/
    date: {
        validator: function (value) {
            var r = value.match(/^(\d{1,4})(-|\/)(\d{1,2})\2(\d{1,2})$/);
            if (r == null) {
                return false;
            }
            var d = new Date(r[1], r[3] - 1, r[4]);
            return (d.getFullYear() == r[1] && (d.getMonth() + 1) == r[3] && d.getDate() == r[4]);
        },
        message: '时间格式不正确，请重新输入。'
    },

    /*2014-01-01 13:04:06*/
    datetime: {
        validator: function (value) {
            var r = value.match(/^(\d{1,4})(-|\/)(\d{1,2})\2(\d{1,2}) (\d{1,2}):(\d{1,2}):(\d{1,2})$/);
            if (r == null) return false;
            var d = new Date(r[1], r[3] - 1, r[4], r[5], r[6], r[7]);
            return (d.getFullYear() == r[1] && (d.getMonth() + 1) == r[3] && d.getDate() == r[4] && d.getHours() == r[5] && d.getMinutes() == r[6] && d.getSeconds() == r[7]);
        },
        message: '时间格式不正确，请重新输入。'
    },

    /*number value*/
    number: {
        validator: function( value ) {
            return /^(?:-?\d+|-?\d{1,3}(?:,\d{3})+)?(?:\.\d+)?$/.test( value );
        },
        message: '请输入正确的数值'
    },

    /*digits value*/
    digits: {
        validator: function( value ) {
            return /^\d+$/.test( value );
        },
        message: '请输入正确的数值'
    },

    /*current input equal with another*/
    equals: {
        validator: function(value, param){
            return value == $(param[0]).val();
        },
        message: '两次输入不一致，请重新输入。'
    },

    /*minimal value*/
    min: {
        validator: function( value, param ) {
            return value >= param[0];
        },

        message: '请输入正确的数值'
    },

    /*maximum value*/
    max: {
        validator: function( value, param ) {
            return value <= param[0];
        },
        message: '请输入正确的数值'
    },

    /*range value*/
    range: {
        validator: function( value, param ) {
            return value >= param[0] && value <= param[1];
        },
        message: '请输入正确的数值'
    },

    /*length range*/
    rangelength: {
        validator: function( value, param ) {
            var length = value.length;
            return ( length >= param[ 0 ] && length <= param[ 1 ] );
        },
        message: '输入长度不正确'
    },

    /*large than*/
    largethan: {
        validator: function(value, param) {
            return value > Number($(param[0]).val());
        },
        message: '请输入正确的数值'
    },

    /*large equal than*/
    largeequal: {
        validator: function(value, param) {
            return value >= Number($(param[0]).val());
        },
        message: '请输入正确的数值'
    },

    /*less than*/
    lessthan: {
        validator: function(value, param) {
            return value < Number($(param[0]).val());
        },
        message: '请输入正确的数值'
    },

    /*less equal than*/
    lessequal: {
        validator: function(value, param) {
            return value <= Number($(param[0]).val());
        },
        message: '请输入正确的数值'
    },
});
