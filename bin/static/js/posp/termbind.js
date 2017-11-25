
$(document).ready(function(){

    var table = $('#termbindList').DataTable({
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
            var $termbindList_length = $("#termbindList_length");
            var $termbindList_paginate = $("#termbindList_paginate");
            var $page_top = $('.top');

            $page_top.addClass('row');
            $termbindList_paginate.addClass('col-md-8');
            $termbindList_length.addClass('col-md-4');
            $termbindList_length.prependTo($page_top);
        },
        "ajax": function(data, callback, settings){
            var get_data = {
	           'page': Math.ceil(data.start / data.length) + 1,
	           'maxnum': data.length
            };

            var se_userid = window.localStorage.getItem('myid');
            get_data.se_userid = se_userid;

            var termbind_name = $("#s_termbind_name").val();

            if(termbind_name){
                get_data.name = termbind_name;
            }

            $.ajax({
	            url: '/posp/v1/api/terminal/bind/list',
	            type: 'GET',
	            dataType: 'json',
	            data: get_data,
	            success: function(data) {
                    var respcd = data.respcd;
                    if(respcd != '0000'){
                        $processing = $("#termbindList_processing");
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
                targets: 1,
                render: function(data, type, full) {
                    return split_key(data);
                }
            },
            {
                targets: 11,
                data: '操作',
                render: function(data, type, full) {
                    var termbind_id =full.id;
                    var view ="<button type='button' class='btn btn-warning btn-sm viewEdit' data-termbind__id="+termbind_id+">"+'查看'+"</button>";
                    return view;
                }
            }
        ],
		'columns': [
				{ data: 'userid'},
				{ data: 'udid'},
				{ data: 'terminalid'},
                { data: 'psamid'},
				{ data: 'diskey'},
				{ data: 'fackey'},
				{ data: 'key_version'},
				{ data: 'os'},
				{ data: 'os_ver'},
				{ data: 'state'},
				{ data: 'active_date'},
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

})