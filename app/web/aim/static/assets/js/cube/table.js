/**
* @author polly
* version: 0.1
* 
*/

function CubeTable(init) {
  //table id
  this.id = init.id;

  //ajax url
  this.url = init.url;

  //table elements
  this.dom = {
    form: $('#'+this.id+"_form"),
    body: $('#'+this.id+"_body"),
    info: $('#'+this.id+"_info"),
    page: $('#'+this.id+"_page"),
    size: $('#'+this.id+"_size"), 
    input: {
      start: $('#'+init.id+"_start"),
      count: $('#'+init.id+"_count"),
      order: $('#'+init.id+"_order"),
      orderby: $('#'+init.id+"_order_by")
    },
    query: $('#'+init.id+"_query")
  };

  //table data
  this.data = {
    total: 0,
    start: 0,
    end: 0,
    items: {}
  };

  //table page
  this.page = {
    size: 20,
    total: 0,
    current: 1,
    options: [10, 20, 30, 50, 100, 200, 500],
    style: 'float: center; margin: 0px;'
  };

  //table info
  this.info = {
    style: 'float: left'
  };

  //table size
  this.size = {
    style: 'float: right'
  };

  //table columns
  this.columns = init.columns;
}

CubeTable.prototype = {
	constructor: CubeTable,

  renderEmpty: function() {
    html = '<tr class="odd"><td valign="top" colspan="'+this.columns.length+'" style="text-align: center;">没有数据</td></tr>';
    this.dom.body.html(html);
  },

  renderLoading: function() {
    html = '<tr class="odd"><td valign="top" colspan="'+this.columns.length+'" style="text-align: center;">正在加载数据...</td></tr>';
    this.dom.body.html(html);
  },

  renderFailure: function(msg) {
    html = '<tr class="odd"><td valign="top" colspan="'+this.columns.length+'" style="text-align: center;">'+msg+'</td></tr>';
    this.dom.body.html(html);
  },

  renderRows: function() {
    //epmpty data
    if(this.data.items.length == 0){
      this.renderEmpty();
      return;
    }

    //html row array
    htmlrows = [];

    //process each row item data
    for (i=0; i<this.data.items.length; i++){
      //current row data
      item = this.data.items[i];

      //row columns
      htmlcols = []

      //add row start
      htmlrow = '<tr>\n'

      //extract column data for row
      for (j=0; j<this.columns.length; j++){
        column = this.columns[j];
        
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

    //body html
    html = htmlrows.join('\n');

    //render body
    this.dom.body.html(html);
  },

  // render page data
  renderPage: function() {  
    prestatus = '', nextstatus = '';
    if (this.page.current <= 1)
      prestatus = ' disabled';

    if (this.page.current >= this.page.total)
      nextstatus = ' disabled';

    html = '<ul class="pagination" style="' + this.page.style + '">\n'
            + '\t<li class="'+prestatus+'"><a linktbl="'+this.id+'" act="first">&lt;&lt;</a></li>\n'
            + '\t<li class="'+prestatus+'"><a linktbl="'+this.id+'" act="previous" href="#">&lt;</a></li>\n'
            + '\t<li class="disabled"><a href="#">'+this.page.current+'</a></li>\n'
            + '\t<li class="'+nextstatus+'"><a linktbl="'+this.id+'" act="next" href="#">&gt;</a></li>\n'
            + '\t<li class="'+nextstatus+'"><a linktbl="'+this.id+'" act="last" href="#">&gt;&gt;</a></li>\n'
            + '</ul>';

    //render
    this.dom.page.html(html);
  },

  // render size selector
  renderSize: function() {
    html = '<span style="'+this.size.style+'">每页\n'
            + '\t<select sztbl="'+this.id+'">\n';

    for (i=0; i<this.page.options.length; i++){
      if (this.page.size == this.page.options[i])
        html += '\t\t<option value="'+this.page.options[i]+'" selected>'+this.page.options[i]+'</option>\n';
      else
        html += '\t\t<option value="'+this.page.options[i]+'">'+this.page.options[i]+'</option>\n';
    }
    
    html += '\t</select>\n';
    html += '条</span>';

    //render
    this.dom.size.html(html);
  },

  // render items information
  renderInfo: function() {
    html = '<span style="'+this.info.style+'">第'+this.data.start+'-'+this.data.end+'条, 共'+this.data.total+'条; 第'+this.page.current+'页, 共'+this.page.total+'页</span>';
    //render
    this.dom.info.html(html);
  },

 // add page event
  addPageEvent: function() {
    $('a[linktbl="'+this.id+'"]').on('click', {table: this}, function(e){
      act = $(this).attr('act');
      e.data.table.goto(act);
    });
  },

  // add size event
  addSizeEvent: function() {
    $('select[sztbl="'+this.id+'"]').on('change', {table: this}, function(e){
      e.data.table.resize();
    });
  },


  // render table
  render: function() {
    // render table body
    this.renderRows();

    // render table info
    this.renderInfo();

    // render table size
    this.renderSize();

    // render table pager
    this.renderPage();
  },

   // go to page
  goto: function(act) {
    //change current page
    if(act == 'first'){
      this.page.current = 1;      
    }
    else if ( act == 'previous') {
      if(this.page.current > 1)
        this.page.current--;
    }
    else if( act == 'next'){
      if(this.page.current < this.page.total)
        this.page.current++;
    }
    else if( act == 'last'){
      this.page.current = this.page.total;
    }
    else
      ;

    //load table data
    this.load();
  },

  // change page size
  resize: function() {
    //reset page size
    this.page.size = $('select[sztbl="'+this.id+'"]').val();

    //reset current page
    this.page.current = 1;

    //reload table data
    this.load();
  },

  // update table
  update: function() {
    //update total page
    this.page.total = Math.ceil(this.data.total / this.page.size);

    //update current page
    this.page.current = Math.ceil(this.data.start / this.page.size);
  },

  // query table data
  load: function() {
    //set loading tips
    this.renderLoading();

    //set hidden input
    this.dom.input.start.val(this.page.size*(this.page.current-1));
    this.dom.input.count.val(this.page.size);

    //check form data
    if(this.dom.form.valid()){
      this.dom.form.ajaxSubmit({
         url: this.url,
         type: 'get',
         table: this,
         success: function(resp) {
            if(resp.status){
              // table data
              this.table.data = resp.data;

              // update table
              this.table.update();

              // render table
              this.table.render();

              // add change page event
              this.table.addPageEvent();

              // add change page size event
              this.table.addSizeEvent();
            } else {
              this.table.setFailureInfo(resp.message);
            }
         }
      });
    }
  },

  // init table
  init: function() {
    // set search event
    $(this.dom.query).on('click', {table: this}, function(e){
      //reset page
      e.data.table.page.current = 1;
      //load data
      e.data.table.load();
    });

    //load data
    this.load();
  }
};



