$(document).ready(function(){
    var table = $('#chnlbindList').DataTable({
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
            var $channelList_length = $("#channelList_length");
            var $channelList_paginate = $("#channelList_paginate");
            var $page_top = $('.top');

            $page_top.addClass('row');
            $channelList_paginate.addClass('col-md-8');
            $channelList_length.addClass('col-md-4');
            $channelList_length.prependTo($page_top);
        },
        "ajax": function(data, callback, settings){
            var get_data = {
	           'page': Math.ceil(data.start / data.length) + 1,
	           'maxnum': data.length
            };

            var se_userid = window.localStorage.getItem('myid');
            get_data.se_userid = se_userid;

            var channel_name = $("#s_channel_name").val();

            if(channel_name){
                get_data.name = channel_name;
            }

            $.ajax({
	            url: '/posp/v1/api/channel/bind/list',
	            type: 'GET',
	            dataType: 'json',
	            data: get_data,
	            success: function(data) {
                    var respcd = data.respcd;
                    if(respcd != '0000'){
                        $processing = $("#chnlbindList_processing");
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
                targets: 10,
                data: '操作',
                render: function(data, type, full) {
                    var status = full.available;
                    var channel_bind_id =full.id;
                    var msg = status ? '打开' : '关闭';
                    var op = "<button type='button' class='btn btn-success btn-sm setStatus' data-channel_bind_id="+channel_bind_id+" data-status="+status+">"+msg+"</button>";
                    var view ="<button type='button' class='btn btn-warning btn-sm viewEdit' data-channel_bind_id="+channel_bind_id+">"+'查看'+"</button>";
                    return op+view;
                }
            }
        ],
		'columns': [
				{ data: 'userid'},
                { data: 'qffee'},
				{ data: 'chnlfee'},
				{ data: 'priority'},
				{ data: 'name'},
				{ data: 'mchntid'},
				{ data: 'mchntnm'},
				{ data: 'termid'},
				{ data: 'mcc'},
				{ data: 'available'},
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

        $(document).on('click', '.setStatus', function(){
        var channel_bind_id = $(this).data('channel_bind_id');
        var status = $(this).data('status');
        var value = status ? 0 : 1;
        var se_userid = window.localStorage.getItem('myid');
        var post_data = {
            'channel_bind_id': channel_bind_id,
            'available': value,
            'se_userid': se_userid
        };
        $.ajax({
	        url: '/posp/v1/api/channel/bind/switch',
	        type: 'POST',
	        dataType: 'json',
	        data: post_data,
	        success: function(data) {
                var respcd = data.respcd;
                if(respcd != '0000'){
                    var resperr = data.resperr;
                    var respmsg = data.respmsg;
                    var msg = resperr ? resperr : respmsg;
                    toastr.warning(msg);
                    return false;
                }
                else {
                    $('#chnlbindList').DataTable().draw();
                    toastr.success('操作成功');
                }
	        },
	        error: function(data) {
                toastr.warning('请求异常');
	        }
        });
    });

})