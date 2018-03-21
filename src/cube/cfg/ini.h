/*
*	ini - ini configure file module
*/
#pragma once
#include <map>
#include "cube\ns.h"
BEGIN_CUBE_CFG_NS
//section structure of configure file
class section {
public:
	section(std::string name) : _name(name){}
	virtual ~section() {}

	/*
	*	add a item to section
	*@param key: in, key of item
	*@param value: in, value of item
	*@return:
	*	void
	*/
	void set_item(const std::string &key, const std::string &value);

	/*
	*	get item value from section
	*@param key: in, key of item
	*@param value: out, value of item
	*return:
	*	0--sucess, -1--failed
	*/
	int	get_item(const std::string &key, std::string &value);

	/*
	*	convert section to string
	*@return:
	*	string of represent the section
	*/
	std::string tostring();

private:
	//section name
	std::string _name;
	//items in section
	std::map<std::string, std::string>	_items;
};

//sections of configure file
class sections {
public:
	sections() {}
	virtual ~sections() {}

	/*
	*	add a item to section
	*@param section_name: in, section name
	*@param key: in, key of item
	*@param value: in, value of item
	*@return:
	*	void
	*/
	void set_item(const std::string &section_name, const std::string &key, const std::string &value);

	/*
	*	get item value from section
	*@param section_name: in, section name
	*@param key: in, key of item
	*@param value: out, value of item
	*return:
	*	0--sucess, -1--failed
	*/
	int	get_item(const std::string &section_name, const std::string &key, std::string &value);

	/*
	*	convert sections to string
	*@return:
	*	string of represent the sections
	*/
	std::string tostring();

private:
	//sections of configure
	std::map<std::string, section>	_sections;
};


class ini {
public:
	ini() {}
	virtual ~ini() {}

	/*
	*	load a configure
	*@param file_path: in, the configure file path to read from
	*@return:
	*	0--success, -1--open configure file failed.
	*/
	int load(const char* file_path);

	/**
	* 	write current configure to file
	*@param file_path: in, the configure file path write to
	*@return
	* 	0-- successed, -1-- failed
	*/
	int save(const char *file_path);

	/*
	*	read a string value from the configure file which specified by the section and item value.
	*@param section: in, the string value in []
	*@param key: in, the string value before = of every line
	*@param value: out, the string value
	*@return:
	*	0--success, -1--failed
	*/
	void set_string_value(const std::string &section, const std::string& key, const std::string &value);
	std::string get_string_value(const std::string &section, const std::string& key, const char *default = 0);

	/*
	*	read a integer value from the configure file which specified by the section and item value.
	*@param section: in, the string value in []
	*@param key: in, the string value before = of every line
	*@param value: out, the string value
	*@return:
	*	0--success, -1--failed
	*/
	void set_integer_value(const std::string &section, const std::string &key, int value);
	int get_integer_value(const std::string &section, const std::string &key, int default = 0);

	/*
	*	read a float value from the configure file which specified by the section and item value.
	*@param section: in, the string value in []
	*@param key: in, the string value before = of every line
	*@param value: out, the float value
	*@return:
	*	0--success, -1--failed
	*/
	void set_float_value(const std::string &section, const std::string &key, float value);
	float get_float_value(const std::string &section, const std::string &key, float default = 0.0);

	/*
	*	convert ini to string
	*@return:
	*	string of represent the sections
	*/
	std::string tostring();
private:
	/*
	*	 check if current line of string is section
	*@param line: in, a line of string
	*@return:
	*	true if is section, otherwise false
	*/
	bool is_section(const std::string &line);

	/*
	*	check if current line of string is comment which start with specified tag characters
	*@param line: in, a line of string
	*@param ctags: in, tag of comment start characters
	*@return:
	*	true if is comment, otherwise false
	*/
	bool is_comment(const std::string &line, const char* ctags = "#;/");

	/*
	*	parse section name from a line of string with format "[section name]", e.g. "[section1]" -> "section1"
	*@param line: in, a line of string
	*@return:
	*	section name without square bracket
	*/
	std::string	parse_section_name(const std::string &line);

	/*
	*	parse key value of item
	*@param line: in, a line of string
	*@param key: out, key of item
	*@param value: out, value of item
	*@param ctags: in, tag of comment start characters
	*@return:
	*	true if parse success, otherwise false
	*/
	bool parse_key_value(const std::string &line, std::string &key, std::string &value, const char* ctags = "#;/");

private:
	//configure file path
	std::string	_file_path;

	//sections of configure
	sections _sections;
};
END_CUBE_CFG_NS
