#include "cube\http\parser.h"
BEGIN_CUBE_HTTP_NS
///////////////////////////////request message parser class////////////////////////////////////////
bool request_message_parser::has_body_done() const {
	return false;
}

int request_message_parser::add_head_line(const std::string &data) {
	//process start line
	if (_start_line) {
		_start_line = false;
		//return _request.set_start_line(data);
	}

	//process header line
	//return _request.add_header_line(data);
	return -1;
}

int request_message_parser::end_head_data() {
	return -1;
	//return _request.end_header_data();
}

int request_message_parser::add_body_data(const char *data, int sz) {
	return -1;
	//return _request.add_entity_data(data, sz);
}

int request_message_parser::end_body_data() {
	return -1;
	//return _request.end_entity_data();
}
///////////////////////////////request stream parser class////////////////////////////////////////
int request_stream_parser::feed(const char *data, int sz) {
	//check data size
	if (sz < 0)
		return -1;

	//no more stream data to feed
	if (sz == 0) {
		//check if head completed
		if (!_head_feed_completed)
			return -1;

		//set body complete flag
		_body_feed_completed = true;
		_message_parser.end_body_data();

		return 0;
	}

	//head has completed, feed body data
	if (_head_feed_completed)
		return _message_parser.add_body_data(data, sz);

	//head not completed, feed head data first
	int fsz = 0;
	while (fsz < sz) {
		fsz += _line_buffer.put(data+ fsz, sz- fsz);
		if (_line_buffer.full()) {
			//new message line
			std::string strline = _line_buffer.line();
			if (strline.empty()) {
				//set head completed flag
				_head_feed_completed = true;
				_message_parser.end_head_data();

				//send left body data to message parser
				int bsz = _message_parser.add_body_data(data + fsz, sz - fsz);
				if (bsz < 0)
					return -1;

				//add new body feed size
				fsz += bsz;

				break;
			} else {
				//send to message parser
				if (_message_parser.add_head_line(strline) != 0)
					return -1;

				//clear current line buffer for next line
				_line_buffer.clear();
			}
		}
	}

	return fsz;
}

bool request_stream_parser::done() const {
	return _head_feed_completed && (_body_feed_completed || _message_parser.has_body_done());
}
END_CUBE_HTTP_NS
