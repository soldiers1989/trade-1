#include <fstream>
#include "cube\cfg\ini.h"
#include "cube\str\stype.h"
#include "cube\str\cast.h"
#include "cube\str\strip.h"

BEGIN_CUBE_CFG_NS
void section::set_item(const std::string &key, const std::string &value) {
	_items.insert(std::pair<std::string, std::string>(key, value));
}

int	section::get_item(const std::string &key, std::string &value) {
	std::map<std::string, std::string>::const_iterator iter = _items.find(key);
	if (iter != _items.end()) {
		value = iter->second;
		return 0;
	}
	return -1;
}

std::string section::tostring() {
	std::string res = "[" + _name + "]\n";

	std::map<std::string, std::string>::const_iterator iter = _items.begin();
	while (iter != _items.end()) {
		res = res + iter->first + "=" + iter->second + "\n";
		iter++;
	}
	return res;
}


void sections::set_item(const std::string &section_name, const std::string &key, const std::string &value) {
	std::map<std::string, section>::iterator iter = _sections.find(section_name);
	if (iter != _sections.end())
		iter->second.set_item(key, value);
	else {
		section newsection(section_name);
		newsection.set_item(key, value);
		_sections.insert(std::pair<std::string, section>(section_name, newsection));
	}
}

int	sections::get_item(const std::string &section_name, const std::string &key, std::string &value) {
	std::map<std::string, section>::iterator iter = _sections.find(section_name);
	if (iter != _sections.end())
		return iter->second.get_item(key, value);
	return -1;
}

std::string sections::tostring() {
	std::string res("");
	std::map<std::string, section>::iterator iter = _sections.begin();
	while (iter != _sections.end()) {
		res.append(iter->second.tostring());
		iter++;
	}
	return res;
}

int ini::load(const char *file_path) {
	//save file path
	_file_path = file_path;

	//read content from file
	std::ifstream ifs(file_path, std::ifstream::in);
	if (!ifs.is_open())
		return -1;

	//line buffer
	const std::streamsize BUFSZ = 2048;
	char buf[BUFSZ] = { 0 };

	//current section name
	std::string section("");

	//process each file line
	ifs.getline(buf, BUFSZ);
	while (ifs.good()) {
		//process current line
		std::string line = str::strip(buf);
		if (!line.empty() && !is_comment(line)) {
			if (is_section(line))
				section = parse_section_name(line);
			else {
				std::string key, value;
				if (parse_key_value(line, key, value))
					_sections.set_item(section, key, value);
				else
					return -1; //invalid configure
			}
		}

		//next line
		ifs.getline(buf, BUFSIZ);
	}

	return 0;
}

int ini::save(const char * file_path) {
	std::ofstream ofs(file_path, std::ofstream::out);
	if (!ofs.is_open())
		return -1;

	ofs << _sections.tostring();

	return 0;
}

void ini::set_string_value(const std::string &section, const std::string& key, const std::string &value) {
	_sections.set_item(section, key, value);
}

std::string ini::get_string_value(const std::string &section, const std::string& key, const char *default) {
	std::string value("");
	int err = _sections.get_item(section, key, value);
	if (err != 0 && default != 0) {
		value = default;
	}
	return value;
}


void ini::set_integer_value(const std::string &section, const std::string &key, int value) {
	_sections.set_item(section, key, str::string(value));
}

int ini::get_integer_value(const std::string &section, const std::string &key, int default) {
	std::string svalue;
	int err = _sections.get_item(section, key, svalue);
	if (err != 0 && str::isnum(svalue.c_str()))
		return ::atoi(svalue.c_str());

	return default;
}

void ini::set_float_value(const std::string &section, const std::string &key, float value) {
	_sections.set_item(section, key, str::string(value));
}

float ini::get_float_value(const std::string &section, const std::string &key, float default) {
	std::string svalue;
	int err = _sections.get_item(section, key, svalue);
	if (err != 0 && str::isfloat(svalue.c_str())) {
		return (float)::atof(svalue.c_str());
	}

	return default;
}

bool ini::is_section(const std::string &line) {
	if (line[0] == '[' && line[line.length() - 1] == ']')
		return true;

	return false;
}

bool ini::is_comment(const std::string &line, const char* ctags/* = "#;/"*/) {
	if (strchr(ctags, line[0]) != 0)
		return true;
	return false;
}

std::string	ini::parse_section_name(const std::string &line) {
	return str::strip(line.substr(1, line.length() - 2));
}

bool ini::parse_key_value(const std::string &line, std::string &key, std::string &value, const char* ctags/* = "#;/"*/) {
	size_t pos = line.find('=');
	if (pos == std::string::npos)
		return false; // invalid item

	//parse key
	key = str::strip(line.substr(0, pos));

	//process value and comment
	std::string vc = str::strip(line.substr(pos + 1)); // value and comment
	size_t cpos = std::string::npos; //comment pos
	for (pos = 0; pos < value.length(); pos++) {
		if (strchr(ctags, value[pos]) != 0) {
			cpos = pos;
			break;
		}
	}

	//parse value
	value = str::strip(vc.substr(0, cpos));

	return true;
}

std::string ini::tostring() {
	return _sections.tostring();
}
END_CUBE_CFG_NS
