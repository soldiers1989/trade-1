/**
* @author polly
* version: 0.1
* 
*/

function CubeTable(init) {
  this.tableid = init.id;
	this.tableform = $('#'+init.id+"_form");
  this.tablebody = $('#'+init.id+"_body");
  this.tabledetail = $('#'+init.id+"_detail");
  this.tablepager = $('#'+init.id+"_pager");

  this.tablecols = init.columns;

  this.tablesize = init.size;
  this.tablesizes = init.sizes;

  this.requesturl = init.url;
}

CubeTable.prototype = {
	constructor: CubeTable,

  /**
  * @method
  * @param rowitems: array, table row items data
  *   [{'name1': data1, 'name2': data2, ...}, ...]
  * @param columns: array, table column definiation
  *   [{'name': 'name or index in data item', 'render': function(data)}, ...]
  * @return: str, row/col html text 
  */
  renderRows: function(items) {
    //html row array
    htmlrows = [];

    //process each row item data
    for (i=0; i<items.length; i++){
      //current row data
      item = items[i];

      //row columns
      htmlcols = []

      //add row start
      htmlrow = '<tr>\n'

      //extract column data for row
      for (j=0; j<this.tablecols.length; j++){
        column = this.tablecols[j];
        
        name = j;
        if (column.data)
          name = column.data;

        render = function(x){
          return x;
        };
        if (column.render)
          render = column.render

        data = '';
        // column original data
        if (name) {
          data = item[name];
        } else {
          data = item[j];
        }

        // column rendered data
        if (render) {
          data = render(data);
        }

        // column html data
        htmlcol = '\t<td>' + data + '</td>';

        // add to html columns
        htmlcols.push(htmlcol);
      }

      // add row columns
      htmlrow += htmlcols.join('\n');

      // add row end
      htmlrow += '\n</tr>';

      htmlrows.push(htmlrow);
    }

    return htmlrows.join('\n');
  },

  // render page data
  renderPage: function(page, total, size, style) {
    pages = Math.ceil(total/size);
    if (page > pages)
      page = pages;

    if (page < 0 || pages == 0)
      page = 0;

    if (!style)
      style = 'float: right; margin: 0px;';

    prestatus = '', nextstatus = '', currstatus = ' disabled';
    if (page <= 1)
      prestatus = ' disabled';

    if (page == pages)
      nextstatus = ' disabled';

    html = '<ul class="pagination" style="' + style + '">\n'
            + '\t<li class="page-item'+prestatus+'"><a class="page-link" tbl="'+this.tableid+'" act="first">&lt;&lt;</a></li>\n'
            + '\t<li class="page-item'+prestatus+'"><a class="page-link" tbl="'+this.tableid+'" act="pre" href="#">&lt;</a></li>\n'
            + '\t<li class="page-item'+currstatus+'"><a class="page-link" tbl="'+this.tableid+'" act="curr" href="#">'+page+'</a></li>\n'
            + '\t<li class="page-item'+nextstatus+'"><a class="page-link" tbl="'+this.tableid+'" act="next" href="#">&gt;</a></li>\n'
            + '\t<li class="page-item'+nextstatus+'"><a class="page-link" tbl="'+this.tableid+'" act="last" href="#">&gt;&gt;</a></li>\n'
            + '</ul>';

    return html;
  },

  // render size selector
  renderSize: function(size) {
    html = '<span>每页\n'
            + '\t<select name="page">\n';

    for (i=0; i<this.tablesizes.length; i++){
      if (size == this.tablesizes[i])
        html += '\t\t<option value="'+this.tablesizes[i]+'" selected>'+this.tablesizes[i]+'</option>\n';
      else
        html += '\t\t<option value="'+this.tablesizes[i]+'">'+this.tablesizes[i]+'</option>\n';
    }
    
    html += '\t</select>\n';
    html += '条</span>';

    return html;
  },

  // render items information
  renderInfo: function(page, total, size) {
    pages = Math.ceil(total/size);
    spos = (page-1)*size, epos = page*size;
    if (spos < 0)
      spos = 0;
    if (epos > total)
      epos = total;

    html = '<span>第'+spos+'-'+epos+'条, 共'+total+'条; 第'+page+'页, 共'+pages+'页</span>';
    return html;
  },

  // render table info&size html
  renderDetail: function(page, total, size) {
    htmlsep = '\n<span>|</span>\n';
    return this.renderInfo(page, total, size) + htmlsep + this.renderSize(size, this.tablesizes);
  },


  // render table
  render: function(data) {
    // render table body
    this.tablebody.html(this.renderRows(data.items));

    // render table detail
    this.tabledetail.html(this.renderDetail(data.page, data.total, data.size));

    // render table pager
    this.tablepager.html(this.renderPage(data.page, data.total, data.size));
  },


  // go to first page
  gotoFirstPage: function() {
    alert('goto first page');
  },

  // go to last page
  gotoLastPage: function() {
    alert('goto last page');
  },

  // go to pre page
  gotoPrePage: function() {
    alert('goto pre page');
  },

  // go to next page
  gotoNextPage: function() {
    alert('goto next page');
  },

  // change page size
  changePageSize: function() {
    alert('change page size');
  },

  // query table data
  load: function() {
      //set form default input value

      //check form data
      if(this.tableform.valid()){
          this.tableform.ajaxSubmit({
             url: this.requesturl,
             type: 'get',
             table: this,
             success: function(resp) {
                  if(resp.status){
                    // render table
                    this.table.render(resp.data);

                    // add change page event
                    $('.page-link').click(function(){
                      tableid = $(this).attr('tbl');
                      pageact = $(this).attr('act');
                    });


                    // add change page size event
                  } else {
                    alert(resp.status);
                  }
             }
          });
      }
  }
};



