/**
* @author polly
* version: 0.1
* 
*/

// cube table
function CubeTable(init) {
  //table id
  this.id = init.id;

  //row id name
  this.rowid = init.rowid;

  //ajax url
  this.url = init.url;

  //default render
  if(init.render)
    this.render = init.render;
  else
    this.render = function(d){
      return d;
    };

  //table elements
  this.dom = {
    form: $('#'+this.id+"_form"),
    head: $('#'+this.id+"_head"),
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
    query: $('#'+init.id+"_query"),
    reset: $('#'+init.id+"_reset")
  };

  //table data
  this.data = {
    total: 0,
    start: 0,
    items: {}
  };

  //table page
  this.page = {
    total: 0, // total pages index
    curr: 0, //current page index
    goto: 1,  //will goto page index


    size: 20,
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

  //column sort
  this.sort = {
    seq: '',
    by: '',
    order: ''
  },

  //table columns
  this.columns = init.columns;
}

// cube table prototype
CubeTable.prototype = {
	constructor: CubeTable,

  renderEmpty: function() {
    html = '<tr><td valign="top" colspan="'+this.columns.length+'" style="text-align: center;">没有数据</td></tr>';
    this.dom.body.html(html);
  },

  renderLoading: function() {
    html = '<tr><td valign="top" colspan="'+this.columns.length+'" style="text-align: center;">正在加载数据...</td></tr>';
    this.dom.body.html(html);
  },

  renderFailure: function(msg) {
    html = '<tr><td valign="top" colspan="'+this.columns.length+'" style="text-align: center;">'+msg+'</td></tr>';
    this.dom.body.html(html);
  },

  //render table head
  renderHead: function() {
    // get heads
    heads = $(this.dom.head).children('th');

    // add attrs
    for (i=0; i<heads.length; i++){
      //set head name with original name
      $(heads[i]).html(this.columns[i].name);
      //set head sequence
      $(heads[i]).attr('seq', i);

      //add sortable style
      if (this.columns[i].sortable){
        $(heads[i]).attr('style', 'cursor: pointer;');
        $(heads[i]).attr('sortable', 'true');
        $(heads[i]).html(this.columns[i].name+'&#8597;');
      }

      //add sort flag
      if (this.sort.by == this.columns[i].id){
        //set head name with sort flag
        if (this.sort.order == 'asc')
          $(heads[i]).html(this.columns[i].name+'&#8593;');
        else if (this.sort.order == 'desc')
          $(heads[i]).html(this.columns[i].name+'&#8595;');
        else
          $(heads[i]).html(this.columns[i].name+'&#8597;');
      }
    }
  },

  //render table rows
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
        
        id = j;
        if (column.id)
          id = column.id;

        render = this.render;
        if (column.render)
          render = column.render

        data = '';
        // column original data
        if (name) {
          data = item[id];
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
    html = '<ul class="pagination" style="' + this.page.style + '">\n'
            + '\t<li><a linktbl="'+this.id+'" act="first">&lt;&lt;</a></li>\n'
            + '\t<li><a linktbl="'+this.id+'" act="previous">&lt;</a></li>\n'
            + '\t<li><a linktbl="'+this.id+'" act="current">'+this.page.curr+'</a></li>\n'
            + '\t<li><a linktbl="'+this.id+'" act="next">&gt;</a></li>\n'
            + '\t<li><a linktbl="'+this.id+'" act="last">&gt;&gt;</a></li>\n'
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
    if(this.data.items.length == 0){
      start = 0;
      end = 0;
    } else {
      start = this.data.start+1;
      end = this.data.start+this.data.items.length;
    }

    html = '<span style="'+this.info.style+'">第'+start+'-'+end+'条, 共'+this.data.total+'条; 第'+this.page.curr+'页, 共'+this.page.total+'页</span>';
    //render
    this.dom.info.html(html);
  },

  // init query event
  addQueryEvent: function() {
    // add query event
    $(this.dom.query).on('click', {table: this}, function(e){
      //goto first page
      e.data.table.page.goto = 1;
      //load data
      e.data.table.load();
    });
  },

  // init query event
  addResetEvent: function() {
    // add query event
    $(this.dom.reset).on('click', {table: this}, function(e){
      //reset form
      $(e.data.table.dom.form)[0].reset();
      //goto first page
      e.data.table.page.goto = 1;
      //load data
      e.data.table.load();
    });
  },

  // add sort event
  addSortEvent: function() {
    sorts = $(this.dom.head).children('th[sortable="true"]');
    $(sorts).on('click', {table: this}, function(e){
      // process display
      i = $(this).attr('seq');
      if(e.data.table.sort.by == e.data.table.columns[i].id){
        if(e.data.table.sort.order == 'asc') {
          e.data.table.sort.order = 'desc';
          $(this).html(e.data.table.columns[i].name+"&#8595;");
        }
        else{
          e.data.table.sort.order = 'asc';
          $(this).html(e.data.table.columns[i].name+"&#8593;");
        }
      } else {
        //reset last sort column head
        lseq = e.data.table.sort.seq;
        if(lseq != ''){
          $(this).siblings('th[seq="'+lseq+'"]').html(e.data.table.columns[lseq].name+"&#8597;");
        }

        //set sort data
        e.data.table.sort.seq = i;
        e.data.table.sort.by = e.data.table.columns[i].id;
        e.data.table.sort.order = 'asc';

        //set current sort column head
        $(this).html(e.data.table.columns[i].name+"&#8593;");
      }

      //load data
      e.data.table.load();
    });
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

  // init head
  initHead: function() {
    // init column names for table head
    heads = $(this.dom.head).children('th');
    for(i=0; i<heads.length; i++){
      this.columns[i].name = $(heads[i]).text();
    }
  },

  // init event
  initEvent: function() {
    // add query event
    this.addQueryEvent();

    // add reset event
    this.addResetEvent();

    // add sort event
    this.addSortEvent();

    // add change page event
    this.addPageEvent();

    // add change page size event
    this.addSizeEvent();
  },

  //update page
  updatePage: function() {
    //update current page
    $('a[linktbl="'+this.id+'"][act="current"]').text(this.page.curr);
    $('a[linktbl="'+this.id+'"][act="current"]').parent().attr('class', 'active');

    //update previous&first buttons
    if(this.page.curr <= 1){
      $('a[linktbl="'+this.id+'"][act="first"]').parent().attr('class', 'disabled');
      $('a[linktbl="'+this.id+'"][act="previous"]').parent().attr('class', 'disabled');
    } else {
      $('a[linktbl="'+this.id+'"][act="first"]').parent().attr('class', '');
      $('a[linktbl="'+this.id+'"][act="previous"]').parent().attr('class', '');
    }

    //update next&last buttons
    if(this.page.curr >= this.page.total) {
      $('a[linktbl="'+this.id+'"][act="next"]').parent().attr('class', 'disabled');
      $('a[linktbl="'+this.id+'"][act="last"]').parent().attr('class', 'disabled');
    } else {
      $('a[linktbl="'+this.id+'"][act="next"]').parent().attr('class', '');
      $('a[linktbl="'+this.id+'"][act="last"]').parent().attr('class', '');
    }
  },

   // go to page
  goto: function(act) {
    //change current page
    if(act == 'first'){
      if(this.page.curr == 1)
        return;
      this.page.goto = 1;    
    }
    else if ( act == 'previous') {
      if(this.page.curr == 1)
        return;

      if(this.page.curr > 1)
        this.page.goto = this.page.curr-1;
    }
    else if( act == 'next'){
      if(this.page.curr >= this.page.total)
        return;

      if(this.page.curr < this.page.total)
        this.page.goto = this.page.curr+1;
    }
    else if( act == 'last'){
      if(this.page.curr >= this.page.total)
        return;

      this.page.goto = this.page.total;
    }
    else
      return;

    //check goto value
    if(this.page.goto < 1)
      this.page.goto = 1;

    //load table data
    this.load();
  },

  // change page size
  resize: function() {
    //reset page size
    this.page.size = $('select[sztbl="'+this.id+'"]').val();

    //reset current page
    this.page.goto = 1;

    //reload table data
    this.load();
  },

  // update table
  update: function() {
    //update total page
    this.page.total = Math.ceil(this.data.total / this.page.size);

    //update current page
    if (this.data.items.length > 0)
      this.page.curr = Math.ceil(this.data.start / this.page.size)+1;
    else {
      this.page.start = 0;
      this.page.curr = 0;
    }


    //update row data
    this.renderRows();

    //update table info
    this.renderInfo();

    //update table page
    this.updatePage();
  },

  // query table data
  load: function() {
    //set loading tips
    this.renderLoading();

    //set hidden input
    this.dom.input.start.val(this.page.size*(this.page.goto-1));
    this.dom.input.count.val(this.page.size);
    this.dom.input.orderby.val(this.sort.by);
    this.dom.input.order.val(this.sort.order);

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
            } else {
              this.table.renderFailure(resp.message);
            }
         }
      });
    }
  },

  // init table
  init: function() {
    // init head
    this.initHead();

    // render head
    this.renderHead();

    // render page
    this.renderPage();

    // render size
    this.renderSize();

    // init event
    this.initEvent();

    //load data
    this.load();
  }
};



