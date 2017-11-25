$(document).ready(function(){

    var table = $('#terminalList').DataTable({
        "autoWidth": false,     //通常被禁用作为优化
        "processing": true,
        "serverSide": true,
        "paging": true,         //制指定它才能显示表格底部的分页按钮
        "info": true,
        "ordering": false,
        "searching": false,
        "lengthChange": true,
        "deferRender": true,
        "iDisplayLength": 10,
        "sPaginationType": "full_numbers",
        "lengthMenu": [[10, 40, 100],[10, 40, 100]],
        "dom": 'l<"top"p>rt',
        "fnInitComplete": function(){
            var $terminalList_length = $("#terminalList_length");
            var $terminalList_paginate = $("#terminalList_paginate");
            var $page_top = $('.top');

            $page_top.addClass('row');
            $terminalList_paginate.addClass('col-md-8');
            $terminalList_length.addClass('col-md-4');
            $terminalList_length.prependTo($page_top);
        },
        "ajax": function(data, callback, settings){
            var get_data = {
	           'page': Math.ceil(data.start / data.length) + 1,
	           'maxnum': data.length
            };

            var se_userid = window.localStorage.getItem('myid');
            get_data.se_userid = se_userid;

            var terminal_id = $("#s_terminal_id").val();

            if(terminal_id){
                get_data.terminalid = terminal_id;
            }

            $.ajax({
	            url: '/posp/v1/api/terminal/list',
	            type: 'GET',
	            dataType: 'json',
	            data: get_data,
	            success: function(data) {
                    var respcd = data.respcd;
                    if(respcd != '0000'){
                        $processing = $("#terminalList_processing");
                        $processing.css('display', 'none');
                        var resperr = data.resperr;
                        var respmsg = data.respmsg;
                        var msg = resperr ? resperr : respmsg;
                        toastr.warning(msg);
                        return false;
                    }
	                detail_data = data.data;
	                num = detail_data.num;
	                callback({
	                    recordsTotal: num,
	                    recordsFiltered: num,
	                    data: detail_data.info
	                });
	            },
	            error: function(data) {
	                toastr.warning('获取数据异常');
	                return false;
	            }
            });
        },
        'columnDefs': [
            {
                targets: 8,
                data: '操作',
                render: function(data, type, full) {
                    var terminal_table_id =full.id;
                    var view ="<button type='button' class='btn btn-warning btn-sm viewEdit' data-terminal_table_id="+terminal_table_id+">"+'查看'+"</button>";
                    return view;
                }
            }
        ],
		'columns': [
				{ data: 'terminalid'},
                { data: 'psamid'},
				{ data: 'model'},
				{ data: 'deliver_date'},
				{ data: 'tck'},
				{ data: 'used'},
				{ data: 'state'},
				{ data: 'last_modify'},
		],
        'oLanguage': {
            'sProcessing': '<span style="color:red;">加载中....</span>',
            'sLengthMenu': '每页显示_MENU_条记录',
            'sInfo': '显示 _START_到_END_ 的 _TOTAL_条数据',
            'sInfoEmpty': '没有匹配的数据',
            'sZeroRecords': '没有找到匹配的数据',
            'oPaginate': {
                'sFirst': '首页',
                'sPrevious': '前一页',
                'sNext': '后一页',
                'sLast': '尾页'
            }
        }
    });

    $("#terminalSearch").click(function(){
        var terminal_query_vt = $('#terminal_query').validate({
           rules: {
               s_terminal_id: {
                   required: false,
                   maxlength: 20
               }
           },
           messages: {
               s_terminal_id: {
                   required: '请输入通道ID',
                   maxlength: $.validator.format("请输入一个长度最多是 {0} 的字符串")
               }
           },
           errorPlacement: function(error, element){
               var $error_element = element.parent().parent().next();
               $error_element.text('');
               error.appendTo($error_element);
           }
        });
        var ok = terminal_query_vt.form();
        if(!ok){
            $("#query_label_error").show();
            $("#query_label_error").fadeOut(1000);
            return false;
        }
        $('#terminalList').DataTable().draw();
    });

	$("#terminalCreate").click(function(){
        $("#terminalCreateForm").resetForm();
        $("label.error").remove();
		$("#terminalCreateModal").modal();
	});

})